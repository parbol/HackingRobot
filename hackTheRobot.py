import socket
from optparse import OptionParser
import time
import sys


################# Some global variables good to have #########################
robot_IP = '127.0.0.1'
robot_PORT = 1999
BUFFER_SIZE = 1024

serverHi = [0x00, 0x00, 0x00, 0x04, 0x00, 0x0a, 0x00, 0xa4, 0x02, 0x8c, 0x02, 0xa5, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00]
clientHi = [0x00, 0x04, 0x04, 0x1a, 0x17, 0x02, 0xe6, 0xdf, 0x00, 0x00, 0x00, 0x00]
serverMessage = [0x02, 0x00, 0xff, 0x44, 0x00, 0x14]
sendSequenceOK = [0xff, 0xff, 0xff, 0xff]

startCounting = [0x00, 0x04, 0x04, 0xde, 0x16, 0x02, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00]
sendorder = [0xff, 0x44, 0x44, 0x6a, 0x00, 0x02, 0x00, 0x0d, 0x00, 0x00, 0x00, 0x00]


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
def update_crono(countingSequence):

    dec = countingSequence[3]
    inc1 = countingSequence[6]
    inc2 = countingSequence[7]
    if dec == 0x00:
        dec = 0xff
    else:
        dec = dec - 0x01
    if inc2 == 0xff:
        inc2 = 0x01
        inc1 = inc1 + 0x01
    else:
        inc2 = inc2 + 0x01
    countingSequence[3] = dec
    countingSequence[6] = inc1
    countingSequence[7] = inc2

##############################################################################
def say_hi(s):
    
    s.send(make_string_fromHEX(clientHi))
    data = s.recv(BUFFER_SIZE)
    if not is_equal(data, serverHi):
        print bcolors.FAIL + "Server Hi response is not valid" + bcolors.ENDC
        s.close()
        sys.exit()
    s.send(make_string_fromHEX(sendSequenceOK))

    data = s.recv(BUFFER_SIZE)
    if not is_equal(data, serverMessage):
        print bcolors.FAIL + "The server tried to send an invalid message" + bcolors.ENDC
        s.close()
        sys.exit()
    size = ord(data[7])
    block = data[8:8+size]
    print bcolors.OKBLUE + "Message received from server: " + bcolors.ENDC
    print block
    s.send(make_string_fromHEX(sendSequenceOK))
    
    data = s.recv(BUFFER_SIZE)
    if not is_equal(data, serverMessage):
        print bcolors.FAIL + "The server tried to send an invalid message" + bcolors.ENDC
        s.close()
        sys.exit()
    size = ord(data[7])
    block = data[8:8+size]
    print bcolors.OKBLUE + "Message received from server: " + bcolors.ENDC
    print block
    s.send(make_string_fromHEX(sendSequenceOK))
    print bcolors.OKGREEN + 'Successful handshake with server' + bcolors.ENDC

##############################################################################
def send_counter(s, counter):

    thecounter = make_string_fromHEX(counter)
    s.send(thecounter)
    data = s.recv(BUFFER_SIZE)
    thedata = bytearray(data)
    if thedata[9] == thecounter[7] and thedata[8] == thecounter[6]:
        s.send(make_string_fromHEX(sendSequenceOK))
        update_crono(counter) 
        return True
    return False


##############################################################################
def getCommand(filename):
    
    if os.path.exists(filename):
        f = open(filename, 'r')
        command = f.readline()
        f.close()
        os.remove(filename)
        return command
    else:
        return 'none'



##############################################################################
def send_character(s, character):

    order = sendorder
    order[3] = 0x77 - character
    order[7] = character
    s.send(make_string_fromHEX(order))
    data = s.recv(BUFFER_SIZE)
    if data[9] == counter[8]:
        s.send(make_string_fromHEX(sendSequenceOK))
        return True
    return False

    
##############################################################################
def processCommand(s, command):

   n = len(command)
   #I make sure that the command ends with a 0x0d, otherwise I add it
   if command[n-1] != 0x0d:
       command = command + '\n'
   #I loop character by character and send it with the correct format
   for i in range(0, len(command)):
       if not send_character(s, command[i]):
           print 'Error in transmission'
           sys.exit()
   #Once the message was sent I read the answer from the module     
   block = ''
   while True:
        data = s.recv(BUFFER_SIZE)
        size = ord(data[7])
        block = block + size[8:8+size]
        s.send(make_string_fromHEX(sendSequenceOK))
        if block[-4] == 0x0d and block[-3] == 0x0a and block[-2] == 0x0d and block[-1] == 0x0a:
            break
   return block


##############################################################################

if __name__ == "__main__":
    
    parser = OptionParser(usage="%prog --help")
    parser.add_option("-f", "--filename",  dest="filename",  type='string',  help="Name of the interchange name.")
    (options, args) = parser.parse_args()

 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((robot_IP, robot_PORT))
    
    print 'Connection to: ', str(robot_IP), str(robot_PORT)

 
    counter = list(startCounting) 

    say_hi(s)

    while True:

        if not send_counter(s, counter):
            print bcolors.FAIL + 'There was a problem with the counter' + bcolors.ENDC
            s.close()
            sys.exit()
        print bcolors.OKGREEN + 'A counter message was sent to the server' + bcolors.ENDC
 
        #command = getCommand(options.filename)
        #if command == 'none': 
        #    if not send_counter(s, counter):
        #        print 'Problem with communications'
        #        s.close()
        #        sys.exit()
        #    time.sleep(5)
        #else:
        #    processCommand(command)


    s.close()


