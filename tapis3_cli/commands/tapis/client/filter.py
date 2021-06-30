__all__ = ['TapisResultsDisplay']


class TapisResultsDisplay(object):
    """Adds interpretation and filtering of TapisResults
    """

    DISPLAY_FIELDS = []

    def filter_record_dict(self, record, formatter='table'):
        if len(self.DISPLAY_FIELDS) == 0 or formatter != 'table':
            return record
        else:
            new_record = {}
            for k, v in record.items():
                if k in self.DISPLAY_FIELDS:
                    new_record[k] = v
            return new_record

    def filter_tapis_result(self, tapis_response, formatter='table'):
        return self.filter_record_dict(tapis_response.__dict__, formatter)

    def filter_tapis_results(self, tapis_response, formatter='table'):
        try:
            filtered = [
                self.filter_record_dict(o.__dict__, formatter)
                for o in tapis_response
            ]
            return filtered
        except TypeError:
            # Tapipy can returns a single response from a limit/offset response if
            # number of records == 1. This wraps it into a list
            return [self.filter_tapis_result(tapis_response, formatter)]

    def headers_from_result(self, tapis_data):
        if isinstance(tapis_data, list):
            if len(tapis_data) > 0:
                return [k for k in tapis_data[0].keys()]
            else:
                return []
        else:
            return [k for k in tapis_data.keys()]
