
from matplotlib import pyplot as plt
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import rasterio
from rasterio.mask import mask
from rasterio.io import MemoryFile
from glob import glob
import geopandas as gpd
from scipy.stats import skew,kurtosis

sys.path.append(os.path.realpath(__file__))

#A function to convert linux paths to windows
def convert_path(path):
    if os.name == "nt":
        return path.replace("/", "\\")
    else:
        return path

def get_clipped_chip(file_path,polygon):
      
    """
        Clips a raster image based on the provided polygon shape.

        Args:
            file_path (str): The path to the raster image file.
            polygon (shapely.geometry.Polygon): The polygon shape to clip the raster.

        Returns:
            numpy.ndarray: The clipped raster image as a NumPy array.

    """
    with rasterio.open(file_path) as src:
        out_image, out_transform = rasterio.mask.mask(src,polygon, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "count": out_image.shape[0],
                    "transform": out_transform})   

    clipped_raster=array_to_raster(out_image,out_meta)

    return clipped_raster

def array_to_raster(array,meta):
    """
    Converts a NumPy array to a rasterio object.
    
    Parameters:
        array (numpy.ndarray): The NumPy array to convert to a rasterio object.
        crs (rasterio.crs.CRS): The CRS of the raster.
        transform (affine.Affine): The geotransform of the raster.
        
    Returns:
        A rasterio DatasetReader object.
    """
    count, height, width = array.shape
    
    # Create a rasterio MemoryFile
    memfile = rasterio.MemoryFile()
    
    # Write the NumPy array to the MemoryFile
    with memfile.open(**meta) as dst:
      for i in range(count):
          dst.write(array[i,:,:], i+1)
        
    # Return a rasterio DatasetReader object
    return memfile.open()

def get_tile_transform(parent_transform, pixel_x:int,pixel_y:int):
    '''
    creating tile transform matrix from parent tif image
    '''
    crs_x = parent_transform.c + pixel_x * parent_transform.a
    crs_y = parent_transform.f + pixel_y * parent_transform.e
    tile_transform = rasterio.Affine(parent_transform.a, parent_transform.b, crs_x,
                                     parent_transform.d, parent_transform.e, crs_y)
    return tile_transform
    
def get_tile_profile(parent_tif:rasterio.io.DatasetReader, pixel_x:int, pixel_y:int):
    '''
    preparing tile profile
    '''
    tile_crs = parent_tif.crs
    tile_nodata = parent_tif.nodata if parent_tif.nodata is not None else 0
    tile_transform = get_tile_transform(parent_tif.transform, pixel_x, pixel_y)
    profile = dict(
                driver="GTiff",
                crs=tile_crs,
                nodata=tile_nodata,
                transform=tile_transform
            )
    return profile

def validate_array(img_array):
    """
    Validates an image array by calculating the percentage of zero values in the first channel.

    Args:
        img_array (numpy.ndarray): The image array to validate.

    Returns:
        float: The percentage of zero values in the first channel of the image array.

    """
    percentage=np.where(img_array[0,:,:].flatten()==0)[0].shape[0]/(img_array.shape[1]*img_array.shape[2])
    return percentage

def generate_tile(tif,coordinates,size,valid_threshold=0.1):

    """
    Generates a tile from a TIFF image based on the given coordinates and size.

    Args:
    
        tif (rasterio.DatasetReader): The TIFF image to generate the tile from.
        coordinates (tuple): The (x, y) coordinates of the tile.
        size (int): The size of the tile (width and height).
        filter_percentage (float, optional): The maximum percentage of anomaly values allowed in the tile.
                                             Defaults to 0.1.
        valid_threshold :Percentage value between 0 to 1 to create valid tiles having no data values less than / equal to 
        the valid_threshold

    Returns:
        rasterio.DatasetReader or None: The generated tile as a rasterio DatasetReader object if it passes
                                        the anomaly filter, or None if it exceeds the filter threshold.

    """
    x,y=coordinates
    # creating the tile specific profile
    profile = get_tile_profile(tif, x, y)
    # extracting the pixel data (couldnt understand as i dont think thats the correct way to pass the argument)
    tile_data = tif.read(window=((y, y + size), (x, x + size)),
                            boundless=True, fill_value=profile['nodata'])

    anomaly_percentage=validate_array(tile_data)
    if anomaly_percentage<=valid_threshold:
        c, h, w = tile_data.shape
        profile.update(
            height=h,
            width=w,
            count=c,
            dtype=tile_data.dtype,
        )

        memfile = rasterio.MemoryFile()
    
        # Write the NumPy array to the MemoryFile
        with memfile.open(**profile) as dst:
            for i in range(c):
                dst.write(tile_data[i,:,:], i+1)
        # Return a rasterio DatasetReader object
        return memfile.open()
    else:
       return None

