class WebException(Exception):
    status_code: int = 500

    def payload(self) -> dict:
        return {}

