# Content Analyzer Sample Tool - Python package

This tool is a python script package for uploading files, checking processing status, downloading and deleting files via the IBM Business Automation Content Analyzer APIs. This sample application can be used as a companion tool to your new Content Analyzer solution.

### Basic Components

+ [**config.json**](config.json) - Input file of your configuration settings
+ [**start.py**](start.py) - Starting point of the tool that will upload, download, and delete
+ [**reupload.py**](reupload.py) - Starting point of the tool that will redo the failed
or unfinished processing: re-upload, download, and delete

+ [**readConfigJSON.py**](readConfigJSON.py) - Verify the configuration file
+ [**uploadFiles.py**](uploadFiles.py) - Call directly just to do uploads
+ [**downloadFiles.py**](downloadFiles.py) - Call directly just to do downloads
+ [**deleteFiles.py**](deleteFiles.py) - Call directly just to do deletes
+ [**updateReport.py**](updateReport.py) - Writes out the output.json
+ [**loggingHandler.py**](loggingHandler.py) - Writes to the processing.log
+ [**reUploadUnfinished.py**](reUploadUnfinished.py) -  Call directly to reupload the failed or unfinished files, this overrides the previous output.json file.

### Developers

Install the latest **python3**, **pip** and these packages:

    python -m pip install --upgrade pip
    python -m pip install requests
    python -m pip install python-dateutil
    python -m pip install logging

### Prerequisites
1.	You must have access to a Content Analyzer cloud deployment.
2.	You might want to access the Content Analyzer Knowledge Center web page as a reference. The link is in the Related Links section below.
3.	You will need a Content Analyzer API key and the API request URL. You can get this information from your Content Analyzer administrator.
The administrator can use the Content Analyzer web interface to generate an API key specifically for you. This API key will identify you as the caller of the APIs.
4.  You will need a user ID and password from the IBM Digital Business Automation on Cloud. You can get this information from your Content Analyzer administrator.
The administrator can use the IBM Digital Business Automation on Cloud user portal to create a functional user ID for you.
5.	You should also decide what output you want to be produced for each file: JSON, UTF-8 Text, and/or PDF. The JSON output will contain the extracted
key-value pair information. The UTF-8 Text will be the raw OCR text results. The PDF will be an enhanced searchable PDF.
6.	If you selected JSON output, you should know what subset of JSON options you want to be included. Enter all or see documentation for details.

### Input

Update [**config.json**](config.json) with your server connection and options information as follows.

1. **directory_path**: The directory containing the files to be processed, supports nested directory files
2. **output_directory_path**: The directory to write the output files (JSON, UTF8, PDF) after processing. If the directory does not exist, the script will create it.
3. **api_key**: Key generated in the API Page from the Content Analyzer web UI. All API usage with this api_key will be tracked on the server.
4. **main_url**: The URL to the Content Analyzer API server, shown in My Activity tab on the server web UI. Make sure to add /contentAnalyzer to your request URL
5. **output_options**: List of output options. Available values : json, pdf, utf8 (case does not matter)
6. **json_options**: List of json options. Available values : ocr, dc, kvp, sn, hr, th, mt, wi, shw (case does not matter)
7. **ssl_verification**: Boolean whether your system uses SSL certificates. Default is boolean False
8. **function_id** and **password**: Required when authenticating through the IBM Digital Business Automation on Cloud portal.
Created by the administrator in IBM Digital Business Automation on Cloud.
9. **file_type**: This is optional but can be specified if user requires specific file types to be uploaded and not all the BACA accepted file types

### Sample config.json
    {
    "directory_path": "/Users/janedoe/test-files",
    "output_directory_path": "/Users/janedoe/output-files",
    "api_key": "39f40e36-040b-4375-a665-b3853107d9c5",
    "main_url": "https://9.30.123.456/ca/rest/content/v1/ContentAnalyzer",
    "output_options": "\"utf8\",\"json\",\"pdf\"",
    "json_options": "\"ocr\",\"dc\",\"kvp\",\"sn\",\"th\",\"mt\",\"hr\",\"wi\",\"shw\"",
    "function_id": "janedoe",
    "password": "password4janedoe",
    "ssl_verification": false,
    "file_type":
    }

### Run the tool
The tool will upload all the files found in the input directory and check for processing status. As the output files are ready, they will be downloaded to your output directory. Then the output files will be deleted from the server.

+ Update the **config.json** with your configuration settings
+ Make sure the **directory_path** contains all the files you want to process. Files in nested subdirectories will also be processed
+ Run the script from the terminal command line:
      python start.py
+ Monitor the console log.

### Rerun the tool
If there are any errors and files did not get processed, you can call **reupload.py** to redo the upload, download, and delete.
The script will reprocess the unfinished files listed in the **output.json**. It will upload the files again
in the input directory and check for processing status. As the output files are ready, they will be downloaded to
your output directory. Then the output files will be deleted from the server.

+ You may want to backup the processing.log and the **output.json** and delete these files before calling reupload.
+ Run the script from the terminal command line:
      python reupload.py
+ Monitor the console log.

### Run the individual python scripts
You may want to rerun individual Python scripts, for example to download the output files again or to clean up the files on the
server. These scripts rely on previous uploads and references the **output.json** file that was generated.
+ Run the scripts from the terminal command line:
      python downloadFiles.py
      python deleteFiles.py
+ Monitor the console log.

### Output
+ Terminal console
+ Check the **processing.log** for processing details (same as console log)
+ Check the **output.json** for upload and download results in json format, including HTTP return codes and errors
+ Check the output_directory for the output files
+ The output files are immediately deleted from the server

### Important Note
+ The Content Analyzer server will track all usage from the **api_key** used in the API calls.
Do not share the **api_key** or the **function_id** or the **password**. Keep the **config.json** file in a
secure place.

### Related Links
1.	https://www.ibm.com/support/knowledgecenter/SSUM7G/com.ibm.bacanalyzertoc.doc/bacanalyzer_1.0.html
2.	The Content Analyzer web interface also has the API documentation in the API page.


### DISCLAIMER OF WARRANTIES
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
