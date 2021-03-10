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
using System.IO;
using NLog;
using NLog.Config;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Start
{
    static class start
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();

        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            //To run it, please edit the params in config.json file according to your request
            //Logs can be found in the directory, Example_Code_C#/logs/; 
            //APIs response details can be found in Example_Code_C#/output.json

            var startTime = DateTime.Now;
            DirectoryInfo currentDir = new DirectoryInfo(Directory.GetCurrentDirectory());
            string configFile = currentDir.Parent.Parent.FullName + @"/NLog.config";
            LogManager.Configuration = new XmlLoggingConfiguration(configFile);
            logger.Info("==========Content Analyzer C# API Batch Tool=========");
            logger.Info("Logs can be found in the directory, C#/Start/bin/Debug/; Processing details can be found in C#/output.json");
            logger.Info("Start Uploading Files");
            var fileTarget = LogManager.Configuration.FindTargetByName("logfile");

            string configPath = @"../../../configuration.json";
            var uploadFiles = new ContentAnalyzer.UploadFiles();
            bool resUpload = uploadFiles.UploadFile(configPath);

            if (resUpload)
            {
                logger.Info("Ready to check the processing status and download the output files");
                var downloadFiles = new ContentAnalyzer.DownloadFiles();
                bool resDownload = downloadFiles.DownloadFile();

                if (resDownload)
                {
                    logger.Info("Start deleting the files from the server");
                    var deleteFiles = new ContentAnalyzer.DeleteFiles();
                    deleteFiles.DeleteFile();

                    var endTime = DateTime.Now;
                    string outputDir = @"../../../output.json";
                    string outputFile = File.ReadAllText(outputDir);
                    if (outputFile != "")
                    {
                        JObject outputFiles = JObject.Parse(outputFile);
                        outputFiles["total_secodes"] = (endTime - startTime).TotalSeconds;
                        System.IO.File.WriteAllText(outputDir, JsonConvert.SerializeObject(outputFiles));
                        logger.Info("Completed. The total seconds is: " + (endTime - startTime).TotalSeconds);
                    }
                }
                else
                {
                    logger.Error("Could not delete the files because download is not completed");
                }
            }
            else
            {
                logger.Error("Failed to upload files for processing.");
            }

            Console.ReadLine();
        }
    }
}
