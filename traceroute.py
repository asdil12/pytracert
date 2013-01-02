#!/usr/bin/python2

import socket

class Traceroute:
	def __init__(self, port=33434, max_hops=30, timeout=1):
		self.nodecallback = None
		self.port = port
		self.max_hops = max_hops
		self.timeout = timeout
		self.old_timeout_handler = None
		self.timeout_set = False

	def set_callback(self, callback):
		self.callback = callback

	def run(self, target):
		dest_addr = socket.gethostbyname(target)
		icmp = socket.getprotobyname('icmp')
		udp = socket.getprotobyname('udp')
		ttl = 1
		while True:
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			recv_socket.settimeout(self.timeout)
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
			recv_socket.bind(("", self.port))
			send_socket.sendto("", (dest_addr, self.port))
			curr_addr = None
			curr_name = None
			try:
				_, curr_addr = recv_socket.recvfrom(512)
				curr_addr = curr_addr[0]
				try:
					curr_name = socket.gethostbyaddr(curr_addr)[0]
				except (socket.error):
					curr_name = curr_addr
			except socket.error:
				pass
			except socket.timeout:
				pass
			finally:
				send_socket.close()
				recv_socket.close()

			if curr_addr is not None:
				payload = {'ip': curr_addr, 'hostname': curr_name}
			else:
				payload = None

			self.callback(ttl=ttl, payload=payload)

			ttl += 1

			if curr_addr == dest_addr or ttl > self.max_hops:
				break
