/*disclaimer of warranties.
 this code is sample code created by ibm corporation. ibm grants you a
 nonexclusive copyright license to use this sample code example. this
 sample code is not part of any standard ibm product and is provided to you
 solely for the purpose of assisting you in the development of your
 applications. this example has not been thoroughly tested under all
 conditions. ibm, therefore cannot guarantee nor may you imply reliability,
 serviceability, or function of these programs. the code is provided "as is",
 without warranty of any kind. ibm shall not be liable for any damages
 arising out of your or any other parties use of the sample code, even if ibm
 has been advised of the possibility of such damages. if you do not agree with
 these terms, do not use the sample code.
 copyright ibm corp. 2019 all rights reserved.
 to run, see readme.md
 * */

using System;
using System.Linq;
using System.Net;
using System.IO;
using RestSharp;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using NLog;

namespace ContentAnalyzer
{
    public class UploadFiles
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();

        /// <summary>
        ///Input params in JSON configuration file (example):
        ///</summary>       
        public class Config
        {
            public string functionalID { get; set; }
            public string password { get; set; }
            public string LDAP_userName { get; set; }
            public string LDAP_password { get; set; }
            public string apiKey { get; set; }
            public string mainURL { get; set; }
            public string responseType { get; set; }
            public string jsonOptions { get; set; }
            public string directoryPath { get; set; }
            public string outputDirectoryPath { get; set; }

        }
        public static Config configParams;

        /// <summary>
        /// Read the configuration.json file to get the request parameters required for the uploading request.
        /// start uploading the files, return the response and save the response into the output.json file. 
        /// </summary>
        /// <param>configFilePath</param>
        ///<returns>analyzerId in the output.json, which will be used in the get request</returns>
        public Boolean UploadFile(string configFilePath)
        {
            var startTime = DateTime.Now;

            ServicePointManager.ServerCertificateValidationCallback += (sender, certificate, chain, sslPolicyErrors) => true;
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;

            DirectoryInfo currentDir = new DirectoryInfo(Directory.GetCurrentDirectory());
            string configFile = currentDir.Parent.Parent.FullName + @"/NLog.config";

            string result = String.Empty;
            string outputDir = @"../../../output.json";
            configParams = new Config();
            string jsonParams = File.ReadAllText(@configFilePath);
            configParams = (JsonConvert.DeserializeObject<Config>(jsonParams));

            string functionalID = configParams.functionalID;
            string password = configParams.password;
            string LDAP_userName = configParams.LDAP_password;
            string LDAP_password = configParams.LDAP_password;
            string mainURL = configParams.mainURL.Trim();
            string apiKey = configParams.apiKey;
            string responseType = configParams.responseType;
            string jsonOptions = configParams.jsonOptions;
            string directoryPath = configParams.directoryPath;

            string outputDirectoryPath = @configParams.outputDirectoryPath;
            JArray output = new JArray();
            JArray errors = new JArray();

            string url = mainURL + "/contentAnalyzer";
            string auth = "";
            if (functionalID != "" && password != "") {
               auth = Base64Encode(functionalID + ":" + password);
            }
            else if (LDAP_userName != "" && LDAP_password != "")
            {
                auth = Base64Encode(LDAP_userName + ":" + LDAP_password);
            } 
            if (Directory.Exists(directoryPath))
            {
                string[] extensions = new[] { ".jpg", ".jpeg", ".tif", ".tiff", ".png", ".pdf", ".doc", ".docx" };
                DirectoryInfo di = new DirectoryInfo(@directoryPath);
                FileInfo[] files = di.GetFiles().Where(f => extensions.Contains(f.Extension.ToLower())).ToArray();
                int success_count = 0;
                int failed_count = 0;           
                foreach (FileInfo file in files)
                {             
                    JObject dictObject = new JObject();
                    dictObject["filename"] = file.Name;

                    var client = new RestClient(url);
                    var request = new RestRequest(Method.POST);

                    request.AddHeader("Authorization", "Basic " + auth);
                    request.AddHeader("apiKey", apiKey);
                    request.AddHeader("content-type", "multipart/form-data");
                    request.AddParameter("responseType", responseType);
                    request.AddParameter("jsonOptions", jsonOptions);
                    string filepath = file.DirectoryName + "/" + file.Name;
                    //bool fileExist = (File.Exists(filepath));
                    request.AddFile("file", filepath);
                    IRestResponse response = client.Execute(request);

                    if (response.StatusCode == System.Net.HttpStatusCode.Accepted)
                    { 
                        success_count += 1;
                        dictObject["upload_response"] = JObject.Parse(response.Content);
                        output.Add(dictObject);

                    } else {
                        failed_count += 1;
                        logger.Error("Http error occurred when uploading file " + file);
                        dictObject["upload_error"] = response.Content;
                        errors.Add(dictObject);

                    }
                }

                var endTime = DateTime.Now;
                JObject resultUpload = new JObject();
                resultUpload["startTime"] = startTime;
                resultUpload["no_files"] = success_count + failed_count;
                resultUpload["upload_results"] = output;
                resultUpload["total_upload_seconds"] = (endTime - startTime).TotalSeconds;
                resultUpload["upload_errors"] = errors;

                System.IO.File.WriteAllText(@outputDir, JsonConvert.SerializeObject(resultUpload));
                if (success_count == 0)
                {
                    logger.Error("No file uploaded successfully.");
                    return false;
                }
                else
                {
                    logger.Info("Uploaded all the files");
                    return true;
                }
                
            }
            logger.Error("No file exist in the directory");
            return false;
        }

        // To convert the basic auth
        public static string Base64Encode(string plainText)
        {
            var plainTextBytes = System.Text.Encoding.UTF8.GetBytes(plainText);
            return System.Convert.ToBase64String(plainTextBytes);
        }
    }
}
