#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import tornado.websocket
import argparse
import os
import serial
import json
from model import TrainSet 


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


active_sockets = set()


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, trainset):
        self.trainset = trainset

    def open(self):
        print("WebSocket opened")
        active_sockets.add(self)
        for name in self.trainset.status_attrs:
            self.send_status(name, getattr(self.trainset, name))
    
    def send_status(self, key, value):
        message = {'status': {key: value}}
        self.write_message(json.dumps(message))

    def on_message(self, message):
        message = json.loads(message)
        if 'forward' in message:
            power = message['forward']
            self.trainset.throttle_forward(power)
        elif 'reverse' in message:
            power = message['reverse']
            self.trainset.throttle_reverse(power)
        elif 'turnout' in message:
            turnout = message['turnout']
            if turnout == 'left':
                self.trainset.turnout_left()
            else:
                self.trainset.turnout_right()
        elif 'decoupler' in message:
            decoupler = message['decoupler']
            if decoupler == 'up':
                self.trainset.decoupler_up()
            elif decoupler == 'down':
                self.trainset.decoupler_down()
            elif decoupler == 'auto':
                self.trainset.auto_decouple()
        elif 'light1' in message:
            light1 = message['light1']
            if light1 == 'on':
                self.trainset.light1_on()
            else:
                self.trainset.light1_off()
        elif 'light2' in message:
            light2 = message['light2']
            if light2 == 'on':
                self.trainset.light2_on()
            else:
                self.trainset.light2_off()

    def on_close(self):
        print("WebSocket closed")
        active_sockets.remove(self)


def configure_app(args, ioloop):
    if args.serial_port == 'dummy':
        from serialhandler import DummyPort
        port = DummyPort()
    else:
        port = serial.Serial(args.serial_port, baudrate=9600, timeout=0.5)

    trainset = TrainSet(port, ioloop)
    
    @trainset.add_listener
    def model_changed(model, name):
        value = getattr(model, name)
        for sock in active_sockets:
            sock.send_status(name, value)

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", WebSocketHandler, { 'trainset': trainset }),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": args.static_path}),
    ], debug=True, template_path=args.template_path)
    return application


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--template-path',
        default=os.path.join(os.getcwd(), 'templates'))
    parser.add_argument('--static-path',
        default=os.path.join(os.getcwd(), 'static'))
    parser.add_argument('--serial-port', required=True)
    args = parser.parse_args()
    ioloop = tornado.ioloop.IOLoop.instance()
    application = configure_app(args, ioloop)
    application.listen(8888)
    ioloop.start()

