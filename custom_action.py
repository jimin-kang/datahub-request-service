# custom_action.py
from datahub_actions.action.action import Action
from datahub_actions.event.event_envelope import EventEnvelope
from datahub_actions.pipeline.pipeline_context import PipelineContext
from send_email import send_email

class CustomAction(Action):
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
                
        # self.recipient = ctx.recipient
        # self.smtp_server = ctx.smtp_server
        # self.smtp_port = ctx.smtp_port
        # self.sender_email = ctx.sender_email
        # self.sender_password = ctx.sender_password

    def act(self, event: EventEnvelope) -> None:
        """
        Description:
            Send email to data domain/product owners upon metadata changes in data product.
            If no URN prefix specified, this will send emails for any MetadataChangeEvent.
            
        TO DO:
            - email owners as listed in data product aspects
            - link event to specific entity
        """
        # send_email()

        entity_urn = event.event.entityUrn

        # if target_urn filter specified and it doesn't match
        if self.target_urn_prefix and not entity_urn.startswith(self.target_urn_prefix):
            return  # Not a matching entity

        subject = f"[DataHub] Metadata changed for {entity_urn}"
        body = f"""
        A metadata change has occurred for:
        
        URN: {entity_urn}
        Change Type: {event.event.changeType}
        Aspect: {event.event.aspectName}
        """

        send_email(subject, body)


    def close(self) -> None:
        pass