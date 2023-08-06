import glob
import pandas as pd
import geopandas as gpd
import pathlib
from datetime import datetime, timedelta
from joblib import Parallel, delayed
from hydrotrack.vector_methods import *
from .utils import loading_bar


def vector_methods(name_list, read_function, parallel=True, previous_times=3, merge=True, tempavg=True, icor=True, optflow=True,):
    """ Extract the vector data from the input files. """
    print('Vector methods has been started...')
    # Get features files
    files_list = sorted(glob.glob(name_list['output_path'] + 'features/geometries/*.feather', recursive=True))
    if not files_list:
        print('No files found in the input directory')
        return
    # Check if the first file contains status column when opening
    geodf = gpd.read_feather(files_list[0])
    if 'uid' not in geodf.columns:
        print('The first file does not contain uid column, please run the spatial operations first')
        return
    # Extract the timestamp from the path
    tstamp_list = [datetime.strptime(pathlib.Path(x).stem, '%Y%m%d_%H%M%S') for x in files_list]
    time_delta = timedelta(minutes=name_list['delta_time'])
    boundary_path = name_list['output_path'] + 'features/geometries/'
    # Add methods to the list
    methods_list = []
    if merge:
        methods_list.append('merge')
    if tempavg:
        methods_list.append('tempavg')
    if icor:
        methods_list.append('icor')
    if optflow:
        methods_list.append('optflow')
    if parallel:
        # Run the parallel process
        results = Parallel(n_jobs=name_list['n_jobs'])(delayed(process_timestamp)((tstamp_list[tstamp], boundary_path, time_delta, \
                                                                                previous_times, methods_list, \
                                                                                read_function, \
                                                                                tstamp, len(tstamp_list))) for tstamp in range(len(tstamp_list)))
    else:
        # Run in serial
        results = [process_timestamp((tstamp_list[tstamp], boundary_path, time_delta, \
                                        previous_times, methods_list, \
                                        read_function, \
                                        tstamp, len(tstamp_list))) for tstamp in range(len(tstamp_list))]
    # Save the results    
    frames, timestamps = zip(*results)
    for frame, timestamp in zip(frames, timestamps):
        frame.to_feather(boundary_path + timestamp.strftime('%Y%m%d_%H%M%S') + '.feather')
    loading_bar(len(tstamp_list), len(tstamp_list))
    print('\tDone!')

def process_timestamp(args):
    timestamp, boundary_path, time_delta, previous_times, methods_list, read_function, tstamp, total = args
    current_frame = gpd.read_feather(boundary_path + timestamp.strftime('%Y%m%d_%H%M%S') + '.feather')
    previous_stamp = pd.date_range(timestamp - (time_delta * (previous_times - 1)), timestamp - time_delta, freq=time_delta)
    previous_frames = [gpd.read_feather(boundary_path + pstamp.strftime('%Y%m%d_%H%M%S') + '.feather') \
                        if pathlib.Path(boundary_path + pstamp.strftime('%Y%m%d_%H%M%S') + '.feather').exists() \
                        else pd.DataFrame() for pstamp in previous_stamp]
    # Process the corretions
    for method in methods_list:
        frame = call_corretions((method, current_frame, previous_frames, read_function))
        if len(frame) > 0:
            current_frame.loc[frame.index, frame.columns] = frame
    # Call loading bar
    loading_bar(tstamp, total)
    return (current_frame, timestamp)

def call_corretions(args):
    " Call the corretions methods. "
    method, current_frame, previous_frames, read_function = args
    if method == 'merge':
        return merge_corretion(current_frame, previous_frames)
    elif method == 'tempavg':
        return temporal_avg_corretion(current_frame, previous_frames)
    elif method == 'icor':
        innerc_corretion(current_frame)
        return pd.DataFrame(columns=['dis_icor', 'dir_icor'])
    elif method == 'optflow':
        method_frame = optflow_corretion(current_frame,
                                                       previous_frames,
                                                       read_function,
                                                       method='lucas-kanade')
        return method_frame
    else:
        return pd.DataFrame(columns=['dis_' + method, 'dir_' + method])
