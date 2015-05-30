#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import tornado.websocket
import argparse
import os
import serialhandler
import serial
import json
from model import TrainSet


trainset = TrainSet()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


active_sockets = set()


def status_received(key, value):
    setattr(trainset, key, value)


@trainset.add_listener
def model_changed(model, name):
    value = getattr(model, name)
    for sock in active_sockets:
        sock.send_status(name, value)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, serial_protocol):
        self.serial_protocol = serial_protocol

    def open(self):
        print("WebSocket opened")
        active_sockets.add(self)
        for name in trainset.status_attrs():
            self.send_status(name, getattr(trainset, name))
    
    def send_status(self, key, value):
        message = {'status': {key: value}}
        self.write_message(json.dumps(message))

    def on_message(self, message):
        message = json.loads(message)
        if 'forward' in message:
            power = message['forward']
            self.serial_protocol.throttle_forward(power)
        elif 'reverse' in message:
            power = message['reverse']
            self.serial_protocol.throttle_reverse(power)
        elif 'turnout' in message:
            turnout = message['turnout']
            if turnout == 'left':
                self.serial_protocol.turnout_left()
            else:
                self.serial_protocol.turnout_right()
        elif 'decoupler' in message:
            decoupler = message['decoupler']
            if decoupler == 'up':
                self.serial_protocol.decoupler_up()
            else:
                self.serial_protocol.decoupler_down()
        elif 'light1' in message:
            light1 = message['light1']
            if light1 == 'on':
                self.serial_protocol.light1_on()
            else:
                self.serial_protocol.light1_off()
        elif 'light2' in message:
            light2 = message['light2']
            if light2 == 'on':
                self.serial_protocol.light2_on()
            else:
                self.serial_protocol.light2_off()

    def on_close(self):
        print("WebSocket closed")
        active_sockets.remove(self)


def configure_app(args, ioloop):
    if args.serial_port == 'dummy':
        class DummyPort(object):
            def read(self, size=None):
                from time import sleep
                sleep(0.1)
                return 0
            def inWaiting(self):
                return 0
            def write(self, bytes):
                print('Write bytes:', bytes)
        port = DummyPort()
    else:
        port = serial.Serial(args.serial_port, baudrate=9600, timeout=0.5)

    def serial_callback(key, value):
        ioloop.add_callback(status_received, key, value)

    serial_protocol = serialhandler.SerialProtocol(port, serial_callback)
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", WebSocketHandler, { 'serial_protocol': serial_protocol }),
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

