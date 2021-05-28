from ..client import AuthFormatMany


class ActorsList(AuthFormatMany):
    """List available Actors
    """
    DISPLAY_FIELDS = [
        'id', 'name', 'owner', 'image', 'lastUpdateTime', 'status'
    ]

    def take_action(self, parsed_args):
        # TapisResult
        self.load_client(parsed_args)
        # TODO - add support for limit and offset
        # https://github.com/tapis-project/tapipy/blob/a62c5e9bece9e829919b1f2d0f56f25334dcc0f1/tapipy/resources/openapi_v3-actors.yml#L42
        resp = self.tapis3_client.actors.listActors()

        filt_resp = [
            self.filter_record_dict(o.__dict__, parsed_args.formatter)
            for o in resp
        ]
        headers = [k for k in filt_resp[0].keys()]
        data = []
        for item in filt_resp:
            data.append(item.values())

        self.save_client()
        return (tuple(headers), tuple(data))
