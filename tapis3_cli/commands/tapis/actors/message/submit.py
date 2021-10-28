from .base import ActorsMessage

__all__ = ['ActorsSubmit']


class ActorsSubmit(ActorsMessage):
    """Send a message an Actor and return an Execution ID.
    """
    SYNCHRONOUS_EXECUTION = False

    def take_action(self, parsed_args):
        super(ActorsSubmit, self).take_action(parsed_args)
        # NOTE: The OAPI spec says this is supposed to be request_body not message
        if isinstance(self.config['message'], dict):
            method = self.tapis3_client.actors.sendMessage
            # NOTE: sendJSONMessage is listed in the OAPI spec but I don't know that works
            #method = self.tapis3_client.actors.sendJSONMessage
        elif isinstance(self.config['message'], str):
            method = self.tapis3_client.actors.sendMessage
        else:
            # Placeholder for BinaryMessage
            method = self.tapis3_client.actors.sendBinaryMessage

        resp = method(**self.config)

        filt_resp = self.filter_record_dict(resp.__dict__, parsed_args)
        headers = [k for k in filt_resp.keys()]
        data = filt_resp.values()

        return (tuple(headers), tuple(data))
