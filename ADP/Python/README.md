# ADP Sample Tool - Python package

This tool is a python script package for uploading files, checking processing status, downloading and deleting files via the IBM Automation Document Processing (ADP) APIs.

### Basic Components

+ [**config.json**](config.json) - Input file of your configuration settings
+ [**start.py**](start.py) - Starting point of the tool that will upload, download, and delete
+ [**reupload.py**](reupload.py) - Starting point of the tool that will redo the failed or unfinished processing: re-upload, download, and delete

+ [**readConfigJSON.py**](readConfigJSON.py) - Verify the configuration file
+ [**checkToken.py**](checkToken.py) - Check or generate the token for authentication
+ [**uploadFiles.py**](uploadFiles.py) - Call directly just to do uploads
+ [**downloadFiles.py**](downloadFiles.py) - Call directly just to do downloads
+ [**deleteFiles.py**](deleteFiles.py) - Call directly just to do deletes
+ [**updateReport.py**](updateReport.py) - Writes out the output.json
+ [**loggingHandler.py**](loggingHandler.py) - Writes to the processing.log
+ [**reUploadUnfinished.py**](reUploadUnfinished.py) -  Call directly to reupload the failed or unfinished files, this overrides the previous output.json file.


### Prerequisites
1. You must have access to Automation Document Processing project.
2. You might want to access the Automation Document Processing Knowledge Center web page as a reference. The link is in the Related Links section below.
3. You will need to provide Zen host, username, and password  to generate a token for authentication
4. You should know what subset of JSON options you want to be included. Enter all or see documentation for details.

### Input

Update [**config.json**](config.json) with your server connection and options information as follows.

1. **directory_path**: The directory containing the files to be processed, supports nested directory files
2. **output_directory_path**: The directory to write the output files (JSON) after processing. If the directory does not exist, the script will create it.
3. **zen_host**: The URL to the server for generating the Zen token and sending the file processing reqests
4. **zen_username**: The username that belongs  to the appropriate group such as `captureadmins` or `projectadmins`. For more information on roles, please refer to [here](https://www.ibm.com/docs/en/SSYHZ8_21.0.3/com.ibm.dba.dp/topics/con_deploy_permission.html)
5. **zen_password**: Password
9. **adp_project_id**: Automation Document Processing project ID
10. **output_options**: Output options. ADP only support json. The output will contain the extracted key-value pair information
11. **json_options**: List of json options. Available values : ocr, dc, kvp, sn, hr, th, mt, ai, ds, char (case does not matter)
12. **ssl_verification**: Boolean whether your system uses SSL certificates. Default is boolean False
13. **file_type**: This is optional but can be specified if user requires specific file types to be uploaded and not all the BACA accepted file types ('pdf', 'jpg', 'jpeg', 'tif', 'tiff', 'png', 'doc', 'docx')

Note: 
1. Command to get `zen_host`:
`oc get route cpd -o jsonpath="{.spec.host}"`
Please check **Related Links** section for the commands to get more details.

### Sample config.json
```
{
  "zen_host": "route-host-without-https",
  "zen_username": "admin",
  "zen_password": "password",
  "adp_project_id": "your-project-name",
  "directory_path": "/sample/input",
  "output_directory_path": "/sample/output",
  "output_options": "json",
  "json_options": "ocr,dc,kvp,sn,hr,th,mt,ai,ds",
  "ssl_verification": false,
  "file_type": [
    "pdf"
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
https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/21.0.3?topic=integrations-automation-document-processing-api


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

 Copyright IBM Corp. 2022 All Rights Reserved.
