"""
Name: Get customs from your Google Analytics account
Developer: Gasyd GAGNON
Date: June 23, 2023
Description: Get all custom dimensions and metrics from your GA3 account and return them in a dictionnary
"""

import sys
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/analytics.edit'
]


def custom_inputs():
    """
        Retrieves custom dimensions and metrics from properties in the Google Analytics account, analyzing each property and collecting the relevant data. 
        The resulting custom dimensions and metrics are returned as dictionaries
        
        requires key_file - Path to client_secrets.json
        
    """

    key_file = "/Users/gasyd/Hanalytics_package_python/hanalytics-package/test/keyga3.json"
    creds = Credentials.from_service_account_file(key_file, scopes=SCOPES)

    service = build('analytics', 'v3', credentials=creds)

    print("Reading custom dimensions and metrics from property")
    print("Analyzing available accounts.")

    properties = service.management().webproperties().list(accountId='~all').execute()
    propertiesList = properties.get("items")
    nItems = len(propertiesList)
    print("Found " + str(nItems) + " properties.")

    if nItems > 30:
        print("This script will take a long time to run...")
        

    custom_dimensions = {}
    custom_metrics = {}

    for property in propertiesList:
        print("Analyzing property:\t" + property["id"] + "\t" + property["name"])
        pchunks = property["id"].split("-")

        # Custom Dimensions
        dimensions = service.management().customDimensions().list(
            accountId=pchunks[1],
            webPropertyId=property["id"],
        ).execute()
        dimList = dimensions.get("items")
        for dimension in dimList:
            dimension_name = dimension["name"]
            dimension_index = dimension["index"]
            if dimension_name not in custom_dimensions:
                custom_dimensions[dimension_name] = {"index": dimension_index, "property_ids": []}
            custom_dimensions[dimension_name]["property_ids"].append(property["id"])

        # Custom Metrics
        metrics = service.management().customMetrics().list(
            accountId=pchunks[1],
            webPropertyId=property["id"],
        ).execute()
        metList = metrics.get("items")
        for metric in metList:
            metric_name = metric["name"]
            metric_index = metric["index"]
            if metric_name not in custom_metrics:
                custom_metrics[metric_name] = {"index": metric_index, "property_ids": []}
            custom_metrics[metric_name]["property_ids"].append(property["id"])

    return custom_dimensions, custom_metrics
