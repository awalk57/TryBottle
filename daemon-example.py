#!/usr/bin/env python

import sys, time
from daemon import Daemon
from time import gmtime, strftime
from tryGrequests import get_checks

class MyDaemon(Daemon):
	def run(self):
		while True:
#			get_checks()
#			test_daemon()
			time.sleep(100)

	def test_daemon(self):
		curtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		with open("daemonout.txt", "a") as f:
			 f.write("time_now->%s" % curtime)

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
