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

 Copyright IBM Corp. 2021 All Rights Reserved.

 To run, see README.md
'''
import json, os
import requests
import datetime as dt
from loggingHandler import logger
from readConfigJSON import readJSON
import time, copy
from ssl import SSLError
from base64 import b64encode
from checkToken import checkTokenValid
from checkToken import generateToken_pw_flow
import datetime as dt

'''
    Function to check file status if completed, failed or inprogress
'''
def checkStatus(configuration_settings, token, analyzerId):
    # Make request
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    get_url = configuration_settings['aca_main_url'] + "/{0}".format(analyzerId)
    try:
        response = requests.request("GET", get_url, headers=headers, verify=configuration_settings['ssl_verification'])
        if response.status_code >= 400:
            logger.error("An error occurred while trying to get file status.")
            return False, response.text
        else:
            response_json = json.loads(response.text)
            if "result" in response_json:
                return True, response_json["result"][0]
            else:
                return False, {}
    except SSLError as sslerror:
        logger.error("SSL error was thrown due to certificate failure, set ssl_verification to false in configuration config.json file.")
        logger.debug(sslerror, exc_info=True)
    except Exception as ex:
        print(ex)
        logger.error("An error occured when trying to get file")
        logger.debug(ex, exc_info=True)
        pass
    return False, {}

'''
    Function to download file and save in user's output_directory_path, based on the output type (pdf, utf8,json)
'''
def downloadFile(configuration_settings, token, analyzerId, output, output_path, filename):
    # Make request
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    extra_path = "/{0}/{1}".format(analyzerId, output.lower())
    get_url = configuration_settings['aca_main_url'] + extra_path
    try:
        response = requests.request("GET", get_url, headers=headers, verify=configuration_settings['ssl_verification'])
        # print(response.text)
        if response.status_code >= 400:
            logger.error("An error occurred while trying to download output.")
            return False, response.text
        else:
            file_name = copy.copy(filename)
            filename_output = "{0}.{1}".format(file_name, output.lower()) if output.lower() != "utf8" else "{0}.txt".format(file_name)
            filename_output = filename_output if output.lower() != "pdf" else "New_{0}.{1}".format(file_name, output.lower())
            file_output_path = os.path.join(configuration_settings["output_directory_path"], output_path, output.lower())
            filename_output_path = os.path.join(file_output_path, filename_output)
            if( not os.path.exists(file_output_path)):
                os.makedirs(file_output_path)
                logger.info("Created new output directory, "+ file_output_path)
            if(output.lower() == "json"):
                response_output = json.loads(response.text)
                if "result" in response_output and "data" in response_output["result"][0]:
                    json.dump(response_output["result"][0]["data"], open(filename_output_path, "w"), indent=4)
            elif output.lower() == "pdf":
                output_write = open(filename_output_path, "wb")
                output_write.write(response.content)
                output_write.close()
            return True, ""
    except SSLError as sslerror:
        logger.error("SSL error was thrown due to certificate failure, set ssl_verification to false in configuration config.json file.")
        logger.debug(sslerror, exc_info=True)
    except Exception as ex:
        logger.error("An error occurred when trying to get file")
        logger.debug(ex, exc_info=True)
        pass
    return False, ""

'''
    Function to confirm if download outputs already exists
'''
def checkCompleted(latest_output_outputs, result):
    output_exists = []
    for output in latest_output_outputs:
        if (output in result):
            output_exists.append(output)
    if(len(output_exists) >= len(latest_output_outputs)):
        return True
    else:
        return False


'''
    Function to begin looking at the output.json file, for each content, check file processing status if ready, download the file, if not ready keep looping, till you get all the file, loop 30000 times and stop if not complete, so system resources are freed while looping, user's can always run downloadFiles.py again to continue downloading
