"""
Code to push DataProduct spec to DataHub (https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/examples/library/create_dataproduct.py).
"""
import requests
import json
import uuid
from datahub.api.entities.dataproduct.dataproduct import DataProduct
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph
from datahub_utils import *

def main():
    # TO DO: insert datahub utilities to run
    search_data_product()

if __name__ == "__main__":
    main()
