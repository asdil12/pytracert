#!/usr/bin/python2

import os
import glob
import types
from operator import attrgetter

import exceptions
from base import returninfo

backend_classes_unsorted = []

for file in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "*.py")):
	name = os.path.splitext(os.path.basename(file))[0]
	if name == "__init__" or name == "base" or name == "exceptions":
		continue
	# add package prefix to name, if required
	module = __import__("%s.%s" % (__name__, name))
	module = eval("module.%s" % name)
	for member in dir(module):
		if member == "DNSGeoBase":
			continue
		if isinstance(getattr(module, member), types.ClassType):
			cls = getattr(module, member)
			if cls.priority != 0:
				backend_classes_unsorted.append(cls)

backend_classes = sorted(backend_classes_unsorted, key=attrgetter('priority'), reverse=True)
del backend_classes_unsorted


backend_instances = []
for backend_class in backend_classes:
	backend_instances.append(backend_class())

def lookup(**kwargs):
	global backend_instances
	for instance in backend_instances:
		try:
			return instance.lookup(**kwargs)
		except exceptions.NotApplicable:
			pass
	return returninfo
