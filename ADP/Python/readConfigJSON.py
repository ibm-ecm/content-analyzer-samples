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

import json, os
from loggingHandler import *

'''
    Function to read configuration settings and ensure all the parameters needed are present.
'''
def readJSON():
    current_directory = os.getcwd()
    json_path = os.path.join(current_directory, "config.json")
    false_result = False, {}
    if(os.path.exists(json_path)):
        try:
            json_info = json.load(open(json_path, "r"))
            input_path = json_info["directory_path"]
            true_result = True, json_info
            if(not os.path.exists(input_path)):
                logger.error("Cannot find directory_path {0}.".format(input_path))
                return false_result
            else:
                list_keys = json_info.keys()
                value = True
                expected_keys = ['zen_host', 'zen_username', 'zen_password', 'adp_project_id', 
                        'directory_path', 'output_directory_path', 'output_options', 'json_options']
                for key in expected_keys:
                    if key not in list_keys:
                        logger.error("Missing key: " + key)
                        value = False
                    elif not json_info.get(key):
                        logger.error("Missing value for key " + key)
                if "zen_host" in list_keys and json_info["zen_host"]:
                    if ("zen_username" not in list_keys or json_info["zen_username"] == "") or ("zen_password" not in list_keys or json_info["zen_password"] == ""):
                        logger.error("Missing username or password")
                        value = False
                if(value):
                    if 'ssl_verification' not in list_keys:
                        json_info['ssl_verification'] = False

                    expected_json_options = ['json', 'pdf']
                    json_options = json_info["output_options"].split(',')
                    for option in json_options:
                        option = option.strip().lower()
                        if option not in expected_json_options:
                            logger.error('{} cannot be in output_options. Only json, pdf supported'.format(option))
                            return false_result
                    if("json" in json_info["output_options"] and json_info["json_options"] == ""):
                        logger.error("JSON selected however no json_options was set")
                        return false_result
                    elif ("json" in json_info["output_options"] or "pdf" in json_info["output_options"]):
                        json_info["aca_main_url"] = 'https://' + json_info['zen_host'].strip() + '/adp/aca/v1/projects/' + json_info['adp_project_id'] + '/analyzers'
                        json_info["accepted_extensions"] = ["pdf", "jpeg", "jpg", "png", "pneg", "tiff", "tif", "docx", "doc"]
                        return true_result
                    else:
                        logger.error("only json or pdf can be inputted for output_options.")
                        return false_result
                else:
                    return false_result
        except Exception as ex:
            logger.error("Error reading configuration file {0}".format(json_path))
            logger.error("Exception: "+str(ex))
            return false_result
    else:
        logger.error("Cannot find configuration file in directory: {0}".format(json_path))
        return false_result




if __name__ == '__main__':
    logger.info("**************************************")
    logger.info("API Sample tool readConfigJSON starting...")
    logger.info("Logs can be found in the current directory, processing.log")
    result = readJSON()
    print(result)