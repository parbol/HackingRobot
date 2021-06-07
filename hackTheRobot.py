import socket
from optparse import OptionParser

################# Some global variables good to have #########################
robot_IP = '172.16.110.151'
robot_PORT = 1999
BUFFER_SIZE = 1024

initialSequence = [0x00, 0x04, 0x04, 0x1a, 0x17, 0x02, 0xe6, 0xdf, 0x00, 0x00, 0x00, 0x00]
sendSequenceOK = [0xff, 0xff, 0xff, 0xff]
startCounting = [0x00, 0x04, 0x04, 0xde, 0x16, 0x02, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00]



##############################################################################
def make_string_fromHEX(sample):

    sample = ''
    for i in sample:
        sample += i
    return sample


##############################################################################
def update_crono(countingSequence):

    dec = countingSequence[3]
    inc1 = countingSequence[6]
    inc2 = countingSequence[7]
    if dec == 0x00:
        dec = 0xff
    elif:
        dec = dec - 0x01
    if inc2 == 0xff:
        inc2 = 0x01
        inc1 = inc1 + 0x01
    elif:
        inc2 = inc2 + 0x01
    countingSequence[3] = dec
    countingSequence[6] = inc1
    countingSequence[7] = inc2

##############################################################################
def say_hi(s):

    s.send(make_string_fromHEX(initialSequence))
    block = ''
    while True:
        data = s.recv(BUFFER_SIZE)
        size = ord(data[7])
        block = block + size[8:8+size]
        if block[-4] == 0x0d and block[-3] == 0x0a and block[-2] == 0x0d and block[-1] == 0x0a:
            break
    s.send(make_string_fromHEX(sendSequenceOK))
    return block 

##############################################################################
def send_counter(s, counter):

    s.send(make_string_fromHEX(counter))
    data = s.recv(BUFFER_SIZE)
    if data[9] == counter[7]:
        s.send(make_string_fromHEX(sendSequenceOK))
        update_crono(counter) 
        return True
    return False


##############################################################################
def getCommand():


##############################################################################

if __name__ == "__main__":
    
    parser = OptionParser(usage="%prog --help")
    parser.add_option("-G", "--global",    action='store_true', dest="globalX",                help="Run the global reconstruction program.")
    parser.add_option("-A", "--all",       action='store_true', dest="allX",                   help="Run all the reconstruction.")
    (options, args) = parser.parse_args()

 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    
    counter = initialSequence 

    say_hi(s)

    if not send_counter(s, counter):
        print 'Problem with communications'
        s.close()
        sys.exit()

    while True:

        command = getCommand()
        if command == 'none': 
            if not send_counter(s, counter):
                print 'Problem with communications'
                s.close()
                sys.exit()
            os.sleep(1s)
        else:
            processCommand()


    s.close()


