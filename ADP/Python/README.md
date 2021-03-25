# ADP Sample Tool - Python package

This tool is a python script package for uploading files, checking processing status, downloading and deleting files via the IBM Automation Document Processing (ADP) APIs.

### Basic Components

+ [**config.json**](config.json) - Input file of your configuration settings
+ [**start.py**](start.py) - Starting point of the tool that will upload, download, and delete
+ [**reupload.py**](reupload.py) - Starting point of the tool that will redo the failed or unfinished processing: re-upload, download, and delete

+ [**readConfigJSON.py**](readConfigJSON.py) - Verify the configuration file
+ [**checkToken.py**](checkToken.py) - Check or generate the UMS token for authentication
+ [**uploadFiles.py**](uploadFiles.py) - Call directly just to do uploads
+ [**downloadFiles.py**](downloadFiles.py) - Call directly just to do downloads
+ [**deleteFiles.py**](deleteFiles.py) - Call directly just to do deletes
+ [**updateReport.py**](updateReport.py) - Writes out the output.json
+ [**loggingHandler.py**](loggingHandler.py) - Writes to the processing.log
+ [**reUploadUnfinished.py**](reUploadUnfinished.py) -  Call directly to reupload the failed or unfinished files, this overrides the previous output.json file.


### Prerequisites
1.	You must have access to Automation Document Processing project.
2.	You might want to access the Automation Document Processing Knowledge Center web page as a reference. The link is in the Related Links section below.
3.	You will need to provide ums username, password, client id and client secret to generate the UMS token for authentication
4.  You will need content analyzer basic url to get the APIs work
5.	You should also decide what output you want to be produced for each file: JSON, and/or PDF. The JSON output will contain the extracted key-value pair information. The PDF will be an enhanced searchable PDF.
6.	If you selected JSON output, you should know what subset of JSON options you want to be included. Enter all or see documentation for details.

### Input

Update [**config.json**](config.json) with your server connection and options information as follows.

1. **directory_path**: The directory containing the files to be processed, supports nested directory files
2. **output_directory_path**: The directory to write the output files (JSON, UTF8, PDF) after processing. If the directory does not exist, the script will create it.
3. **ums_base_url**: The URL to the UMS server for generating the UMS token.
4. **ums_username**: UMS admin user name
5. **ums_password**: UMS admin password
6. **client_id**: UMS client id
7. **client_secret**: UMS client secret
8. **aca_base_url**: The URL to the Content Analyzer API server
9. **adp_project_id**: Automation Document Processing project ID
10. **output_options**: List of output options. Available values : json, pdf (case does not matter)
11. **json_options**: List of json options. Available values : ocr, dc, kvp, sn, hr, th, mt, ai, ds, char (case does not matter)
12. **ssl_verification**: Boolean whether your system uses SSL certificates. Default is boolean False
13. **file_type**: This is optional but can be specified if user requires specific file types to be uploaded and not all the BACA accepted file types (doc, docx, pdf, png, pneg, jpg, jpeg, tif, tiff)

Note: 
1. Please check **Related Links** section for the commands to get `ums_base_url, ums_username, ums_password, client_id`.
2. Command to get `client_secret`
`oc get cm icp4adeploy-aca-config -oyaml | grep UMS_CLIENT_SECRET`
3. Please contact the project admin to get `aca_base_url, adp_project_id`.

### Sample config.json
```
{
  "ums_base_url": "https://sample-ums/ibm.com",
  "ums_username": "admin",
  "ums_password": "password",
  "client_id": "",
  "client_secret": "",
  "aca_base_url": "https://sample-aca-backend.ibm.com",
  "adp_project_id": "your-project-id",
  "directory_path": "/sample/input",
  "output_directory_path": "/sample/output",
  "output_options": "json",
  "json_options": "ocr,dc,kvp,sn,hr,th,mt,ai,ds",
  "ssl_verification": false,
  "file_type": [
    "pdf",
    "docx",
    "doc"
  ]
}
```


### Before Running the tool

Install the latest **python3**, **pip** and these packages:

    python -m pip install --upgrade pip
    python -m pip install requests
    python -m pip install python-dateutil

### Run the tool
The tool will upload all the files found in the input directory and check for processing status. As the output files are ready, they will be downloaded to your output directory. Then the output files will be deleted from the server.

+ Update the **config.json** with your configuration settings
+ Make sure the **directory_path** contains all the files you want to process. Files in nested subdirectories will also be processed
+ Run the script from the terminal command line:
      `python start.py`
+ Monitor the console log.

### Rerun the tool
If there are any errors and files did not get processed, you can call **reupload.py** to redo the upload, download, and delete.
The script will reprocess the unfinished files listed in the **output.json**. It will upload the files again
in the input directory and check for processing status. As the output files are ready, they will be downloaded to
your output directory. Then the output files will be deleted from the server.

+ You may want to backup the processing.log and the **output.json** and delete these files before calling reupload.
+ Run the script from the terminal command line:
      `python reupload.py`
+ Monitor the console log.

### Run the individual python scripts
You may want to rerun individual Python scripts, for example to download the output files again or to clean up the files on the
server. These scripts rely on previous uploads and references the **output.json** file that was generated.
+ Run the scripts from the terminal command line:
      `python downloadFiles.py`
      `python deleteFiles.py`
+ Monitor the console log.

### Output
+ Terminal console
+ Check the **processing.log** for processing details (same as console log)
+ Check the **output.json** for upload and download results in json format, including HTTP return codes and errors
+ Check the output_directory for the output files
+ The output files are immediately deleted from the server


### Related Links
https://www.ibm.com/support/knowledgecenter/SSYHZ8_20.0.x/com.ibm.dba.dp/topics/con_ca_api.html


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

 Copyright IBM Corp. 2021 All Rights Reserved.
