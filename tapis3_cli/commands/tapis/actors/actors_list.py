from ..client import AuthFormatMany


class ActorsList(AuthFormatMany):
    """List available Actors
    """
    DISPLAY_FIELDS = [
        'id', 'name', 'owner', 'image', 'lastUpdateTime', 'status'
    ]

    def take_action(self, parsed_args):
        return super().take_action(parsed_args)
