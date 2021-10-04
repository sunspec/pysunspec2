#!/usr/bin/env python3

"""
  Copyright (c) 2021, SunSpec Alliance
  All Rights Reserved

"""

import sys
import time
import sunspec2.modbus.client as client
import sunspec2.file.client as file_client
from optparse import OptionParser

"""
  Original suns options:

      -o: output mode for data (text, xml)
      -x: export model description (slang, xml)
      -t: transport type: tcp or rtu (default: tcp)
      -a: modbus slave address (default: 1)
      -i: ip address to use for modbus tcp (default: localhost)
      -P: port number for modbus tcp (default: 502)
      -p: serial port for modbus rtu (default: /dev/ttyUSB0)
      -R: parity for modbus rtu: None, E (default: None)
      -b: baud rate for modbus rtu (default: 9600)
      -T: timeout, in seconds (can be fractional, such as 1.5; default: 2.0)
      -r: number of retries attempted for each modbus read
      -m: specify model file
      -M: specify directory containing model files
      -s: run as a test server
      -I: logger id (for sunspec logger xml output)
      -N: logger id namespace (for sunspec logger xml output, defaults to 'mac')
      -l: limit number of registers requested in a single read (max is 125)
      -c: check models for internal consistency then exit
      -v: verbose level (up to -vvvv for most verbose)
      -V: print current release number and exit
"""

if __name__ == "__main__":

    usage = 'usage: %prog [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-t', metavar=' ',
                      default='tcp',
                      help='transport type: rtu, tcp, file [default: tcp]')
    parser.add_option('-a', metavar=' ', type='int',
                      default=1,
                      help='modbus slave address [default: 1]')
    parser.add_option('-i', metavar=' ',
                      default='localhost',
                      help='ip address to use for modbus tcp [default: localhost]')
    parser.add_option('-P', metavar=' ', type='int',
                      default=502,
                      help='port number for modbus tcp [default: 502]')
    parser.add_option('-p', metavar=' ',
                      default='/dev/ttyUSB0',
                      help='serial port for modbus rtu [default: /dev/ttyUSB0]')
    parser.add_option('-b', metavar=' ',
                      default=9600,
                      help='baud rate for modbus rtu [default: 9600]')
    parser.add_option('-R', metavar=' ',
                      default=None,
                      help='parity for modbus rtu: None, E [default: None]')
    parser.add_option('-T', metavar=' ', type='float',
                      default=2.0,
                      help='timeout, in seconds (can be fractional, such as 1.5) [default: 2.0]')
    parser.add_option('-m', metavar=' ',
                      help='modbus map file')

    options, args = parser.parse_args()

    try:
        if options.t == 'tcp':
            sd = client.SunSpecModbusClientDeviceTCP(slave_id=options.a, ipaddr=options.i, ipport=options.P,
                                                     timeout=options.T)
        elif options.t == 'rtu':
            sd = client.SunSpecModbusClientDeviceRTU(slave_id=options.a, name=options.p, baudrate=options.b,
                                                     parity=options.R, timeout=options.T)
        elif options.t == 'file':
            sd = file_client.FileClientDevice(filename=options.m)
        else:
            print('Unknown -t option: %s' % (options.t))
            sys.exit(1)

    except client.SunSpecModbusClientError as e:
        print('Error: %s' % e)
        sys.exit(1)
    except file_client.FileClientError as e:
        print('Error: %s' % e)
        sys.exit(1)

    if sd is not None:
        print( '\nTimestamp: %s' % (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())))

        # read all models in the device
        sd.scan()

        print(sd.get_text())
