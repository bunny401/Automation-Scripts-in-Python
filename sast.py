#!/usr/bin/python3
import argparse
import code
from lib2to3.pgen2 import token
import os
from re import L, S
from tokenize import Token
import urllib 
import requests
import logging
import sys
import json
import time
from pprint import pprint
from datetime import datetime
import http.client as http_client
from dotenv import load_dotenv
load_dotenv()
import csv
from requests.api import head


URL = "https://cloud.appscan.com/api/V2/"
ASOC_KEY_ID = os.getenv("ASOC_KEY_ID")
ASOC_KEY_SECRET = os.getenv("ASOC_KEY_SECRET")
EVS_APP_ID = "6637faa4-eaf6-4240-9f8e-7b00d5839a50"
ECDN_APP_ID = "6028f372-9e95-45c5-b3fd-fe69826e5818"

# print(ASOC_KEY_SECRET)

#log in to the appscan
def asoc_auth():
    print("[+] Logging into the AppScan")
    json_body = {"KeyId": ASOC_KEY_ID, "KeySecret": ASOC_KEY_SECRET}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    r = requests.post(URL+"Account/ApiKeyLogin", json=json_body, headers=headers)
    #dont forget to remove it
    #print(r.text) 
    
    
    if r.ok:
        return{"Accept": "application/json", "Authorization": f"Bearer {r.json()['Token']}"}  
    else:
        print("[!] ASoC authentication failed!")
        sys.exit(1)

        
#(1) To get the details of a specific scan
# def specific_scan_details(headers, SCAN_ID):
#     print("[+] Getting the details of the scan ")
#     r=requests.get(URL+"Scans/StaticAnalyzer/"+ SCAN_ID, headers=headers)
#     pretty_json = json.loads(r.text)  
#     print (json.dumps(pretty_json, indent=2))  
    
    
# (2) To get all the issues beloging to the provded Fix Group ID
def specific_scans_issues(headers, SCAN_ID, FIX_GROUP_ID):
    print("[+] Getting Details of the issue of the provided Fix Group ID")
    r=requests.get(URL+"FixGroups/Scan/"+SCAN_ID+"/"+FIX_GROUP_ID+"/Issues?$filter=Status ne 'Noise'", headers=headers )
    # pretty_json = json.loads(r.text)  
    # print(r.text)
    
    myjson=r.json()
    ourdata=[]
    
    csvheader = ['ID','Language','Severity','Status','Issue Type','Location']
    for x in myjson ['Items']:
        listing=[x['Id'],x['Language'],x['Severity'],x['Status'],x['IssueType'],x['Location']]
        ourdata.append(listing)
        
        # chane 'a' to 'w' when first time creating the file
    with open('Scans.csv','a',encoding='UTF8', newline='')as f:
        writer=csv.writer(f)
        writer.writerow(csvheader)
        writer.writerows(ourdata)
        
    print('done')
    # print (json.dumps(pretty_json, indent=2)) 



#(3) To get the issues by severity
def Issues_by_Severity(headers, SCAN_ID, Severity_Provided ):
    print("[+] Getting Details of the issue of the provided Severity")
    r=requests.get(URL+"Issues/Scan/"+SCAN_ID+"?$filter=Severity eq"+Severity_Provided, headers=headers )
    # pretty_json = json.loads(r.text)  
    # print(r.text)
    
    myjson=r.json()
    ourdata=[]
    
    csvheader = ['ID','Language','Severity','Status','Issue Type','Location']
    for x in myjson ['Items']:
        listing=[x['Id'],x['Language'],x['Severity'],x['Status'],x['IssueType'],x['Location']]
        ourdata.append(listing)
        
        # chane 'a' to 'w' when first time creating the file
    with open('Scans_ordered_by_Severity.csv','a',encoding='UTF8', newline='')as f:
        writer=csv.writer(f)
        writer.writerow(csvheader)
        writer.writerows(ourdata)
        
    print('done')


if __name__ == "__main__":
   headers= asoc_auth()
   
   SCAN_ID=input("Please Provide the Scan ID:")
#    specific_scan_details(headers, SCAN_ID)
   
FIX_GROUP_ID=input("Please provide the Fix Group ID: ")
specific_scans_issues(headers, SCAN_ID, FIX_GROUP_ID)
   
Severity_Provided=input("Please enter which severity issues you want(Type 'NO' to exit): ")
   
if Severity_Provided == 'NO' or Severity_Provided=='No' or Severity_Provided=='no' or Severity_Provided =='no' :
       print("[+] Exiting")
       exit()
else:
       Issues_by_Severity(headers, SCAN_ID, Severity_Provided)
       
   
   
   
   
   
