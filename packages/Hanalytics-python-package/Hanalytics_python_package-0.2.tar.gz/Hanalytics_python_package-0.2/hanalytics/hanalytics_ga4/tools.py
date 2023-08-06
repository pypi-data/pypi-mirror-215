"""
Name: Some tools to help you with Google Analytics 4 
Developer: Gasyd GAGNON
Date: June 23, 2023
"""
import os
import csv
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import MetricType
from google.analytics.data_v1beta.types import GetMetadataRequest
from google.analytics.data_v1beta import BetaAnalyticsDataClient



def _get_client(service_account):
    """Create a connection using a service account.
    Args:
        service_account (string): Path to the Google Service Account JSON keyfile
    Returns:
        client (object): Google Analytics Data API client
    """
    try:
        open(service_account)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account
        client = BetaAnalyticsDataClient()
        return client
    except Exception:
        print('Error: Google Service Account JSON keyfile does not exist')
        exit()


def _get_request(service_account, request, report_type="report"):
    """Send a request to the API and return a response.
    Args:
        service_account (string): Path to the Google Service Account JSON keyfile
        request (protobuf): API request in Protocol Buffer format.
        report_type (string): Report type (report, batch_report, pivot, batch_pivot, or realtime)
    Returns:
        response: API response.
    """

    client = _get_client(service_account)

    if report_type == "realtime":
        response = client.run_realtime_report(request)

    elif report_type == "pivot":
        response = client.run_pivot_report(request)

    elif report_type == "batch_pivot":
        response = client.batch_run_pivot_reports(request)

    elif report_type == "batch_report":
        response = client.batch_run_reports(request)

    else:
        response = client.run_report(request)

    return response


def _get_headers(response):
    """Returns a Python list containing the names of the dimension and metric headers from the Protobuf response.
    Args:
        response (object): Google Analytics Data API response
    Returns:
        headers (list): List of column header names.
    """

    headers = []

    for header in response.dimension_headers:
        headers.append(header.name)

    for header in response.metric_headers:
        headers.append(header.name)

    return headers


def _get_rows(response):
    """Returns a Python list containing the row values from the Protobuf response.
    Args:
        response (object): Google Analytics Data API response
    Returns:
        rows (list): List of rows.
    """

    rows = []
    for _row in response.rows:
        row = []
        for dimension in _row.dimension_values:
            row.append(dimension.value)
        for metric in _row.metric_values:
            row.append(metric.value)
        rows.append(row)
    return rows


def _to_dataframe(response):
    """Returns a Pandas dataframe of the results.
    Args:
        response (object): Google Analytics Data API response
    Returns:
        df (dataframe): Pandas dataframe created from the response.
    """

    headers = _get_headers(response)
    rows = _get_rows(response)
    df = pd.DataFrame(rows, columns=headers)
    return df


def _batch_to_dataframe_list(response):
    """Returns a list of dataframes from the results of a batchRunReports request.
    Args:
        response (object): Response object from a batchRunReports request.
    Returns:
        output (list): List of Pandas dataframes of the results.
    """

    output = []
    for report in response.reports:
        output.append(_to_dataframe(report))
    return output


def _batch_pivot_to_dataframe_list(response):
    """Returns a list of dataframes from the results of a batchRunPivotReports request.
    Args:
        response (object): Response object from a batchRunPivotReports request.
    Returns:
        output (list): List of Pandas dataframes of the results.
    """

    output = []
    for report in response.pivot_reports:
        output.append(_to_dataframe(report))
    return output


def _handle_response(response):
    """Uses the type to determine the requested report type and reformats the output into a Pandas dataframe.
    Args:
        response (object): Protobuf response object from the Google Analytics Data API.
    Returns:
        output (dataframe, or list of dataframes): Returns a single dataframe for runReport, runPivotReport,
        or runRealtimeReport,
        or a list of dataframes for batchRunReports and batchRunPivotReports.
    """

    if response.kind == "analyticsData#runReport":
        return _to_dataframe(response)
    if response.kind == "analyticsData#batchRunReports":
        return _batch_to_dataframe_list(response)
    if response.kind == "analyticsData#runPivotReport":
        return _to_dataframe(response)
    if response.kind == "analyticsData#batchRunPivotReports":
        return _batch_pivot_to_dataframe_list(response)
    if response.kind == "analyticsData#runRealtimeReport":
        return _to_dataframe(response)
    else:
        print('Not supported')


def query(service_account, request, report_type="report"):
    """Returns the Pandas formatted data for a Google Analytics Data API request.
    Args:
        service_account (string): Path to the Google Service Account JSON keyfile
        request (protobuf): Protocol buffer request of the Google Analytics Data API
        report_type (string): Report type (report, batch_report, pivot, batch_pivot, or realtime)
    Returns:
        output (dataframe, or list of dataframes): Returns a single dataframe for runReport, runPivotReport,
        or runRealtimeReport,
        or a list of dataframes for batchRunReports and batchRunPivotReports.
    """

    response = _get_request(service_account, request, report_type)
    output = _handle_response(response)
    return output


def get_metadata(service_account, property_id):
    """Returns the metadata for the Google Analytics property.
    Args:
        service_account (string): Path to the Google Service Account JSON keyfile
        property_id (string): Google Analytics 4 property ID
    Returns:
        df (dataframe): Pandas dataframe of the property metadata.
    """

    client = _get_client(service_account)
    request = GetMetadataRequest(name=f"properties/{property_id}/metadata")
    response = client.get_metadata(request)

    metadata = []
    for dimension in response.dimensions:
        metadata.append({
            "Type": "Dimension",
            "Data type": "STRING",
            "API Name": dimension.api_name,
            "UI Name": dimension.ui_name,
            "Description": dimension.description,
            "Custom definition": dimension.custom_definition
        })

    for metric in response.metrics:
        metadata.append({
            "Type": "Metric",
            "Data type": MetricType(metric.type_).name,
            "API Name": metric.api_name,
            "UI Name": metric.ui_name,
            "Description": metric.description,
            "Custom definition": metric.custom_definition
        })

    return pd.DataFrame(metadata).sort_values(by=['Type', 'API Name']).drop_duplicates()


def write_dimensions_to_csv(dimensions, output_file):
    """Writes dimension names to a CSV file.
    Args:
        dimensions (list): List of dimension names.
        output_file (string): Path of the output CSV file.
    """
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Dimension Name'])
        for dimension in dimensions:
            writer.writerow([dimension])  # Wrap dimension name in a list


def get_all_dimension_names(service_account, property_id, output_file="dimension_names.csv"):
    """Fetches all dimension names for a specific property and writes them to a CSV file.
    Args:
        service_account (string): Path to the Google Service Account JSON keyfile
        property_id (string): Google Analytics 4 property ID
        output_file (string): Path of the output CSV file to save dimension names.
    """
    # Fetch metadata for the property
    metadata = get_metadata(service_account, property_id)
    
    # Filter the metadata for dimension names
    dimension_names = metadata[metadata["Type"] == "Dimension"]["API Name"].tolist()
    
    # Write the dimension names to the CSV file
    write_dimensions_to_csv(dimension_names, output_file)


"""use this to test 
from tools import query, get_metadata, get_all_dimension_names
# Define the service account and property id
service_account = "path_to_your_service_account.json"
property_id = "your_property_id"

# Use the query function
output = query(service_account, request, report_type="report")

# Use the get_metadata function
metadata = get_metadata(service_account, property_id)

# Use the get_all_dimension_names function
get_all_dimension_names(service_account, property_id, output_file="dimension_names.csv")
"""




