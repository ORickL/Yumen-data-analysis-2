# Yumen-data-analysis-2

## This is a GitHub repository for visualizing positional data acquired by the Yumen sensor system.

The folder visualisation literature contains pdfs with different methods to visualise/calculate different metrics.

The Notebook files contain code to apply these methods to the data acquired by the Yumen sensor system.
  - 2d_plots.ipynb contains code to visualise the x, y, z coordinates in a 2d space (top, front and side views) along with a convex hull to clearly visualise movement boundaries.
  - SQL_csv_processing.ipynb contains code to read a .csv as we would get from running SQL commands from our database.
  - variable_calculation.ipynb contains code to calculate various measures such as:
    - Hours of use (per limb).
    - Use ratio.
    - Magnitude ratio.
    - Bilateral magnitude.
    - Making density plots.
  These variables are further explained in the notebooks.
  
There are example plots (2d plots and density plots) in the /images folder.

These are results from the python API using data collected from our sensor system.

Activity comparison (low activity in the top images and high activity in the bottom images).
The histogram to the right show a higher frequency of low vector magnitudes in the low activity data.
![activity comparison](https://user-images.githubusercontent.com/90693914/231167934-27a9a7cd-65d5-429b-92ee-d00fd9ac2016.png)

This distribution plot shows on the x-axis the magnitude ratio (close to -7 and 7 means high contribution of the left and right arm respectively) and on the y-axis the bilateral magnitude (a measure of the intensity of a movement for both arms combined).
![displot_activity](https://user-images.githubusercontent.com/90693914/231167988-83a74770-9177-46e3-98c8-a776de133945.png)


TO-DO's:
- Make all the data visualisations more visually appealing. X
- Remove start/end times and user from dataprocessor.py, The correct data should be pulled using correct SQL queries and can then be input into these scripts. 

