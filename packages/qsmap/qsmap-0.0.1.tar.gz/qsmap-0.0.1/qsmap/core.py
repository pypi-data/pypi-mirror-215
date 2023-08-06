import enum
import numpy as np
import pandas as pd
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import udf, lit
import pyspark.sql.functions as F
from pyspark.sql.types import StructType, StructField, ArrayType, DoubleType, StringType, MapType
from typing import Any, Dict, List, Optional, Union, Tuple
from statistics import mean
import folium
import numbers

from .elevation import ElevationServerEndpoint
from .overpass import OverpassServerEndpoint
from .tile import TileServerEndpoint
from .routing import RoutingServerEndpoint,response_keys_cfg

class ServiceType(enum.Enum):
    """
    Enum class representing different service types.
    """
    tile = "tile"
    route = "route"
    tags = "tags"
    elevation = "elevation"

    @classmethod
    def isService(cls, value: str) -> bool:
        """
        Check if the given value is a valid service type.

        Args:
            value: The value to check.

        Returns:
            True if the value is a valid service type, False otherwise.
        """
        return value in cls._value2member_map_
    
host_cfg={
    "public": {
        ServiceType.tile.value: "OpenStreetMap",
        ServiceType.route.value: "http://router.project-osrm.org",
        ServiceType.tags.value: "http://overpass-api.de/api/interpreter",
        ServiceType.elevation.value: "https://api.opentopodata.org"
    },
    "private": {
        ServiceType.tile.value: "OSM Bright",
        ServiceType.route.value: "https://map-routing.ds.questarauto.com",
        ServiceType.tags.value: "https://map-overpass.ds.questarauto.com/api/interpreter",
        ServiceType.elevation.value: "https://map-elevation.ds.questarauto.com"
    }
}

col_name_cgf={
    'outputCol':'outputCol',
    'outputLatCol': 'outputLatCol',
    'outputLonCol': 'outputLonCol',
    'outputElevCol': 'outputElevCol',
    'inputLatLocCol': 'inputLatLocCol'
}



