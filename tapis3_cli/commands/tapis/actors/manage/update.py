from .base import ActorsManage

__all__ = ['ActorsUpdate']


class ActorsUpdate(ActorsManage):
    """Update an Actor
    """
    CREATE_ONLY = False

    def take_action(self, parsed_args):
        super(ActorsManage, self).take_action(parsed_args)
        config = self.get_configuration(parsed_args)
        actor_id = self.get_identifier(parsed_args)

        # TapisResult
        self.load_client(parsed_args)
        resp = self.tapis3_client.actors.update(actorId=actor_id, body=config)

        # This is the singular form for handling ONE TapisResult
        filt_resp = self.filter_record_dict(resp.__dict__,
                                            parsed_args.formatter)
        headers = [k for k in filt_resp.keys()]
        data = filt_resp.values()

        self.save_client()
        return (tuple(headers), tuple(data))
