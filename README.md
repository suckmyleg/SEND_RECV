# SEND_RECV

Create servers and connect to servers.

# SERVER

```python

import send_recv

def main(client):
	username = client.inp("username: ")

	while True:
		answer = client.inp("{}: ".format(username))

host = "192.168.1.111"

port = 4444

server = send_recv.server(host=host, port=port, function_to_call=main)

server.start()

```

# CLIENT

```python

import send_recv

client = send_recv.connection("192.168.1.111", 4444, log=False)

client.start()

client.react()

```



