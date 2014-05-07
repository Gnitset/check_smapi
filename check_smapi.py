#! /usr/bin/env python
#coding: utf-8
#åäö

import optparse
import sys
import os
import urllib2
import traceback
import string

EXIT_UNKNOWN, EXIT_CRITICAL, EXIT_WARNING, EXIT_OK = 3, 2, 1, 0

def parse_row(row):
	ret = dict()
	ret["status"], ret["category"], value = map(string.strip, row.strip().split("/", 2))
	ret["name"], args = map(string.strip, value.split(":", 1))
	if args:
		for kv in map(string.strip, args.split(" ", 1)):
			k, v = map(string.strip, kv.split(":", 1))
			ret[k] = v
	return ret

if __name__ == "__main__":
	parser = optparse.OptionParser("usage: %prog [options]")
	parser.add_option("-H", "--host", dest="host", default="localhost")
	parser.add_option("-p", "--port", dest="port", default=80, type="int")
	parser.add_option("-s", "--ssl", dest="ssl", default=None)
	parser.add_option("-P", "--path", dest="path", default="/smapi/")
	parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true")
	opts, rest = parser.parse_args(sys.argv[1:])

	try:
		prod = dict()
		basepath="http://%s:%s%s"%(opts.host, opts.port, opts.path)
		for row in urllib2.urlopen(basepath+"status").readlines():
			if "prod" in row:
				d = parse_row(row)
				prod[d["name"]] = d
		print prod
		sys.exit(EXIT_OK)
	except Exception as e:
		print "UNKNOWN, %s %s"%(type(e), e)
		if opts.debug:
			traceback.print_exc()
		sys.exit(EXIT_UNKNOWN)
