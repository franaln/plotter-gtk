#! /usr/bin/env python

import sys
import signal

from plotter.app import App

if __name__ == '__main__':

    app = App(sys.argv[1:])

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = app.run()
    sys.exit(exit_status)
