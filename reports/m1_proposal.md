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
- `AIRLINE_CODE`, `ORIGIN_CITY`, `DEST_CITY`, `FL_DATE` for essential information about each flight and filter.
- `AIR_TIME` for flight time.
- `ARR_DELAY` for arrival delay.

We will also derive the following summary statistics:
- Percentage of flights on time.
- Average flight time.
- Average arrival delay.
- Average arrival delay by airline.
- Number of flights by each airline on each day of the week.