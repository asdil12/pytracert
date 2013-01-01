#!/usr/bin/python2

import base
import exceptions

import re
import simplejson as json

"""
network: pos-1-8-0-0-cr01.dallas.tx.ibone.comcast.net
                          CITY  .ST

"""

class Comcast(base.DNSGeoBase):
	priority = 80
	applre = re.compile(r".*\.(\w*)\.(\w\w)\.ibone\.comcast\.net$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = Comcast.applre.match(hostname)
			if match:
				city_code, state_code = match.group(1,2)
				returninfo = base.returninfo.copy()
				state = base.get_state_by_code('us', state_code)
				returninfo['country'] = 'United States of America'
				returninfo['state'] = state['name']
				returninfo['accuracy'] = 'state'
				returninfo['lat'] = state['lat']
				returninfo['lng'] = state['lng']
				returninfo['company'] = 'Comcast Corporation'
				returninfo['info'] = 'carrier'
				try:
					jsondb = json.load(open('./database/carriers/comcast.json'))
					c = jsondb[city_code.lower()]
					returninfo['city'] = c['city']
					returninfo['accuracy'] = 'city'
					returninfo['lat'] = c['lat']
					returninfo['lng'] = c['lng']
				except:
					pass
				return returninfo
		raise exceptions.NotApplicable()
