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

# def registration(config):
#     client_id = config['client_id']
#     client_secret = config['client_secret']
#     # Make request
#     print(client_id)
#     try:
#         ums_url = config['ums_base_url'].strip() + '/oidc/endpoint/ums/registration'
#         ums_username = config['ums_username'].strip()
#         ums_pw = config['ums_password'].strip()
#         encoding = base64.b64encode('{}:{}'.format(ums_username,ums_pw).encode())
#         headers = {
#             "authorization": "Basic " +  encoding.decode("utf-8"),
#             'Content-Type': 'application/json'
#         }
#         response = requests.request("GET", ums_url + '/' + client_id, headers=headers, verify=config['ssl_verification'])
        
#         if response.status_code == 200:
#             # client is registered already
#             return True
#         elif response.status_code == 404:
#             # need to register
#             logger.info("Need to register the client")
#             payload = {
#                 "scope": "openid",
#                 "preauthorized_scope": "openid",
#                 "introspect_tokens": True,
#                 "client_id": client_id,
#                 "client_secret": client_secret,
#                 "client_name": client_id,
#                 "grant_types": ["password"],
#                 "response_types": [ "token"]
#                 }
#             try:
#                 response1 = requests.request("POST", ums_url, headers=headers, data=json.dumps(payload),verify=False)

#                 if response1.status_code == 201:
#                     logger.info("Successfully registered the client")
#                     return True
#                 else:
#                     logger.error("Failed to register the client")
#                     content1 = getContent(response1)
#                     logger.debug(content1)
#                     return False
#             except Exception as err:
#                 logger.error("Failed to register the client due to exception")
#                 logger.debug(str(err))
#                 return False
#         else:
#             logger.error("Failed to check the client")
#             content = getContent(response)
#             logger.debug(content)
#             return False
    
#     except Exception as ex:
#         logger.error("Failed to check the client due to exception")
#         logger.debug(str(ex))
#         return False


def generateToken_pw_flow(config):
    client_id = config['client_id'] 
    client_secret = config['client_secret']
    ums_token_url = config['ums_base_url'].strip() + '/oidc/endpoint/ums/token'
    ums_username = config['ums_username'].strip()
    ums_pw = config['ums_password'].strip()
    try:
        generated_time = dt.datetime.now()
        encoding = base64.b64encode('{}:{}'.format(client_id,client_secret).encode())
        headers = {
            "authorization": "Basic " +  encoding.decode("utf-8") ,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload="grant_type=password&scope=openid&username={}&password={}".format(ums_username, ums_pw)

        response = requests.request("POST", ums_token_url, headers=headers, data=payload, verify=config['ssl_verification'])
            
        if response.status_code == 200:
            # token is generated
            # {
            #     "access_token": "0nZMCS6pOUMh8fofTi2BiAXN44gAdLynsSPkERLe",
            #     "token_type": "Bearer",
            #     "expires_in": 7199,
            #     "scope": "openid"
            # }
            content = getContent(response)
            # print(content)
            token = content.get('access_token')
            logger.info('Successfully got the token {}'.format(token))
            json.dump({"ums_token": token}, open("output.json", 'w'), indent=4)
            return token, generated_time
        else:
            logger.error("Failed to generate a token")
            content = getContent(response)
            logger.debug(content)
            return None, None
    except Exception as ex:
        logger.error("Failed to generate a token due to exception")
        logger.debug(str(ex))
        return None, None


# # implicit_flow, use aca backend redirect recall, generate the token in location headers
# def generateToken_implicit_flow(config):
#     generated_time = dt.datetime.now()
#     try:
#         client_id = config['client_id'] .strip()
#         aca_base_url = config['aca_base_url'].strip() + '/authorization-code/callback'
#         ums_token_url = config['ums_base_url'].strip() + '/oidc/endpoint/ums/authorize'
#         ums_username = config['ums_username'].strip()
#         ums_pw = config['ums_password'].strip()

#         params = (
#             ('response_type', 'token'),
#             ('client_id', client_id),
#             ('scope', 'openid'),
#             ('state', 'none'),
#             ('redirect_uri', aca_base_url),
#         )
#         encoding = base64.b64encode('{}:{}'.format(ums_username,ums_pw).encode())
#         headers = {"authorization": "Basic " +  encoding.decode("utf-8")}
        
#         response = requests.request("POST", ums_token_url, headers=headers, params=params, allow_redirects=False, verify=config['ssl_verification'])
            
#         if response.status_code == 302:
#             r = re.search(r'access_token=[^&]*', str(response.headers))
#             tokenStr = r.group()
#             token =  tokenStr.split('=')[1]
#             logger.info('Successfully got the token {}'.format(token))
#             json.dump({"ums_token": token}, open("output.json", 'w'), indent=4)
#             return token, generated_time
#         else:
#             logger.error("Failed to generate a token")
#             content = getContent(response)
#             logger.debug(content)
#             return None, None
#     except Exception as ex:
#         logger.error("Failed to generate a token due to exception")
#         logger.debug(str(ex))
#         return None, None


def checkTokenValid(token, config):
    if token:
        if config:
            client_id = config['client_id'] 
            client_secret = config['client_secret']
            ums_check_token_url = config['ums_base_url'].strip() + '/oidc/endpoint/ums/introspect'
            ums_username = config['ums_username'].strip()
            ums_pw = config['ums_password'].strip()
            try:
                encoding = base64.b64encode('{}:{}'.format(client_id,client_secret).encode())
                headers = {
                    "authorization": "Basic " +  encoding.decode("utf-8"),
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                payload="token={}".format(token)

                response = requests.request("POST", ums_check_token_url, headers=headers, data=payload, verify=config['ssl_verification'])
                    
                if response.status_code == 200:
                    content = getContent(response)
                    res = content.get('active')
                    if res:
                        logger.info('ums token provided is valid')
                        generated_time = dt.datetime.fromtimestamp(content.get('iat'))
                        return token, generated_time
                    else:
                        logger.info('ums token provided is invalid or expired, trying to generate a new one')
                        token, generated_time = generateToken_pw_flow(config)
                        return token, generated_time
                else:
                    logger.error("Failed to check the token valid or not")
                    content = getContent(response)
                    logger.debug(content)
                    return None, None
            except Exception as ex:
                logger.error("Failed to check the token valid or not due to exception")
                logger.debug(str(ex))
                return None, None
        else:
            logger.error("Check your configuration file (config.json) for correct format and valid parameters")
            return None, None
    else:
        logger.error("UMS token is required, please provide a valid token")
        return None, None


    
def getFirstToken():
    configuration, configuration_settings = readJSON()
    if (configuration):
        # configuration_settings['client_id'] = "ADP_PYTHON_CLIENT"
        # configuration_settings['client_secret'] = "ADP_PYTHON_CLIENT_SECRET"
        # res_registry = registration(configuration_settings)
        # if res_registry:
        token, generated_time = generateToken_pw_flow(configuration_settings)
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