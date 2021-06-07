import socket
from optparse import OptionParser

################# Some global variables good to have #########################
robot_IP = '172.16.110.151'
robot_PORT = 1999
BUFFER_SIZE = 1024

initialSequence = [0x00, 0x04, 0x04, 0x1a, 0x17, 0x02, 0xe6, 0xdf, 0x00, 0x00, 0x00, 0x00]
sendSequenceOK = [0xff, 0xff, 0xff, 0xff]
startCounting = [0x00, 0x04, 0x04, 0xde, 0x16, 0x02, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00]


############################################################################################################################

if __name__ == "__main__":
    
    parser = OptionParser(usage="%prog --help")
    parser.add_option("-G", "--global",    action='store_true', dest="globalX",                help="Run the global reconstruction program.")
    parser.add_option("-A", "--all",       action='store_true', dest="allX",                   help="Run all the reconstruction.")
    (options, args) = parser.parse_args()


     
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))



MESSAGE = "Hello, World!"
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()
print "received data:", data


