## Which parts have we implemented so far?

In this milestone, we implemented the backbone of our FlightFinder dashboard. We created a control panel that provides inputs for the user to filter the flight data by year, origin and destination. We implemented three cards to display summary statistics for the selected route, including the percentage of flights on time, the average flight time and the average delay. 

In the main panel of our dashboard, we have implemented four charts. In the top left, we have a visualization of the average delay in minutes by carrier for the selected route. To the right of this we implemented a count of the unique flights per day. We also implemented a map showing the route between the origin and destination, and a histogram showing the probabilities of being delayed or early by a certain amount.

## Which parts have we done differently?

One aspect that we didn’t consider was that the user could select two cities that are not connected in the dropdown lists, leading to an error. We fixed this by implementing callbacks that filter the dropdown list options based on the city selected in the other dropdown.

Another aspect we did not consider in the previous milestone was obtaining the latitude and longitude coordinates. We found an additional dataset that has the latitude and longitude coordinates for major US airports, and we supplemented this with any missing data manually. This supplemented dataset was used to plot the latitude and longitude of each city on the map.

## Intentional deviations from visualization practices

One of the international deviations we have made is in the map. Normally, a map is only used if it is adding extra information. In this case, the route is already known. However, we believe that the inclusion of the map does increase how intuitive the dashboard feels, which is as important as providing deeper analyses. 

Another intentional deviation from visualization practices is the use of many colors in the top two charts. We believe that it is preferable to have a visual correspondence between the two charts and this is achieved most intuitively using colors.

## Features still in development

In our initial proposal we proposed a tab that allows the user to see the raw data for their selected route. This is still in development and increases the complexity of the app, so we did not include it yet in our milestone version.

## Limitations and potential future improvements

One of the current limitations of the app is that it does not allow a user to select an individual flight. We aim to add tab enabling the user to see the underlying datatables and examine individual flights. 

Another limitation is that some of the visualizations are underdeveloped. In particular, we aim to improve our map with further contextual information. We also want to make sure that the number of unique flights and probability of flight delay columns are as useful as possible. We could implement a link between the average delay by carrier column and the two other bar charts as a filtering mechanism.
