import send_recv

s = send_recv.connection("192.168.1.92", 4545, log=True)

s.start()

s.react()
