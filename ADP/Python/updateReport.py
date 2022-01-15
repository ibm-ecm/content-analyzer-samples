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
from loggingHandler import logger
from dateutil import parser
import datetime as dt


'''
    Function to update report
'''
def updateReport():
    output_json_path = os.path.join(os.getcwd(), "output.json")
    if(os.path.exists(output_json_path)):
        output_json = json.load(open(output_json_path, "r"))
        new_output_json_result = []
        unfinished_files = []
        unfinished_files_with_path = []
        new_file_upload_errors = [output["filename"] for output in output_json["upload_errors"]] if "upload_errors" in output_json else []
        new_file_errors = [output["filename"] for output in output_json["errors"]]  if "errors" in output_json else []
        unfinished_files.extend(new_file_upload_errors)
        unfinished_files.extend(new_file_errors)
        new_file_upload_errors_with_path = [{"filename": output["filename"], "path": output["path"]} for output in output_json["upload_errors"]] if "upload_errors" in output_json else []
        new_file_errors_with_path = [{"filename": output["filename"], "path": output["path"]} for output in output_json["errors"]]  if "errors" in output_json else []
        unfinished_files_with_path.extend(new_file_upload_errors_with_path)
        unfinished_files_with_path.extend(new_file_errors_with_path)
        endtime = dt.datetime.now()
        starttime = parser.parse(output_json["starttime"])

        if("output_results" in output_json):
            output_json_result = output_json["output_results"]
            if(len(output_json["output_results"]) > 0):
                for outresult in output_json_result:
                    result = outresult
                    output_outputs = result["output_type"]
                    latest_output_outputs = [output.replace("\"", "").upper() for output in output_outputs]
                    unfinished_object = {"filename": result["filename"], "path": result["path"] if "path" in result else "", "full_path": result["full_path"] if "full_path" in result else ""}
                    try:
                        if("download_success" in result and result["download_success"] == False):
                            if(result["filename"] not in unfinished_files):
                                unfinished_files.append(result["filename"])
                                unfinished_files_with_path.append(unfinished_object)
                        else:
                            output_count = 0
                            for output in latest_output_outputs:
                                if (output not in result):
                                    if (result["filename"] not in unfinished_files):
                                        unfinished_files.append(result["filename"])
                                        unfinished_files_with_path.append(unfinished_object)
                                if output in result:
                                    output_count += 1
                                    if result[output] == False:
                                        if (result["filename"] not in unfinished_files):
                                            unfinished_files.append(result["filename"])
                                            unfinished_files_with_path.append(unfinished_object)
                            if output_count == 0:
                                if (result["filename"] not in unfinished_files):
                                    unfinished_files.append(result["filename"])
                                    unfinished_files_with_path.append(unfinished_object)



                    except:
                        result["deleted"] = False
            # new_output_json_result.append(result)
            seconds = (endtime - starttime).total_seconds()
            output_json["endtime"] = str(endtime)
            output_json["total_seconds"] = str(seconds)
            output_json["unfinished_files"] = unfinished_files_with_path
            output_json["no_of_unfinished_files"] = len(unfinished_files)

            output_json["output_results"] = output_json_result
            json.dump(output_json, open("output.json", 'w'), indent=4)
            logger.info("Done updating report in the current directory, output.json")
        else:
            logger.error("No results available for reporting")

    else:
        logger.error("output.json file does not exist. No results available for reporting.")


if __name__ == '__main__':
    logger.info("**************************************")
    logger.info("API Sample tool updateReport starting...")
    logger.info("Logs can be found in the current directory, processing.log")
    updateReport()
