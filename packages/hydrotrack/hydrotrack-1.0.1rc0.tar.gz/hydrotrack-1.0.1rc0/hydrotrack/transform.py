import glob
import geopandas as gpd
import pandas as pd
import numpy as np
import pathlib
import xarray as xr
from joblib import Parallel, delayed
from shapely.wkt import loads
from shapely.ops import split
from shapely.affinity import translate
from shapely.geometry import MultiPolygon, LineString, MultiLineString
from .utils import loading_bar
import warnings
# Ignore warning UserWarning from geopandas
warnings.filterwarnings("ignore", category=UserWarning)

def geotransform(name_list, geometries=True, clusters=True, comp_lvl=9):
    '''Transform the features in a trajectory'''
    cluster_files = sorted(glob.glob(name_list['output_path'] + 'features/clusters/*.npz', recursive=True))
    if len(cluster_files) == 0:
        print('No clusters files found in the input directory')
        return
    # Get first file shape
    file_shape = np.load(cluster_files[0])['arr_0']
    if file_shape[-2:].ndim < 2:
        print('The first file does not contain 2 dimensions, please run the spatial operations first')
        return
    if 'lat_min' not in name_list.keys() and 'lat_max' not in name_list.keys():
        print('Please set the lat_min and lat_max in the name_list')
        return
    elif 'lon_min' not in name_list.keys() and 'lon_max' not in name_list.keys():
        print('Please set the lon_min and lon_max in the name_list')
        return
    # Set the geotransform
    X_DIM, Y_DIM = file_shape.shape[-2:] # Get the dimensions
    geotransform, inv_geotransform = set_geotransform(name_list, X_DIM, Y_DIM) # Set the geotransform
    geometry_files = sorted(glob.glob(name_list['output_path'] + 'features/geometries/*.feather', recursive=True))
    # Create output directory for geometry files and clusters
    pathlib.Path(name_list['output_path'] + 'geometry/boundary/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(name_list['output_path'] + 'geometry/trajectory/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(name_list['output_path'] + 'geometry/vector_field/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(name_list['output_path'] + 'clusters/').mkdir(parents=True, exist_ok=True)
    # Parallel processing
    if geometries:
        print('Transforming the geometries features...')
        Parallel(n_jobs=name_list['n_jobs'])(delayed(to_geojson)(geometry_files[file], name_list, geotransform, inv_geotransform, file, len(geometry_files)) for file in range(len(geometry_files)))
        loading_bar(len(cluster_files), len(cluster_files))
        print('\tDone!')
    if clusters:
        print('Transforming the clusters features...')
        Parallel(n_jobs=name_list['n_jobs'])(delayed(to_netcdf)(cluster_files[file], name_list, file, len(cluster_files), comp_lvl) for file in range(len(cluster_files)))
        loading_bar(len(cluster_files), len(cluster_files))
    print('\tDone!')
    
def set_geotransform(name_list, Y_DIM, X_DIM,):
    '''Set the geotransform'''
    LON_MIN = name_list['lon_min']
    LON_MAX = name_list['lon_max']
    LAT_MIN = name_list['lat_min']
    LAT_MAX = name_list['lat_max']
     # Calculate pixel size
    xres = abs(LON_MAX - LON_MIN) / X_DIM
    yres = abs(LAT_MAX - LAT_MIN) / Y_DIM
    # Transform matrix
    matrix = np.array([[xres, 0, LON_MIN], [0, yres, LAT_MIN], [0, 0, 1]])
    # Calculate geotransform
    geotransform = (matrix[0,0], matrix[0,1], matrix[1,0], matrix[1,1],matrix[0,2], matrix[1,2])
    # Calculate inverse matrix
    matrix_inv = np.linalg.inv(matrix)
    # Calculate inverse geotransform
    geotransform_inv = (matrix_inv[0,0], matrix_inv[0,1], matrix_inv[1,0], matrix_inv[1,1],matrix_inv[0,2], matrix_inv[1,2])
    return geotransform, geotransform_inv

def to_geojson(file, name_list, geotransform, inv_geotransform, tfile, total):
    '''Convert the features in a trajectory to GeoJSON'''
    # Open the file
    geo_frame = gpd.read_feather(file)
    # Filename
    filename = pathlib.Path(file).stem
    # Check if the file is empty
    if geo_frame.empty:
        geo_frame.to_file(name_list['output_path'] + 'geometry/boundary/' + filename + '.geojson', driver='GeoJSON')
        geo_frame.to_file(name_list['output_path'] + 'geometry/trajectory/' + filename + '.geojson', driver='GeoJSON')
        geo_frame.to_file(name_list['output_path'] + 'geometry/vector_field/' + filename + '.geojson', driver='GeoJSON')
        return
    
    # Set columns to geometry/boundary and trajectory
    boundary_columns = ['timestamp','cluster_id', 'uid','iuid','threshold','threshold_level', 'mean', 'std', 'min', 'Q1', 'Q2', 'Q3', 'max',
                        'size', 'inside_clusters', 'dis_','dis_avg', 'dis_inc', 'dis_opt', 'dir_','dir_avg', 'dir_inc', 'dir_opt',
                        'lifetime', 'status', 'geometry']
    trajectory_columns = ['timestamp', 'uid','iuid','threshold','threshold_level', 
                          'dis_','dis_avg', 'dis_inc', 'dis_opt', 'dir_','dir_avg', 'dir_inc', 'dir_opt',
                          'lifetime', 'status', 'trajectory']
    vectorfield_columns = ['timestamp', 'uid','iuid','threshold','threshold_level',
                           'dis_','dis_avg', 'dis_inc', 'dis_opt', 'dir_','dir_avg', 'dir_inc', 'dir_opt',
                            'lifetime', 'status', 'vector_field']
    # Compare the geo_frame columns to the boundary_columns and drop the columns, but ordering by boundary_columns
    order_b_columns = [col for col in boundary_columns if col in geo_frame.columns]
    order_t_columns = [col for col in trajectory_columns if col in geo_frame.columns]
    order_v_columns = [col for col in vectorfield_columns if col in geo_frame.columns]
    # Set the data type to string
    geo_frame["timestamp"] = geo_frame["timestamp"].astype(str)
    geo_frame["lifetime"] = geo_frame["lifetime"].astype(str)
    # Set the geometry to the boundary frame
    bound_frame = geo_frame[order_b_columns] # Boundary frame
    traj_frame = geo_frame[order_t_columns] # Trajectory frame
    vec_frame = geo_frame[order_v_columns] # Vector field frame
    # Set the geometry to the boundary frame
    bound_frame = bound_frame.set_geometry('geometry')
    bound_frame['geometry'] = bound_frame['geometry'].affine_transform(geotransform)
    if name_list['lon_max'] > 180:
        bound_frame = split_lon_max(bound_frame, geotype=MultiPolygon)

    # Save to GeoJSON
    schema_ = gpd.io.file.infer_schema(bound_frame)
    bound_frame.to_file(name_list['output_path'] + 'geometry/boundary/' + filename + '.geojson', driver='GeoJSON', schema=schema_)
    if 'trajectory' in traj_frame.columns:
        traj_frame['geometry'] = traj_frame['trajectory'].apply(lambda x: loads(x))
        traj_frame = gpd.GeoDataFrame(traj_frame, geometry='geometry')
        traj_frame['geometry'] = traj_frame['geometry'].affine_transform(geotransform)
        if name_list['lon_max'] > 180:
            traj_frame = split_lon_max(traj_frame, geotype=MultiLineString)
        schema_ = gpd.io.file.infer_schema(traj_frame)
        # Save to GeoJSON
        traj_frame.to_file(name_list['output_path'] + 'geometry/trajectory/' + filename + '.geojson', driver='GeoJSON', schema=schema_)
    else: # Create empty GeoDataFrame to save the timestamp
        traj_frame = gpd.GeoDataFrame(traj_frame)
        traj_frame['geometry'] = loads('LINESTRING EMPTY')
        # Save to GeoJSON
        traj_frame.to_file(name_list['output_path'] + 'geometry/trajectory/' + filename + '.geojson', driver='GeoJSON')
    if 'vector_field' in vec_frame.columns:
        vec_frame = vec_frame.rename(columns={'vector_field': 'geometry'})
        vec_frame['geometry'] = vec_frame['geometry'].fillna('LINESTRING EMPTY')
        vec_frame['geometry'] = vec_frame['geometry'].apply(lambda x: loads(x))
        vec_frame = gpd.GeoDataFrame(vec_frame, geometry='geometry')
        vec_frame['geometry'] = vec_frame['geometry'].affine_transform(geotransform)
        if name_list['lon_max'] > 180:
            vec_frame = split_lon_max(vec_frame, geotype=MultiLineString)
        schema_ = gpd.io.file.infer_schema(vec_frame)
        # Save to GeoJSON
        vec_frame.to_file(name_list['output_path'] + 'geometry/vector_field/' + filename + '.geojson', driver='GeoJSON', schema=schema_)
    else:
        vec_frame = gpd.GeoDataFrame(vec_frame)
        vec_frame['geometry'] = loads('LINESTRING EMPTY')
        # Save to GeoJSON
        vec_frame.to_file(name_list['output_path'] + 'geometry/vector_field/' + filename + '.geojson', driver='GeoJSON')       
    loading_bar(tfile, total)
        
def to_netcdf(file, name_list, tfile, total, comp_lvl=3):
    
    filename = pathlib.Path(file).stem
    # Open the file
    cluster_file = np.load(file)['arr_0']
    # Open geoframe file
    geo_frame = gpd.read_feather(name_list['output_path'] + 'features/geometries/' + filename + '.feather')
    # Replace cluster_id with uid
    for _, row in geo_frame.iterrows():
        if row['threshold_level'] == 0:
            cluster_file[row['threshold_level']][cluster_file[row['threshold_level']] == row['cluster_id']] = row['uid']
        else:
            cluster_file[row['threshold_level']][cluster_file[row['threshold_level']] == row['cluster_id']] = row['iuid']
    # Create longitude and latitude array
    LON_MIN = name_list['lon_min']
    LON_MAX = name_list['lon_max']
    LAT_MIN = name_list['lat_min']
    LAT_MAX = name_list['lat_max']
    lon = np.linspace(LON_MIN, LON_MAX, cluster_file.shape[-1])
    lat = np.linspace(LAT_MIN, LAT_MAX, cluster_file.shape[-2])
    # Check if the longitude is between -180 and 180
    if LON_MAX > 180:
        lon_pos = np.where(lon > 180)
        lon_val = lon[lon_pos] - 360
        lon = np.delete(lon, lon_pos)
        lon = np.insert(lon, 0, lon_val)
        saved_ = cluster_file[..., lon_pos[0]]
        cluster_file = np.delete(cluster_file, lon_pos, axis=-1)
        cluster_file = np.concatenate((saved_, cluster_file), axis=-1)
    if LON_MIN < -180:
        lon_pos = np.where(lon < -180)
        lon_val = lon[lon_pos] + 360
        lon = np.delete(lon, lon_pos)
        lon = np.append(lon, lon_val)
        saved_ = cluster_file[..., lon_pos[0]]
        cluster_file = np.delete(cluster_file, lon_pos, axis=-1)
        cluster_file = np.concatenate((cluster_file, saved_), axis=-1)        
     
    if len(cluster_file.shape) == 2:
        data_xarray = xr.DataArray(cluster_file,
                                   coords=[lat, lon],
                                   dims=['lat', 'lon'])
    elif len(cluster_file.shape) > 2:
        data_xarray = xr.DataArray(cluster_file,
                                   coords=[np.arange(cluster_file.shape[0]), lat, lon],
                                   dims=['level', 'lat', 'lon'])
    else:
        return
    data_xarray.name = "Band1"
    # Set the attributes
    data_xarray.attrs["crs"] = "EPSG:4326"
    # Set FillValue
    data_xarray.attrs["_FillValue"] = 0
    # Set description
    data_xarray.attrs["description"] = "This is an output from PyForTrack"
    # Save compressed netcdf file
    filename = pathlib.Path(file).stem
    data_xarray.to_netcdf(name_list['output_path'] + 'clusters/' + filename + '.nc', encoding={'Band1': {'zlib': True, 'complevel': comp_lvl}})
    loading_bar(tfile, total)


def split_lon_max(geo_df,geotype=MultiPolygon):
    ### Clip geometries in tttt larger LONGITUDE than 180
    geo_df1 = geo_df[geo_df.geometry.bounds['maxx']<=180]
    geo_df2 = geo_df[geo_df.geometry.bounds['maxx']>180]
    nones = geo_df[~geo_df.index.isin(geo_df1.index) & ~geo_df.index.isin(geo_df2.index)]
    geo_df2.geometry = geo_df2.translate(xoff=-360)
    geo_df3 = geo_df2[geo_df2.geometry.bounds['minx']<-180]
    # Create a line -90 to 90 in latitude and 180 to 180 in longitude
    line = LineString([(-180, -90), (-180, 90)])
    geo_df4 = geo_df3.geometry.apply(lambda x: split(x,line))
    # Get GeometryCollection explode and bounds['maxx'] < -180 apply translate xoff=360 and set as MultiPolygon
    geo_df5 = geo_df4.explode().apply(lambda x: translate(x, xoff=360)  if x.bounds[0]<-180 else x)
    # Merge to a single geotype
    multgeos = geo_df5.reset_index().groupby('level_0').apply(lambda x: geotype(x.geometry.values))
    if len(multgeos) > 0:
        geo_df2.loc[multgeos.index, 'geometry'] = multgeos.values
    output_df = gpd.GeoDataFrame(pd.concat([geo_df1, geo_df2]))
    output_df = gpd.GeoDataFrame(pd.concat([output_df, nones])).sort_index()
    return output_df