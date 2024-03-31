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

### Section 3: Research questions and usage scenarios
Malissa is a financial consultant at Deloitte who travels often to meet with high-profile clients across the states and provide expert financial advice. Therefore, she needs to keep a rigorous schedule to make sure that she can attend the meetings on time with sufficient preparation, and thus getting to know more about the delay times of flights available between two locations is important to her.

Recently, she has been preparing for the onsite financial audits and strategy sessions held at New York City. To attend the sessions in person, she needs to travel from the city she lives, Seattle, to New York City. Her objective is to find flights that are consistently on time to maintain her strict schedule and to ensure she can maximize her productivity before and after flights. She can [select] the years for which she want to [extract] summary statistics, and [compare] the delay time across different airlines and different days of a week.

When Malissa logs in to our “Flight Finder” dashboard, she is immediately presented with a summary of flight statistics, including the percentage of flights on time, the average flight time in hours and the average delay in minutes. This gives her an overview of the travel from the origin to the destination that she specified. She can proceed with comparing the delay time for different airlines, different days of the week, and how probable the delay time would be around each time interval. With all these information, Malissa may find that Delta Air Lines outperform its counterparts, and that Thursday is among the days of the week with the least delay time. She will then proceed to the next page with all metadata of the flights, rank the durations to find the flights that span comparatively less amount of time. With much consideration, she decide to take the flight DL 927.