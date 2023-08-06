import glob
import geopandas as gpd
import pathlib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from shapely.ops import linemerge
from shapely.wkt import loads
from shapely.geometry import MultiLineString
from .utils import loading_bar, get_columns, find_previous_frame, save_feather

import sys

def trajectory_linking(name_list):
    """ Link trajectories together.
    """
    print('Processing the trajectory linking (Serial mode) ...')
    # Get features files
    files_list = sorted(glob.glob(name_list['output_path'] + 'features/geometries/*.feather', recursive=True))
    if not files_list:
        print('No files found in the input directory')
        return
    tstamp_list = [datetime.strptime(pathlib.Path(x).stem, '%Y%m%d_%H%M%S') for x in files_list]
    dt_time = timedelta(minutes=name_list['delta_time'])
    features_path = name_list['output_path'] + 'features/geometries/'

    # Set initial UID
    uid = 1
    counter = 0
    # Loop through the files
    for cstamp in range(len(tstamp_list)):
        current_timestamp = tstamp_list[cstamp]
        current_path = features_path + current_timestamp.strftime('%Y%m%d_%H%M%S') + '.feather'
        current_frame = gpd.read_feather(current_path) # Read the current frame
        current_columns = current_frame.columns
        # Add trajectory columns in current frame at 3rd position
        trajectory_columns = get_columns()['trajectory']
        # check if the trajectory columns are already in the current frame
        if not all(elem in current_columns for elem in trajectory_columns):
            current_frame = current_frame.reindex(columns=np.concatenate((current_columns[:3], trajectory_columns, current_columns[3:])))
        # Check if the current frame is empty
        if current_frame.empty:
            continue
        if counter == 0:
            current_frame = new_frame(current_frame, uid, dt_time)
            current_frame = refact_inside_uids(current_frame, dt_time)
            if 'touch_idx' in current_frame.columns:
                current_frame = boarder_uid(current_frame)
            if ~np.isnan(current_frame['uid'].max()):
                uid = current_frame['uid'].max() + 1
            else:
                uid = uid + 1
            counter += 1
            save_feather(current_frame, current_path) # Save the current frame
            loading_bar(cstamp, len(tstamp_list))
            continue
        # Previous frame
        previous_stamp = current_timestamp - dt_time
        previous_file = features_path + previous_stamp.strftime('%Y%m%d_%H%M%S') + '.feather'
        # previous_frame = None
        if pathlib.Path(previous_file).exists():
            previous_frame = gpd.read_feather(previous_file)
        else:
            previous_frame, previous_stamp, dt_time = find_previous_frame(current_timestamp,
                                                                          cstamp,
                                                                          tstamp_list,
                                                                          files_list,
                                                                          name_list,
                                                                          dt_time,
                                                                          error_columns=get_columns()['features'] + \
                                                                                        get_columns()['spatial'] + \
                                                                                        get_columns()['trajectory'])
        # Check if previous frame is empty
        if previous_frame is None:
            current_frame = new_frame(current_frame, uid, dt_time)
            current_frame = refact_inside_uids(current_frame, dt_time)
            if 'touch_idx' in current_frame.columns:
                current_frame = boarder_uid(current_frame)
            if ~np.isnan(current_frame['uid'].max()):
                uid = current_frame['uid'].max() + 1
            else:
                uid = uid + 1
            counter += 1
            save_feather(current_frame, current_path) # Save the current frame
            loading_bar(cstamp, len(tstamp_list))
            continue
        # Get previous index in current frame
        not_none_current = current_frame.loc[(~current_frame['prev_idx'].isnull()) &
                                             (current_frame['prev_idx']!= -1)]
        if not_none_current.empty: # All clusters are new
            current_frame = new_frame(current_frame, uid, dt_time)
            current_frame = refact_inside_uids(current_frame, dt_time)
            if 'touch_idx' in current_frame.columns:
                current_frame = boarder_uid(current_frame)
            if np.isnan(current_frame['uid'].max()):
                uid_list = np.arange(uid, uid + len(current_frame), 1, dtype=int)
                iuids = [float(str(uid_list[x]) + '.' + str(x)) for x in range(len(uid_list))]
                current_frame['uid'] = uid_list
                current_frame['iuid'] = iuids
                current_frame['lifetime'] = dt_time
            if ~np.isnan(current_frame['uid'].max()):
                uid = current_frame['uid'].max() + 1
            else:
                uid = uid + 1
            counter += 1
            save_feather(current_frame, current_path) # Save the current frame
            loading_bar(cstamp, len(tstamp_list))
            continue
        # Get uid from previous frame
        not_none_current = not_none_current['prev_idx'].apply(lambda x: previous_frame.loc[x])
        current_frame.loc[not_none_current.index, 'uid'] = not_none_current['uid']
        current_frame.loc[not_none_current.index, 'iuid'] = not_none_current['iuid']
        delta_life = current_timestamp - previous_stamp
        current_frame.loc[not_none_current.index, 'lifetime'] = not_none_current['lifetime'] + delta_life
        # Merge trajectories
        current_frame['trajectory'] = loads(current_frame['trajectory'])
        previous_frame['trajectory'] = loads(previous_frame['trajectory'])
        # Merge the trajectorie
        trajectory = current_frame.loc[not_none_current.index].apply(lambda x: new_trajectory(x['trajectory'],
                                                                    previous_frame.loc[x['prev_idx']]['trajectory']) \
                                                                    if previous_frame.loc[x['prev_idx']]['trajectory'].is_empty == False \
                                                                    else x['trajectory'], axis=1)
        current_frame.loc[not_none_current.index, 'trajectory'] = trajectory # Update the trajectory
        current_frame['trajectory'] = current_frame['trajectory'].astype(str) # Convert to string
        # Add news
        none_current = current_frame[current_frame['prev_idx'].isnull()].index
        if len(none_current) > 0:
            none_current = new_frame(current_frame.loc[none_current], uid, dt_time)
            current_frame.loc[none_current.index, none_current.columns] = none_current
            current_frame = refact_inside_uids(current_frame, dt_time)
            if 'touch_idx' in current_frame.columns:
                current_frame = boarder_uid(current_frame)
        if ~np.isnan(current_frame['uid'].max()):
            uid = current_frame['uid'].max() + 1
        else:
            uid = uid + 1
        counter += 1
        save_feather(current_frame, current_path) # Save the current frame
        loading_bar(cstamp, len(tstamp_list))
    loading_bar(len(tstamp_list), len(tstamp_list))
    print('\tDone!')

