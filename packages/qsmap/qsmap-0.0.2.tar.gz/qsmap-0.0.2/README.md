# qsmap Package

The qsmap package provides functionality for working with geographical data, routing, and mapping. It offers convenient methods for various operations such as snapping coordinates to roads, finding the fastest route, finding nearest nodes, and obtaining elevation data. The package utilizes different APIs to provide accurate and efficient results.

### Features
- Snapping coordinates to the nearest road
- Finding the fastest route between coordinates
- Finding the nearest nodes based on coordinates
- Obtaining elevation data for given coordinates
- Obtaining tags for given way_id (look at osm for more details)
- Plotting trajectories on interactive maps
- qsmap package allows use various types as input data, including pandas and pyspark dataframes

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install qsmap.

```bash
pip install qsmap
```

## Usage

Here are some examples of how to use QMap package:

### Snapping Coordinates to Road
```python
from qsmap import QMap

qmap = QMap()

data = [[32.005013, 34.78869], [32.005003, 34.788822], [32.004992, 34.788953], [32.004985, 34.7891]]
result = qmap.snap_to_road(data, details=True)

print(result)
```

### Finding the Fastest Route
```python
from qsmap import QMap

qmap = QMap()

data = [[32.005013, 34.78869], [32.005003, 34.788822], [32.004992, 34.788953], [32.004968, 34.790198]]
result = qmap.find_fastest_route(data)

print(result)
```

### Finding Nearest Nodes
```python
from qsmap import QMap

qmap = QMap()

data = [32.005013, 34.78869]
result = qmap.find_nearest_node(data, number=5)

print(result)
```

### Obtaining Elevation Data
```python
from qsmap import QMap

qmap = QMap()

data = [[32.005013, 34.78869], [32.005003, 34.788822], [32.004992, 34.788953]]
result = qmap.get_elevation(data)

print(result)
```

### Plotting Trajectory on Map
```python
from qsmap import QMap

qmap = QMap()

data = [[32.005013, 34.78869], [32.005003, 34.788822], [32.004992, 34.788953]]
qmap.plot_trajectory(data)
```

### Direct request from services
```python
from qsmap import QMap

qmap = QMap()

elevationS=qmap.service("elevation")
routeS=qmap.service("route")
tagS=qmap.service("tags")
tileS=qmap.service("tile")

print(elevationS.estimate(coordinates=[[32.005013, 34.78869], [32.005003, 34.788822]]))
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)