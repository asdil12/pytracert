#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: cr2.cgcil.ip.att.net
            .CTTY.

"""

class ATT(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r".*\.([a-z0-9]*)\.ip\.att\.net$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = ATT.applre.match(hostname)
			if match:
				city_code = match.group(1)
				returninfo = base.returninfo.copy()
				returninfo['company'] = 'American Telegraph and Telephone'
				returninfo['info'] = 'carrier'
				try:
					jsondb = json.load(open('./database/att.json'))
					c = jsondb[city_code.lower()]
					returninfo['city'] = c['city']
					returninfo['accuracy'] = 'city'
					returninfo['lat'] = c['lat']
					returninfo['lng'] = c['lng']
					returninfo['country'] = c['country']
				except:
					pass
				return returninfo
		raise exceptions.NotApplicable()