def new_frame(frame, max_uid, time_delta):
    # lock the threshold level 0
    new_index = frame.loc[(frame['uid'].isnull()) & (frame['threshold_level'] == 0)].index.values
    if len(new_index) == 0:
        return frame
    # Create new uid
    uid_list = np.arange(max_uid, max_uid + len(new_index), 1, dtype=int)
    frame.loc[new_index, 'uid'] = uid_list
    frame.loc[new_index, 'lifetime'] = time_delta
    return frame

def refact_inside_uids(frame, delta_time):
    # Get the inside index
    insd_inx = frame[(~frame['inside_idx'].isnull())]
    # Lock inside index threshold level 0
    insd_idx_lv0 = insd_inx[insd_inx['threshold_level'] == 0]
    insd_idx_idx = insd_idx_lv0.index
    insd_idx_val = insd_idx_lv0['inside_idx'].values
    # Create column iuid if not exist
    if 'iuid' not in frame.columns:
        frame['iuid'] = np.nan
    for idx, val in zip(insd_idx_idx, insd_idx_val):
        # Transform the uid to string
        uid_vl = str(int(frame.loc[idx]['uid']))
        # Get the threshold level
        inside_counter = 999
        for v in val:
            frame.loc[v,'uid'] = int(uid_vl)
            thld_vl = frame.loc[v]['threshold_level']
            if np.isnan(frame.loc[v,'iuid']):
                frame.loc[v,'iuid'] = float(uid_vl +'.'+'0' * (thld_vl - 1) + str(inside_counter))
                frame.loc[v,'lifetime'] = delta_time
                inside_counter -= 1
    return frame

def new_trajectory(current_line, previous_line):
    try: # TODO: Check the type of current and previous line to avoid error
        # Check if previous line is multiline
        if previous_line.type == 'MultiLineString':
            previous_line = [line for line in previous_line.geoms]
            previous_line.insert(0, current_line)
            merged = MultiLineString(previous_line)
        elif current_line.type == 'MultiLineString':
            current_line = [line for line in current_line.geoms]
            current_line.append(previous_line)
            merged = MultiLineString(current_line)
        else:
            merged = linemerge([current_line, previous_line])
        return merged
    except:
        return current_line

def boarder_uid(current_frame):
    # Get values in touch_idx column that are not null and add uid to them
    touch_lines = current_frame[~current_frame['touch_idx'].isnull()]
    touch_val = touch_lines['touch_idx'].values.astype(int)
    touch_idx = touch_lines.index
    if len(touch_idx) > 0:
        current_frame.loc[touch_idx, 'uid'] = -1
        current_frame.loc[touch_idx, 'iuid'] = -1
        current_frame.loc[touch_idx, 'lifetime'] = timedelta(seconds=0)
    return current_frame