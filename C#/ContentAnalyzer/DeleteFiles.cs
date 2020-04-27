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
    public class DeleteFiles
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();

        /// <summary>
        /// Read the configuration.json file to get the request parameters required for the delete request.
        /// If the output is downloaded already, this function will be called to delete all the related resources from data base.
        /// </summary>
        /// <param></param>
        ///<returns>"deleted":true will be saved in the same output.json file</returns>
        public bool DeleteFile()
        {

            ServicePointManager.ServerCertificateValidationCallback += (sender, certificate, chain, sslPolicyErrors) => true;
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;

            DirectoryInfo currentDir = new DirectoryInfo(Directory.GetCurrentDirectory());
            string configFile = currentDir.Parent.Parent.FullName + @"/NLog.config";

            string functionalID = ContentAnalyzer.UploadFiles.configParams.functionalID;
            string password = ContentAnalyzer.UploadFiles.configParams.password;
            string LDAP_userName = ContentAnalyzer.UploadFiles.configParams.LDAP_userName;
            string LDAP_password = ContentAnalyzer.UploadFiles.configParams.LDAP_password;
            string mainURL = ContentAnalyzer.UploadFiles.configParams.mainURL.Trim();
            string apiKey = ContentAnalyzer.UploadFiles.configParams.apiKey;
            string outputDirectoryPath = ContentAnalyzer.UploadFiles.configParams.outputDirectoryPath;
            string[] types = ContentAnalyzer.DownloadFiles.getTypes(ContentAnalyzer.UploadFiles.configParams.responseType);
            string auth = "";
            if (functionalID != "" && password != "")
            {
                auth = ContentAnalyzer.UploadFiles.Base64Encode(functionalID + ":" + password);
            }
            else if (LDAP_userName != "" && LDAP_password != "")
            {
                auth = ContentAnalyzer.UploadFiles.Base64Encode(LDAP_userName + ":" + LDAP_password);
            } 

            string outputDir = @"../../../output.json";
            string outputFile = File.ReadAllText(@outputDir);
            if (outputFile != "")
            {
                JObject outputFiles = JObject.Parse(@outputFile);
                JArray uploadResults = JArray.Parse(outputFiles["upload_results"].ToString());
                foreach (JObject uploadResult in uploadResults)
                {
                    JObject response = JObject.Parse(uploadResult["upload_response"].ToString());
                    JObject data = JObject.Parse(response["data"].ToString());
                    string analyzerId = data["analyzerId"].ToString();

                    Boolean allCompleted = true;
                    foreach (string type in types)
                    {
                        if (uploadResult[type].ToString() != "downloaded" && uploadResult[type].ToString() != "failed")
                        {
                            allCompleted = false;
                        }
                    }
                    if (allCompleted == true)
                    {
                        logger.Info("Deleting the output of the analyzerId: " + analyzerId);
                        string url_delete = mainURL + "/contentAnalyzer/" + analyzerId;
                        var client_delete = new RestClient(url_delete);
                        var request_delete = new RestRequest(Method.DELETE);

                        request_delete.AddHeader("Authorization", "Basic " + auth);
                        request_delete.AddHeader("apiKey", apiKey);

                        IRestResponse response_delete = client_delete.Execute(request_delete);
                        if (response_delete.StatusCode == System.Net.HttpStatusCode.OK)
                        {
                            uploadResult["deleted"] = true;
                        }
                        else
                        {
                            uploadResult["deleted"] = false;
                        }
                    }
                }
                outputFiles["upload_results"] = uploadResults;
                System.IO.File.WriteAllText(@outputDir, JsonConvert.SerializeObject(outputFiles));
            }
            return true;
        }
    }
}
