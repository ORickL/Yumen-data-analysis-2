from utils import *
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from matplotlib.image import imread

class DataProcessor():
    '''
    This is a class to calculate a bunch of features from dataframes with positional data (for both arms!)
    Also has functionality to make a density plot which visualizes assymetry in arm movement.
    '''
    def __init__(self, data_path, user, start_time='1800-01-01T01:01:00.0000000Z', end_time='2200-01-01T01:01:00.0000000Z', dt=1, threshold=0.1, upper_arm_length=33, forearm_length=28):
        self.data = read_data(data_path=data_path, user=user, start_time=start_time, end_time=end_time)
        self.data.dropna(how='any', inplace=True)
        self.dt = dt
        self.threshold = threshold
        self.upper_arm_length = upper_arm_length
        self.forearm_length = forearm_length

        # calculating acceleration dataframes (required for vector magnitude and all measures) 
        self.left_acceleration_df = get_acceleration(df=self.data, dt=self.dt, x='l_wrist_x', y='l_wrist_y', z='l_wrist_z')
        self.right_acceleration_df = get_acceleration(df=self.data, dt=self.dt, x='r_wrist_x', y='r_wrist_y', z='r_wrist_z')

        # calculating vector magnitudes for each arm
        self.left_vector_magnitude = calculate_vector_magnitude(self.left_acceleration_df['accel_x'], 
                                                                self.left_acceleration_df['accel_y'], 
                                                                self.left_acceleration_df['accel_z'])
        self.right_vector_magnitude = calculate_vector_magnitude(self.right_acceleration_df['accel_x'], 
                                                                self.right_acceleration_df['accel_y'], 
                                                                self.right_acceleration_df['accel_z'])        

        # calculating hours of use for each arm
        self.left_hours_of_use = calculate_hours_of_use(self.left_vector_magnitude, threshold=self.threshold, dt=self.dt)
        self.right_hours_of_use = calculate_hours_of_use(self.right_vector_magnitude, threshold=self.threshold, dt=self.dt)

        # calculating use ratio
        self.use_ratio = self.left_hours_of_use / self.right_hours_of_use

        # calculating magnitude ratio
        self.magnitude_ratio = calculate_magnitude_ratio(self.left_vector_magnitude, self.right_vector_magnitude)

        # calculating biltateral magnitude
        self.bilateral_magnitude = calculate_bilateral_magnitude(self.left_vector_magnitude, self.right_vector_magnitude)

        # calculating elbow angles
        self.left_elbow_angle = calculate_elbow_angles(shoulder=
                                                      np.column_stack((self.data['l_shoulder_x'], self.data['l_shoulder_y'], self.data['l_shoulder_z'])), 
                                                      elbow=
                                                      np.column_stack((self.data['l_elbow_x'], self.data['l_elbow_y'], self.data['l_elbow_z'])), 
                                                      wrist=
                                                      np.column_stack((self.data['l_wrist_x'], self.data['l_wrist_y'], self.data['l_wrist_z'])), 
                                                      upper_arm_length=self.upper_arm_length, forearm_length=self.forearm_length)
        self.right_elbow_angle = calculate_elbow_angles(shoulder=
                                                      np.column_stack((self.data['r_shoulder_x'], self.data['r_shoulder_y'], self.data['r_shoulder_z'])), 
                                                      elbow=
                                                      np.column_stack((self.data['r_elbow_x'], self.data['r_elbow_y'], self.data['r_elbow_z'])), 
                                                      wrist=
                                                      np.column_stack((self.data['r_wrist_x'], self.data['r_wrist_y'], self.data['r_wrist_z'])), 
                                                      upper_arm_length=self.upper_arm_length, forearm_length=self.forearm_length)

    # function to make a density plot out of the magnitude ratio and bilateral magnitude -> visualizes the activity of each arm (assymetry in figure means assymerty in usage)
    def density_plot(self):
        sns.displot(x=-1*self.magnitude_ratio, y=self.bilateral_magnitude, binwidth=(0.5, 10) ,cbar=True, cmap='plasma')
        plt.xlabel('Magnitude ratio')
        plt.ylabel('Bilateral magnitude')
        plt.xlim((-8, 8))
        plt.show()
    
    def magnitude_histogram(self, arm, scale):
        if arm == 'l':
            plt.hist(self.left_vector_magnitude, bins=20)
        if arm == 'r':
            plt.hist(self.right_vector_magnitude, bins=20) 
        plt.yscale(scale)  # Set y-axis to logarithmic scale
        plt.xlabel('Magnitude')  # Add x-axis label
        plt.ylabel(f'Frequency ({scale} scale)')  # Add y-axis label
        plt.title('Magnitude Histogram')  # Add title
        plt.ylim((0, 10**2))
        plt.xlim((0, 60))
        plt.show()


