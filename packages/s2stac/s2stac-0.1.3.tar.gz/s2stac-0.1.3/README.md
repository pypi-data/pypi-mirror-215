# s2stac

Easily access many Sentinel-2 safe folders from a convenient xarray DataArray.

## Purpose

The purpose of this library is to create on-the-fly STAC from a list Sentinel-2 products in the form of SAFE folders and provide a xarray DataArray to easily access the main Sentinel-2 bands and more!

Accessible information includes:
- all bands from the IMG_DATA folder (B01, B02, ..., B11)
- all viewing/sun zenith/azimuth angles.
- all detector footprints (for each band)
- ECMWF data (msl, tco3, ...)

## How it works

s2stac uses the stackstac library internally to interogate a static STAC database created on the fly with pystac.
The database can be persisted so the user does not need to build it everytime.

## Installation

This library requires Python 3.10 or higher.

This library also requires the eccodes library (version 2.16.0) to be able to parse the GRIB ECMWF DataArray containing the meteorological data associated with each tile.
You can install it on Ubuntu with the following command:
```bash
sudo apt-get install libeccodes-dev
```

On MacOs you will need to do:

```bash
brew install eccodes
```

Now you can simply install s2stac with:
```bash
pip install s2stac
```

On MacOs you will also need to install *ecmfwlibs*:
```bash
pip install ecmwflibs
```

## Usage

It is very easy to load some SAFE folders into a DataArray.
Here we import 5 SAFE folders of imagery taken over the south of Finland.

```python
from pathlib import Path
from s2stac import stacify

safe_folders = list(Path("/path/to/your/safe/folders").glob("*.SAFE"))

stack = stacify(safe_folders)
stack
```
![DataArray](./res/exemple_output_dataarray.png)

To preview the result, you can use the preview function from the s2stac module:

```python
from s2stac import preview

preview(stack)
```
![Preview](res/exemple_output_rgb_plot.png)


This preview function only displays a small collage of bands B04, B03 and B02 (RGB).

Many other bands are available, here are a few more:

![Preview](res/exemple_bands_available.png)


From there, you can use all the convenient methods offered by xarray to manipulate DataArrays.

```bash
stack.sel(band=["B02", "B08", "B11"]).loc[:,:,::4,::4].mean("time").plot.imshow(col="band")
```
![Plot a few bands per columns](res/exemple_output_col_plot.png)


## Extra

A few extra more options have been added to s2stac that are not considered to be part of the expected functionnalities.

One of them is the ability to retrieve DEM (digital elevation models) data from [USGS](https://www.usgs.gov/) (United States Geological Survey).

The [SRTM](https://www.usgs.gov/centers/eros/science/usgs-eros-archive-digital-elevation-shuttle-radar-topography-mission-srtm) asset can be downloaded by specifying in the *stacify* function the intent to download such imagery as well as username and password.

Here's a small demo of it in action, using imagery taken over Guadeloupe:

```python
from s2stac import stacify,preview
from pathlib import Path
import matplotlib.pyplot as plt
    

safe_folders = list(
    Path("/path/to/safe/folders").glob("*.SAFE")
)[:2]

usgs_username = "<your USGS username>"
usgs_password = "<your USGS password>"

stack = stacify(
    safe_folders,
    include_aux_data=False,
    include_ecmwf=False,
    include_footprint=False,
    include_mtd_tl=False,
    include_qi_data=False,
    include_srtm=True,
    usgs_password=usgs_password,
    usgs_username=usgs_username,
    catalog_folder=Path("./out"),
)


fig,ax = plt.subplots(1, 2)

stack.sel(band="srtm").mean("time").plot.imshow(ax=ax[0])
(stack.sel(band=["B04", "B03", "B02"]).loc[:,:,::4,::4].mean("time") / 10_000).plot.imshow(ax=ax[1])
ax[0].set_aspect("equal")
ax[1].set_aspect("equal")
```

![SRTM preview](res/exemple_srtm_result.png)




## License

MIT


## Author

Pierre Louvart - plouvart@argans.eu

## Credit

gjoseph92, the creator of [https://stackstac.readthedocs.io/en/latest/](stackstac)

