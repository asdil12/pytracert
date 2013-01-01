#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: xr-bay1-te1-1.x-win.dfn.de

"""

class DFN(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r"^\w*-(\w*)\d-.*\.x-win\.dfn\.de$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = DFN.applre.match(hostname)
			if match:
				city_code = match.group(1)
				returninfo = base.returninfo.copy()
				jsondb = json.load(open('./database/carriers/dfn.json'))
				c = jsondb[city_code.upper()]
				returninfo['city'] = c['city']
				returninfo['accuracy'] = 'city'
				returninfo['lat'] = c['lat']
				returninfo['lng'] = c['lng']
				returninfo['country'] = c['country']
				returninfo['company'] = 'Deutschen Forschungsnetz'
				returninfo['info'] = 'carrier'
				return returninfo
		raise exceptions.NotApplicable()
