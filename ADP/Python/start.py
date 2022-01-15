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

import datetime as dt
from loggingHandler import logger
from downloadFiles import downloadFiles
from uploadFiles import uploadFiles
from deleteFiles import deleteFiles
from updateReport import updateReport
from checkToken import getFirstToken


starttime = dt.datetime.now()

if __name__ == '__main__':
    logger.info("**************************************")
    logger.info("ADP API Sample tool starting...")
    logger.info("Logs can be found in the current directory, processing.log")

    token = getFirstToken()
    if token:
        token_time = dt.datetime.now()
        logger.info("Successfully generate the token, continue...")
        logger.info("Uploading files")
        uploadSuccess = uploadFiles(token)

        if (uploadSuccess):
            logger.info("Ready to download output files...")
            complete = downloadFiles(token)

            if(complete):
                logger.info("Deleting files on the server")
                deleteFiles(token)
            else:
                logger.info("Could not delete at this time because download has not been completed yet, please run deleteFiles.py at a later time")

            logger.info("Updating report")
            updateReport()

        endtime = dt.datetime.now()
        seconds = (endtime - starttime).total_seconds()
        logger.info("ADP API Sample tool ended. Processing time took {0} seconds, Disclaimer: This includes time to upload, download and delete and has nothing to do with actual processing time.".format(int(seconds)))
    else:
        logger.error("Failed to generate token to continue")