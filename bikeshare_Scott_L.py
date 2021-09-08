# we want to inform the user that we're exploring bikeshare data from one of three cities
# they will select a city
# they will then choose to filter data by month, day or none
# we will build the dataframe according to their selections
# answer questions per time, stations, and user data

import pandas as pd
import numpy as np
import time
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# print the messages and sleep
def print_sleep(message_to_print):
    print(message_to_print)
    time.sleep(2.5)

def intro():
    print_sleep("Let's explore some US bikeshare data!")
    print_sleep("\nWe have 3 cities to choose from: Chicago, New York City and Washington")

# Get inputs from user, city, month, day
def user_inputs():
# Choose a City
    while True:
        cities = ['chicago','new york city','washington']
        city = input("\nWhich city would you like to explore?").lower()
        if city in cities:
            print_sleep(city.title() + " it is.")
            break
        else:
                print("Invalid response. Please try again:")
                continue

# Filter by Month
    while True:
        filters = ['month','day','all','none']
        print_sleep("\nLet's filter our data. We can do this by month, day or both.")
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = input("\nWe'll use the first 6 months: January, February, March, April, May, June.\n\nPlease select a month, or choose all:\n").lower()
        if month in months:
            print_sleep("\nCool, let's look more closely at " + month.title() + ".")
            break
        elif month == 'all':
            break
        else:
            if month not in months and month != 'all':
                print("Invalid response. Please try again:")
                continue

# Filter by Day
    while True:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input("\nWould you also like to filter by day of the week: Monday - Sunday.\nPlease select a day of the week, or choose all:\n").lower()
        if day in days:
            print_sleep("\nOkay, " + day.title() + " is our chosen day.")
            break
        elif day == 'all':
            break
        else:
            if day not in days and day != 'all':
                print("Invalid response. Please try again:")
                continue

    print_sleep("\nYOUR SELECTIONS\ncity: {}\nmonth: {}\nday: {}".format(city.title(), month.title(), day.title()))
    return city, month, day

# Generate the DataFrame
def load_data(city, month, day):

    # city yields dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract the month and day
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1

        # filter by month to create new DF
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

### Questions to answer based off df results

###### popular times data
def popular_time_data(df):

    #start timer to calculate executions
    print_sleep("\nCalculating bikeshare data for time stats...")
    start_time = time.time()

    # most common month to ride - mode
    print("\nThe most popular month is", df['month'].mode()[0])

    # most common day of the day of week
    print("The most popular day is", df['day_of_week'].mode()[0])

    # most common hour to ride
    df['hour'] = df['Start Time'].dt.hour
    print("The most common hour to ride is", df['hour'].mode()[0])

    # stop timer
    e_t = ("execution: %s seconds" % (time.time() - start_time))

    print(e_t)
    time.sleep(2)

###### stations data
def popular_stations_data(df):

    # start timer to calculate executions
    print_sleep("\nCalculating bikeshare data for station stats...")
    start_time = time.time()

    # most common starting station
    print("\nThe most popular Start Station is:",df['Start Station'].mode()[0])

    # most common end station
    print("The most popular End Station is:",df['End Station'].mode()[0])

    # most common trip from start to finish - (combo of start/end stations)
    df['Common Trip'] = df['Start Station'] + " to " + df['End Station']
    print("The most common trip is:",df['Common Trip'].mode()[0])

    # stop timer
    e_t = ("execution: %s seconds" % (time.time() - start_time))
    print(e_t)
    time.sleep(2)

###### trip data
def trip_duration_data(df):

    # start timer to calculate executions
    print_sleep("\nCalculating bikeshare data for trip stats...")
    #start timer
    start_time = time.time()

    # total travel time
    print("\nTotal travel time is", df['Trip Duration'].sum())

    # average travel time
    print("Average travel time is", df['Trip Duration'].mean())

    e_t = ("execution: %s seconds" % (time.time() - start_time))
    print(e_t)
    time.sleep(2)

####### user data
def user_data(df, city):

    # start timer to calculate executions
    print_sleep("\nCalculating bikeshare data for user stats...")
    #start timer
    start_time = time.time()

    # count each type of user
    user_type = df['User Type'].value_counts()
    print("\nUser Type count:", user_type)

    # counts gender type (only available NYC and Chicago)
    cities2 = ['chicago','new york city']
    if city in cities2:
        gender = df['Gender'].value_counts()
        print("Gender Type count:", gender)
    else:
        pass

    # earliest, most recent, most common birth year (only available NYC and Chicago)
    if city in cities2:
        print("The earliest birthday is", df['Birth Year'].min())
        print("The most recent birthday is", df['Birth Year'].max())
        print("The most common birth year is", df['Birth Year'].value_counts())

    e_t = ("execution: %s seconds" % (time.time() - start_time))
    print(e_t)
    time.sleep(2)

def display_data(df):
    while True:
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
        start_loc_x = 0
        start_loc_y = 5
        if view_data == 'yes':
            print_sleep(print(df.iloc[start_loc_x:start_loc_y]))
            break
        elif view_data == 'no':
            continue
        else:
            if view_data != 'yes' or 'no':
                print("Invalid response. Please try again.")
                continue
    while True:
        view_display = input("Do you wish to see the next 5 rows, or quit?\nEnter yes or quit.").lower()
        if view_display == 'quit':
            print_sleep("Have a nice day!")
            break
        elif view_display =='yes':
            start_loc_x += 5
            start_loc_y += 5
            print_sleep(print(df.iloc[start_loc_x:start_loc_y]))
            continue
        else:
            if view_display != 'yes' or 'quit':
                print("Invalid response. Please try again.")
                continue

# run the program
def run():
    while True:
        intro()
        city, month, day = user_inputs()
        df = load_data(city, month, day)
        popular_time_data(df)
        popular_stations_data(df)
        trip_duration_data(df)
        user_data(df, city)
        display_data(df)
        replay = input("\nWould you like to explore more?\nPlease choose yes or no:").lower()
        if "yes" in replay:
            run()
        elif "no" in replay:
            print_sleep("\nThanks for exploring! Have a nice day!")
            break
        else:
            if "yes" and "no" not in replay:
                print("Invalid response. Please try again:")
                continue
