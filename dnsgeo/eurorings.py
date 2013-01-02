#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: mchn-s1-rou-1103.DE.eurorings.net
         CITY-           .CT.

"""

class Eurorings(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r"^(\w*)-.*-rou-.*\.([A-Z][A-Z])\.eurorings\.net$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = Eurorings.applre.match(hostname)
			if match:
				city_code, country_code = match.group(1,2)
				returninfo = base.returninfo.copy()
				country = base.get_country_by_iso(country_code)
				returninfo['country'] = country['name']
				returninfo['accuracy'] = 'country'
				returninfo['lat'] = country['lat']
				returninfo['lng'] = country['lng']
				returninfo['company'] = 'KPN Internet'
				returninfo['info'] = 'carrier'
				try:
					jsondb = json.load(open('./database/carriers/eurorings.json'))
					c = jsondb[city_code.lower()]
					returninfo['city'] = c['city']
					returninfo['accuracy'] = 'city'
					returninfo['lat'] = c['lat']
					returninfo['lng'] = c['lng']
				except:
					pass
				return returninfo
		raise exceptions.NotApplicable()
