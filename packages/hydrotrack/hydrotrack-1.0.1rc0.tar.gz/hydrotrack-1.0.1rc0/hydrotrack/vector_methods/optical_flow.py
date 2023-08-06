import pandas as pd
import numpy as np
import cv2
import geopandas as gpd
from shapely.geometry import Point, LineString, MultiLineString
from shapely.ops import linemerge
from scipy import stats
from ..utils import calculate_direction


def optflow_corretion(current_frame, previous_frames, read_function, method='lucas-kanade'):
    # Check if current_frame['file'] is empty
    if len(current_frame) == 0:
        return pd.DataFrame(columns=['dis_opt', 'dir_opt'])
    if len(previous_frames) == 0:
        return pd.DataFrame(columns=['dis_opt', 'dir_opt'])
    # Concatenate all previous frames and get file names
    past_frames = pd.concat(previous_frames)
    if len(past_frames) == 0:
        return pd.DataFrame(columns=['dis_opt', 'dir_opt'])
    if len(current_frame) == 0:
        return pd.DataFrame(columns=['dis_opt', 'dir_opt'])
    # Files list
    files_list = list(past_frames.file.unique()) # Get all file names
    files_list.append(current_frame.file.unique()[0]) # Add current frame file name
    files_list = sorted(files_list)[::-1] # Reverse the list
    # Get minimum and maximum values of current image used to normalize
    min_val = current_frame['min'].min()
    max_val = current_frame['max'].max()
    # Loop over reversed files list
    vector_field = []
    for time in range(len(files_list) - 1):
        cur_path = files_list[time] # Current path
        prv_path = files_list[time + 1] # Previous path
        if time == 0: # First iteration read current image
            cur_img = norm_img(read_function(cur_path), min_val, max_val)
            currPts = np.empty((0,1,2), dtype=np.float32) # Initialize empty array for current points
        prv_img = norm_img(read_function(prv_path), min_val, max_val) # Read previous image
        # Call Optical Flow Methods
        if method == 'lucas-kanade':
            nextPts, currPts = lucas_kanade(cur_img, prv_img, currPts)
        elif method == 'farneback':
            nextPts, currPts = farneback(cur_img, prv_img)
        # Add to current_vectors list
        vector_field.extend(list(map(lambda x: LineString([Point(x[0]), Point(x[1])]), zip(nextPts,currPts))))
        # Update current image
        cur_img = prv_img
        currPts = nextPts
    if len(vector_field) == 0:
        return pd.DataFrame(columns=['dis_opt', 'dir_opt'])
    # Merge lines comming from Optical Flow
    merged_lines = linemerge(vector_field)
    # check if merged_lines is empty
    if merged_lines.is_empty:
        return pd.DataFrame(columns=['dis_opt', 'dir_opt'])
    elif isinstance(merged_lines, LineString):
        vector_field = gpd.GeoDataFrame(geometry=[merged_lines])
    elif isinstance(merged_lines, MultiLineString):
        vector_field = gpd.GeoDataFrame(geometry=list(merged_lines.geoms))
    else:
        return pd.DataFrame(columns=['dis_opt', 'dir_opt'])
    vector_field['p0'] = vector_field.geometry.apply(lambda x: Point(x.coords[-1]))
    vector_field = vector_field.set_geometry('p0')
    # Group by inside threshold_levels
    thd_curframe = current_frame.groupby('threshold_level')
    output_frame = pd.DataFrame(columns=['index','dis_opt', 'dir_opt','vector_field'])
    for _, idx in reversed(thd_curframe.groups.items()):
        if len(vector_field) == 0:
            continue
        # Spatial join between vector_field and current_frame
        operation = gpd.sjoin(vector_field, current_frame.loc[idx], how='inner', predicate='within')
        if len(operation) == 0:
            continue
        # Remove inside vectors from vector_field
        vector_field = vector_field.loc[~vector_field.index.isin(operation.index)]
        vector_field = vector_field.set_geometry('geometry')        
        # Group by index_right at operation from inside threshold_levels to outside
        for idx2, ggroup in operation.groupby('index_right'):
            qtd_coords = ggroup['geometry'].apply(lambda x: len(x.coords))
            lenght_coords = ggroup['geometry'].length
            mean_leangth = np.mean(lenght_coords / qtd_coords)
            direct_coords = ggroup['geometry'].apply(lambda x: calculate_direction(x.coords[0], x.coords[1]))
            mean_direction = stats.circmean(direct_coords.to_numpy(), high=360, axis=0,nan_policy='omit')
            v_field = str(ggroup['geometry'].unary_union)
            output_frame = pd.concat([output_frame, pd.DataFrame([[idx2, mean_leangth, mean_direction,v_field]],
                                                                 columns=['index','dis_opt', 'dir_opt','vector_field'])])
    output_frame = output_frame.set_index('index') # Set index
    return output_frame

