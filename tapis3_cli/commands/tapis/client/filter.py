__all__ = ['TapisResultsDisplay']


class TapisResultsDisplay(object):
    """Adds interpretation and filtering of TapisResults
    """

    DISPLAY_FIELDS = []

    def _formatter(self, parsed_args=None):
        if parsed_args is None:
            return 'table'
        else:
            return getattr(parsed_args, 'formatter', 'table')

    def filter_record_dict(self, record, parsed_args=None):
        if len(self.DISPLAY_FIELDS
               ) == 0 or self._formatter(parsed_args) != 'table':
            return record
        else:
            new_record = {}
            for k, v in record.items():
                if k in self.DISPLAY_FIELDS:
                    new_record[k] = v
            return new_record

    def filter_tapis_result(self, tapis_response, parsed_args=None):
        return self.filter_record_dict(tapis_response.__dict__, parsed_args)

    def filter_tapis_results(self, tapis_response, parsed_args=None):
        try:
            filtered = [
                self.filter_record_dict(o.__dict__, parsed_args)
                for o in tapis_response
            ]
            return filtered
        except TypeError:
            # Tapipy can returns a single response from a limit/offset response if
            # number of records == 1. This wraps it into a list
            return [self.filter_tapis_result(tapis_response, parsed_args)]

    def headers_from_result(self, tapis_data):
        if isinstance(tapis_data, list):
            if len(tapis_data) > 0:
                return [k for k in tapis_data[0].keys()]
            else:
                return []
        else:
            return [k for k in tapis_data.keys()]
