#!/usr/bin/python2

import base
import exceptions

import simplejson as json
import re

"""

network: hos-tr2.ex3k13.rz1.hetzner.de

http://wiki.hetzner.de/index.php/Rechenzentren_und_Anbindung

"""

class Hetzner(base.DNSGeoBase):
	priority = 40
	applre = re.compile(r".*\.rz(\d*)\.hetzner\.de$")
	def lookup(self, ip=None, hostname=None):
		if hostname:
			match = Hetzner.applre.match(hostname)
			if match:
				returninfo = base.returninfo.copy()
				returninfo['country'] = 'Germany'
				returninfo['info'] = 'isp'
				returninfo['company'] = 'Hetzner Online AG'
				datacenter_code = int(match.group(1))
				try:
					jsondb = json.load(open('./database/isps/hetzner.json'))
					if datacenter_code in range(1, 9 + 1): location = 'nuernberg'
					elif datacenter_code in range(10, 23 + 1): location = 'falkenstein'
					c = jsondb[location]
					returninfo['lat'] = c['lat']
					returninfo['lng'] = c['lng']
					returninfo['city'] = c['city']
				except:
					raise
					pass
				return returninfo
		raise exceptions.NotApplicable()
