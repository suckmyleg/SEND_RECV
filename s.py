import send_recv
import time


def mouth(f):
	while f.status:
		f.check()
		time.sleep(5)
		for i in range(10):
			f.pr("Module {} connected.".format(i))
		f.die()

s = send_recv.server("192.168.1.92", 4545, function_to_call=mouth)

s.start()