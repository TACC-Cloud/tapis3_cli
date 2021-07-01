from .base import ActorsManage

__all__ = ['ActorsCreate']


class ActorsCreate(ActorsManage):
    """Create an Actor
    """
    DISPLAY_FIELDS = []
    CREATE_ONLY = True

    def take_action(self, parsed_args):
        super(ActorsManage, self).take_action(parsed_args)
        config = self.get_configuration(parsed_args)
        # raise SystemError(config)

        # TapisResult
        self.load_client(parsed_args)
        # NOTE - this is different from V2 where one passed body=config
        # See
        resp = self.tapis3_client.actors.createActor(**config)

        # This is the singular form for handling ONE TapisResult
        filt_resp = self.filter_record_dict(resp.__dict__, parsed_args)
        headers = [k for k in filt_resp.keys()]
        data = filt_resp.values()

        return (tuple(headers), tuple(data))