def norm_img(matrix, min_value, max_value, gauss_filter=True):
    """ Normalize matrix. """
    matrix = np.nan_to_num(matrix, nan=0.0)
    # Fill between min and max values
    matrix[matrix < min_value] = 0
    matrix[matrix > max_value] = 0
    # Apply gaussian filter
    if gauss_filter:
        kernel_size = (5, 5)
        sigma = 0.5
        matrix = cv2.GaussianBlur(matrix, kernel_size, sigma)
    # Normalize
    matrix = ((matrix - min_value) / (max_value - min_value) * 255)
    matrix = matrix.astype(np.uint8)
    return matrix

    
def lucas_kanade(current_img, previous_img, currPts):
    """Lucas Kanade optical flow method used to compute the optical flow for a sparse feature set using the iterative
    Using reverse image order (t-1,t-2,t-3,...)
    """
    # Check if currPts is empty (first iteration) and call ShiTomasi corner detection
    if len(currPts) == 0:
        # Params for ShiTomasi corner detection
        feature_params = dict(
            maxCorners=None,
            qualityLevel=0.01,  # Parameter characterizing the minimal accepted quality of image corners.
            minDistance=0.5,  # Minimum possible Euclidean distance between the returned corners.
            blockSize=2,  # Size of an average block for computing a derivative covariation matrix over each pixel neighborhood.
            useHarrisDetector=True,  # Parameter indicating whether to use a Harris detector (see cornerHarris) or cornerMinEigenVal.
            k=0.04,  # Free parameter of the Harris detector.
        )
        # ShiTomasi corner detection
        currPts = cv2.goodFeaturesToTrack(current_img, mask=None, **feature_params)
    # Call Lucas Kanade optical flow
    nextPts, status, _ = cv2.calcOpticalFlowPyrLK(prevImg=current_img,
                                                  nextImg=previous_img,
                                                  prevPts=currPts,
                                                  nextPts=None,
                                                  winSize=(50, 50),
                                                  maxLevel=3,
                                                  criteria=(3, 10, 0),
                                                  flags=cv2.OPTFLOW_LK_GET_MIN_EIGENVALS,
                                                  minEigThreshold=1e-4)
    # Select good points
    nextPts = nextPts[status == 1]
    currPts = currPts[status == 1]
    nextPts = nextPts[:, np.newaxis, :] # Add new axis
    currPts = currPts[:, np.newaxis, :] # Add new axis
    return nextPts, currPts

def farneback(current_img, previous_img):
    """Farneback optical flow method used to compute the optical flow for a sparse feature set using the iterative
    Using reverse image order (t-1,t-2,t-3,...)
    """
    flow = cv2.calcOpticalFlowFarneback(prev=current_img,
                                        next=previous_img,
                                        flow=None,
                                        pyr_scale=0.5, # Parâmetro de escala piramidal.
                                        levels=3, # Número de níveis piramidais.
                                        winsize=15, # Tamanho da janela de busca.
                                        iterations=3, # Número de iterações do algoritmo a cada nível piramidal.
                                        poly_n=5, # Tamanho da vizinhança considerada ao calcular o polinômio de expansão.
                                        poly_sigma=1.1, # Desvio padrão do filtro gaussiano aplicado ao polinômio de expansão.
                                        flags=0)
    # Get magnitude and angle
    magn, angle = cv2.cartToPolar(flow[...,0], flow[...,1])
    y_idx, x_idx = np.where(magn > 1)  # Get position of points with magnitude > 10
    magn = magn[y_idx, x_idx] # Get magnitude of points with magnitude > 10
    angle = np.rad2deg(angle[y_idx, x_idx]) # Get angle of points with magnitude > 10
    points = [point_position(x_idx[p],y_idx[p], magn[p], angle[p]) for p in range(len(y_idx))]
    nextPts = np.array(points).reshape(-1, 1, 2)
    currPts = np.array([x_idx, y_idx]).T.reshape(-1, 1, 2)
    if np.any(np.isinf(nextPts)): # Verify if have inf values in nextPts
        inf_idx = np.where(np.isinf(nextPts))
        nextPts = np.delete(nextPts, inf_idx[0], axis=0)
        currPts = np.delete(currPts, inf_idx[0], axis=0)
    return nextPts, currPts

def point_position(x1=None, y1=None, lenght=None, angle=None):
    """
    Calculates the position of a point for displacement.
    """
    rad_theta = np.radians(angle)
    x2 = x1 + lenght * np.cos(rad_theta)
    y2 = y1 + lenght * np.sin(rad_theta)
    return x2, y2