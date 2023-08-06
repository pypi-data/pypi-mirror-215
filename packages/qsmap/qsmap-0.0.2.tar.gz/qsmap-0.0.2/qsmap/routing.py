import requests
import json
import polyline
import numbers
import copy
from typing import Any, Dict, List, Optional, Union, Tuple

response_keys_cfg = {
    "match": "matchings",
    "route": "routes"
}

class RoutingServerEndpoint:
    def __init__(
        self,
        host: str = "http://router.project-osrm.org",
        version: str = "v1",
        profile: str = "driving",
        timeout: float = 5,
        max_retries: int = 5,
    ):
        """
        Initializes a RoutingServerEndpoint object.

        Args:
            host (str): The host URL of the routing server. Defaults to "http://router.project-osrm.org".
            version (str): The version of the routing API. Defaults to "v1".
            profile (str): The routing profile to use. Defaults to "driving".
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
        self.profile = profile
        self.timeout = timeout
        self.max_retries = max_retries

        self.session = requests.Session()
        self.adapter = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        self.session.mount("http://", self.adapter)
        self.session.mount("https://", self.adapter)

    def _build_request(self, service: str, coordinates: str) -> str:
        """
        Builds the request URL for the given service and coordinates.

        Args:
            service (str): The routing service to use.
            coordinates (str): The coordinates in the format "lat1,lon1;lat2,lon2;...".

        Returns:
            str: The complete request URL.
        """
        url = f"{self.host}/{service}/{self.version}/{self.profile}/{coordinates}"
        return url

    def _encode_val(self, value) -> Union[str, numbers.Number]:
        """
        Encodes the given value to a string.

        Args:
            value: The value to encode.

        Returns:
            str or numeric: The encoded value.
        """
        return str(value).lower() if isinstance(value, (bool, str)) else value

    def _decode_response(self, response, service: str, params: dict) -> dict:
        """
        Decodes the response received from the routing server.

        Args:
            response: The response object.
            service (str): The routing service used.
            params (dict): The request parameters.

        Returns:
            dict: The decoded response.

        Raises:
            ValueError: If the response does not contain a valid code or if the geometry decoding fails.
        """
        response = response.json()
        if ("code" not in response) or ("Ok" not in response.get("code", {})):
            raise ValueError(
                f"No valid response from RoutingServerEndpoint. Please review your input parameters. Response={response}"
            )
        if service in ("match", "route"):
            if response_keys_cfg[service] in response:
                for item in response[response_keys_cfg[service]]:
                    geom_encoded = item["geometry"]
                    if (params["geometries"] in ("polyline", "polyline6")) and geom_encoded:
                        geom_decoded = [
                            [point[0], point[1]] for point in polyline.decode(geom_encoded)
                        ]
                    else:
                        geom_decoded = copy.deepcopy(geom_encoded)
                        geom_decoded["coordinates"] = [
                            [point[1], point[0]] for point in geom_encoded["coordinates"]
                        ]
                    item["geometry"] = geom_decoded
            else:
                raise ValueError(f"No {service} geometry found to decode")
        return response

    def match(
        self,
        coordinates,
        steps: bool = False,
        overview: str = "full",
        geometry: str = "polyline",
        timestamps: list = None,
        radius: list = None,
        annotations: Union[bool,str] = False,
        gaps: str = "ignore",
        tidy: bool = False,
        waypoints: list = None,
    ) -> dict:
        """
        Finds the best match for a set of input coordinates.

        Args:
            coordinates : The input coordinates.
            steps (bool): Whether to return step-by-step instructions. Defaults to False.
            overview (str): The level of overview geometry to be returned. Defaults to "full".
            geometry (str): The type of geometry to use in the response. Defaults to "polyline".
            timestamps (list): Optional timestamps corresponding to the input coordinates.
            radius (list): Standard deviation of GPS precision used for map matching. If applicable use GPS accuracy.
            annotations (bool or str): Whether to include additional metadata in the response. Defaults to False.
            gaps (str): Allows the input track splitting based on huge timestamp gaps between points. Defaults to "ignore".
            tidy (bool): Allows the input track modification to obtain better matching quality for noisy tracks. Defaults to False.
            waypoints (list): Treats input coordinates indicated by given indices as waypoints in returned Match object.

        Returns:
            dict: The decoded response from the routing server.

        Raises:
            ValueError: If there is no valid response or if geometry decoding fails.
        """
        params = {
            "steps": self._encode_val(steps),
            "overview": overview,
            "geometries": geometry,
            "timestamps": timestamps,
            "radiuses": radius,
            "annotations": self._encode_val(annotations),
            "gaps": gaps,
            "tidy": self._encode_val(tidy),
            "waypoints": waypoints,
        }
        url = self._build_request("match", ";".join([f"{coord[1]},{coord[0]}" for coord in coordinates]))
        return self._decode_response(
            self.session.get(url, params=params, timeout=self.timeout), "match", params
        )

    def nearest(self, coordinates, number: int = 1) -> dict:
        """
        Finds the nearest road segment(s) for the given coordinates.

        Args:
            coordinates : The input coordinate.
            number (int): The number of nearest segments that should be returned. Defaults to 1.

        Returns:
            dict: The decoded response from the routing server.

        Raises:
            ValueError: If there is no valid response or if geometry decoding fails.
        """
        if isinstance(coordinates[0], numbers.Number):
            coordinates = [coordinates]
        params = {
            "number": number
        }

        url = self._build_request("nearest", ";".join([f"{coord[1]},{coord[0]}" for coord in coordinates]))
        return self._decode_response(
            self.session.get(url, params=params, timeout=self.timeout), "nearest", params
        )

    def route(
        self,
        coordinates,
        steps: bool = False,
        overview: str = "simplified",
        geometry: str = "polyline",
        annotations: Union[bool,str] = False,
        alternatives: Union[bool,int] = False,
        continue_straight: Union[str, bool] = "default",
        waypoints: list = None,
    ) -> dict:
        """
        Calculates the route between the given coordinates.

        Args:
            coordinates : The input coordinates.
            steps (bool): Returned route steps for each route leg. Defaults to False.
            overview (str): The level of overview geometry to be returned. Defaults to "simplified".
            geometry (str): The type of geometry to use in the response. Defaults to "polyline".
            annotations (bool or str): Whether to include additional metadata in the response. Defaults to False.
            alternatives (bool or int): Whether to compute alternative routes. Defaults to False.
            continue_straight (str or bool): Forces the route to keep going straight at waypoints constraining uturns there even if it would be faster. Defaults to "default".
            waypoints (list): Optional waypoints to include in the route.

        Returns:
            dict: The decoded response from the routing server.

        Raises:
            ValueError: If there is no valid response or if geometry decoding fails.
        """
        params = {
            "steps": self._encode_val(steps),
            "overview": overview,
            "geometries": geometry,
            "annotations": self._encode_val(annotations),
            "continue_straight": self._encode_val(continue_straight),
            "alternatives": self._encode_val(alternatives),
            "waypoints": waypoints,
        }

        url = self._build_request("route", ";".join([f"{coord[1]},{coord[0]}" for coord in coordinates]))
        return self._decode_response(
            self.session.get(url, params=params, timeout=self.timeout), "route", params
        )
