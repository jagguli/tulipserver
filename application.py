#!/usr/bin/env python3

"""Simple server written using an event loop."""

import argparse
import email.message
import logging
import os
import sys
try:
    import ssl
except ImportError:  # pragma: no cover
    ssl = None

assert sys.version >= '3.3', 'Please use Python 3.3 or higher.'

import tulip
import tulip.http

from urllib.parse import urlparse

from static_handler import StaticFileHandler
from router import Router
from server import HttpServer



ARGS = argparse.ArgumentParser(description="Run simple http server.")
ARGS.add_argument(
    '--host', action="store", dest='host',
    default='127.0.0.1', help='Host name')
ARGS.add_argument(
    '--port', action="store", dest='port',
    default=8888, type=int, help='Port number')
ARGS.add_argument(
    '--iocp', action="store_true", dest='iocp', help='Windows IOCP event loop')
ARGS.add_argument(
    '--ssl', action="store_true", dest='ssl', help='Run ssl mode.')
ARGS.add_argument(
    '--sslcert', action="store", dest='certfile', help='SSL cert file.')
ARGS.add_argument(
    '--sslkey', action="store", dest='keyfile', help='SSL key file.')


def main():
    args = ARGS.parse_args()

    if ':' in args.host:
        args.host, port = args.host.split(':', 1)
        args.port = int(port)

    if args.iocp:
        from tulip import windows_events
        sys.argv.remove('--iocp')
        logging.info('using iocp')
        el = windows_events.ProactorEventLoop()
        tulip.set_event_loop(el)

    if args.ssl:
        here = os.path.join(os.path.dirname(__file__), 'tests')

        if args.certfile:
            certfile = args.certfile or os.path.join(here, 'sample.crt')
            keyfile = args.keyfile or os.path.join(here, 'sample.key')
        else:
            certfile = os.path.join(here, 'sample.crt')
            keyfile = os.path.join(here, 'sample.key')

        sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslcontext.load_cert_chain(certfile, keyfile)
    else:
        sslcontext = None

    loop = tulip.get_event_loop()
    f = loop.start_serving(
        lambda: HttpServer(debug=True, keep_alive=75), args.host, args.port,
        ssl=sslcontext)
    socks = loop.run_until_complete(f)
    print('serving on', socks[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
