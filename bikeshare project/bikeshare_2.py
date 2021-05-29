import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

cities = ["chicago", "new york city", "washington"]
months = {"all": 0, "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8,
          "september": 9, "october": 10, "november": 11, "december": 12}
days = {"All": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}

all_months = False
all_days = False


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    city = ""
    valid = False
    while not valid:
        city = input("\nwould tou like to see data for chicago, new york city, or washington? \n").lower().strip()
        valid = city in cities
        if not valid:
            print("please enter a valid option \n")

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ""
    valid = False
    while not valid:
        month = input("\nwhich month do you want to filter? type 'all' if you want all months \n").lower().strip()
        valid = month in months
        if not valid:
            print("please enter a valid option \n")

    if month == "all":
        """ will be used later 
        if true we will print the most common month 
        else  we will be filtering only one month"""
        global all_months
        all_months = True
    else:
        all_months = False

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    valid = False
    while not valid:
        day = input("\nwhich day do you want to filter? type 'all' if you want all days \n").title().strip()
        valid = day in days
        if not valid:
            print("please enter a valid option \n")

    if day == "All":
        """ will be used later 
        if true we will print the most common day 
        else  we will be filtering only one day"""
        global all_days
        all_days = True
    else:
        all_days = False

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df["Start Time"] = pd.to_datetime(df["Start Time"])

    df['month'] = df["Start Time"].dt.month
    df['day'] = df["Start Time"].dt.weekday_name
    df['hour'] = df["Start Time"].dt.hour

    if month != 'all':
        """we will use all months if month == 'all' """
        df = df[df['month'] == months[month]]

    if day != 'All':
        """we will use all months if days == 'all' """
        df = df[df['day'] == day]

    return df


def get_key(dictionary, search_val):
    """get the key of the dictionary using the value"""
    for key, value in dictionary.items():
        if search_val == value:
            return key


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if all_months:
        print("the most common month:\n{}\n".format(get_key(months, df['month'].mode()[0])))
    else:
        print("we are filtering one month only\n")

    # display the most common day of week
    if all_days:
        print("the most common day:\n{}\n".format(df['day'].mode()[0]))
    else:
        print("we are filtering one day only\n")

    # display the most common start hour
    print("the most common start hour:\n{}\n".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("the most common start station:\n{}\n".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("the most common end station:\n{}\n".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print("the most frequent combination of start station and end station:\n('{}', '{}')\n".format(
        df[['End Station', 'Start Station']].mode()['Start Station'][0],
        df[['End Station', 'Start Station']].mode()['End Station'][0]))

    print("the most common trip: \n{}\n".format(
        (" from '" + df['Start Station'] + "' to '" + df['End Station'] + "' ").mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def convert_time(seconds):
    """convert time from seconds to: (weeks, days, hours, minutes, seconds) to make it more readable for the user

    descreption :
        week = 7 day, day = 24 hour, hour = 60 minute, minute = 60 seconds

        week = 7 * 24 * 60 * 60 second
        number of weeks = seconds / (7 * 24 * 60 * 60)

        day = 24 * 60 * 60 second
        number of days = seconds / (24 * 60 * 60) - (7 * number of weeks)
        note : we sabtract to get the remainder of weeks (5 days isn't a complete week)

        etc.....

    """
    weeks = seconds // (7 * 24 * 60 * 60)
    days = seconds // (24 * 60 * 60) - (7 * weeks)
    hours = seconds // (60 * 60) - (7 * 24 * weeks) - (24 * days)
    minutes = seconds // 60 - (7 * 24 * 60 * weeks) - (24 * 60 * days) - (60 * hours)
    seconds = seconds - (7 * 24 * 60 * 60 * weeks) - (24 * 60 * 60 * days) - (60 * 60 * hours) - (60 * minutes)

    return weeks, days, hours, minutes, round(seconds, 1)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    weeks, days, hours, minutes, seconds = convert_time(df['Trip Duration'].sum())

    print("total travel time:\n{} Weeks : {} Day : {} Hour : {} Minutes : {} Seconds \n".format(weeks, days, hours,
                                                                                                minutes, seconds))

    # display mean travel time
    weeks, days, hours, minutes, seconds = convert_time(df['Trip Duration'].mean())

    print("mean travel time:\n{} Weeks : {} Day : {} Hour : {} Minutes : {} Seconds \n".format(weeks, days, hours,
                                                                                               minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        print("counts of user types:\n{}\n".format(df['User Type'].value_counts().to_string()))
    except:
        print("no user types data to share")

    # Display counts of gender
    try:
        print("counts of gender:\n{}\n".format(df['Gender'].value_counts().to_string()))
    except:
        print("no gender data to share")

    # Display earliest, most recent, and most common year of birth
    try:
        print("earliest year of birth:\n{}\n".format(int(min(df['Birth Year']))))
        print("most recent year of birth:\n{}\n".format(int(max(df['Birth Year']))))
        print("most common year of birth:\n{}\n".format(int(df['Birth Year'].mode()[0])))
    except:
        print("no birth year data to share")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """ asking the user if he wants to display some data """
    i = 0
    raw = input("would you like to view individual trip data? type 'yes' or 'no'\n").lower().strip()

    pd.set_option('display.max_columns', 200)

    while True:
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i + 5])
            raw = input("\nwould you like to view individual trip data? type 'yes' or 'no'\n").lower().strip()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower().strip()


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day, "\n")
        df = load_data(city, month, day)

        if df.empty:
            print("no data available for this filter!")
        else:
            display_raw_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()
        while not restart in ['yes', 'no']:
            restart = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower().strip()

        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
