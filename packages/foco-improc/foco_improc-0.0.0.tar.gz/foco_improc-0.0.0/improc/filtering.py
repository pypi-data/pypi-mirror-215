import numpy as np

"""
Get the MIP across a temporal window around the requested frame. Where requested frame is too early or late
for the requested window size, the temporal window will be truncated as necessary.
"""
def get_tmip(mft, frame, num_timepoints=11):
    start_t = max(0, frame - num_timepoints // 2)
    stop_t = min(np.rint(mft.numframes / mft.numz).astype(int) - 1, frame + num_timepoints // 2)
    volume_indices = list(range(start_t, stop_t + 1))
    volumes = np.array([mft.get_t(frame) for frame in volume_indices])
    return np.max(volumes, axis=0)

"""
Get the average across a temporal window around the requested frame. Where requested frame is too early or late
for the requested window size, the temporal window will be truncated as necessary.
"""
def get_tavg(mft, frame, num_timepoints=11):
    start_t = max(0, frame - num_timepoints // 2)
    stop_t = min(np.rint(mft.numframes / mft.numz).astype(int) - 1, frame + num_timepoints // 2)
    volume_indices = list(range(start_t, stop_t + 1))
    volumes = np.array([mft.get_t(frame) for frame in volume_indices])
    return np.mean(volumes, axis=0)
