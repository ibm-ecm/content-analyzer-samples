#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed Materials - Property of IBM
# 6949-68N
#
# © Copyright IBM Corp. 2018 All Rights Reserved

# initialize postgresql functions, create schema and ontology tables and migrate jena data into postgresql
# ************************************************************

import json, sys
import os
from datetime import datetime
import time
import csv
import configparser
import ibm_db_dbi as DB2Driver


def main():
    class tenant:
        # Constructor
        def __init__(self, tenantid, dbname, ontology, connect_string, bas_id):
            self.tenantid = tenantid
            self.dbname = dbname
            self.ontology = ontology
            self.connect_string = connect_string
            self.bas_id = bas_id

    # read the config file and populate baseDBString to connect to base database 
    baseDBString = None
    parser = configparser.ConfigParser()
    file = parser.read('/Users/sudhakar/SmartPages-Cloud-Backend/x-ray/pythonfiles/config.ini')
    if file:
        base_db = parser.get('BaseDBSettings','base_db')
        host_name = parser.get('BaseDBSettings', 'host_name')
        port_number = parser.get('BaseDBSettings', 'port_number')
        base_db_schema = parser.get('BaseDBSettings', 'base_db_schema')
        user_id = parser.get('BaseDBSettings', 'user_id')
        password = parser.get('BaseDBSettings', 'password')
        number_days = int(parser.get('QuerySettings', 'number_days'))
        baseDBString = "DATABASE=" + base_db + ";HOSTNAME=" + host_name + ";PORT=" + port_number + ";PROTOCOL=TCPIP;" + "UID=" + user_id + ";PWD=" + password
    else:
        sys.exit("Configuration File Not Found")

    try:
        conn = DB2Driver.connect(baseDBString)
        cursor = conn.cursor()
        cursor.execute("SET SCHEMA " + base_db_schema)

        cursor.execute("select tenantid, dbname, ontology, connstring, bas_id from tenantinfo where dbstatus=1")
        row = cursor.fetchone()
        tenants = {}
        i = 0

        while row is not None:
            # print(row)
            i = i + 1
            obj = tenant(row[0], row[1], row[2], row[3], row[4])
            tenants.update({i: obj})
            row = cursor.fetchone()

        cursor.close()
        if conn is not None:
            conn.close()

        dtNow = datetime.now()
        file_name = "usage_data_" + str(dtNow) + '.csv'
        header = ['tenantid', 'ontology', 'bas_id', 'date','num_pages']
        write_header = True


        for x, tenant in tenants.items():
            #get Tenant, Ontology and Bas ID
            tenant_id = tenant.tenantid
            ontology = tenant.ontology
            bas_id = tenant.bas_id
            try:
                print(f'Getting information for , TenantId: {tenant.tenantid}, Ontolgy: {tenant.ontology}, BasId: {tenant.bas_id}')

                tenant_string = "DATABASE=" + tenant.dbname + ";HOSTNAME=" + host_name + ";PORT=" + port_number + ";PROTOCOL=TCPIP;" + "UID=" + \
                                user_id + ";PWD=" + password

                conn = DB2Driver.connect(tenant_string)
                cursor = conn.cursor()
                cursor.execute("SET SCHEMA " + tenant.ontology)

                # Usage query against each project
                usage_query = "with temp(dates) as (select DATE(CURRENT_TIMESTAMP - CURRENT_TIMEZONE) - (? - 1) Days as dates from sysibm.sysdummy1 union all select dates + 1 Days from temp where dates < DATE(CURRENT_TIMESTAMP - CURRENT_TIMEZONE)) SELECT temp.dates as date, coalesce(sum(d.NUMBER_OF_PAGE), 0) as pages from temp LEFT OUTER JOIN PROCESSED_FILE as d on DATE(TIMESTAMP('1970-01-01', '00:00:00') + (d.Date / 1000) SECOND) = temp.dates group by temp.dates order by temp.dates desc"

                # cursor.execute("select sum(number_of_page) from processed_file")
                cursor.execute(usage_query, (number_days,))
                row = cursor.fetchone()
                # rows = cursor.fetchall()


                #write header
                with open(file_name, "a") as file:
                    if write_header:
                        csv.writer(file).writerow(header)
                        write_header = False

                    # for row in  rows:
                    #     tenant_id = tenant.tenantid
                    #     ontology  = tenant.ontology
                    #     add_with_meta = (tenant_id, ontology, *row)
                    #     csv.writer(file).writerow(add_with_meta)

                    while row is not None:
                        tenant_id = tenant.tenantid
                        ontology = tenant.ontology
                        bas_id = tenant.bas_id
                        add_with_meta = (tenant_id, ontology, bas_id, *row)
                        csv.writer(file).writerow(add_with_meta)

                        row = cursor.fetchone()

                cursor.close()
                if conn is not None:
                    conn.close()
            except Exception as ex:
                # Add exption Projects to csv
                with open(file_name, "a") as file:
                    add_with_meta = (tenant_id, ontology, bas_id, 'Failed', 'Failed')
                    csv.writer(file).writerow(add_with_meta)
                line_no = sys.exc_info()[-1].tb_lineno
                print(f'Exception Happened For  , TenantId: {tenant.tenantid}, Ontolgy: {tenant.ontology}')
                #print("Failure on : {0} on line {1} ".format(str(ex), line_no))

    except Exception as ex:
        line_no = sys.exc_info()[-1].tb_lineno
        print("Failure on initDB: {0} on line {1} ".format(str(ex), line_no))


if __name__ == "__main__":
    result = main()
