from .base import ActorsManage

__all__ = ["ActorsUpdate"]


class ActorsUpdate(ActorsManage):
    """Update an Actor"""

    CREATE_ONLY = False

    def take_action(self, parsed_args):
        super(ActorsUpdate, self).take_action(parsed_args)
        config = self.get_configuration(parsed_args)
        config["force"] = True
        actor_id = self.get_identifier(parsed_args, "actor_id")

        # TapisResult
        self.load_client(parsed_args)
        resp = self.tapis3_client.actors.updateActor(actor_id=actor_id, **config)

        # This is the singular form for handling ONE TapisResult
        filt_resp = self.filter_record_dict(resp.__dict__, parsed_args)
        headers = [k for k in filt_resp.keys()]
        data = filt_resp.values()

        return (tuple(headers), tuple(data))