class DataViz():
    '''
    Class to visualize positional data, nice to have class because might want to have multiple datasets of different people/times to compare.
    '''
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.data.dropna(how='any', inplace=True)

    def plot_2d(self, view, arm):
        '''
        'view' can be either 'top', 'right' or 'front' for different views
        'arm' can be either 'l', 'r' or 'both' for the left or right arm respectively.

        thoughts: does not need to be perfectly scaled with the image, just give a good indication of the movements
        more thoughts: can add functionality to plot wrist/elbow/shoulder coordinates if required... although wrist seems most informative.
        '''
        if arm == 'r' or arm == 'l':
            x = self.data[f'{arm}_elbow_x'].values * 10# * 10 for scaling to the image
            y = self.data[f'{arm}_elbow_y'].values * 10
            z = self.data[f'{arm}_elbow_z'].values * 10
        elif arm == 'both':
            # implement later
            ...
        else:
            print('arm variable must be either l for left or r for right arm or both for both!')

        fig, ax = plt.subplots()

        if view == 'top':
            hull = ConvexHull(np.column_stack((x, y)))
            ax.scatter(x, y, alpha=0.05)
            img = imread('images/top_view.jpg', format='gray')
            if arm == 'r':
                ax.imshow(img, cmap='gray', extent=(-88, img.shape[1]-88, -155, img.shape[0]-155))
            elif arm == 'l':
                ax.imshow(img, cmap='gray', extent=(-317, img.shape[1]-317, -155, img.shape[0]-155))
            for simplex in hull.simplices:
                ax.plot(x[simplex], y[simplex], 'k-', lw=5, alpha=0.5)
            ax.fill(x[hull.vertices], y[hull.vertices], 'b', alpha=0.05)
        elif view == 'front':
            hull = ConvexHull(np.column_stack((x, z)))
            ax.scatter(x, z, alpha=0.05)
            img = imread('images/front_view.jpg')
            if arm == 'r':
                ax.imshow(img, cmap='gray', extent=(-105, img.shape[1]-105, -378, img.shape[0]-378))
            elif arm == 'l':
                ax.imshow(img, cmap='gray', extent=(-348, img.shape[1]-348, -378, img.shape[0]-378))
            for simplex in hull.simplices:
                ax.plot(x[simplex], z[simplex], 'k-', lw=5, alpha=0.5)
            ax.fill(x[hull.vertices], z[hull.vertices], 'b', alpha=0.05)
        elif view == 'side':
            hull = ConvexHull(np.column_stack((y, z)))
            ax.scatter(-1*y, z, alpha=0.05)
            if arm == 'r':
                img = imread('images/side_view_right.jpg')
                ax.imshow(img, cmap='gray', extent=(-131, img.shape[1]-131, -364, img.shape[0]-364))
            elif arm == 'l':
                img = imread('images/side_view_left.jpg')
                ax.imshow(img, cmap='gray', extent=(-131, img.shape[1]-131, -364, img.shape[0]-364))
            for simplex in hull.simplices:
                ax.plot(-1*y[simplex], z[simplex], 'k-', lw=5, alpha=0.5)
            ax.fill(-1*y[hull.vertices], z[hull.vertices], 'b', alpha=0.05)

        else:
            print('view must be either top, front or side!')
        plt.show()

processor = DataProcessor(data_path='test_data/left_active_right_inactive.csv', user=1234, threshold=0.2, dt=0.5)
processor.density_plot()

#Visualiser = DataViz(data_path='test_data/left_active_right_inactive.csv')
#Visualiser.plot_2d(view='side', arm='r')