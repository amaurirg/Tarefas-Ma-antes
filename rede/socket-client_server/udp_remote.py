# coding: utf-8
#!/usr/bin/env python3
# Pogramação de Redes com Python
# htpps://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter02/udp_remote.py
# Cliente e servidor UDP para a comunicação de rede


import argparse, random, socket, sys


MAX_BYTES = 65535


def server(interface, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((interface, port))
	print('Listening at', sock.getsockname())
	while True:
		data, address = sock.recvfrom(MAX_BYTES)
		if random.random() < 0.5:
			print('Pretending to drop packet from {}'.format(address))
			continue
		text = data.decode('utf-8')
		print('The client at {} says {}'.format(address, text))		# {!r}
		message = 'Your data was {} bytes long'.format(len(data))
		sock.sendto(message.encode('utf-8'), address)


def client(hostname, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	hostname = sys.argv[2]
	sock.connect((hostname, port))
	print('Client socket name is {}'.format(sock.getsockname()))

	delay = 0.1 	#segundos
	text = 'This is another message'
	data = text.encode('utf-8')
	while True:
		sock.send(data)
		print('Waiting up to {} seconds for a replay'.format(delay))
		sock.settimeout(delay)
		try:
			data = sock.recv(MAX_BYTES)
		except socket.timeout:
			delay *= 2 		# espera ainda mais pela próxima solicitação
			if delay > 2.0:
				raise RuntimeError('I think the server is down')
			else:
				break 		# terminamos e não podemos interromper o loop

	print('The server says {}'.format(data.decode('utf-8')))		# {!r}


if __name__ == '__main__':
	choices = {'client': client, 'server': server}
	parser = argparse.ArgumentParser(description='Send and receive UDP,'
									' pretending packets are often dropped')
	parser.add_argument('role', choices=choices, help='wich role to take')
	parser.add_argument('host', help='interface the server listen at;'
						'host the client sends to')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060,
						help='UDP port (default(1060)')
	args = parser.parse_args()
	function = choices[args.role]
	function(args.host, args.p)
