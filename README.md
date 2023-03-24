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
  
 This is an example density plot, which gives information on the usage of both hands. This can be intresting because it might show discrepancies between arm usage.
 
 ![density_plot](https://user-images.githubusercontent.com/90693914/227542445-78068e3b-a6ee-41b2-a089-c3d13c83cab7.png)
