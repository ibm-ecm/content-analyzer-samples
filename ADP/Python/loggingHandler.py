'''
DISCLAIMER OF WARRANTIES.
 This code is sample code created by IBM Corporation. IBM grants you a
 nonexclusive copyright license to use this sample code example. This
 sample code is not part of any standard IBM product and is provided to you
 solely for the purpose of assisting you in the development of your
 applications. This example has not been thoroughly tested under all
 conditions. IBM, therefore cannot guarantee nor may you imply reliability,
 serviceability, or function of these programs. The code is provided "AS IS",
 without warranty of any kind. IBM shall not be liable for any damages
 arising out of your or any other parties use of the sample code, even if IBM
 has been advised of the possibility of such damages. If you do not agree with
 these terms, do not use the sample code.

 Copyright IBM Corp. 2022 All Rights Reserved.

 To run, see README.md
'''
import logging, sys
import logging.handlers

formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

logger = logging.getLogger("ContentAnalyzer")
logger.setLevel(logging.DEBUG)

file_handler = logging.handlers.RotatingFileHandler('processing.log', maxBytes=5*1024*1024, backupCount=0)
file_handler.setLevel(logging.DEBUG)


stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)