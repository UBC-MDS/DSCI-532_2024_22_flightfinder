### Section 1: Motivation and Purpose

#### Our Role: Travel planning platform
#### Target Audience: Individual Travelers
Traveling, whether for leisure or business, requires careful planning. Delays are more than just minor inconveniences; they can disrupt connections, lead to missed engagements, and even affect accommodation plans. For individuals planning their travels, having access to historical flight data can provide an edge in making informed decisions to minimize disruptions.

Our dashboard is specifically designed for travelers, enabling them to navigate the complexities of air travel with ease and confidence:

- Historical Delay Patterns: Travelers can identify which times have the highest incidence of delays to avoid booking flights during those periods.
- Airline Punctuality Records: Our tool allows users to compare historical on-time performances of different airlines, making it easier to choose the most reliable one.
- Efficient Route Planning: The dashboard provides information on flight durations and distances, helping travelers select the most direct and time-efficient routes.
- Airport Performance Statistics: By presenting data on airport punctuality, travelers can choose to fly from airports with the best track records for on-time departures and arrivals.

### Section 2: Description of the data
We will use the Flight Delay and Cancellation Dataset
(https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023/data)
from kaggle.
This dataset contains information for 3 million flights and is sampled from approximately 30 million flights between January 2019 to August 2023.

We will use the following columns in the dataset:
- `AIRLINE`, `AIRLINE_CODE`, `ORIGIN_CITY`, `ORIGIN`, `DEST_CITY`, `DEST`, `FL_DATE` for essential information about each flight and filter.
- `AIR_TIME` for flight time.
- `ARR_DELAY` for arrival delay.

We will also derive the following summary statistics:
- Percentage of flights on time.
- Average flight time.
- Average arrival delay.
- Average arrival delay by airline.
- Number of flights by each airline on each day of the week.

### Section 4: App sketch & brief description

![Dashboard](../../img/sketch.png)

Our landing page ‘Overview’ shows a combination of summary statistics and visualizations relating to the delay times of flights between cities in the US. The side panel on the left contains input text boxes for the origin city and departure city. As the user types in one of these inputs, this will trigger a dropdown with cities present in the dataset. The year slider allows the user to select a timeframe for the data, for example, if they want to examine only flights in 2022 and 2023. These are essentially filters for the dataset.

There are three summary statistics displayed at the top of the landing page: the percentage of flights on time, the average flight time in hours and the average delay in minutes. These give the user an overall expectation for what delays might occur during their journey. Below this we have four visualizations. The first is a sorted bar chart of the average delay time by carrier. This allows the user to see which airline has the shortest delays and longest delays for their route. The best performing airline is highlighted in green and the worst in red, providing a visual intuition for the user. To the right of this, we include a stack bar-chart of the number of unique flights from each airline on each weekday, with tooltips on hover, showing the count and airline name. The user can identify which airlines operate on their intended travel day. A map of the route is also shown, as well as a bar chart showing the distribution of delays. This gives a sense of how likely it is that the users flight will be delayed by each amount. When the user hovers over this bar chart, a tooltip with appear “Based on past data, there is a 1% chance of a delay of at least 1hr.”

Finally, there is a tab at the top, which user a user can click to switch from the Overview page to the Flight data page. On the flight data page, the user can see metadata for individual flights, and can click the sort button above a column to sort by flights with the smallest delays and duration. This allows users to optimize their flight choice based on multiple criteria.
