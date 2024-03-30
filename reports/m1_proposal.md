### Section 1: Motivation and Purpose

#### Our Role: Aviation Data Analytics Firm
#### Target Audience: Airline Operations Managers & Individual Travelers
In the aviation industry, flight delays can have far-reaching consequences, not just for airline operations and financials, but also for travelers' schedules and satisfaction. Airline operations managers require in-depth analysis to streamline flight schedules and enhance operational efficiency. Meanwhile, individual travelers seek reliable information to plan their journeys effectively and avoid disruptions.

Our dashboard utilizes the "flights.csv" dataset to address these diverse needs by providing:

- Temporal Trend Analysis: To help all users identify the best times to fly and anticipate potential delays.
- Reliability Ratings: Travelers can compare delay records of different airlines, helping them choose the carrier with the best on-time performance for their needs.
- Airline Performance Benchmarking: Enabling industry professionals to assess and improve operational strategies, while also guiding travelers in choosing reliable airlines.
- Delay Analysis: Offering insights into service quality and delay patterns, assisting airlines in addressing issues and travelers in making informed choices.
- Route Efficiency Metrics: Assisting airlines and analysts in optimizing route planning, and informing travelers about typical flight durations and potential delays.
- Airport Performance Indicators: Equipping airports with data to enhance their operations and informing travelers about airports with better on-time records.

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
