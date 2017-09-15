#!/usr/bin/env python
# ******************************************************************************
# 
# Name:    catfeeder.py
# Author:  Gabriel Gonzalez
# Email:   gabeg@bu.edu
# License: The MIT License (MIT)
# 
# Syntax: catfeeder.py [options] <args>
# 
# Description: Display weather information at a given zipcode, using the Weather
#              Underground API.
# 
# Notes: None.
# 
# ******************************************************************************

# Imports
import __init__
import argparse
import logging
import motor.servo
import os
import personal.util
import sys

logging.basicConfig(level=logging.INFO)

# Globals
PROG = os.path.basename(sys.argv[0])
LOG  = logging.getLogger(__name__)

# Exit statuses
EARG = 2

# ******************************************************************************
def main():
    '''
    Main for pet feeder.
    '''

    if (len(sys.argv) <= 1):
        print usage()
        exit(0)

    parser = argparse.ArgumentParser(prog=PROG,
                                     usage=get_usage(),
                                     add_help=False)

    # Parse options
    parser.add_argument('-h', '--help',     action='help')
    parser.add_argument('-p', '--pin',      action='store')
    parser.add_argument('-d', '--duration', action='store')
    parser.add_argument('-l', '--log',      action='store')
    args = parser.parse_args()

    # Define servo motor
    servo = motor.servo.ServoMotor(pin=args.pin, dur=args.duration)

    # Check inputs
    if (not servo.is_pin(args.pin)):
        print "%s: Invalid circuit board pin '%s'." % (PROG, args.pin)
        exit(EARG)
    if (not servo.is_duration(args.duration)):
        print "%s: Invalid feed duration time '%s'." % (PROG, args.duration)
        exit(EARG)
    if (args.log is not None):
        LOG.addHandler(personal.util.log_file_handler(args.log))

    # Run pet feeder
    return run(servo)

# ******************************************************************************
def usage():
    '''
    Print usage.
    '''

    print get_usage()
    return 0

# ******************************************************************************
def run(servo):
    '''
    Run pet feeder.
    '''

    LOG.info('Dispensing food.')
    servo.turn_cw()
    return 0

# ******************************************************************************
def get_usage():
    '''
    Return usage message.
    '''

    string  = "Usage: %s [options] <args>\n" % (PROG)
    string += "\n"
    string += "Options:\n"
    string += "    -h, --help\n"
    string += "        Print the program usage.\n"
    string += "\n"
    string += "    -p, --pin <pin>\n"
    string += "        Pin that servo motor is connected to.\n"
    string += "\n"
    string += "    -d, --dur <time>\n"
    string += "        Amount of time (sec) to run servo motor, in order to feed pet.\n"
    string += "\n"
    string += "    -l, --log <logfile>\n"
    string += "        File to log contents to.\n"
    string += "\n"
    string += "Arguments:\n"
    string += "    <pin>\n"
    string += "        Pin that servo motor is connected to.\n"
    string += "\n"
    string += "    <time>\n"
    string += "        Amount of time (sec) to run servo motor in order to feed cat.\n"
    string += "\n"
    string += "    <log>\n"
    string += "        File to log contents to.\n"
    return string

# ******************************************************************************
main()
