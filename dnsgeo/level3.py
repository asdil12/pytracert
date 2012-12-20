#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: foo.%CITY1.Level3.net

"""

class Level3(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r".*\.(\w*)\d\.Level3\.net$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = Level3.applre.match(hostname)
			if match:
				city_raw = match.group(1)
				returninfo = base.returninfo.copy()
				jsondb = json.load(open('./database/level3.json'))
				c = jsondb[city_raw]
				returninfo['city'] = c['city']
				returninfo['lat'] = c['lat']
				returninfo['lng'] = c['lng']
				returninfo['country'] = c['country']
				returninfo['company'] = 'Level 3 Communications, Inc'
				returninfo['info'] = 'carrier'
				return returninfo
		raise exceptions.NotApplicable()
