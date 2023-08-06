from tempfile import TemporaryDirectory
import rioxarray
import rioxarray.merge
from shapely.geometry import Polygon
import xarray as xr
import requests
from lxml.html.soupparser import fromstring
import geopandas as gpd
from pathlib import Path
import pystac
from pystac.extensions.eo import Band

from ._asset import add_asset


SRMT_DATASET_ID = "5e83a43c37d31d83"


def download_product(
    session: requests.Session,
    product_url: str,
    output_file: Path,
) -> Path:
    """Download SRTM product

    This function handles the download of the product given by the
    url specified using the provided session.
    The result is stored in the provided Path.

    Parameters
    ----------
    session: requests.Session
        The requests Session object used to establish the connection on the USGS platform.
    product_url: str
        The URL to fetch the product from.
    output_file: Path
        The Path to store the downloaded product.

    Returns
    -------
    output_file: Path
        The Path where the output product is located.
    """
    headers = session.get(product_url, stream=True).headers
    size = 0 if "Content-length" not in headers else int(headers["Content-length"])

    # print(output_file)
    chunk_size = int(2**20)
    with session.get(product_url, stream=True) as r:
        r.raise_for_status()
        with open(output_file, "wb") as f:
            cumul = 0
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                cumul += chunk_size
                print(f"Writting {chunk_size}, {cumul} of {size}")
    return output_file


def download_srtm_from_usgs_with_gdf(
    roi_gdf: gpd.GeoDataFrame,
    usgs_username: str,
    usgs_password: str,
    tmp_folder: Path | None = None,
    shape: tuple | None = None,
) -> xr.DataArray:
    """Download SRTM data with GDF

    Download SRTM data using the provided GeoDataFrame as the area of interest to cover.
    This function returns the DataArray of the result, the downloaded data is stored
    into a temporary folder and may be discarded later.

    Parameters
    ----------
    roi_gdf: gpd.GeoDataFrame
        The GeoDataFramespecifying the ROI to cover.
    usgs_username: str
        The username to use to access the USGS data.
    usgs_password: str
        The password to use to access the USGS data.
    tmp_folder: Path | None
        The temporary folder to store individualy downloaded tiles.
    shape: tuple
        The output shape of the result.

    Results
    -------
    out_da: xr.DataArray
        The output SRTM DataArray covering the ROI in the GDF.
    """
    if tmp_folder is None:
        tmp_dir = TemporaryDirectory()
        tmp_folder = Path(tmp_dir.name)

    roi_polygon = roi_gdf.to_crs("4326").dissolve().geometry[0].convex_hull

    # Create a requests session and access the login page of USGS
    session = requests.session()
    c = session.get(
        "https://ers.cr.usgs.gov/login/?redirectUrl=https://earthexplorer.usgs.gov/"
    ).content.decode()
    tree = fromstring(c)

    # Save the csrf values, which prevents "Man in the middle attacks"
    # Then connects
    csrf = tree.xpath("/html/body/div/div[2]/form/input[1]")[0].attrib["value"]
    url_post = "https://ers.cr.usgs.gov/login"
    login_data = {"username": usgs_username, "password": usgs_password, "csrf": csrf}
    r = session.post(url_post, data=login_data)

    # Get to the geoportal
    url_post = "https://earthexplorer.usgs.gov/"
    r = session.post(url_post)

    # Post the area to search
    url_post = "https://earthexplorer.usgs.gov/tabs/save"
    data = {
        "data": (
            '{"tab":1,"destination":4,"coordinates":['
            + ",".join(
                [
                    "{" + f'"c":"0","a":"{y}","o":"{x}"' + "}"
                    for i, (x, y) in enumerate(
                        list(roi_polygon.convex_hull.exterior.coords)[:-1]
                    )
                ]
            )
            + "],"
            + '"format":"dms","dStart":"","dEnd":"",'
            + '"searchType":"Std","includeUnknownCC":"1","maxCC":100,"minCC":0,'
            + '"months":["","0","1","2","3","4","5","6","7","8","9","10","11"],'
            + '"pType":"polygon"}'
        )
    }
    r = session.post(url_post, data=data)

    # Access only SRTM products
    url_post = "https://earthexplorer.usgs.gov/tabs/save"
    data = {"tab": 2, "destination": 4, "cList": ["5e83a43c37d31d83"], "selected": 0}
    r = session.post(url_post, data=data)

    # Trigger the actual search
    url_post = "https://earthexplorer.usgs.gov/scene/search"
    data = {"datasetId": SRMT_DATASET_ID, "resultsPerPage": 10}
    r = session.post(url_post, data=data)
    c = r.content.decode()
    tree = fromstring(c)

    product_name_to_url_map = dict()
    for item in tree.find("table").find("tbody").getchildren():
        product_name = item.attrib["data-orderingid"]
        url_post = (
            f"https://earthexplorer.usgs.gov/scene/downloadoptions/"
            f"{SRMT_DATASET_ID}/{product_name}"
        )
        print(url_post)
        while 1:
            r = session.post(url_post)
            print(r)
            c = r.content.decode()
            tree = fromstring(c)
            if len(tree.findall("body")) == 0:
                break
            else:
                print("retrying...")

        product_id = tree.xpath(".//div[@class = 'downloadButtons']")[2][0].attrib[
            "data-productid"
        ]

        product_url = (
            f"https://earthexplorer.usgs.gov/download/{product_id}/{product_name}/"
        )
        product_name_to_url_map[product_name] = product_url

    # Download all
    product_paths = []
    for product_name, product_url in product_name_to_url_map.items():
        product_path = tmp_folder / f"{product_name}.tiff"
        product_paths.append(product_path)
        download_product(
            product_url=(
                "https://earthexplorer.usgs.gov/download/"
                f"{product_id}/{product_name}/"
            ),
            session=session,
            output_file=product_path,
        )

    product_das = [
        rioxarray.open_rasterio(product_path) for product_path in product_paths
    ]

    xmin, ymin, xmax, ymax = roi_gdf.total_bounds
    out_da = (
        rioxarray.merge.merge_arrays(product_das)
        .squeeze()
        .rio.clip_box(
            minx=xmin,
            miny=ymin,
            maxx=xmax,
            maxy=ymax,
            crs=roi_gdf.crs,
        )
        .rio.reproject(
            roi_gdf.crs,
            shape=shape,
        )
    )
    return out_da


