import socket
from optparse import OptionParser
import sys
import time





################# Some global variables good to have #########################

#Connection information 
#robot_IP = '172.16.110.151'
#robot_PORT = 1999
robot_IP = '127.0.0.1'
robot_PORT = 1999
BUFFER_SIZE = 1024

serverHi = [0x00, 0x00, 0x00, 0x04, 0x00, 0x0a, 0x00, 0xa4, 0x02, 0x8c, 0x02, 0xa5, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00]
clientHi = [0x00, 0x04, 0x04, 0x1a, 0x17, 0x02, 0xe6, 0xdf, 0x00, 0x00, 0x00, 0x00]
serverMessage = [0x02, 0x00, 0xff, 0x44, 0x00, 0x14]
sendallSequenceOK = [0xff, 0xff, 0xff, 0xff]
startCounting = [0x00, 0x04, 0x04, 0xde, 0x16, 0x02, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00]
countingAnswer = [0x00, 0x00, 0x00, 0x04, 0x00, 0x0f, 0x00, 0x02]

sendallorder = [0xff, 0x44, 0x44, 0x6a, 0x00, 0x02, 0x00, 0x0d, 0x00, 0x00, 0x00, 0x00]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
###############################################################################



##############################################################################
def make_string_fromHEX(sample):

    arr = bytearray(sample)
    return arr


##############################################################################
def is_equal(data1, data2):

    thedata1 = bytearray(data1)
    thedata2 = make_string_fromHEX(data2)
    for i in range(0, len(thedata2)):
        if thedata1[i] != thedata2[i]:
            return False
    return True

##############################################################################
def is_handshake(data):

    return is_equal(data, clientHi)


##############################################################################
def is_counter(data):

    thedata = bytearray(data)
    counter = make_string_fromHEX(startCounting)
 
    if counter[0] == thedata[0] and counter[1] == thedata[1] and counter[2] == thedata[2] and counter[4] == thedata[4] and counter[5] == thedata[5]:
        return True
    return False 


##############################################################################
def check_answer(connection):

    data = connection.recv(4)
    print 'the answer was ', len(data)
    return is_equal(data, sendallSequenceOK)
    
##############################################################################
def handle_handshake(connection, data):

    firstmessage = make_string_fromHEX(serverHi) 
    message = bytearray('Hello stupid robot\x0d\x0a\x0d\x0a', 'ascii')
    firstmessage.extend(message)
    connection.sendall(firstmessage)
    if not check_answer(connection):
        print bcolors.FAIL + "The OK message was not received" + bcolors.ENDC
        sys.exit()

    message2 = "This is some random information"
    n = len(message2)
    message = bytearray(message2, 'ascii')
    server = list(serverMessage)
    server.append(0x00)
    server.append(n)
    secondmessage = make_string_fromHEX(server)
    secondmessage.extend(message)
    connection.sendall(secondmessage)
    if not check_answer(connection):
        print bcolors.FAIL + "The OK message was not received" + bcolors.ENDC
        connection.close()
        sys.exit()
    message3 = "This is the ROBOT information"
    n = len(message3)
    message = bytearray(message3, 'ascii')
    server = list(serverMessage)
    server.append(0x00)
    server.append(n)    
    thirdmessage = make_string_fromHEX(server)
    thirdmessage.extend(message)
    connection.sendall(thirdmessage)
    if not check_answer(connection):
        print bcolors.FAIL + "The OK message was not received" + bcolors.ENDC
        connection.close()
        sys.exit()
    print bcolors.OKGREEN + "Handshake was correctly done in the server" + bcolors.ENDC 
    return True

##############################################################################
def handle_counter(connection, data):

    thedata = bytearray(data)
    answer = list(countingAnswer)
    answer.append(ord(data[6]))
    answer.append(ord(data[7]))
    message = make_string_fromHEX(answer)
    time.sleep(1)
    connection.sendall(message)
    if not check_answer(connection):
        print bcolors.FAIL + "The OK message was not received" + bcolors.ENDC
        connection.close()
        sys.exit()
    print bcolors.OKGREEN + "Counter message with id " + str(ord(data[6])) + ' ' + str(ord(data[7])) + ' received by server' + bcolors.ENDC
    return True
      

##############################################################################

if __name__ == "__main__":
    
    parser = OptionParser(usage="%prog --help")
    parser.add_option("-i", "--ip",         dest="ip",    type='string',  default='172.16.110.151', help="IP of the server.")
    parser.add_option("-p", "--port",       dest="port",  type=int,       default=1999,             help="Port of the server.")
    parser.add_option("-b", "--buffer",     dest="buffer",  type=int,     default=1024,             help="buffer size")
    (options, args) = parser.parse_args()

    print bcolors.HEADER + "##############################" + bcolors.ENDC
    print bcolors.HEADER + "Starting ROBOT server emulator" + bcolors.ENDC
    print bcolors.HEADER + "##############################" + bcolors.ENDC
    print bcolors.OKBLUE + "Emulator IP: "     + options.ip          + bcolors.ENDC
    print bcolors.OKBLUE + "Emulator PORT: "   + str(options.port)   + bcolors.ENDC
    print bcolors.OKBLUE + "Emulator buffer: " + str(options.buffer) + bcolors.ENDC
    print bcolors.HEADER + "##############################" + bcolors.ENDC

    #Setup the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (options.ip, options.port)
    s.bind(server_address)
    s.listen(1)

    connection, client_address = s.accept()
    try:
        print bcolors.OKGREEN + "Connection request from: " + client_address[0] + bcolors.ENDC
        print bcolors.HEADER + "##############################" + bcolors.ENDC
        data = connection.recv(12) 
        if is_handshake(data):
            if handle_handshake(connection, data):
                print bcolors.OKBLUE + "The handshake was successful" + bcolors.ENDC
            else:
                print bcolors.FAIL + "The handshake was not successful" + bcolors.ENDC
                connection.close()
                sys.exit()
        else:
            print bcolors.FAIL + "The handshake process was not successful: exiting" + bcolors.ENDC
            connection.close()
            sys.exit()
        while True:
            print 'before data' 
            data = connection.recv(12) 
            print 'aftere data' 
            if is_counter(data):
                print 'before handle' 
                handle_counter(connection, data)
                print 'after handle' 
            #elif is_command(data):
            #    handle_command(connection, data)
            else:
                print bcolors.FAIL + "Unexpected message from the client: exiting" + bcolors.ENDC
                sys.exit()     
    finally:
        connection.close()    



