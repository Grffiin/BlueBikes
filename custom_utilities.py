import numpy as np
import pandas as pd

# gets the row's time step start's month name
def month_name(row):
    return row["time_step_start"].month_name()

# gets the row's time step start's day name
def day_name(row):
    return row["time_step_start"].day_name()

# determines if the row's time step start is on a weekend 
def is_weekend(row):
    return row["time_step_start"].day_name() in ["Saturday", "Sunday"]

# determines if the row's time step start is during the night
def is_night(row):
    hour = row["time_step_start"].hour
    return 18 <= hour < 24 or 0 <= hour < 7

# determines the row's time step start's season
# (using meteorological seasons see: 
# https://www.timeanddate.com/calendar/aboutseasons.html)
def season(row):
    month = row["time_step_start"].month
    if 3 <= month < 6:
        return "Spring"
    if 6 <= month < 9:
        return "Summer"
    if 9 <= month < 12:
        return "Fall"
    return "Winter"

# gets the row's time step start's day of the month
def day_of_month(row):
    return row["time_step_start"].day

# determines in which third of the month the row's time step start is 
# First: [1, 10]; Second: (10, 20], Third: (20, {28, 29, 30, 31}]
def thirth_of_month(row):
    day = row["time_step_start"].day
    if 0 < day <= 10:
        return "First"
    if 10 < day <= 20:
        return "Second"
    if 20 < day:
        return "Third"

# determines in which part of the day the row's time step start is
# Early Morning: 5am to 9am; Mid Day: 9am to 3pm; 
# Afternoon: 3pm to 7pm; Evening: 7pm to midnight;
# Late Night: midnight to 5am  
def part_of_day(row):
    hour = row["time_step_start"].hour
    if 5 < hour <= 9:
        return "EarlyMorning"
    if 9 < hour <= 15:
        return "Midday"
    if 15 < hour <= 19:
        return "Afternoon"
    if 19 < hour <= 24:
        return "Evening"
    return "LateNight"

# gets the row's time step start's hour
def hour_of_day(row):
    return row["time_step_start"].hour

# Loads this precomputed extracted features dataset
def load_popular_stations_extracted_data(demand_cutoff):
	# Path to the extracted features dataset
	extracted_path = "/content/drive/My Drive/DS 3000 Final Project/CSVs/hourly.extracted_features.final.csv"
	dtypes_dict = { 
	    # defaults for: "time_step_start", "time_step_end", "station", 
	    #               "latitude", "longitude", "municipality",
	    #               "PRCP", "SNOW", "TMIN", "TMAX", "TAVG"
	    # Setting these for better memory management
	    "total_docks": np.int8,
	    "trips_from_station": np.int16,
	    "trips_to_station": np.int16,
	}

	extracted = pd.read_csv(extracted_path, dtype = dtypes_dict, 
	                        usecols=["station", "trips_from_station", 
	                                 "PRCP", "SNOW", "TMIN", "TMAX", "TAVG", 
	                                 "month_name", "day_name", "is_weekend", 
	                                 "is_night", "season", "day_of_month", 
	                                 "part_of_day", "hour_of_day"])

	# Culling the extracted_features dataset down to only the popular stations
	ehds = extracted.groupby("station").sum()
	epopular_stations_ids = ehds.loc[ehds["trips_from_station"] > demand_cutoff].index
	epopular_stations = extracted.loc[extracted["station"].isin(epopular_stations_ids)].copy()
	return epopular_stations

# gets the data in the range (start, end] (for the given colname) on the given dataset
def get_data_in_range(data, start, end, colname):
    mask = (data[colname] > start) & (data[colname] <= end)
    return data.loc[mask]

# Recovers the category names after one hot encoding
def recover_cat_names(categories, colnames):
    colnames = colnames.tolist()
    for i in range(0, len(categories)):
        real_cat_name = categories[i]
        gen_cat_name = f"x{i}"
        for j in range(0, len(colnames)):
            colnames[j] = colnames[j].replace(gen_cat_name, real_cat_name)
    return colnames