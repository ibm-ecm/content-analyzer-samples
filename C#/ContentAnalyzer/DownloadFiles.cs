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
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.IO;
using RestSharp;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using NLog;

namespace ContentAnalyzer
{
    public class DownloadFiles
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();

        /// <summary>
        /// Read the configuration.json file to get the request parameters required for the get request.
        /// will read the analyzer ID saved in the uploadFile function and use it to get the processing status first
        /// if the status is Completed, will download the output, if the status is inProgress, will wait for 5 second and check the status again
        /// the maximum loop to check the status is set to be 50
        /// </summary>
        /// <param></param>
        ///<returns>the response will be saved in the same output.json file, such as, "json":"downloaded","pdf":"downloaded","utf8":"downloaded"</returns>
        public bool DownloadFile()
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
            string[] types = getTypes(ContentAnalyzer.UploadFiles.configParams.responseType);
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

                var analyzers_unfinished = new List<JObject>();

                int no = 0;
                foreach (JObject uploadResult in uploadResults)
                {
                    JObject response = JObject.Parse(uploadResult["upload_response"].ToString());
                    JObject data = JObject.Parse(response["data"].ToString());
                    string id = data["analyzerId"].ToString();
                    JObject ID = new JObject(uploadResult);
                    ID["analyzerId"] = id;
                    ID["deleted"] = false;
                    ID["time_elapsed"] = "";
                    foreach(string type in types) {
                        ID[type] = "";
                    }
                    analyzers_unfinished.Add(ID);
                    no++;
                }

                if (Directory.Exists(outputDirectoryPath))
                {
                    foreach (string type in types)
                    {
                        if (! Directory.Exists(outputDirectoryPath + "/" + type))
                        {
                            DirectoryInfo path = Directory.CreateDirectory(outputDirectoryPath + "/" + type);
                        }
                    }
                }

