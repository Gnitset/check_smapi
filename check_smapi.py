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

def parse_rows(rows):
	ret = dict()
	ret["not_ok"] = list()
	for row in rows:
		status, category, value = map(string.strip, row.strip().split("/", 2))
		if category not in ret:
			ret[category] = dict()
		name_args = map(string.strip, value.split(":", 1))
		if len(name_args) == 1:
			name, args = name_args[0], None
		else:
			name, args = name_args
		target = ret[category][name] = dict()
		target["status"] = status
		if args:
			if category == "info":
				target["value"] = args
				continue
			for kv in map(string.strip, args.split(" ", 1)):
				if ":" not in kv:
					target["value"] = kv
				else:
					k, v = map(string.strip, kv.split(":", 1))
					target[k] = v
		if target["status"] != "OK":
			ret["not_ok"].append(target)
	return ret

def request_smapi(*path):
	print ''.join(path)
	return urllib2.urlopen(''.join(path)).readlines()

if __name__ == "__main__":
	parser = optparse.OptionParser("usage: %prog [options]")
	parser.add_option("-H", "--host", dest="host", default="localhost")
	parser.add_option("-p", "--port", dest="port", default=80, type="int")
	parser.add_option("-s", "--ssl", dest="ssl", default=None)
	parser.add_option("-P", "--path", dest="path", default="/smapi/")
	parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true")
	opts, rest = parser.parse_args(sys.argv[1:])

	try:
		ret = EXIT_OK
                output = {"critical": list(), "warning": list(), "ok": list()}
		basepath = "http://%s:%s"%(opts.host, opts.port)
		main_status = request_smapi(basepath, opts.path, "status")
		parsed_main_status = parse_rows(main_status)
		if parsed_main_status["not_ok"]:
			output["critical"].append(str(parsed_main_status["not_ok"]))
			if ret < EXIT_CRITICAL: ret = EXIT_CRITICAL
		for module_name, module in parsed_main_status["prod"].iteritems():
			if "mountpoint" not in module:
				raise Exception("Module missing mountpoint", module_name)
			module_status = request_smapi(basepath, module["mountpoint"], opts.path, "status")
			module["status_obj"] = parse_rows(module_status)
                for level in ("critical", "warning", "ok"):
                        for row in output[level]:
                                print row
		print parsed_main_status
		sys.exit(ret)
	except Exception as e:
		print "UNKNOWN, %s %s"%(type(e), e)
		if opts.debug:
			traceback.print_exc()
		sys.exit(EXIT_UNKNOWN)
