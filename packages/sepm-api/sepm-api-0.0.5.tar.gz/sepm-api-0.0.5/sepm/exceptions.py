# To catch exceptions while making API calls
class APIError(Exception):
    def __init__(self, metadata, response):
        self.response = response
        self.tag = metadata["tags"][0]
        self.operation = metadata["operation"]
        self.status = (
            self.response.status_code
            if self.response is not None and self.response.status_code
            else None
        )
        self.reason = (
            self.response.reason
            if self.response is not None and self.response.reason
            else None
        )
        try:
            self.message = (
                self.response.json()
                if self.response is not None and self.response.json()
                else None
            )
        except ValueError:
            self.message = self.response.content[:100].decode("UTF-8").strip()

        super(APIError, self).__init__(
            f"{self.tag}, {self.operation} - {self.status} {self.reason}, {self.message}"
        )

    def __repr__(self):
        return f"{self.tag}, {self.operation} - {self.status} {self.reason}, {self.message}"