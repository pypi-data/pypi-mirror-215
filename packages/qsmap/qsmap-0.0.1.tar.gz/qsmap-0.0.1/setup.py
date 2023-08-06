import setuptools

setuptools.setup(
    name = 'qsmap', 
    packages = ['qsmap'],
    version='0.0.1',
    author='Yaroslav Mavliutov',
    author_email='yaroslavm@questarauto.com',
    description = 'Package provides functionality for working with geographical data, routing, and mapping',
    url='https://github.com/saferide-tech/QuestarMap',
    license='MIT',
    keywords = ['geo', 'routing', 'mapping'],
    install_requires=[
        'folium==0.14.0',
        'numpy==1.25.0',
        'overpy==0.6',
        'pandas==2.0.2',
        'polyline==2.0.0',
        'pyspark==3.4.0',
        'Requests==2.31.0'
      ],
)