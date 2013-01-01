#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: 0.xe-7-1-0.BR3.NYC4.ALTER.NET

"""

class Level3(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r".*\.([A-Z]*)\d+\.ALTER\.NET$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = Level3.applre.match(hostname)
			if match:
				city_code = match.group(1)
				returninfo = base.returninfo.copy()
				returninfo['company'] = 'Verizon'
				returninfo['info'] = 'carrier'
				country = base.get_country_by_iso('us')
				returninfo['country'] = country['name']
				returninfo['accuracy'] = 'country'
				returninfo['lat'] = country['lat']
				returninfo['lng'] = country['lng']
				try:
					jsondb = json.load(open('./database/carriers/verizon.json'))
					c = jsondb[city_code.upper()]
					returninfo['city'] = c['city']
					returninfo['accuracy'] = 'city'
					returninfo['lat'] = c['lat']
					returninfo['lng'] = c['lng']
					returninfo['country'] = c['country']
				except:
					pass
				return returninfo
		raise exceptions.NotApplicable()
