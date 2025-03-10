from packet import Packet
packet = Packet("hi", 3)
dic = {1:packet, 3:5, "hola":[0,1,2,3]}
print(dic)
packet.action = "bruh"
print(dic)