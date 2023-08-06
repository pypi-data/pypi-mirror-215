import setuptools

setuptools.setup(
    name = 'qsmap', 
    packages = ['qsmap'],
    version='0.0.2',
    author='Yaroslav Mavliutov',
    author_email='yaroslavm@questarauto.com',
    description = 'Package provides functionality for working with geographical data, routing, and mapping',
    url='https://github.com/saferide-tech/QuestarMap',
    license='MIT',
    keywords = ['geo', 'routing', 'mapping'],
    install_requires=[
        'folium==0.14.0',
        'numpy',
        'overpy==0.6',
        'pandas',
        'polyline==2.0.0',
        'pyspark',
        'Requests==2.31.0'
      ],
)