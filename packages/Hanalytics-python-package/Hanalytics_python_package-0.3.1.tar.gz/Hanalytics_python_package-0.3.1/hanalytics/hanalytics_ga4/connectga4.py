
"""
Name: Connect to the Google Analytics 4 API
Developer: Gasyd GAGNON
Date: June 23, 2023
Description: Authenticates with the Google Analytics 4 API using a client secrets JSON key file
and returns a Google Analytics service for use in other functions.
"""

import os
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient




def _get_client(service_account):
    """Create a connection using a service account.
    Args:
        service_account (string): Filepath to Google Service Account client secrets JSON keyfile
    Returns:
        client (object): Google Analytics Data API client
    """

    try:
        open(service_account)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account
        client = BetaAnalyticsDataClient()
        return client
    except Exception:
        print('Error: Google Service Account client secrets JSON key file does not exist')
        exit()


""""use this to test
from connectga4 import get_service

    # IMPORTANT: replace 'your_service_account.json' with your actual service account JSON file
    service_account = 'your_service_account.json'
    
    # Call get_service function
    service = get_service(service_account)
"""