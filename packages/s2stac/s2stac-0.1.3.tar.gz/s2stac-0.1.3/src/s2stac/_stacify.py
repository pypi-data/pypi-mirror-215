import pystac
from pathlib import Path
import xarray as xr
import stackstac
import numpy as np
from typing import Literal

from s2stac._catalog import create_stac_catalog


def stacify(
    safe_folders: list[Path],
    catalog_folder: Path | None = None,
    # Include flags
    include_img_data: bool = True,
    include_qi_data: bool = False,
    include_aux_data: bool = False,
    include_footprint: bool = False,
    include_cloud_proba: bool = False,
    include_ecmwf: bool = False,
    include_mtd_tl: bool = False,
    include_srtm: bool = False,
    usgs_password: str | None = None,
    usgs_username: str | None = None,
    # Stackstac parameters
    epsg: int | None = None,
    chunksize: int
    | Literal["auto"]
    | str
    | None
    | tuple[int | Literal["auto"] | str | None, ...]
    | dict[int, int | Literal["auto"] | str | None] = 1024,
    **kwargs,
) -> pystac.Catalog:
    catalog = create_stac_catalog(
        safe_folders=safe_folders,
        catalog_folder=catalog_folder,
        include_img_data=include_img_data,
        include_qi_data=include_qi_data,
        include_aux_data=include_aux_data,
        include_footprint=include_footprint,
        include_cloud_proba=include_cloud_proba,
        include_ecmwf=include_ecmwf,
        include_mtd_tl=include_mtd_tl,
        include_srtm=include_srtm,
        usgs_username=usgs_username,
        usgs_password=usgs_password,
    )
    items = list(catalog.get_all_items())

    if len(set(item.properties["proj:epsg"] for item in items)) > 1 and epsg is None:
        epsg = items[0].properties["proj:epsg"]
    stack = stackstac.stack(items, epsg=epsg, chunksize=chunksize, **kwargs)

    # Turn no data (0) into NaNs
    stack = xr.where(stack, stack, np.nan)
    return stack