                int maxLoop = 50;
                int loop = 1;
                var finished_analyzers = new List<JObject>();
                while (loop < maxLoop)
                {
                    logger.Info("Check processing status: loop " + loop);
                    System.Threading.Thread.Sleep(5000);
                    var latest_analyzers_unfinished = new List<JObject>(analyzers_unfinished);

                    foreach (JObject analyzer in latest_analyzers_unfinished)
                    {
                        string analyzerId = analyzer["analyzerId"].ToString();
                        logger.Info("Checking status of analyzerId: " + analyzerId);

                        string url = mainURL + "/contentAnalyzer/" + analyzerId;
                        var client = new RestClient(url);
                        var request = new RestRequest(Method.GET);

                        request.AddHeader("Authorization", "Basic " + auth);
                        request.AddHeader("apiKey", apiKey);

                        IRestResponse response = client.Execute(request);

                        if (response.StatusCode == System.Net.HttpStatusCode.OK)
                        {
                            string res = response.Content;
                            JObject resObj = JObject.Parse(res);
                            JObject dataObj = JObject.Parse(resObj["data"].ToString());
                            JArray statusDetails = JArray.Parse(dataObj["statusDetails"].ToString());
                            var final_analyzers = new List<JObject>();

                            foreach (JObject statusDetail in statusDetails)
                            {
                                string typeDownload = statusDetail["type"].ToString().ToLower();
                                string status = statusDetail["status"].ToString();
                                if (status == "Completed" && analyzer[typeDownload].ToString() != "downloaded" && analyzer[typeDownload].ToString() != "failed")
                                {
                                    string url_download = mainURL + "/contentAnalyzer/" + analyzerId + "/" + typeDownload;
                                    var client_download = new RestClient(url_download);
                                    var request_download = new RestRequest(Method.GET);

                                    request_download.AddHeader("Authorization", "Basic " + auth);
                                    request_download.AddHeader("apiKey", apiKey);

                                    IRestResponse response_download = client_download.Execute(request_download);

                                    logger.Info("Downloading the " + typeDownload + " output of the analyzerId: " + analyzerId);

                                    if (response_download.StatusCode == System.Net.HttpStatusCode.OK)
                                    {
                                        if (Directory.Exists(@outputDirectoryPath))
                                        {

                                            var res_download = response_download.Content;
                                            //string fileExt = Path.GetExtension(analyzer["filename"].ToString());
                                            string newFileName = "";
                                            if (typeDownload == "pdf")
                                            {
                                                newFileName = "New_" + Path.GetFileNameWithoutExtension(analyzer["filename"].ToString()) + ".pdf";
                                                //if (fileExt == ".pdf")
                                                //    newFileName = "New_" + Path.GetFileNameWithoutExtension(analyzer["filename"].ToString()) + ".pdf";
                                                //else
                                                //    newFileName = Path.GetFileNameWithoutExtension(analyzer["filename"].ToString()) + ".pdf";

                                                string outputPath = outputDirectoryPath + "/" + typeDownload + "/" + newFileName;
                                                System.IO.File.WriteAllBytes(@outputPath, response_download.RawBytes);
                                            }
                                            else if (typeDownload == "json")
                                            {
                                                newFileName = Path.GetFileNameWithoutExtension(analyzer["filename"].ToString()) + ".json";
                                                string outputPath = outputDirectoryPath + "/" + typeDownload + "/" + newFileName;
                                                JObject resJson = JObject.Parse(res_download);
                                                System.IO.File.WriteAllText(@outputPath, resJson["data"].ToString());
                                                analyzer["time_elapsed"] = statusDetail["timeElapsed"].ToString();

                                            }
                                            else
                                            {
                                                newFileName = Path.GetFileNameWithoutExtension(analyzer["filename"].ToString()) + ".txt";
                                                string outputPath = outputDirectoryPath + "/" + typeDownload + "/" + newFileName;
                                                System.IO.File.WriteAllText(@outputPath, res_download);
                                            }
                                            analyzer[typeDownload] = "downloaded";
                                        }
                                        else
                                        {
                                            logger.Error("Failed to download " + typeDownload + " output of the analyzerId: " + analyzerId);
                                            analyzer[typeDownload] = "failed";
                                        }
                                    }
                                    else {
                                        logger.Error("Output directory defined in config.json does not exist.");
                                    }

                                }
                                else if (status == "failed")
                                {
                                    analyzer[typeDownload] = "failed";
                                }
                            }

                            bool allCompleted = true;
                            foreach (string type in types)
                            {
                                if (analyzer[type].ToString() != "downloaded" && analyzer[type].ToString() != "failed")
                                {
                                    allCompleted = false;
                                }
                            }
                            if (allCompleted == true)
                            {
                                analyzers_unfinished.Remove(analyzer);
                                finished_analyzers.Add(analyzer);
                            }

                            final_analyzers.AddRange(finished_analyzers);
                            final_analyzers.AddRange(analyzers_unfinished);
                            //Update output
                            outputFiles["upload_results"] = new JArray(final_analyzers);
                            System.IO.File.WriteAllText(@outputDir, JsonConvert.SerializeObject(outputFiles));
                        }
                        else
                        {

                            logger.Error("Http error occurred when checking status of analyzerId: " + analyzerId);
                            foreach (string type in types)
                            {
                                analyzer[type] = "Failed";
                            }
                        }
                    }
                    logger.Info("Number of unfinished files: " + analyzers_unfinished.Count);
                    if (analyzers_unfinished.Count != 0)
                    {
                        loop++;
                    }
                    else
                    {
                        loop = maxLoop + 1;
                    }
                }
            }
            return true;
        }


        public static string[] getTypes(string options)
        {
            string[] types = options.Split(',').Select(p => p.Trim().ToLower()).ToArray();
            int i = 0;
            foreach(string type in types)
            {
                string type1 = type.Substring(1);
                types[i] = type1.Substring(0, type.Length - 2);
                i++;
            }

            return types;
        }

    }
}
