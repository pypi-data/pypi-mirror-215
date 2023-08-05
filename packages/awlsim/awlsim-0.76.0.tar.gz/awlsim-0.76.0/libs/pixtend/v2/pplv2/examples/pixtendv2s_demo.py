#!/usr/bin/env python
# coding=utf-8

# MIT License
# 
# Copyright (C) 2021 Kontron Electronics GmbH <support@pixtend.de>
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# 
# For further details see LICENSE.txt.

# -----------------------------------------------------------------------------
# Attention:
# The PiXtend Python Library v2 (PPLv2) was developed as a Python 
# library / module to make use of the inheritance functionality of Python.
# However, since the library must access the hardware based SPI bus on the
# Raspberry Pi only ONE single instance of the PiXtendV2S or PiXtendV2L
# class per PiXtend is allowed! The PPLv2 as well as the SPI bus is not 
# capable of aggregating (multiplexing) multiple instances of either
# PiXtend class. Please keep this in mind when developing your application.
# We suggest building one central program which creates the PiXtend object
# and all other programs, functions, threads use inter-process communication
# with the main program to send data to the PiXtend board to manipulate the
# analog and/or digital outputs or to get information from the inputs.
# -----------------------------------------------------------------------------

from __future__ import print_function
# Import PiXtend V2 class
from pixtendv2s import PiXtendV2S
import time
import sys

strSlogan1 = "PiXtend Python Library v2 (PPLv2) demo."
strSlogan2 = "PiXtend Python Library v2 (PPLv2) demo finished."

# -----------------------------------------------------------------
# Print Art and Slogan
# -----------------------------------------------------------------
print("")
print("    ____  _ _  ____                 __   _    _____        _____")
print("   / __ \\(_) |/ / /____  ____  ____/ /  | |  / /__ \\      / ___/")
print("  / /_/ / /|   / __/ _ \\/ __ \\/ __  /   | | / /__/ / ____ \\__ \\ ")
print(" / ____/ //   / /_/  __/ / / / /_/ /    | |/ // __/ /___/__ / / ")
print("/_/   /_//_/|_\\__/\\___/_/ /_/\\__,_/     |___//____/     /____/  ")
print("")
print(strSlogan1)
print("")

# -----------------------------------------------------------------
# Create instance - SPI communication starts automatically
# -----------------------------------------------------------------
p = PiXtendV2S()

