import numbers
import requests


class ElevationServerEndpoint:
    def __init__(
        self,
        host: str = "https://api.opentopodata.org",
        version: str = "v1",
        timeout: float = 5,
        max_retries: int = 5,
    ):
        """
        Initializes an ElevationServerEndpoint object.

        Args:
            host (str): The host URL of the elevation server. Defaults to "https://api.opentopodata.org".
            version (str): The version of the elevation API. Defaults to "v1".
            timeout (float): The request timeout in seconds. Defaults to 5.
            max_retries (int): The maximum number of retries for failed requests. Defaults to 5.

        Raises:
            AssertionError: If the timeout value is not a number.
            AssertionError: If the max_retries value is not an integer or less than 1.
        """
        assert isinstance(timeout, numbers.Number), "Invalid timeout value"
        assert isinstance(max_retries, int) and max_retries >= 1, "Invalid max_retries value"

        self.host = host
        self.version = version
        self.timeout = timeout
        self.max_retries = max_retries

        self.session = requests.Session()
        self.adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        self.session.mount("http://", self.adapter)
        self.session.mount("https://", self.adapter)

    def _build_request(self, dataset: str) -> str:
        """
        Builds the request URL for the given dataset.

        Args:
            dataset (str): The dataset to use.

        Returns:
            str: The complete request URL.
        """
        url = f"{self.host}/{self.version}/{dataset}"
        return url

    def _decode_response(self, response) -> dict:
        """
        Decodes the response received from the elevation server.

        Args:
            response: The response object.

        Returns:
            dict: The decoded response.

        Raises:
            Exception: If the response does not contain a valid status.
        """
        response = response.json()
        if "status" not in response or "OK" not in response.get("status", {}):
            raise Exception(
                f"No valid response from ElevationServerEndpoint. Please review your input parameters. Response={response}"
            )
        return response

    def estimate(self, coordinates, dataset: str = "mapzen") -> dict:
        """
        Estimates the elevation for the given coordinates using the specified dataset.

        Args:
            coordinates: The input coordinates.
            dataset (str): The dataset to use. Defaults to "mapzen".

        Returns:
            dict: The decoded response from the elevation server.

        Raises:
            Exception: If there is no valid response.
        """
        if isinstance(coordinates[0], numbers.Number):
            coordinates = [coordinates]
        params = {
            "locations": "|".join([",".join([str(coord[0]), str(coord[1])]) for coord in coordinates])
        }
        url = self._build_request(dataset)
        return self._decode_response(self.session.get(url, params=params, timeout=self.timeout))
