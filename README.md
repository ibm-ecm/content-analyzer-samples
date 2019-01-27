# Content Analyzer Sample Tools

This repository contains two types of IBM Business Automation Content Analyzer sample Tools. One is a desktop application that has been built for Windows and for MacOS platforms, the other is a Python script package.

The sample tools can be used for uploading files, checking processing status, downloading and deleting files via the IBM Business Automation Content Analyzer APIs. The sample tools can be used as a companion tool to your new Content Analyzer solution.

### Introduction
The IBM Business Automation Content Analyzer is a cloud-based API web service that can help you rapidly accelerate extraction and classification of data in your documents. Content Analyzer can digitize, classify and extract unstructured document content using OCR and PDF text extraction, and enable Watson and other AI technologies to reveal business insight from your documentation.

Once you have used the web interface to “train” your Content Analyzer instance to recognize your specific ontology of document classes, you will need to incorporate the Content Analyzer API calls into your workflow to integrate the data extraction and document classification capabilities.

Instead of waiting for your custom application to be written to call the Content Analyzer APIs, you can use this sample tool to get started right away. This sample tool can be installed on any system that has the python compiler and is written with the Content Analyzer RESTful APIs as a quick verification tool for your ontology and to jump start your integration. With a simple configuration file, the API Sample tool allows you to upload multiple documents, and automatically download the requested output files.

### Basic Components
+ [**WindowsMac**](WindowsMac) - This folder contains the installation packages for the Windows and MacOS desktop application.
+ [**Python**](Python) - This folder contains the python scripts for API uploading, processing, downloading and deleting.

### Configuration Information
Both of these sample tools need configuration information before running. Please look at the readme file in each folder for more detail.

### Related Links
+ https://www.ibm.com/support/knowledgecenter/SSUM7G/com.ibm.bacanalyzertoc.doc/bacanalyzer_1.0.html
+ The Content Analyzer web interface also has the API documentation in the API page.

### Disclaimers
This code is sample code created by IBM Corporation. IBM grants you a nonexclusive copyright license to use this sample code example. This sample code is not part of any standard IBM product and is provided to you solely for the purpose of assisting you in the development of your applications. This example has not been thoroughly tested under all conditions. IBM, therefore cannot guarantee nor may you imply reliability, serviceability, or function of these programs. The code is provided "AS IS", without warranty of any kind. IBM shall not be liable for any damages arising out of your or any other parties use of the sample code, even if IBM has been advised of the possibility of such damages. If you do not agree with these terms, do not use the sample code.

Copyright IBM Corp. 2019 All Rights Reserved.
