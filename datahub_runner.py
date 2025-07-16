import requests
import json
import uuid
from datahub.api.entities.dataproduct.dataproduct import DataProduct
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph
from datahub_utils import *

def main():
    # Insert datahub utilities to run
    modify_data_product()
    

if __name__ == "__main__":
    main()