'''
def downloadFiles(token):
    pending_completion = True
    configuration, configuration_settings = readJSON()
    if (configuration):
        token, generated_time = checkTokenValid(token, configuration_settings)
        if token:
            loop = 0
            failed_download = []
            completed_download = []
            compelted_check = []
            completed_count = 0
            output_json_path = os.path.join(os.getcwd(), "output.json")
            if(os.path.exists(output_json_path)):
                while pending_completion and loop < 1000:
                    output_json = json.load(open(output_json_path, "r"))
                    loop += 1
                    logger.info("Loop " + str(loop))
                    # print(output_json)
                    if("output_results" in output_json and len(output_json["output_results"]) > 0):
                        output_json_result = output_json["output_results"]
                        new_output_json_result = []
                        for outresult in output_json_result:
                            result = outresult
                            try:
                                if "response" in result and "result" in json.loads(result["response"]) and "data" in json.loads(result["response"])["result"][0] and "analyzerId" in json.loads(result["response"])["result"][0]["data"]:
                                    if "download_success" not in result:
                                        response = json.loads(result["response"])
                                        path = result["path"]
                                        filename = result["filename"]
                                        analyzerId = response["result"][0]["data"]["analyzerId"]

                                        output_outputs = result["output_type"]
                                        latest_output_outputs = [output.replace("\"", "").upper() for output in
                                                                output_outputs]

                                        if("download_completed" not in result):
                                            completed = checkCompleted(latest_output_outputs, result)
                                            if(completed):
                                                result["download_completed"] = True

                                            else:
                                                current_time = dt.datetime.now()
                                                seconds = (current_time - generated_time).total_seconds()
                                                if seconds < 7000: # ums token is not expired (7199 = 2 hours)
                                                    if token:
                                                        headers = {
                                                            'Authorization': 'Bearer {}'.format(token)
                                                        }
                                                        logger.info("Checking status of analyzerId: {}, filename: {}".format(analyzerId, filename))
                                                        status, result_response = checkStatus(configuration_settings, token, analyzerId)

                                                        if (status):
                                                            if ("data" in result_response and "statusDetails" in result_response[
                                                                "data"]):
                                                                status_result_response = result_response["data"]["statusDetails"]

                                                                done_output = []
                                                                for output in status_result_response:
                                                                    # print(output)
                                                                    logger.info("status: {}, type {}, analyzerId: {}, filename: {}".format(output.get("status"),output.get("type"),analyzerId, filename))
                                                                    if (output["type"] in latest_output_outputs and output[
                                                                        "status"] == "Completed" and output["type"] not in result):
                                                                        logger.info("Downloading {0} of analyzerId: {1}".format(output["type"], analyzerId))
                                                                        response, reason = downloadFile(configuration_settings, token, analyzerId,
                                                                                                output["type"], path,
                                                                                                filename.rsplit(".")[0])

                                                                        result[output["type"]] = response
                                                                        if (not response):
                                                                            result[output["type"] + "_error"] = reason
                                                                        done_output.append(output["type"])
                                                                    elif (output["type"] in latest_output_outputs and output[
                                                                        "status"] == "Failed" and output["type"] not in result):

                                                                        result[output["type"]] = False
                                                                        result[output["type"] + "_error"] = output["status"]
                                                                        logger.info("Processing failed of analyzerId: {}, filename: {}".format(analyzerId, filename))
                                                                        done_output.append(output["type"])
                                                                    elif output["type"] in result:
                                                                        logger.info("Processing of analyzerId: {}, filename: {}".format(analyzerId, filename))
                                                                        done_output.append(output["type"])
                                                                if (len(done_output) == len(latest_output_outputs)):
                                                                    completed_download.append(True)
                                                                    compelted_check.append(filename)

                                                                completed = checkCompleted(latest_output_outputs, result)
                                                                if(completed):
                                                                    result["download_completed"] = True

                                                        else:
                                                            logger.error("Cannot get status of analyzerId: {}, filename: {}".format(analyzerId, filename))
                                                            result["download_success"] = False
                                                            result["download_failure_reason"] = result_response
                                                            failed_download.append(True)
                                                    else:
                                                        message = "UMS token is required to check file status, filename {}".format(filename)
                                                        logger.error(message)
                                                        failed_download.append(True)
                                                else:
                                                    token, generated_time = generateToken_pw_flow(configuration_settings)

                                else:
                                    logger.error("We could not find any information to download files from.")
                                    result["download_success"] = False
                                    result["download_failure_reason"] = "No available data to download from"
                                    failed_download.append(True)
                            except Exception as err:
                                result["download_success"] = False
                                result["download_failure_reason"] = "No analyzerID available to download results"
                                logger.error("No analyzerID available to download results. The file upload may have failed. File name: {0}".format(result["filename"]))
                                failed_download.append(True)
                                logger.error(err)

                            # new_output_json_result.append(result)
                            # print(len(new_output_json_result))
                            endtime = dt.datetime.now()
                            output_json["output_results"] = output_json_result
                            output_json["endtime"] = str(endtime)
                            json.dump(output_json, open("output.json", 'w'), indent=4)
                            completed_count = len(failed_download) + len(completed_download)


                        logger.info("count, failed {}, completed {}".format(len(failed_download), len(completed_download)))
                        if (completed_count >= len(output_json_result)):
                            print(compelted_check)
                            pending_completion = False
                        else:
                            if (loop >= 1000):
                                pending_completion = False
                                logger.error("Reached maximum number of download retries.")
                            else:
                                time.sleep(10)
                    else:
                        pending_completion = False
                        logger.error("No results available to download.")
                        return True


                logger.info("Done downloading all output files to your output_directory_path")
                logger.info("Download status reported in output.json")
                if(loop < 999):
                    return True
                else:
                    return False
            else:
                logger.error("output.json file does not exist. No results available to download.")

                return False
        else:
            logger.error("UMS token is required to download the files")
            return False
    else:
        logger.error("Check your configuration file (config.json) for correct format and valid parameters")
        return False


if __name__ == '__main__':
    logger.info("**************************************")
    logger.info("API Sample tool downloadFiles starting...")
    logger.info("Logs can be found in the current directory, processing.log")
    output_json_path = os.path.join(os.getcwd(), "output.json")
    if(os.path.exists(output_json_path)):
        output_json = json.load(open(output_json_path, "r"))
        token = output_json.get('ums_token') if output_json.get('ums_token') else "token"
        print(token)
    else:
        token = "token"
    downloadFiles(token)
