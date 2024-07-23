import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze which is very important
        (str) month - name of the month to filter by, or "all" to apply no month filter, as the user wishes
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s see some data for cities in the United States regarding bike usage!')

    # get user input for city
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter a valid city name (Chicago, New York City, Washington).")

    # get user input for month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? January, February, March, April, May, June, or 'all' to apply no month filter? ").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please enter a valid month (January, February, March, April, May, June) or 'all'.")

    # get user input for day of week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all' to apply no day filter? ").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) or 'all'.")

    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nAbout to calculate most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', common_end_station)

    # display most frequent combination of start station and end station trip
    df['start_end_combination'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['start_end_combination'].mode()[0]
    print('Most Frequent Combination of Start Station and End Station Trip:', common_trip)

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total Travel Time:', total_duration)

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_duration)

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types:')
    print(user_types)

    # Display counts of gender (if available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].dropna().value_counts()
        print('\nCounts of gender:')
        print('Male: {}'.format(gender_counts.get('Male', 0)))
        print('Female: {}'.format(gender_counts.get('Female', 0)))
    else:
        print('\nGender data is not available.')

    # Display earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df.columns:
        # Drop NaN values before calculating statistics
        birth_years = df['Birth Year'].dropna()
        earliest_year = int(birth_years.min())
        most_recent_year = int(birth_years.max())
        most_common_year = int(birth_years.mode()[0])
        print('\nEarliest year of birth: {}'.format(earliest_year))
        print('Most recent year of birth: {}'.format(most_recent_year))
        print('Most common year of birth: {}'.format(most_common_year))
    else:
        print('\nBirth year data is not available.')

    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data upon request by the user in chunks of 5 lines."""

    print('\nDisplaying Raw Data...\n')
    start_index = 0
    while True:
        while True:
            show_data = input("Would you like to see 5 lines of raw data? Enter yes or no: ").strip().lower()
            if show_data in ['yes', 'no']:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if show_data == 'no':
            break

        end_index = start_index + 5
        print(df.iloc[start_index:end_index])
        start_index = end_index

        if start_index >= len(df):
            print("No more data to display.")
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
