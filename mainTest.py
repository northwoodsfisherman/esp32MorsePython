import utelnetserver, network,utime
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('DorrieNet','ganshill1')
while not wlan.isconnected():
	utime.sleep(5)
	print('Waiting')
print('connected')
utelnetserver.start()
