import pandas as pd
import numpy as np
import math

# Data reader function
def read_data(data_path, user=None, start_time='1800-01-01T01:01:00.0000000Z', end_time='2200-01-01T01:01:00.0000000Z'):
    # Read data and convert the Timepoint column to datetime object
    df = pd.read_csv(data_path)
    df['Timepoint'] = pd.to_datetime(df['Timepoint'])

    # Selecting data for the specified user
    if user not in df['UserID'].unique():
        print('User not present in the given data, known users in the given data are:', df['UserID'].unique())
        return None
    df = df[df['UserID'] == user]

    # Defining start and end times, if both are specified -> get inbetween, if one is specified -> get before/after the specified, if none is specified -> get all
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    
    # Making mask to only show data from a single day
    mask = (df['Timepoint'] >= start_time) & (df['Timepoint'] <= end_time)
    df = df.loc[mask]
    df = df.sort_values(by='Timepoint')

    return df


def get_acceleration(df, dt, x, y, z):
    # get velocity by difference divided by dt
    accel_df = pd.DataFrame()
    velocity_x = np.insert(np.diff(df[x]) / dt, 0, 0)
    velocity_y = np.insert(np.diff(df[y]) / dt, 0, 0) 
    velocity_z = np.insert(np.diff(df[z]) / dt, 0, 0)
    # same method for acceleration and add to df
    accel_df['accel_x'] = np.insert(np.diff(velocity_x) / dt, 0, 0)
    accel_df['accel_y'] = np.insert(np.diff(velocity_y) / dt, 0, 0)
    accel_df['accel_z'] = np.insert(np.diff(velocity_z) / dt, 0, 0)

    return accel_df


def calculate_vector_magnitude(x, y, z):
    return np.sqrt(x**2 + y**2, z**2)

def calculate_hours_of_use(vector_magnitude, threshold=0.1, dt=1):
    '''
    Function to sum up all the instances where the magnitude vector is greater than a set threshold to detect activity.
    magnitude vector is an 1D-array like object containing the magnitudes per time step
    threshold is a float which must be exceeded for a signal to be counted as active
    dt is the time difference between variables.
    '''
    above_threshold = (vector_magnitude > threshold).sum()
    return above_threshold / (3600 * dt)

def calculate_magnitude_ratio(vector_magnitude_left, vector_magnitude_right):
    '''
    function which calculates in each time step which hand contributed more to the movement intensity.
    values close to 0 indiate equal usage
    values close to -7 indicate more usage of right arm
    values close to 7 indicate more usage of left arm
    '''
    ln_left = np.log(vector_magnitude_left)
    ln_right = np.log(vector_magnitude_right)
    magnitude_ratio = ln_left / ln_right
    
    return np.clip(magnitude_ratio, a_min=-7, a_max=7)

def calculate_bilateral_magnitude(vector_magnitude_left, vector_magnitude_right):
    return np.sum((vector_magnitude_left, vector_magnitude_right), axis=0)


def calculate_elbow_angles(shoulder, elbow, wrist, upper_arm_length, forearm_length):
    # Initialize lists for storing timeseries data
    angles = []
    upper_arm_vectors = []
    forearm_vectors = []
    for i in range(len(shoulder)):
        # Calculate vectors representing upper arm and forearm
        upper_arm_vector = [elbow[i][0] - shoulder[i][0],
                            elbow[i][1] - shoulder[i][1], 
                            elbow[i][2] - shoulder[i][2]]
        forearm_vector = [wrist[i][0] - elbow[i][0], 
                          wrist[i][1] - elbow[i][1], 
                          wrist[i][2] - elbow[i][2]]
        # Store vectors in list for debugging purposes
        upper_arm_vectors.append(upper_arm_vector)
        forearm_vectors.append(forearm_vector)
        # Calculate dot product of upper arm and forearm vectors
        dot_product = upper_arm_vector[0] * forearm_vector[0] + upper_arm_vector[1] * forearm_vector[1] + upper_arm_vector[2] * forearm_vector[2]
        # Calculate angle between upper arm and forearm vectors using law of cosines
        angle = math.acos(dot_product / (upper_arm_length * forearm_length))
        # Convert angle from radians to degrees
        angle_degrees = 180 - math.degrees(angle)
        # Append the angle to the list
        angles.append(angle_degrees)
    return angles