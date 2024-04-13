
## New implementations

We drastically improved the speed of our dashboard this week by implementing multi-index filtering, as opposed to string matching. This cut our loading times for startup and filtering by 30 seconds. 

One of the main improvements we made this week was ensuring the interdependency of all of the dropdowns. We resolved bugs where an origin destination pair was marked as available in years where there was no data. To achieve this we used the year slider as input to the other two dropdowns. 

We also fixed a bug in the filtering mechanism when no option was selected and ensured that charts would not display without any data.

Another major change was revising the unique flight count chart to show the intended data. This makes it far more useful than previously, where it was displaying a count of 1 for all airlines, regardless of the number of flights.

We implemented a complete redesign of the summary cards, aligning them with the theme of the dashboard. We also improved the map by adding labels for the origin and destination cities, changing the color scheme and features. We also chose a far less jarring color scheme for our delay time bar chart and unique flight count chart. 

Another minor change was realigning the summary text on the control panel.

Finally, we also modularised our code, ensuring that it is much easier to debug.

## What is not yet implemented

Map interactivity has not yet been implemented. We would also like to improve the probability graph in the bottom right, for instance by allowing the user to click on a city on the map.

We have not yet implemented a data table showing individual flight data.

## Current limitations

We encountered some problems with getting the Python paths working both locally and with onrender. Currently, we are importing modules using src.components etc, but this does not work locally so we have been deleting the src prefix for local development. We would like to fix that next week.

Overall, this week’s dashboard is hugely improved over last week, both in terms of efficiency, appearance and functionality.



