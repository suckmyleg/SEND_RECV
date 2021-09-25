import send_recv

s = send_recv.connection("192.168.1.92", 4545, log=False)

s.start()

s.react()
