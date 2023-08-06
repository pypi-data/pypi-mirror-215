# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['s2stac']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.12.2,<5.0.0',
 'bokeh==2.4.2',
 'cfgrib>=0.9.10.3,<0.10.0.0',
 'dask>=2023.5.0,<2024.0.0',
 'distributed>=2023.5.0,<2024.0.0',
 'eccodes==1.2.0',
 'geopandas>=0.13.0,<0.14.0',
 'jinja2==3.0.3',
 'lxml>=4.9.2,<5.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.3,<2.0.0',
 'pygeoapi>=0.14.0,<0.15.0',
 'pygrib>=2.1.4,<3.0.0',
 'pystac-client>=0.6.1,<0.7.0',
 'pystac>=1.7.3,<2.0.0',
 'rasterio>=1.3.6,<2.0.0',
 'rioxarray>=0.14.1,<0.15.0',
 'shapely==1.8.5',
 'stackstac>=0.4.3,<0.5.0',
 'xarray>=2023.4.2,<2024.0.0']

setup_kwargs = {
    'name': 's2stac',
    'version': '0.1.3',
    'description': 'Create a STAC from local S2 data.',
    'long_description': '# s2stac\n\nEasily access many Sentinel-2 safe folders from a convenient xarray DataArray.\n\n## Purpose\n\nThe purpose of this library is to create on-the-fly STAC from a list Sentinel-2 products in the form of SAFE folders and provide a xarray DataArray to easily access the main Sentinel-2 bands and more!\n\nAccessible information includes:\n- all bands from the IMG_DATA folder (B01, B02, ..., B11)\n- all viewing/sun zenith/azimuth angles.\n- all detector footprints (for each band)\n- ECMWF data (msl, tco3, ...)\n\n## How it works\n\ns2stac uses the stackstac library internally to interogate a static STAC database created on the fly with pystac.\nThe database can be persisted so the user does not need to build it everytime.\n\n## Installation\n\nThis library requires Python 3.10 or higher.\n\nThis library also requires the eccodes library (version 2.16.0) to be able to parse the GRIB ECMWF DataArray containing the meteorological data associated with each tile.\nYou can install it on Ubuntu with the following command:\n```bash\nsudo apt-get install libeccodes-dev\n```\n\nOn MacOs you will need to do:\n\n```bash\nbrew install eccodes\n```\n\nNow you can simply install s2stac with:\n```bash\npip install s2stac\n```\n\nOn MacOs you will also need to install *ecmfwlibs*:\n```bash\npip install ecmwflibs\n```\n\n## Usage\n\nIt is very easy to load some SAFE folders into a DataArray.\nHere we import 5 SAFE folders of imagery taken over the south of Finland.\n\n```python\nfrom pathlib import Path\nfrom s2stac import stacify\n\nsafe_folders = list(Path("/path/to/your/safe/folders").glob("*.SAFE"))\n\nstack = stacify(safe_folders)\nstack\n```\n![DataArray](./res/exemple_output_dataarray.png)\n\nTo preview the result, you can use the preview function from the s2stac module:\n\n```python\nfrom s2stac import preview\n\npreview(stack)\n```\n![Preview](res/exemple_output_rgb_plot.png)\n\n\nThis preview function only displays a small collage of bands B04, B03 and B02 (RGB).\n\nMany other bands are available, here are a few more:\n\n![Preview](res/exemple_bands_available.png)\n\n\nFrom there, you can use all the convenient methods offered by xarray to manipulate DataArrays.\n\n```bash\nstack.sel(band=["B02", "B08", "B11"]).loc[:,:,::4,::4].mean("time").plot.imshow(col="band")\n```\n![Plot a few bands per columns](res/exemple_output_col_plot.png)\n\n\n## Extra\n\nA few extra more options have been added to s2stac that are not considered to be part of the expected functionnalities.\n\nOne of them is the ability to retrieve DEM (digital elevation models) data from [USGS](https://www.usgs.gov/) (United States Geological Survey).\n\nThe [SRTM](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-shuttle-radar-topography-mission-srtm) asset can be downloaded by specifying in the *stacify* function the intent to download such imagery as well as username and password.\n\nHere\'s a small demo of it in action, using imagery taken over Guadeloupe:\n\n```python\nfrom s2stac import stacify,preview\nfrom pathlib import Path\nimport matplotlib.pyplot as plt\n    \n\nsafe_folders = list(\n    Path("/path/to/safe/folders").glob("*.SAFE")\n)[:2]\n\nusgs_username = "<your USGS username>"\nusgs_password = "<your USGS password>"\n\nstack = stacify(\n    safe_folders,\n    include_aux_data=False,\n    include_ecmwf=False,\n    include_footprint=False,\n    include_mtd_tl=False,\n    include_qi_data=False,\n    include_srtm=True,\n    usgs_password=usgs_password,\n    usgs_username=usgs_username,\n    catalog_folder=Path("./out"),\n)\n\n\nfig,ax = plt.subplots(1, 2)\n\nstack.sel(band="srtm").mean("time").plot.imshow(ax=ax[0])\n(stack.sel(band=["B04", "B03", "B02"]).loc[:,:,::4,::4].mean("time") / 10_000).plot.imshow(ax=ax[1])\nax[0].set_aspect("equal")\nax[1].set_aspect("equal")\n```\n\n![SRTM preview](res/exemple_srtm_result.png)\n\n\n\n\n## License\n\nMIT\n\n\n## Author\n\nPierre Louvart - plouvart@argans.eu\n\n## Credit\n\ngjoseph92, the creator of [https://stackstac.readthedocs.io/en/latest/](stackstac)\n\n',
    'author': 'Pierre Louvart',
    'author_email': 'pierre.louvart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.5,<3.12',
}


setup(**setup_kwargs)
