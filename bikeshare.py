import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please choose a city from these three cities:(chicago, new york city, washington)\n').lower()
    while city not in CITY_DATA:
        city = input('Please choose a city from the list\n')
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please choose a month from the list or you can choose all: (january, february, march, april, may, june) \n').lower()
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input('Sorry, Can you type the month correctly\n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please choose a day from the list or you can choose all: (monday, tuesday, wednesday, thursday, friday, saturday, sunday)\n').lower()
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input('Sorry, Can you enter the day correctly\n')

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        df = df[df['month'].str.lower() == month]
        
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('\nThe most common month is: ', popular_month)
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('\nThe most common day is: ', popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most common start hour is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_count = df['Start Station'].value_counts().max()
    print('\nThe most commonly used start station is:{}, and it has been used for {} times '.format(popular_start_station, popular_start_count)) 
          
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_count = df['End Station'].value_counts().max()
    print('\nThe most commonly used end station is:{}, and it has been used for {} times '.format(popular_end_station, popular_end_count))

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + ' -----> ' + df['End Station']
    popular_trip = df['start_end'].mode()[0]
    popular_trip_count = df['start_end'].value_counts().max()
    print('\nThe most frequent trip is:{}, and people took this trip for {} times'.format(popular_trip, popular_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    days, remainder = divmod(total_travel_time, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    print('\nThe total travel time is:{}days, {}hours, {}minutes, {}seconds'.format(days, hours, minutes,seconds))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is: {} seconds '.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe counts of each user type is:\n', user_types)
    
    # Check if you have Gender and birth year columns in the data frame
    try:
        # TO DO: Display counts of gender
        gender = df['Gender'].value_counts()
        print('\nThe counts of each gender is:\n', gender)

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print('\nThe earliest year of birth is:{}\nThe most recent year of birth is:{}\nThe most common year of birth is:{}'.format(earliest_year, recent_year, common_year))
    except:
        print('Sorry, the data set of Washington is missing information about gender and birth year.')
        pass
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    raw_data_display = input('\nWould you like to have a look on some raw data? Enter yes or no\n')
    if raw_data_display.lower() == 'yes':
        i = 0
        while True:
            print(df.iloc[i:i+5])
            i += 5
            if i < df.shape[0]-1:
                raw_data_display = input('Would you like to have a look on more raw data? Enter yes or no\n')
                if raw_data_display.lower() != 'yes':
                    break
                elif i >= df.shape[0]-5:
                    print(df.iloc[i:df.shape[0]-1])
                    print('\nNo more data to display\n')
                else:
                    pass
            
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
