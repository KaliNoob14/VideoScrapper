
class MissingFunctionException(Exception):
    def __init__(self, domain, function_name):
        self.domain = domain
        self.function_name = function_name
        super().__init__(self._generate_message())

    def _generate_message(self):
        return f"{self.domain} module is missing the function: {self.function_name}"


class DownloadException(Exception):
    """Exception raised for errors in the download process."""
    pass