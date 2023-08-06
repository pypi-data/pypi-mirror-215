import folium

tiles_cfg = {
    "Klokantech Basic": 'https://map-tile.ds.questarauto.com/styles/klokantech-basic/{z}/{x}/{y}.png',
    "OSM Bright": 'https://map-tile.ds.questarauto.com/styles/osm-bright/{z}/{x}/{y}.png',
    "OpenStreetMap": "OpenStreetMap",
    "Stamen Terrain": "Stamen Terrain",
    "Stamen Toner": "Stamen Toner",
    "Stamen Watercolor": "Stamen Watercolor",
    "CartoDB positron": "CartoDB positron",
    "CartoDB dark_matter": "CartoDB dark_matter"
}

class TileServerEndpoint:
    def __init__(self, default_tiles: str = "OpenStreetMap"):
        """
        Initializes a TileServerEndpoint object.

        Args:
            default_tiles (str): The default tile server to use. Defaults to "OpenStreetMap".
        """
        self.default_tiles = default_tiles

    def create_tile(
        self,
        tiles: str = None,
        location: list[float] = [31.4117, 35.0818],
        zoom_start: float = 9.0,
        **kwargs
    ) -> folium.Map:
        """
        Creates a tile map using Folium library.

        Args:
            tiles (str): The tile server to use. Defaults to None, which uses the default_tiles value.
            location (list[float]): The geographic coordinates of the center of the map. Defaults to [31.4117, 35.0818] (Israel).
            zoom_start (float): The initial zoom level of the map. Defaults to 9.0.
            **kwargs: Additional keyword arguments accepted by the folium.Map function.

        Returns:
            folium.Map: A Folium map object.

        Raises:
            Exception: If the specified tiles server is not found in tiles_cfg dictionary.
            Exception: If any unexpected error occurs during map creation.
        """
        if tiles is None:
            tiles = self.default_tiles
        try:
            tile_url = tiles_cfg.get(tiles)
            if tile_url is None:
                raise Exception(f"Error: No {tiles} tile to use")
            return folium.Map(
                tiles=tile_url,
                attr=tiles,
                location=location,
                zoom_start=zoom_start,
                **kwargs
            )
        except Exception as err:
            raise Exception(f"Unexpected error during map creation: {err}")