# -----------------------------------------------------
# Main Program
# -----------------------------------------------------
if p is not None:
    print("Running Main Program - Hit Ctrl + C to exit")
    # Set some variables needed in the main loop
    is_config = False
    cycle_counter = 0

    while True:
        try:
            # Check if SPI communication is running and the received data is correct
            if p.crc_header_in_error is False and p.crc_data_in_error is False:
                cycle_counter += 1

                if not is_config:
                    is_config = True
                    print("One time configuration: Setting the relays and digital outputs in an alternating pattern")
                    print("The value False = OFF and the value True = ON")
                    print("")
                    # Setting the relays and digital outputs to a pattern which can be toggled later.
                    # Side effect: the LEDs on the PiXtend V2 -S- board alternate nicely back and forth.
                    p.relay0 = p.ON
                    p.relay1 = p.OFF
                    p.relay2 = p.ON
                    p.relay3 = p.OFF
                    p.digital_out0 = p.ON
                    p.digital_out1 = p.OFF
                    p.digital_out2 = p.ON
                    p.digital_out3 = p.OFF

                # clear the text on screen
                str_text = "                                               \n"
                for i in range(0, 27, 1):
                    str_text += "                                               \n"
                str_text += " "
                # Print text to console
                print(str_text, end="\r")
                # Reset cursor
                for i in range(0, 28, 1):
                    sys.stdout.write("\x1b[A")  
                    
                # Print the info text to console
                str_text = "Cycle No.: {0}\n".format(cycle_counter)
                str_text += " \n"
                str_text += "PiXtend V2 -S- Info:\n"
                str_text += "Firmware:    {0}\n".format(p.firmware)
                str_text += "Hardware:    {0}\n".format(p.hardware)
                str_text += "Model:       {0}\n".format(chr(p.model_in))
                str_text += " \n"
                str_text += "Digital Inputs:\n"
                str_text += "DigitalIn0:  {0}\n".format(p.digital_in0)
                str_text += "DigitalIn1:  {0}\n".format(p.digital_in1)
                str_text += "DigitalIn2:  {0}\n".format(p.digital_in2)
                str_text += "DigitalIn3:  {0}\n".format(p.digital_in3)
                str_text += "DigitalIn4:  {0}\n".format(p.digital_in4)
                str_text += "DigitalIn5:  {0}\n".format(p.digital_in5)
                str_text += "DigitalIn6:  {0}\n".format(p.digital_in6)
                str_text += "DigitalIn7:  {0}\n".format(p.digital_in7)
                str_text += " \n"
                str_text += "Digital Outputs:\n"
                str_text += "DigitalOut0: {0}\n".format(p.digital_out0)
                str_text += "DigitalOut1: {0}\n".format(p.digital_out1)
                str_text += "DigitalOut2: {0}\n".format(p.digital_out2)
                str_text += "DigitalOut3: {0}\n".format(p.digital_out3)
                str_text += " \n"
                str_text += "Relays:\n"
                str_text += "Relay0:      {0}\n".format(p.relay0)
                str_text += "Relay1:      {0}\n".format(p.relay1)
                str_text += "Relay2:      {0}\n".format(p.relay2)
                str_text += "Relay3:      {0}\n".format(p.relay3)
                str_text += " "

                # Print text to console
                print(str_text, end="\r")

                # Reset cursor
                for i in range(0, 28, 1):
                    sys.stdout.write("\x1b[A")

                # Toggle the relays and digital outputs on and off
                p.relay0 = not p.relay0
                p.relay1 = not p.relay1
                p.relay2 = not p.relay2
                p.relay3 = not p.relay3
                p.digital_out0 = not p.digital_out0
                p.digital_out1 = not p.digital_out1
                p.digital_out2 = not p.digital_out2
                p.digital_out3 = not p.digital_out3

            else:
                for i in range(0, 29, 1):
                    print("")
                print("")
                print("Communication error, the data from the microcontroller is not correct!")
                print("Leaving the application. Please check that the Raspberry Pi can communicate")
                print("with the microcontroller on the PiXtend V2 -S- board.")
                print("")
                
                p.digital_out0 = p.OFF
                p.digital_out1 = p.OFF
                p.digital_out2 = p.OFF
                p.digital_out3 = p.OFF
                p.relay0 = p.OFF
                p.relay1 = p.OFF
                p.relay2 = p.OFF
                p.relay3 = p.OFF
                time.sleep(0.25)
                p.close()
                time.sleep(0.25)
                del p
                p = None
                break
                
            # Wait some time, SPI communication will continue in the background
            time.sleep(1)

        # Catch errors and if an error is caught, leave the program
        except IOError as e:
            # Print out the caught error and leave program
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            p.close()
            time.sleep(0.25)
            del p
            p = None
            break
            
        except ValueError as ve:
            # Print out the caught error and leave program
            print ("Value error({0}): {1}".format(ve.errno, ve.strerror))
            p.close()
            time.sleep(0.25)
            del p
            p = None
            break

        except RuntimeError as re:
            # Print out the caught error and leave program
            print ("Runtime error({0}): {1}".format(re.errno, re.strerror))
            p.close()
            time.sleep(0.25)
            del p
            p = None
            break 

        except KeyboardInterrupt:
            # Keyboard interrupt caught, Ctrl + C, now clean up and leave program
            for i in range(0, 29, 1):
                print("")
            print(strSlogan2)
            
            p.digital_out0 = p.OFF
            p.digital_out1 = p.OFF
            p.digital_out2 = p.OFF
            p.digital_out3 = p.OFF
            p.relay0 = p.OFF
            p.relay1 = p.OFF
            p.relay2 = p.OFF
            p.relay3 = p.OFF
            time.sleep(0.25)
            p.close()
            time.sleep(0.25)
            del p
            p = None
            break
