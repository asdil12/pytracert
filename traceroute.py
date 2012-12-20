#!/usr/bin/python

import socket
import dnsgeo
import signal

class TimeoutException(Exception):
	pass

class ICMPTimeout(TimeoutException):
	pass

class DNSTimeout(TimeoutException):
	pass

old_timeout_handler = None
timeout_set = False
def timeout(maxtime, exception=TimeoutException):
	global timeout_set
	global old_timeout_handler
	if maxtime > 0 and not timeout_set:
		def timeout_handler(signum, frame):
			raise exception()
		old_timeout_handler = signal.signal(signal.SIGALRM, timeout_handler)
		timeout_set = True
		signal.alarm(maxtime)
	else:
		signal.signal(signal.SIGALRM, old_timeout_handler)
		timeout_set = False
		signal.alarm(0)

def main(dest_name):
	dest_addr = socket.gethostbyname(dest_name)
	port = 33434
	max_hops = 30
	icmp = socket.getprotobyname('icmp')
	udp = socket.getprotobyname('udp')
	ttl = 1
	while True:
		recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
		send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
		send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
		recv_socket.bind(("", port))
		send_socket.sendto("", (dest_name, port))
		curr_addr = None
		curr_name = None
		try:
			timeout(4, exception=ICMPTimeout)
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
			curr_host = "%s (%s)" % (curr_name, curr_addr)
		else:
			curr_host = "*"
		print "%d\t%s" % (ttl, curr_host)
		print "\t",
		print dnsgeo.lookup(ip=curr_addr, hostname=curr_name)
		ttl += 1

		if curr_addr == dest_addr or ttl > max_hops:
			break

if __name__ == "__main__":
	import sys
	main(sys.argv[1])
