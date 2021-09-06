import send_recv2

s = send_recv2.connection("192.168.1.92", 4545, log=True)

s.start()

s.react()