class QMap:
    """
    Class representing a QMap object.
    """

    WAY_TAGS = [
        "highway", "oneway", "lanes", "maxspeed", "access", "tunnel",
        "bridge", "route", "width", "traffic_sign", "traffic_signals"
    ]
    OPTIMIZE_TAGS_SEARCHING = True
    TAG_SEQ_PRECISION = 0.1

    def __init__(self, api: str = "private"):
        """
        Initialize a QMap object.

        Args:
            api: The API to use ("public" or "private").
        """
        assert api in host_cfg.keys(), "The value of \"api\" parameter must be either \"public\" or \"private\""
        self.services = {}
        self._registerAll(host_cfg[api])

    def service(self, service: str):
        """
        Get the service object associated with the specified service type.

        Args:
            service: The service type.

        Returns:
            The service object associated with the specified service type.
        """
        assert ServiceType.isService(service), f"No service {service} to use"
        return self.services[service]

    def _registerAll(self, hosts):
        """
        Register all service endpoints using the provided hosts.

        Args:
            hosts: The host configuration for different services.
        """
        self.services[ServiceType.tile.value] = TileServerEndpoint(default_tiles=hosts[ServiceType.tile.value])
        self.services[ServiceType.route.value] = RoutingServerEndpoint(host=hosts[ServiceType.route.value])
        self.services[ServiceType.tags.value] = OverpassServerEndpoint(host=hosts[ServiceType.tags.value])
        self.services[ServiceType.elevation.value] = ElevationServerEndpoint(host=hosts[ServiceType.elevation.value])

    def _process_input(self, data, input_col_name, func, udf_structure, **args):
        """
        Process the input data based on its type and perform the specified function.

        Args:
            data: The input data.
            input_col_name: The input column name.
            func: The function to be applied.
            udf_structure: The structure of the user-defined function (UDF).
            **args: Additional arguments for the function.

        Returns:
            The processed data.
        """
        if not isinstance(udf_structure, list):
            udf_structure = [udf_structure]
        
        if isinstance(data, list):
            list_dim = lambda x: list_dim(x[0]) + 1 if isinstance(x[0], list) else 1
            if list_dim(data) == 3:
                return [func(coords, **args) for coords in data]
            else:
                return func(data, **args)
        
        if isinstance(data, np.ndarray):
            if len(data.shape) == 3:
                return np.array([func(coords, **args) for coords in data])
            else:
                return func(data, **args)
        
        if isinstance(data, pd.DataFrame):
            if isinstance(input_col_name, list):
                df, meta = self._process_output(func(data[input_col_name].values, **args))
                if meta is None:
                    return df
                else:
                    return df, meta
            data[col_name_cgf['outputCol']] = data[input_col_name].apply(lambda x: func(x, **args))
            return data
        
        if isinstance(data, DataFrame):
            if isinstance(input_col_name, list):
                df, meta = self._process_output(func(data.select(*input_col_name).toPandas().values, **args))
                if meta is None:
                    return SparkSession.builder.getOrCreate().createDataFrame(df)
                else:
                    return SparkSession.builder.getOrCreate().createDataFrame(df), meta
            converted_args = {key: lit(value) for key, value in args.items()}
            _udf = udf(func, udf_structure[0] if not args.get("details", False) else udf_structure[1])
            if args.get("details", False) and (isinstance(self.WAY_TAGS, str)):
                raise Exception(f"Error: WAY_TAGS cannot be {self.WAY_TAGS} saving tag values to pyspark dataframe. Please assign a list of tags you want to get")
            return data.withColumn(col_name_cgf['outputCol'], _udf(*[input_col_name, *list(converted_args.values())]))
        
        raise Exception(f"Unknown type {type(data)} of input data")

    def _process_output(self, data):
        """
        Process the output data.

        Args:
            data: The input data.

        Returns:
            The processed data and metadata (if available).
        """
        if isinstance(data, dict):
            coordinates = np.concatenate((np.array(data["coordinates"]), np.array(data["elevation"])[:, np.newaxis]), axis=1)
            columns = [col_name_cgf['outputLatCol'], col_name_cgf['outputLonCol'], col_name_cgf['outputElevCol']]
            meta = {'distance': data['distance'], 'duration': data['duration'], 'speed': data['speed'], 'tags': data['tags']}
            return pd.DataFrame(coordinates, columns=columns), meta
        else:
            columns = [col_name_cgf['outputLatCol'], col_name_cgf['outputLonCol']]
            return pd.DataFrame(np.array(data), columns=columns), None

    def _concat_columns(self, data, input_col_name):
        """
        Concatenate columns in the data based on the input column name.

        Args:
            data: The input data.
            input_col_name: The input column name.

        Returns:
            The concatenated data and updated input column name.
        """
        if isinstance(data, pd.DataFrame):
            data[col_name_cgf['inputLatLocCol']], input_col_name = data[input_col_name].values.tolist(), col_name_cgf['inputLatLocCol']
        elif isinstance(data, DataFrame):
            data, input_col_name = data.withColumn(col_name_cgf['inputLatLocCol'], F.array(F.col(input_col_name[0]).cast("float"), F.col(input_col_name[1]).cast("float"))), col_name_cgf['inputLatLocCol']
        return data, input_col_name

    def _three2two_dim(self, coordinates):
        """
        Convert three-dimensional coordinates to two-dimensional.

        Args:
            coordinates: The input coordinates.

        Returns:
            The two-dimensional coordinates.
        """
        if np.array(coordinates).shape[-1] == 3:
            return np.array(coordinates)[:, :2].tolist()
        return coordinates

    def _get_step_skip_nodes(self, nodes):
        """
        Get the step skip value based on the number of nodes.

        Args:
            nodes: The input nodes.

        Returns:
            The step skip value.
        """
        if self.OPTIMIZE_TAGS_SEARCHING:
            l = len(nodes)
            if l <= 10:
                return 1
            elif l <= 30:
                return 2
            elif l <= 100:
                return 3
            elif l <= 200:
                return 4
            elif l <= 300:
                return 6
            else:
                return np.ceil(sum(np.log([(l // pow(10, i)) + 1 for i, e in enumerate(str(l))])))
        else:
            return 1

    def _node2way(self, nodes):
        """
        Convert nodes to ways.

        Args:
            nodes: The input nodes.

        Returns:
            The converted ways.
        """
        response = []
        div = self._get_step_skip_nodes(nodes)
        for i, n in enumerate(nodes):
            if i % div == 0:
                response.append(self.services[ServiceType.tags.value].query(f"""node({n});<;out;""").way_ids)

        temp_way_list = set(response[0])
        final_way_list = []
        counter = {n: 1 for n in temp_way_list}

        if self.TAG_SEQ_PRECISION == 0:
            threshold = 1
        elif self.TAG_SEQ_PRECISION == 1:
            threshold = len(response)
        else:
            threshold = int(len(response) * self.TAG_SEQ_PRECISION)
        
        for i, sublist in enumerate(response[1:]):
            temp_way_list = temp_way_list.intersection(sublist)
            if not temp_way_list:
                temp_way_list = set(sublist)
                continue
            for n in temp_way_list:
                if n in counter.keys():
                    counter[n] = counter[n] + 1
                else:
                    counter[n] = 2
            final_way_list.extend(temp_way_list)
        
        return [n for n in list(dict.fromkeys(final_way_list)) if counter[n] > threshold]
    
    def _filter_keys(self, d):
        """
        Filter keys in a dictionary based on WAY_TAGS.

        Args:
            d: The input data.

        Returns:
            The filtered data based on WAY_TAGS.
        """
        if isinstance(self.WAY_TAGS, str):
            if self.WAY_TAGS == "all":
                return d
            else:
                raise Exception(f"Error: Unknown WAY_TAGS={self.WAY_TAGS}")
        elif isinstance(self.WAY_TAGS, list):
            return {key: d.get(key, "None") for key in self.WAY_TAGS}
        else:
            raise Exception(f"Error: Unknown WAY_TAGS={self.WAY_TAGS}")

    def _way2tag(self, ways: list) -> list:
        """
        Get tags from ways.

        Args:
            ways: The input ways.

        Returns:
            The list of tags for each way.
        """
        tags = []
        for w in ways:
            tags.append(self._filter_keys(self.services[ServiceType.tags.value].query(f"""way({w});out tags;""").ways[0].tags))
            tags[-1]["way_id"] = w
        return tags

    def _json2coords(self, response: Dict[str, Any], service: str, match_is_cut: bool) -> List[List[Union[float, int]]]:
        """
        Extract coordinates from the JSON response.

        Args:
            response: The JSON response.
            service: The service name.
            match_is_cut: Indicates if the match is cut.

        Returns:
            The list of coordinates.
        """
        try:
            if match_is_cut:
                return [item for sublist in response[response_keys_cfg[service]] for item in sublist['geometry']['coordinates']]
            else:
                return response[response_keys_cfg[service]][0]['geometry']['coordinates']
        except:
            print("Coordinates were not found")
            return [[]]

    def _json2distance(self, response: Dict[str, Any], service: str, match_is_cut: bool) -> Union[float, int]:
        """
        Extract distance from the JSON response.

        Args:
            response: The JSON response.
            service: The service name.
            match_is_cut: Indicates if the match is cut.

        Returns:
            The distance value.
        """
        try:
            if match_is_cut:
                return sum([sublist['distance'] for sublist in response[response_keys_cfg[service]]])
            else:
                return response[response_keys_cfg[service]][0]['distance']
        except:
            print("Distance was not found")
            return -1

    def _json2duration(self, response: Dict[str, Any], service: str, match_is_cut: bool) -> Union[float, int]:
        """
        Extract duration from the JSON response.

        Args:
            response: The JSON response.
            service: The service name.
            match_is_cut: Indicates if the match is cut.

        Returns:
            The duration value.
        """
        try:
            if match_is_cut:
                return sum([sublist['duration'] for sublist in response[response_keys_cfg[service]]])
            else:
                return response[response_keys_cfg[service]][0]['duration']
        except:
            print("Duration was not found")
            return -1

    def _json_parse_annots(self, response: Dict[str, Any], service: str, match_is_cut: bool) -> Tuple[float, List[Any]]:
        """
        Parse annotations from the JSON response.

        Args:
            response: The JSON response.
            service: The service name.
            match_is_cut: Indicates if the match is cut.

        Returns:
            The mean speed and list of nodes.
        """
        nodes, speed = [], []
        try:
            for m in response[response_keys_cfg[service]]:
                lnodes, lspeeds = [], []
                for l in m["legs"]:
                    lnodes.extend(l['annotation']['nodes'])
                    lspeeds.extend(l['annotation']['speed'])
                speed.extend(lspeeds)
                nodes.extend(list(dict.fromkeys(lnodes)))
        except:
            print("Annotation was not found")
        return mean(speed), nodes

    def snap_to_road(self, data: Any, input_col_name: Optional[str] = None, tidy: bool = True, details: bool = False):
        """
        Snap the coordinates to the road.

        Args:
            data: The input data.
            input_col_name: The name of the input column.
            tidy: Indicates whether to tidy the output.
            details: Indicates whether to include detailed information.

        Returns:
            The snapped coordinates or detailed response including meta.
        """
        udf_structure = [
            ArrayType(ArrayType(DoubleType())),
            StructType([
                StructField('coordinates', ArrayType(ArrayType(DoubleType()))),
                StructField('distance', DoubleType()),
                StructField('duration', DoubleType()),
                StructField('speed', DoubleType()),
                StructField('tags', ArrayType(StructType([StructField(t, StringType()) for t in self.WAY_TAGS]))),
                StructField('elevation', ArrayType(DoubleType()))
            ])
        ]
        return self._process_input(data, input_col_name, self._snap_to_road, udf_structure, tidy=tidy, details=details)

    def _snap_to_road(self, coordinates, tidy: bool = False, details: bool = False) -> Any:
        """
        Internal method to snap the coordinates to the road.

        Args:
            coordinates: The input coordinates.
            tidy: Indicates whether to tidy the output.
            details: Indicates whether to include detailed information.

        Returns:
            The snapped coordinates or detailed response.
        """
        coordinates = self._three2two_dim(coordinates)
        try:
            response = self.services[ServiceType.route.value].match(coordinates=coordinates, geometry="geojson", tidy=tidy, annotations=details)
        except Exception as err:
            print(err)
            return

        match_is_cut = len(response.get(response_keys_cfg["match"], [])) > 1

        if not details:
            return self._json2coords(response, "match", match_is_cut)

        detailed_response = {}
        detailed_response['coordinates'] = self._json2coords(response, "match", match_is_cut)
        detailed_response['distance'] = self._json2distance(response, "match", match_is_cut)
        detailed_response['duration'] = self._json2duration(response, "match", match_is_cut)

        speed, nodes = self._json_parse_annots(response, "match", match_is_cut)
        detailed_response['speed'] = speed
        detailed_response['tags'] = self._way2tag(self._node2way(nodes))

        detailed_response['elevation'] = self._get_elevation(detailed_response['coordinates'])
        return detailed_response

    def find_fastest_route(self, data: Any, input_col_name: Optional[str] = None, details: bool = False) -> Any:
        """
        Find the fastest route.

        Args:
            data: The input data.
            input_col_name: The name of the input column.
            details: Indicates whether to include detailed information.

        Returns:
            The coordinates of the fastest route or detailed response.
        """
        udf_structure = [
            ArrayType(ArrayType(DoubleType())),
            StructType([
                StructField('coordinates', ArrayType(ArrayType(DoubleType()))),
                StructField('distance', DoubleType()),
                StructField('duration', DoubleType()),
                StructField('speed', DoubleType()),
                StructField('tags', ArrayType(StructType([StructField(t, StringType()) for t in self.WAY_TAGS]))),
                StructField('elevation', ArrayType(DoubleType()))
            ])
        ]
        return self._process_input(data, input_col_name, self._find_fastest_route, udf_structure, details=details)

    def _find_fastest_route(self, coordinates, details: bool = False) -> Any:
        """
        Internal method to find the fastest route.

        Args:
            coordinates: The input coordinates.
            details: Indicates whether to include detailed information.

        Returns:
            The coordinates of the fastest route or detailed response.
        """
        coordinates = self._three2two_dim(coordinates)
        try:
            response = self.services[ServiceType.route.value].route(coordinates=coordinates, geometry="geojson", annotations=details)
        except Exception as err:
            print(err)
            return

        match_is_cut = len(response.get(response_keys_cfg['route'], [])) > 1

        if not details:
            return self._json2coords(response, 'route', match_is_cut)

        detailed_response = {}
        detailed_response['coordinates'] = self._json2coords(response, 'route', match_is_cut)
        detailed_response['distance'] = self._json2distance(response, 'route', match_is_cut)
        detailed_response['duration'] = self._json2duration(response, 'route', match_is_cut)

        speed, nodes = self._json_parse_annots(response, 'route', match_is_cut)
        detailed_response['speed'] = speed
        detailed_response['tags'] = self._way2tag(self._node2way(nodes))

        detailed_response['elevation'] = self._get_elevation(detailed_response['coordinates'])

        return detailed_response

    def find_nearest_node(self, data: Any, input_col_name: Optional[str] = None, number: int = 1, details: bool = False):
        """
        Find the nearest node.

        Args:
            data: The input data.
            input_col_name: The name of the input column.
            number: The number of nearest nodes to find.
            details: Indicates whether to include detailed information.

        Returns:
            The nearest node IDs or detailed response.
        """
        udf_structure = [
            ArrayType(StringType()),
            StructType([
                StructField('node_ids', ArrayType(StringType())),
                StructField('name', ArrayType(StringType()))
            ])
        ]
        data, input_col_name = self._concat_columns(data, input_col_name)
        return self._process_input(data, input_col_name, self._find_nearest_node, udf_structure, number=number, details=details)
    
    def _find_nearest_node(self, coordinates, number: int = 1, details: bool = False) -> Any:
        """
        Internal method to find the nearest node.

        Args:
            coordinates: The input coordinates.
            number: The number of nearest nodes to find.
            details: Indicates whether to include detailed information.

        Returns:
            The nearest node IDs or detailed response.
        """
        if isinstance(coordinates[0], numbers.Number):
            coordinates = [coordinates]
        coordinates = self._three2two_dim(coordinates)
        try:
            response = self.services[ServiceType.route.value].nearest(coordinates=coordinates, number=number)
        except Exception as err:
            print(err)
            return

        nodes, names = [], []
        for m in response.get('waypoints', {}):
            nodes.append(m['nodes'])
            names.append(m['name'])

        return {"node_ids": nodes, "name": names} if details else nodes
    
    def _get_elevation(self, coordinates) -> Union[float, List[float]]:
        """
        Internal method to get the elevation.

        Args:
            coordinates: The input coordinates.

        Returns:
            The elevation value(s).
        """
        if isinstance(coordinates[0], numbers.Number):
            coordinates = [coordinates]
        coordinates = self._three2two_dim(coordinates)
        try:
            values = [e['elevation'] for e in self.services[ServiceType.elevation.value].estimate(coordinates)['results']]
            return values[0] if len(values) == 1 else values
        except Exception as err:
            print(err)
            return []
        
    def get_elevation(self, data: Any, input_col_name: Optional[Union[str, List[str]]] = None):
        """
        Get the elevation.

        Args:
            data: The input data.
            input_col_name: The name of the input column(s).

        Returns:
            The elevation value(s).
        """
        udf_structure = ArrayType(DoubleType())
        if isinstance(input_col_name, list):
            udf_structure = DoubleType()
            data, input_col_name = self._concat_columns(data, input_col_name)
        return self._process_input(data, input_col_name, self._get_elevation, udf_structure)
    
    def plot_trajectory(self, data, input_col_name: Optional[Union[str, List[str]]] = None,
                        weight: int = 4, color: str = "black", opacity: float = 0.6, popup: Any = None, tile: folium.Map = None) -> folium.Map:
        """
        Plot the trajectory.

        Args:
            data: The input data.
            input_col_name: The name of the input column(s).
            weight: The weight of the polyline.
            color: The color of the polyline.
            opacity: The opacity of the polyline.
            popup: The popup content.
            tile: The tile object.

        Returns:
            The plotted tile object.
        """
        if isinstance(data, list):
            data = np.array(data)

        if isinstance(data, DataFrame):
            data = data.toPandas()

        if isinstance(data, pd.DataFrame):
            if isinstance(input_col_name, list):
                data = data[input_col_name].values
            elif input_col_name:
                data = data[input_col_name]
            else:
                data = data.values

        if isinstance(data, np.ndarray):
            if len(data.shape) == 2:
                data = pd.Series(np.expand_dims(data, axis=0).tolist())
            data = pd.Series(data.tolist())

        data = data.apply(lambda x: self._three2two_dim(x))

        tolist = lambda x: list(x) if isinstance(x[0], numbers.Number) else [tolist(v) for v in x]

        points = []
        for p in tolist(data.values):
            points.extend(p)
        points = np.array(points).reshape(-1, 2)

        location = points.mean(axis=0).tolist()
        if not tile:
            tile = self.services[ServiceType.tile.value].create_tile(location=location)
        tile.fit_bounds([points.min(axis=0).tolist(), points.max(axis=0).tolist()])
        folium.PolyLine(data, weight=weight, color=color, opacity=opacity, popup=popup).add_to(tile)

        return tile
