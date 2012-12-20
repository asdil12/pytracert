#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: ge-3-3-0.mpr1.%CITY1.%COUNTRY.above.net

"""

class AboveNet(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r".*\.(\w*)\d\.(\w*)\.above\.net$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = AboveNet.applre.match(hostname)
			if match:
				city_code, country_code = match.group(1,2)
				returninfo = base.returninfo.copy()
				country = base.get_country_by_iso(country_code)
				returninfo['country'] = country['name']
				returninfo['lat'] = country['lat']
				returninfo['lng'] = country['lng']
				returninfo['company'] = 'AboveNet Inc'
				returninfo['info'] = 'carrier'
				try:
					jsondb = json.load(open('./database/abovenet.json'))
					c = jsondb[city_code]
					returninfo['city'] = c['city']
					returninfo['lat'] = c['lat']
					returninfo['lng'] = c['lng']
				except:
					pass
				return returninfo
		raise exceptions.NotApplicable()