def download_srtm_from_usgs_with_da(
    target_da: xr.DataArray,
    usgs_username: str,
    usgs_password: str,
    tmp_folder: Path | None = None,
) -> xr.DataArray:
    """Download SRTM data with a DataArray

    Download SRTM data using the provided DataArray as the area of interest to cover.
    This function returns the DataArray of the result, the downloaded data is stored
    into a temporary folder and may be discarded later.
    This function mostly just forwards its arguments to
    :func:`~s2stac._srtm.download_srtm_from_usgs_with_da`. It merely handles
    the GeoDataFrame creation from the DataArray provided.

    Parameters
    ----------
    target_da: xr.DataArray
        The DataArray specifying the ROI to cover.
    usgs_username: str
        The username to use to access the USGS data.
    usgs_password: str
        The password to use to access the USGS data.
    tmp_folder: Path | None
        The temporary folder to store individualy downloaded tiles.

    Results
    -------
    out_da: xr.DataArray
        The output SRTM DataArray covering the ROI in the GDF.
    """
    xmin, ymin, xmax, ymax = target_da.rio.bounds()
    roi_gdf = gpd.GeoDataFrame(
        geometry=[Polygon([(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)])],
        crs=target_da.rio.crs,
    )
    return download_srtm_from_usgs_with_gdf(
        roi_gdf=roi_gdf,
        usgs_username=usgs_username,
        usgs_password=usgs_password,
        tmp_folder=tmp_folder,
        bounds=target_da.rio.bounds(),
        shape=target_da.shape[-2:],
    )


def add_srtm(
    item: pystac.Item,
    srtm_label: str,
    target_da: xr.DataArray,
    tmp_folder: Path,
    usgs_password: str,
    usgs_username: str,
) -> list[Band]:
    """ "Add SRTM asset"""
    srtm_path = tmp_folder / f"{srtm_label}.tiff"
    if srtm_path.exists():
        srtm_da = rioxarray.open_rasterio(srtm_path)
    else:
        srtm_da = download_srtm_from_usgs_with_da(
            target_da=target_da,
            usgs_password=usgs_password,
            usgs_username=usgs_username,
        )
        srtm_da.rio.to_raster(srtm_path)

    return [
        add_asset(
            item=item,
            asset_path=srtm_path,
            asset_label=srtm_label,
            asset_description=srtm_label,
            asset_common_name=srtm_label,
            asset_nodata=0,
            asset_epsg=f"EPSG:{srtm_da.rio.crs.to_epsg()}",
            asset_geometry=item.geometry,
            asset_bbox=item.bbox,
            asset_shape=srtm_da.shape[-2:],
            asset_transform=list(srtm_da.rio.transform()),
        )
    ]
