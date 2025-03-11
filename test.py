from packet import Packet
packet = Packet("hi", 3)
dic = {1:packet, 3:5, "hola":[0,1,2,3]}
print(dic)
packet.action = "bruh"
print(dic[3])
ar = [packet, 0, 3, 6]
print(ar)
del(ar[ar.index(packet)])
print(ar)