def open_shp(shp_file,crs="epsg:32644"):

    """
        Opens a shapefile (SHP) using geopandas library.

        Args:
            shp_file (str): The file path to the shapefile.

        Returns:
            geopandas.geodataframe.GeoDataFrame: The opened shapefile as a GeoDataFrame.

    """
    gdf=gpd.read_file(shp_file)
    gdf=gdf.to_crs(crs)
    return gdf

def open_tiff(path): 

    """
        Opens a TIFF file using rasterio library.

        Args:
            path (str): The file path to the TIFF image.

        Returns:
            rasterio.io.DatasetReader: The opened TIFF image.

    """
    img = rasterio.open(path)
    return img 


class Indices():
    def __init__(self,src):
        pass

    def __get_stats__(self):
        index_data=np.ma.masked_invalid(self.index_array).compressed()
        data_stats={}
        data_stats["Max"]=index_data.max()
        data_stats["Mean"]=index_data.mean()
        data_stats["Median"]=np.median(index_data)
        data_stats["Min"]=index_data.min()
        data_stats['skew']=skew(index_data)
        data_stats['kurtosis']=kurtosis(index_data)
        data_stats['skew x kurtosis']=data_stats['skew']*data_stats['kurtosis']
        return data_stats
        
    def get_histogram(self,ax=None):

        array_flat = self.index_array.flatten()

        # Plot the histogram
        if ax!=None:
          ax.hist(array_flat, bins=50, color='green', alpha=0.8)
        else:
          plt.hist(array_flat, bins=50, color='green', alpha=0.8) 

        ax.set_xlabel('NDVI')
        ax.set_ylabel('Frequency')
        ax.set_title('NDVI Histogram')
        

    def get_heatmap(self,ax=None):
       
       if ax!=None:
         img=ax.imshow(self.index_array, cmap="RdYlGn")
       else:
         plt.imshow(self.index_array, cmap="RdYlGn")
        
       plt.colorbar(img,ax=ax)

    def get_thres_region(self,ax,threshold=0.7):

       red_band = self.src.read(1)
       # Highlight stressed regions on the original image
       stressed_regions = np.where(self.index_array<threshold, 1, 0)
       highlighted_image = red_band.copy()  # Use the red band as a base for highlighting
       highlighted_image[stressed_regions == 1] = 255  # Set stressed regions to maximum intensity

       # Plot the original image with stressed regions highlighted
       #cmap = plt.cm.colors.ListedColormap(['white', 'red'])
       img=ax.imshow(highlighted_image, cmap='gray')
       plt.colorbar(img,ax=ax)


class ndvi(Indices):

    def __init__(self, src,band_identifier):
        self.src=src
        self.band_identifier=band_identifier
        self.index_array=self.__calculate_ndvi__()

    def __calculate_ndvi__(self):
        red_band = self.src.read(self.band_identifier['r'])
        nir_band = self.src.read(self.band_identifier['nir'])
        ndvi = (nir_band.astype(float)-red_band.astype(float))/(nir_band.astype(float)+red_band.astype(float))
        return ndvi    

class vari(Indices):

    def __init__(self, src,band_identifier):
        self.src=src
        self.band_identifier=band_identifier
        self.index_array=self.__calculate_vari__()

    def __calculate_vari__(self):
        red_band = self.src.read(self.band_identifier['r'])
        green_band = self.src.read(self.band_identifier['g'])
        vari = (green_band.astype(float)-red_band.astype(float))/(green_band.astype(float)+red_band.astype(float))
        return vari

class gli(Indices):

    def __init__(self, src,band_identifier):
        self.src=src
        self.band_identifier=band_identifier
        self.index_array=self.__calculate_gli__()

    def __calculate_gli__(self):
        red_band = self.src.read(self.band_identifier['r'])
        green_band = self.src.read(self.band_identifier['g'])
        gli = (2*green_band.astype(float)-red_band.astype(float))/(2*green_band.astype(float)+red_band.astype(float))
        return gli

class nir(Indices):

    def __init__(self, src,band_identifier):
        self.src=src
        self.band_identifier=band_identifier
        self.index_array=self.__calculate_gli__()

    def __calculate_gli__(self):
        nir_band = self.src.read(self.band_identifer['nir'])
        return nir_band

