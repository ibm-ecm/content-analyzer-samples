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
import requests
from loggingHandler import logger
from readConfigJSON import readJSON
from ssl import SSLError
from base64 import b64encode
from checkToken import checkTokenValid
from checkToken import generateToken_pw_flow
import datetime as dt


'''
    Function to delete all output files of one processed file with an analyzer ID through the Content Analyzer API
'''
def deleteFile(configuration_settings, token, analyzerId):
    # Make requests
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    get_url = configuration_settings['aca_main_url'] + "/{0}".format(analyzerId)
    try:
        response = requests.request("DELETE", get_url, headers=headers, verify=configuration_settings['ssl_verification'])
        if response.status_code >= 400:
            logger.error("An error occurred while trying to delete file.")
            return False, response.text
        else:
            response_json = json.loads(response.text)
            return True, response_json
    except SSLError as sslerror:
        logger.error("SSL error was thrown due to certificate failure, set ssl_verification to false in configuration config.json file.")
        logger.debug(sslerror, exc_info=True)
    except Exception as ex:
        logger.error("An error occured when trying to get file")
        logger.debug(ex, exc_info=True)
        pass
    return False, {}

'''
    Function to loop through each processed file and call the deleteFile function
'''
def deleteFiles(token):
    configuration, configuration_settings = readJSON()
    if (configuration):
        token = checkTokenValid(token, configuration_settings)
        if token:
            starttime = dt.datetime.now()
            output_json_path = os.path.join(os.getcwd(), "output.json")
            if(os.path.exists(output_json_path)):
                output_json = json.load(open(output_json_path, "r"))
                if("output_results" in output_json and len(output_json["output_results"]) > 0):
                    output_json_result = output_json["output_results"]
                    new_output_json_result = []
                    for outresult in output_json_result:
                        result = outresult
                        try:
                            if "response" in result and "result" in json.loads(result["response"]) and "data" in json.loads(result["response"])["result"][0] and "analyzerId" in json.loads(result["response"])["result"][0]["data"]:
                                if ("deleted" in result and result["deleted"] == False) or "deleted" not in result:
                                    response = json.loads(result["response"])
                                    # print(response)
                                    analyzerId = response["result"][0]["data"]["analyzerId"]

                                    current_time = dt.datetime.now()
                                    seconds = (current_time - starttime).total_seconds()
                                    if seconds < 7000 * 5: # refresh zen token every 10 hours (7199 = 2 hours)
                                        if token:
                                            status, result_response = deleteFile(configuration_settings, token, analyzerId)
                                            if (status):
                                                result["deleted"] = True
                                            else:
                                                result["deleted"] = False
                                        else:
                                            token = generateToken_pw_flow(configuration_settings)
                        except:
                            result["deleted"] = False
                            logger.error("No analyzerID available to delete results. The file upload may have failed. File name: {0}".format(result["filename"]))

                        # new_output_json_result.append(result)
                        output_json["output_results"] = output_json_result
                        json.dump(output_json, open("output.json", 'w'), indent=4)

                    logger.info("Done deleting files on the server")
                    logger.info("Delete status reported in output.json")
                else:
                    logger.error("No results found that needs deleting.")
            else:
                logger.error("output.json file does not exist. No results available to delete.")
        else:
            logger.error("Zen token is required to delete files")


if __name__ == '__main__':
    logger.info("**************************************")
    logger.info("API Sample tool deleteFiles starting...")
    logger.info("Logs can be found in the current directory, processing.log")
    output_json_path = os.path.join(os.getcwd(), "output.json")
    if(os.path.exists(output_json_path)):
        output_json = json.load(open(output_json_path, "r"))
        token = output_json.get('zen_token') if output_json.get('zen_token') else "token"
        # print(token)
    else:
        token = "token"
    deleteFiles(token)
