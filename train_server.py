#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
import argparse
import os
import serialhandler
import serial


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


def configure_app(args):
    print(args)
    port = serial.Serial(args.serial_port)
    serial_protocol = serialhandler.SerialProtocol(port)
    application = tornado.web.Application([
        (r"/", MainHandler),
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
    application = configure_app(args)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

