"""
Code to push DataProduct spec to DataHub (https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/examples/library/create_dataproduct.py).
"""
import requests
import json
import uuid
from datahub.api.entities.dataproduct.dataproduct import DataProduct
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph

# ***VARIABLES***
# datahub gms endpoint - backend API to send metadata to
# 9002 is the port for the UI
gms_endpoint = "http://localhost:8080"

def create_data_product():
    """
    Description: create a data product in DataHub from user specified data.

    TO DO:
    - accept more parameters
    - data validation
    """

    graph = DataHubGraph(DatahubClientConfig(server=gms_endpoint))
    
    RETRY_LIMIT = 5
    num_entries = 0

    while num_entries < RETRY_LIMIT:
        try:
            data_product = DataProduct(
                id=input("Data Product ID (e.g., `pet_of_the_week`): ").strip(),
                display_name=input("Display Name (e.g., 'Pet of the Week Campagin'): ").strip(),
                domain="urn:li:domain:ef39e99a-9d61-406d-b4a8-c70b16380206",
                description=input("Product Description (ex: This campaign includes Pet of the Week data): ").strip(),
                assets=[
                    "urn:li:dataset:(urn:li:dataPlatform:snowflake,long_tail_companions.analytics.pet_details,PROD)",
                    "urn:li:dashboard:(looker,baz)",
                    "urn:li:dataFlow:(airflow,dag_abc,PROD)",
                ],
                owners=[{
                    "id": "urn:li:corpuser:jdoe",
                     "type": "BUSINESS_OWNER"
                }],
                terms=["urn:li:glossaryTerm:ClientsAndAccounts.AccountBalance"],
                tags=["urn:li:tag:adoption"],
                properties={
                    "lifecycle": "production",
                    "sla": "7am every day"
                },
                external_url="https://en.wikipedia.org/wiki/Sloth",
            )

            for mcp in data_product.generate_mcp(upsert=False):
                graph.emit(mcp)
            break

        except Exception as e:
            print(f"Please resolve the following error(s): {e}")
        
        finally:
            num_entries+=1

def search_data_product():
    """
    Description: search for a data product by a user specified query string.
    Search via GraphQL API:
    https://docs.datahub.com/docs/api/graphql/getting-started#search
    https://forum.datahubproject.io/t/using-datahub-python-sdk-to-perform-graphql-search-operations/1384/3
    """

    
    # Initialize the DataHubGraph client
    # List of config attributes: https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/src/datahub/ingestion/graph/client.py#L227
    client = DataHubGraph(DatahubClientConfig(server=gms_endpoint))
    
    # accept query string from user
    query_string = input(f"Enter query string to search in DataHub (default: *): ") or "*"

    # query for all Data Products
    query = """
    query search($input: SearchInput!) {
        search(input: $input) {
            start
            count
            total
            searchResults {
                entity {
                    urn
                    ...on DataProduct {
                        properties {
                            name
                            description
                        }
                    }
                }
            }
        }
    }
    """
    variables = {
        "input": { 
            "type": "DATA_PRODUCT", 
            "query": query_string, 
            "start": 0, 
            "count": 100 
        }
    }

    # Execute the GraphQL query
    response = client.execute_graphql(query, variables)
    print(response)


def modify_data_product():
    """
    Modify existing data products in DataHub.
    Use GraphQL mutations.

    TO DO: 
    - update product status via custom property?
    """
    # update Domains
    from datahub.metadata.urns import DatasetUrn, DomainUrn
    from datahub.sdk import DataHubClient

    client = DataHubClient.from_env()

    dataset = client.entities.get(DatasetUrn(platform="snowflake", name="example_dataset"))

    # if you don't know the domain id, you can get it from resolve client by name
    # domain_urn = client.resolve.domain(name="marketing")

    # NOTE : This will overwrite the existing domain
    dataset.set_domain(DomainUrn(id="marketing"))

    client.entities.update(dataset)
    
    # update Tags


    # update Owners

    pass
