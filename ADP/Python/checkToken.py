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
import os, json, copy, re
import requests, time
import datetime as dt
import base64
from base64 import b64encode
from readConfigJSON import readJSON
from loggingHandler import logger
from ssl import SSLError
import datetime as dt



'''
    Function to loop through input directory and upload all the files into the Content Analyzer API environment
'''

def getContent(response):
    content = response.content
    content_unicode = content.decode('utf-8')
    content = json.loads(content_unicode)
    return content

def generateToken_pw_flow(config):
    zen_token_url = 'https://' + config['zen_host'].strip() + '/v1/preauth/validateAuth'
    zen_username = config['zen_username'].strip()
    zen_pw = config['zen_password'].strip()
    try:
        encoding = base64.b64encode('{}:{}'.format(zen_username,zen_pw).encode())
        headers = {
            "authorization": "Basic " +  encoding.decode("utf-8") ,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.request("GET", zen_token_url, headers=headers, verify=config['ssl_verification'])
            
        if response.status_code == 200:
            # token is generated
            # {
            #     "accessToken": "xxxxxxxxx"
            # }
            content = getContent(response)
            # print(content)
            token = content.get('accessToken')
            logger.info('Successfully got the token')
            json.dump({"zen_token": token}, open("output.json", 'w'), indent=4)
            return token
        else:
            logger.error("Failed to generate a token")
            content = getContent(response)
            logger.debug(content)
            return None
    except Exception as ex:
        logger.error("Failed to generate a token due to exception")
        logger.debug(str(ex))
        return None


# if token is valid, request response will be 200, or it will be 401 Unauthorized
def checkTokenValid(token, config):
    if token:
        if config:
            zen_check_token_url = 'https://' + config['zen_host'].strip() + '/usermgmt/v1/user/currentUserInfo'
            try:
                headers = {
                    "authorization": "Bearer " +  token,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.request("GET", zen_check_token_url, headers=headers, verify=config['ssl_verification'])
                    
                if response.status_code == 200:
                    # content = getContent(response)
                    # res = content.get('uid')
                    logger.info('zen token provided is valid')
                    return token
                elif response.status_code == 401:
                    logger.info('zen token provided is invalid or expired, trying to generate a new one')
                    token = generateToken_pw_flow(config)
                    return token
                else:
                    logger.error("Failed to check the token valid or not")
                    content = getContent(response)
                    logger.debug(content)
                    return None
            except Exception as ex:
                logger.error("Failed to check the token valid or not due to exception")
                logger.debug(str(ex))
                return None
        else:
            logger.error("Check your configuration file (config.json) for correct format and valid parameters")
            return None
    else:
        logger.error("Zen token is required, please provide a valid token")
        return None


    
def getFirstToken():
    configuration, configuration_settings = readJSON()
    if (configuration):
        token = generateToken_pw_flow(configuration_settings)
        return token
    else:
        logger.error("Check your configuration file (config.json) for correct format and valid parameters")
        return False


if __name__ == '__main__':
    logger.info("Logs can be found in current directory (processing.log)")
    token = None
    try:
        getFirstToken()
    except Exception as ex:
        logger.error("An error occurred, please check logs for more details")
        logger.debug(ex, exc_info=True)