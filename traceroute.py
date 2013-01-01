#!/usr/bin/python2

import socket
import signal

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
		class TimeoutException(Exception):
			pass

		class ICMPTimeout(TimeoutException):
			pass

		class DNSTimeout(TimeoutException):
			pass

		def timeout(maxtime, exception=TimeoutException):
			if maxtime > 0 and not self.timeout_set:
				def timeout_handler(signum, frame):
					raise exception()
				self.old_timeout_handler = signal.signal(signal.SIGALRM, timeout_handler)
				self.timeout_set = True
				signal.alarm(maxtime)
			else:
				signal.signal(signal.SIGALRM, self.old_timeout_handler)
				self.timeout_set = False
				signal.alarm(0)

		dest_addr = socket.gethostbyname(target)
		icmp = socket.getprotobyname('icmp')
		udp = socket.getprotobyname('udp')
		ttl = 1
		while True:
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
			send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
			recv_socket.bind(("", self.port))
			send_socket.sendto("", (dest_addr, self.port))
			curr_addr = None
			curr_name = None
			try:
				timeout(self.timeout, exception=ICMPTimeout)
				_, curr_addr = recv_socket.recvfrom(512)
				curr_addr = curr_addr[0]
				try:
					curr_name = socket.gethostbyaddr(curr_addr)[0]
				except (socket.error):
					curr_name = curr_addr
			except socket.error:
				pass
			except ICMPTimeout:
				pass
			finally:
				timeout(0)
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
