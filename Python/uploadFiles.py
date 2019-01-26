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
import os, json, copy, re

import requests, time
import datetime as dt
from base64 import b64encode
from readConfigJSON import readJSON
from loggingHandler import logger
from ssl import SSLError


'''
    Function to loop through input directory and upload all the files into the Content Analyzer API environment
'''
def uploadFiles():
    configuration, configuration_settings = readJSON()
    if (configuration):
        starttime = dt.datetime.now()
        dir_path = configuration_settings["directory_path"]
        count = 0

        errors = []
        upload_url = configuration_settings['main_url']
        accepted_extensions = ["pdf", "jpeg", "jpg", "png", "pneg", "tiff", "tif", "docx", "ppt", "doc", "pptx", "xls", "xlsx"]
        file_types =  configuration_settings['file_type'] if 'file_type' in configuration_settings and type(configuration_settings['file_type'] is list) and len(configuration_settings['file_type']) > 0 else accepted_extensions
        output_results = []
        for subdir, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(subdir, file)
                new_file = copy.copy(file)

                file_split = new_file.rsplit(".")
                file_extension = str(file_split[-1].strip().lower())
                old_file_name = new_file.replace("." + file_extension, '').strip()
                file_name = re.sub('[^A-Za-z0-9 _]+', ' ', old_file_name) + "." + str(file_extension)
                new_file_path = os.path.join(subdir, file_name)
                if(file_extension != "" and file_extension in accepted_extensions and file_extension in file_types):
                    count += 1
                    try:
                        logger.info("Uploading {0} ".format(new_file_path))
                    except:
                        pass

                    files = {'file': (file_name, open(file_path, 'rb'), "multipart/form-data")}
                    headers = {
                        'apiKey': configuration_settings['api_key']
                    }

                    if "function_id" in configuration_settings:
                            credentials = ('%s:%s' % (
                            configuration_settings["function_id"], configuration_settings["password"]))
                            encoded_credentials = b64encode(credentials.encode('ascii'))
                            headers['Authorization'] = 'Basic %s' % encoded_credentials.decode("utf-8")

                    dict_object = {"filename": file_name, "path": os.path.basename(subdir), "full_path": os.path.join(os.path.abspath(subdir), old_file_name + "." + str(file_extension))}

                    # Make request
                    try:
                        response = requests.request("POST", upload_url, files=files,
                                data={'jsonOptions': configuration_settings['json_options'], 'responseType': configuration_settings['output_options']}, headers=headers, verify=configuration_settings['ssl_verification'])
                        if response.status_code >= 400:
                            logger.error("HTTP error {0} occurred when uploading file: {1} ".format(str(response.status_code), file_path))
                            dict_object.update({"error": response.text})
                            errors.append(dict_object)
                        else:
                            dict_object.update({"response": response.text, "output_type": configuration_settings['output_options'].split(",")})
                            output_results.append(dict_object)

                    except SSLError as sslerror:
                        logger.error("SSL error was thrown due to certificate failure, set ssl_verification to false in configuration config.json file.")
                        dict_object.update({"error": str(sslerror)})
                        errors.append(dict_object)
                    except Exception as ex:
                        dict_object.update({"error": str(ex)})
                        errors.append(dict_object)
                        logger.error("An error occurred when trying to upload file " + file_path)
                        logger.debug(ex, exc_info=True)
                        pass

                endtime = dt.datetime.now()
                seconds = (endtime - starttime).total_seconds()
                result = {"starttime": str(starttime), "endtime": str(endtime), "no_of_files": count,
                          "output_results": output_results, "no_output_results": len(output_results),
                          "total_upload_seconds": seconds, "upload_errors": errors, "no_of_upload_errors": len(errors)}
                json.dump(result, open(os.path.join(os.getcwd(), "output.json"), 'w'), indent=4)
        logger.info("Upload status reported in output.json")
        if count == 0:
            logger.error("No files found in directory_path, " + dir_path)
            return False
        elif len(errors) > 0:
            logger.error("Errors occurred during upload.")
            return True
        else:
            logger.info("Done uploading {0} files".format(count))
            return True
    else:
        logger.error("Check your configuration file (config.json) for correct format and valid parameters")
        return False


if __name__ == '__main__':
    logger.info("Logs can be found in current directory (processing.log)")
    try:
        uploadFiles()
    except Exception as ex:
        logger.error("An error occurred, please check logs for more details")
        logger.debug(ex, exc_info=True)