import send_recv2
import time


def mouth(f):
	while f.status:
		f.check()
		time.sleep(5)
		f.die()

s = send_recv2.server("192.168.1.92", 4545, function_to_call=mouth)

s.start()