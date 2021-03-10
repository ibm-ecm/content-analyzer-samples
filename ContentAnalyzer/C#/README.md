# Content Analyzer Sample Tool - C# package

This tool contains the C# solution and projects to call the Content Analyzer APIs for uploading the files, checking the processing status, downloading the output and deleting the related resources.

## Basic Components
+ [**ContentAnalyzer.sln**](ContentAnalyzer.sln) - The C# solution
+ [**ContentAnalyzer**](ContentAnalyzer) - This project contains the source code of Content Analyzer API functions.
  - [UploadFiles.cs](ContentAnalyzer/UploadFiles.cs) - Upload files for processing
  - [DownloadFiles.cs](ContentAnalyzer/DownloadFiles.cs) - Retrieve peocessing status and downlod JSON, PDF, or UTF8 output after processing
  - [DeleteFiles.cs](ContentAnalyzer/DeleteFiles.cs) - Delete files and outputs
+ [**Start**](Start) - This project contains the entry point to call the API functions.

## Prerequisites
1. You must have access to a Content Analyzer cloud deployment.
2. You might want to access the Content Analyzer Knowledge Center web page as a reference. The link is in the Related Links section below.
3. You will need a Content Analyzer API key and the API request URL. You can get this information from your Content Analyzer administrator. The administrator can use the Content Analyzer web interface to generate an API key specifically for you. This API key will identify you as the caller of the APIs.
4. You will need a functional ID and password from the IBM Digital Business Automation on Cloud. You can get this information from your Content Analyzer administrator. The administrator can use 5. the IBM Digital Business Automation on Cloud user portal to create a functional user ID for you.
5. You should also decide what output you want to be produced for each file: JSON, UTF-8 Text, and/or PDF. The JSON output will contain the extracted key-value pair information. The UTF-8 Text will be the raw OCR text results. The PDF will be an enhanced searchable PDF.
6. If you selected JSON output, you should know what subset of JSON options you want to be included. Enter all or see documentation for details.

After you get all the parameters mentioned above, please edit the [configuration.json](configuration.json) file before you run the Start project.

## Input
Update [configuration.json](configuration.json) with your server connection and options information as follows.
1. functionID and password: Required when authenticating through the IBM Digital Business Automation on Cloud portal. Created by the administrator in IBM Digital Business Automation on Cloud.
2. LDAP_userName and LDAP_passwod: Required for the authentication of LDAP users  .
3. apiKey: Key generated in the API Page from the Content Analyzer web UI. All API usage with this apiKey will be tracked on the server.
4. mainUrl: The URL to the Content Analyzer API server, shown in My Activity tab on the server web UI.
5. responseType: List of output options. Available values : json, pdf, utf8 (case does not matter)
6. jsonOptions: List of json options. Available values : ocr, dc, kvp, sn, hr, th, mt, ai, ds, char (case does not matter)
7. directoryPath: The directory containing the files to be processed, supports nested directory files
8. outputDirectoryPath: The directory to write the output files (JSON, UTF8, PDF) after processing. If the directory does not exist, the script will create it.

## Sample configuration.json
```json
{
  "functionalID": "test.fid@t0006",
  "password": "bMksr1hsoathoyhkeGb2YnmSewSoWFxapfQ92Ob",
  "LDAP_userName": "",
  "LDAP_password": "",
  "apiKey": "MGQzODY0Ydhitpeit836093dha;GFDDDg0NDY5ZTFhO3h5aWJtO2RlZmF1bHQ=",
  "mainURL": "https://ip_address/backendsp/ca/rest/content/v1",
  "responseType": "\"JSON\", \"PDF\", \"UTF8\"",
  "jsonOptions": "\"ocr\",\"dc\",\"kvp\",\"sn\"",
  "directoryPath": "/Users/Administrator/ContentAnalyzer/CASendDocs",
  "outputDirectoryPath": "/Users/Administrator/ContentAnalyzer/CAGetDocs"
}
```

## Output and Logs
- Terminal console will show the processing etails after run the Start.exe file.
- Check the output_directory for the output files.
- Check [output.json](output.json) for upload and download results in json format, including HTTP return codes and errors.
- Check [date.txt](Start/bin/Debug/logs/) in the **Start/bin/Debug/logs** folder for the processing details.

## To Run
- First, please edit the configuration.json file based on your requirement.

- Make sure the directory_path contains all the files you want to process. Files in nested subdirectories will also be processed.

- Run the executable file based on your operation system:
  - Mac: 
    - open the terminal and cd to the Start.exe file. The directory is **Start/bin/Debug**
    - run the command `mono Start.exe`
  - Windows:
    - open the **Start/bin/Debug** folder and double click the Start.exe file to run it.

## Developers
This C# solution includes two projects
- ContentAnalyzer project contains the source code of Content Analyzer API functions, such as, UploadFiles.cs, DownloadFiles.cs and DeleteFiles.cs. Please look at the source code for more details. 
- Start project contains the entry point to call the API functions. It will read the path of the configuration.json file and start the uploading and processing actions.

## Related Links
+ https://www.ibm.com/support/knowledgecenter/SSUM7G/com.ibm.bacanalyzertoc.doc/bacanalyzer_1.0.html

## Third-Party Software
- NLog: Flexible & free open-source logging for .NET. verison 4.6.4. https://nlog-project.org/
- RestSharp: Simple REST and HTTP API Client for .NET. version 106.6.9. http://restsharp.org/
## Disclaimers
This code is sample code created by IBM Corporation. IBM grants you a nonexclusive copyright license to use this sample code example. This sample code is not part of any standard IBM product and is provided to you solely for the purpose of assisting you in the development of your applications. This example has not been thoroughly tested under all conditions. IBM, therefore cannot guarantee nor may you imply reliability, serviceability, or function of these programs. The code is provided "AS IS", without warranty of any kind. IBM shall not be liable for any damages arising out of your or any other parties use of the sample code, even if IBM has been advised of the possibility of such damages. If you do not agree with these terms, do not use the sample code.

Copyright IBM Corp. 2019 All Rights Reserved.
