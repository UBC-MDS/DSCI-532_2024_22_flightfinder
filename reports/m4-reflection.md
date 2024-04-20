This week, we implemented major improvements to our app, enhancing both its performance and appearance. We significantly boosted the app's speed by converting data into Parquet files and processing redundant data before loading it into memory. Additionally, we introduced a caching mechanism for the dropdown functions, enabling automatic loading of data for previously selected routes.

To improve user experience, we added a full-screen loader that clearly indicates the data is being filtered and not yet displayed. A new submit button was incorporated, allowing charts to be generated only after the user's confirmation, further optimizing performance.

Visually, we refined our app by removing unnecessary titles from the map and the delay time bar chart, adjusting the sidebar text width, and introducing a plain logo that complements our dashboard's aesthetic. We unified the color scheme for location markers on the map for consistency and ensured the same airline is represented with consistent colors across different bar charts.

We also adjusted the X-axis of our histogram of delay probabilities to a logarithmic scale, enhancing the visibility of smaller delays while highlighting potential extreme delays.

While we aimed for more detailed enhancements, memory constraints limited the granularity of information about specific flights, their times, airlines, and flight codes. Despite these limitations, our dashboard effectively showcases the reputation of airlines across various U.S. routes, providing users with a reliable starting point for choosing an airline.

Throughout this development phase, we found the Plotly documentation exceptionally helpful. Its straightforward examples were crucial in quickly establishing the basic functionality of different dashboard components.
