import numbers
import overpy

class OverpassServerEndpoint:
    def __init__(self, host: str = "http://overpass-api.de/api/interpreter", timeout: float = 5, max_retries: int = 5):
        """
        Initializes an OverpassServerEndpoint object.

        Args:
            host (str): The host URL of the Overpass API. Defaults to "http://overpass-api.de/api/interpreter".
            timeout (float): The request timeout in seconds. Defaults to 5.
            max_retries (int): The maximum number of retries for failed requests. Defaults to 5.

        Raises:
            AssertionError: If the timeout value is not a number.
            AssertionError: If the max_retries value is not an integer or less than 1.
        """
        assert isinstance(timeout, numbers.Number), "Invalid timeout value"
        assert isinstance(max_retries, int) and max_retries >= 1, "Invalid max_retries value"

        self.api = overpy.Overpass(url=host, max_retry_count=max_retries, retry_timeout=timeout)

    def query(self, q: str) -> overpy.Result:
        """
        Executes an Overpass query and returns the result.

        Args:
            q (str): The Overpass query string.

        Returns:
            overpy.Result: The result of the query.
        """
        return self.api.query(q)
