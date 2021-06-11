from optparse import OptionParser
from RobotControl.RobotServer import RobotServer
  


if __name__ == "__main__":
    
    parser = OptionParser(usage="%prog --help")
    parser.add_option("-i", "--ip",              dest="ip",              type='string',  default='172.16.110.151', help="IP of the server.")
    parser.add_option("-p", "--port",            dest="port",            type=int,       default=1999,             help="Port of the server.")
    (options, args) = parser.parse_args()

    server = RobotServer(options.ip, options.port)



