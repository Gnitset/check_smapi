#! /usr/bin/env python
#coding: utf-8
#åäö

import optparse
import sys
import os
import traceback

EXIT_UNKNOWN, EXIT_CRITICAL, EXIT_WARNING, EXIT_OK = 3, 2, 1, 0

if __name__ == "__main__":
	parser = optparse.OptionParser("usage: %prog [options]")
	parser.add_option("-H", "--host", dest="host", default="localhost")
	parser.add_option("-p", "--port", dest="port", default=80, type="int")
	parser.add_option("-s", "--ssl", dest="ssl", default=None)
	parser.add_option("-P", "--path", dest="path", default="/smapi/")
	opts, rest = parser.parse_args(sys.argv[1:])

	try:
		sys.exit(EXIT_OK)
	except Exception as e:
		print "UNKNOWN, %s %s"%(type(e), e)
		traceback.print_exc()
		sys.exit(EXIT_UNKNOWN)
