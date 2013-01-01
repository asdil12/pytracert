#!/usr/bin/python2

import base
import exceptions

import simplejson as json
import re

class NEFkom(base.DNSGeoBase):
	priority = 50
	applre = re.compile(r"nefkom.de$", re.I)
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = NEFkom.applre.search(hostname)
			if match:
				returninfo = base.returninfo.copy()
				returninfo['country'] = 'Germany'
				returninfo['city'] = 'Nuremberg'
				returninfo['accuracy'] = 'city'
				returninfo['info'] = 'isp'
				returninfo['lat'] = 49.4538501
				returninfo['lng'] = 11.0773238
				returninfo['company'] = 'M-net Telekommunikations GmbH'
				return returninfo
		raise exceptions.NotApplicable()
