import socket
import threading
import pickle
import time
from random import randint
import os

def style(i1, i2, l=30, d=" "):
	return "{} {} {}".format(str(i1), (l-(len(str(i1)) + len(str(i2))))*d, str(i2))

def styl(i1, i2, l=2):
	return "{}{}{}".format(str(i1), " "*l, str(i2))

def function_to_call_defaul(c):
	c.log("Error, not function_to_call supplied")

class server:
	def __init__(self, host=False, port=False, buffer=1024, conn=False, status=False, messages=[], function_to_call=function_to_call_defaul, log=True):
		self.host = host
		self.port = port
		self.buffer = buffer

		self.connections = []

		self.conn = conn
		self.status = status

		self.log_status = log

		self.function_to_call = function_to_call

		self.messages = messages

		self.start_time = time.time()

	def remove_inactive(self):
		for c in self.connections:
			if not c.status:
				del self.connections[self.connections.index(c)]

	def get_duration(self):
		return int((time.time() - self.start_time)*100)/100


	def log_styled(self, a):
		print(style(styl("{}:{}".format(self.host, self.port), a, l=2), "{}s".format(self.get_duration()), l=90))


	def log(self, args, b=False):
		if self.log_status:
			if type(args) == list:
				for a in args:
					if type(a) == list and len(a) == 2:
						self.log_styled(style(a[0], a[1]))
					else:
						self.log_styled(str(a))
			else:
				if not b:
					self.log_styled(args)
				else:
					self.log_styled(style(args, b))

	def show_connections(self):
		self.log("Connections:")
		for c in self.connections:
			print("		{}		{}		{}".format(c.host, c.port, c.status))

	def start_hosting(self):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.conn.bind((self.host, self.port))

		self.conn.listen()

		self.status = True

		self.log("Started hosting")

		threading.Thread(target=self.listen_new_connections).start()

	def add_connection(self, addr, conn):
		self.remove_inactive()

		self.show_connections()

		c = connection(addr[0], addr[1], conn=conn, status=True)

		self.connections.append(c)

		threading.Thread(target=self.function_to_call, args=(c,)).start()

	def listen_new_connections(self):
		self.log("Listening new connections")

		while self.status:
			conn, addr = self.conn.accept()

			self.log([["New connection", addr[0]]])

			self.add_connection(addr, conn)

			

	def auto_recv_messages(self):
		while True:
			d = self.recv()

	def check(self, t):
		d = [0, 0]
		for i in range(t):
			if self.send(r):
				pass

	def start(self):
		self.log("Starting")

		self.start_hosting()













class connection:
	def __init__(self, host=False, port=False, buffer=1024, conn=False, status=True, messages=[], log=True):
		self.host = host
		self.port = port
		self.buffer = buffer

		self.conn = conn
		self.status = status


		if not self.host:
			self.manual_connection = True
		else:
			self.manual_connection = False

		self.messages = messages

		self.start_time = time.time()

		self.log_status = log

		self.type = "server"

		if self.manual_connection:
			self.type = "client"

	#LOG TOOLS

	def get_duration(self):
		return int((time.time() - self.start_time)*100)/100

	def log_styled(self, a):
		l = style(style("{}:{}".format(self.host, self.port), a), "{}s".format(self.get_duration()), l=90)
		if self.log_status:
			print(l)
		open("{}_log.txt".format(self.type), "a").write("{} \n".format(l))


	def log(self, args, b=False):
		if type(args) == list:
			for a in args:
				if type(a) == list and len(a) == 2:
					self.log_styled(style(a[0], a[1]))
				else:
					self.log_styled(str(a))
		else:
			if not b:
				self.log_styled(args)
			else:
				self.log_styled(style(args, b))


	#SEND TOOLS
	#SEND TOOLS
	#SEND TOOLS
	#SEND TOOLS

	def pr(self, a):
		self.send("pr", a)

	def web(self, url):
		self.send("web", url)

	def check(self, l=100):
		if self.manual_connection:
			self.send("check", l)
		else:
			self.recv_check(l)

	def die(self):
		self.status = False
		self.send("die")

	def cls(self):
		self.send("cls")

	def inp(self, arg=None):
		id = randint(0, 9999999)

		self.send("inp", [arg, id])

		data = self.recv()

		try:
			if data[1][1] == id:
				return data[1][0]
			else:
				self.pr("Error, connection not secure-")
				self.die()
		except:
			self.pr("Error, connection not secure-")
			self.die()


	#RECV TOOLS
	#RECV TOOLS
	#RECV TOOLS
	#RECV TOOLS

	def recv_pr(self, args, auto_flush=True):
		for a in args:
			print(a, flush=False, end="")
		if auto_flush:
			print("")

	def recv_inp(self, args):
		for a in args:
			self.recv_pr(a, auto_flush=False)
			break

		self.send("ANSWER", [input(), args[1]])

	def recv_connect(self, args=False):
		if args:
			self.host = args[0]
			self.port = args[1]

		self.start_connection()

	def recv_back(self, args):
		self.send("ANSWER", args)

	def recv_cls(self, args):
		os.system("CLS")

	def recv_check(self, args):
		self.log_status = False
		for l in range(args):
			d = "1"*(l*10)
			s = self.send("back", d)
			r = self.recv()

			if not s[1] == s[1]:
				self.log_status = True
				self.log("Connection not secured")
				return False
		self.log_status = True
		self.log("Connection secured")
		return True

	def recv_die(self, args):
		self.status = False
		input("Connection ended by host.\nPress enter to close.")

	def recv_web(self, args):
		for url in args:
			os.system("START {}".format(url))

	def recv_reconnect(self, args):
		self.recv_die()
		self.recv_connect(args)


	#BASIC FUNCTIONS
	#BASIC FUNCTIONS
	#BASIC FUNCTIONS
	#BASIC FUNCTIONS

	def send(self, command, args=[]):
		if not type(args) == list:
			args = [args]
		self.log([["SEND", command, args]])

		data = [command, args]

		try:
			self.conn.send(pickle.dumps(data))
		except:
			self.status = False
			print(a)

		return data

	def recv(self):
		try:
			d = pickle.loads(self.conn.recv(1024))
		except:
			if self.manual_connection:
				if not self.start_connection(tries=15):
					self.status = False
		else:
			self.log([["RECV", d]])

			return d

	def connect(self, tries=1):
		self.log("Connecting")


		i = 0
		while True:
			try:
				self.conn.connect((self.host, self.port))
			except:
				if i == tries:
					self.log("Connection cant be stablished")
					return False
				else:
					i += 1
					self.log("Retrying {}".format(i))
			else:
				self.manual_connection = True
				return True

	def start_connection(self, tries=10):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		if self.connect(tries=tries):
			self.log("Connected")
			return True
		return False

	def auto_recv_messages(self):
		while True:
			d = self.recv()

	def react(self):
		while self.status:
			d = self.recv()

			try:
				atr = getattr(self, "recv_{}".format(d[0].lower()))
				if callable(atr):
					atr(d[1])
			except Exception as e:
				pass

	def start(self):
		self.log("Starting")
		
		self.start_connection()









class manager:
	def __init__(self):
		self.connections = []
		self.servers = []


	def start(self):
		pass

	def start_server(self, host, port):

		c = connection(host=host, port=port)

		self.connections.append(c)

		c.start()

	def start_connection(self, host, port):

		c = server(host=host, port=port)

		self.servers.append(c)

		c.start()