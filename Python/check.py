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

 Copyright IBM Corp. 2019 All Rights Reserved.

 To run, see README.md
'''
import os, copy

import datetime as dt
from readConfigJSON import readJSON



'''
    Function to loop through input directory and upload all the files into the Content Analyzer API environment
'''
def uploadFiles():
    configuration, configuration_settings = readJSON()
    if (configuration):
        starttime = dt.datetime.now()
        dir_path = "/Users/abisolaadeniran/Documents/SP/EY/EY2"
        count = 0

        accepted_extensions = ["pdf", "jpeg", "jpg", "png", "pneg", "tiff", "tif", "docx", "ppt", "doc", "pptx", "xls", "xlsx"]
        print(configuration_settings['file_type'])
        print(type(configuration_settings['file_type']))
        file_types =  configuration_settings['file_type'] if 'file_type' in configuration_settings and type(configuration_settings['file_type']) is list and len(configuration_settings['file_type']) > 0 else accepted_extensions
        print(file_types)
        for subdir, dirs, files in os.walk(dir_path):
            for file in files:
                new_file = copy.copy(file)

                file_split = new_file.rsplit(".")
                file_extension = str(file_split[-1].strip().lower())
                if(file_extension != "" and file_extension in accepted_extensions and file_extension in file_types):
                    count += 1
                    print(file_extension)


        print(count)
    else:
        return False


if __name__ == '__main__':
    try:
        uploadFiles()
    except Exception as ex:
        print(ex)
        pass