# email_action.py
from datahub_actions.action.action import Action
from datahub_actions.event.event_envelope import EventEnvelope
from datahub_actions.event.event import Event
from datahub_actions.pipeline.pipeline_context import PipelineContext
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph
from send_email import send_email
import json
import pprint
from enum import Enum

# URNs for each status property in request workflow
class StatusProperty(Enum):
    BUSINESS_OWNER = 'urn:li:structuredProperty:e31925a0-1cb0-444d-9ead-6f00f5e35b54'
    TECHNICAL_OWNER = 'urn:li:structuredProperty:fed30a39-35b8-45db-b364-7454f3c02001'
    DATA_STEWARD = 'urn:li:structuredProperty:68d82329-8fcc-4692-9d88-084e0db4933b'

class EmailAction(Action):
    @classmethod
    def create(cls, config_dict: dict, ctx: PipelineContext) -> "Action":
        # Simply print the config_dict.
        print(config_dict)

        # share PipelineContext and Config across all instances
        return cls(ctx, config_dict)

    def __init__(self, ctx: PipelineContext, config_dict: dict):
        self.ctx = ctx
        self.config = config_dict
        
        self.target_urn_prefix = self.config['urn_prefix']  # Optional filter

    def send_email_wrapper(self, event: Event, recipient: str):
        """
        Send email with DataHub data product link.
        """
        subject = f"[DataHub] Metadata changed for {event.entityUrn}"
        url_prefix = 'http://localhost:9002/dataProduct/'
        body = f"""
        A metadata change has occurred for:
        
        URN: {event.entityUrn}
        Change Type: {event.changeType}
        Aspect: {event.aspectName}
        Link: {url_prefix}{event.entityUrn}
        Recipient: {recipient}
        """
        send_email(subject, body)

    def act(self, event: EventEnvelope) -> None:
        """
        Description:
            Send email to data domain/product owners upon metadata changes in data product.
            If no URN prefix specified, this will send emails for any MetadataChangeEvent.
            
        TO DO:
            - email owners as listed in data product aspects
            - link event to specific entity
        """
        event_object = event.event
        entity_urn = event_object.entityUrn

        # if target_urn filter specified and it doesn't match
        if self.target_urn_prefix and not entity_urn.startswith(self.target_urn_prefix):
            return  # Not a matching entity

        event_dict = json.loads(event.as_json())
        # print(json.dumps(event_dict, indent=4))
        
        curr_aspect = json.loads(event_dict['event']['aspect']['value'])
        # print(json.dumps(curr_aspect, indent=4))
        prev_aspect = json.loads(event_dict['event']['previousAspectValue']['value'])
        # print(json.dumps(prev_aspect, indent=4))

        # EXTRACT OWNERS OF DATA PRODUCT
        gms_endpoint = "http://localhost:8080"
        graph = DataHubGraph(DatahubClientConfig(server=gms_endpoint))
        ownership_info = graph.get_entity_semityped(entity_urn)
        print(f"Ownership info for {entity_urn}:")
        print(ownership_info)
        # print(json.dumps(ownership_info, indent=4))


        # CHECK WHICH PROPERTY MODIFIED
        for curr_property, prev_property in zip(curr_aspect['properties'], prev_aspect['properties']):
            # for each property, compare modified times
            assert curr_property['propertyUrn'] == prev_property['propertyUrn']
            property_urn = curr_property['propertyUrn']

            if curr_property['lastModified']['time'] != prev_property['lastModified']['time']:
                print(f"URN of modified property: {property_urn}")
                print(f"----Previous: {prev_property['values']}, Current: {curr_property['values']}")

                # DEPENDING ON MODIFIED PROPERTY, EMAIL NEXT PERSON IN WORKFLOW
                recipient = ""
                if StatusProperty.BUSINESS_OWNER == property_urn:
                    recipient = "BUSINESS OWNER"
                elif StatusProperty.TECHNICAL_OWNER == property_urn:
                    recipient = "TECHNICAL OWNER"
                elif StatusProperty.DATA_STEWARD == property_urn:
                    recipient = "DATA STEWARD"

                self.send_email_wrapper(event_object, recipient)


    def close(self) -> None:
        pass