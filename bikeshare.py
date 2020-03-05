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
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #  To get user input for city (chicago, new york city, washington). 
    city = str(input("Would you like to see data for Chicago, New York City or Washington?"))
    while (city.lower() not in ('chicago','new york city','washington')):
        if city.lower() in ('chicago','washington','new york city'):
            print('City: {}'.format(city))
            break
        else:
            city = str(input("Incorrect city. What is the name of the city to analyze?"))

    # To get user input for month (all, january, february, ... , june)
    result = str(input("Would you like to filer the data by month, day, both or none? (Type none for no filters)"))
    if result == 'month' or result == 'both' or result == 'all':
        month = str(input("Which month? (January, February, March, April, May, June)"))
        while (month.lower() not in ('january','february','march','april','may','june')):
            if month.lower() in ('january','february','march','april','may','june'):
                print('Month: {}'.format(month))
                break
            else:
                month = str(input("Incorrect month. Please re-enter month to analyze?"))
    if result == 'month':
        day = 'all'
                
    # To get user input for day of week (all, monday, tuesday, ... sunday)
    if result == 'day' or result == 'both' or result == 'all':
        day = str(input("Which day? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)"))
        while (day.lower() not in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')):
            if day.lower() in ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
                print('Day: {}'.format(day))
                break
            else:
                day = str(input("Incorrect Day. Please re-enter day to analyze?"))
    if result == 'day':
        month = 'all'
    if result == 'None' or result == 'none':
        month = 'all'
        day = 'all'
    print('-'*40)
    print(city, month, day)
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
    city = city.lower()

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] =  pd.to_datetime(df['Start Time'])
    df['month_of_year'] = df['Start Time'].dt.month 
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month_of_year'] == month]
    
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
	
	Args:
		df - Pandas DataFrame containing city data filtered by month and day
    
	Returns:
        most_common_month, most_common_day, most_common_hour"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mcm = df['month_of_year'].mode()[0]
    print('Most Common Month:', mcm)
    
    # display the most common day of week
    mcd = df['day_of_week'].mode()[0]
    print('Most Common Month:', mcd)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    mch = df['hour'].mode()[0]
    print('Most Common Hour:', mch)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
	
	Args:
		df - Pandas DataFrame containing city data filtered by month and day
    
	Returns:
        most_common_start_station, most_common_end_station, most_common_start_end_station"""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mcss = df['Start Station'].mode()[0]
    print('Most Common Start Station:', mcss)

    # display most commonly used end station
    mced = df['End Station'].mode()[0]
    print('Most Common End Station:', mced)

    # display most frequent combination of start station and end station trip
    df['Start_End']=df['Start Station']+' and '+df['End Station']
    mcses = df['Start_End'].mode()[0]
    print('Most Common Start to End Station:', mcses)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
	
	Args:
		df - Pandas DataFrame containing city data filtered by month and day
    
	Returns:
        total_travel_time, avg_travel_time"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttt = sum(df['Trip Duration'])
    print('Total Travel Time:', ttt)

    # display mean travel time
    avt = np.mean(df['Trip Duration'])
    print('Total Travel Time:', avt)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
	
	Args:
		df - Pandas DataFrame containing city data filtered by month and day
		city - city of the df selected by the user
		
	Returns:
        count_user_types, count_gender, earliest_year, recent_year, most_common_year"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('Count of User Types:', count_user_types)

    # Display counts of gender for New York City and Chicago only
    city = city.lower()
    if city == 'new year city' or city == 'chicago':
        count_gender = df['Gender'].value_counts()
        print('Count of Gender:', count_gender)

        # Display earliest, most recent, and most common year of birth for New York City and Chicago only
        earliest_year = df['Birth Year'].min()
        print('Earliest Year of Birth:', earliest_year)
        recent_year = df['Birth Year'].max()
        print('Most Recent Year of Birth:', recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print('Most Common Year of Birth:', most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Asks user to say yes or no to show raw data.
    
    Arguments:
    df - Pandas DataFrame.
    
    Returns:
    df_raw - Any 5 rows of the Pandas DataFrame 
    """

    #  To get user input to see raw data
    answer = str(input("Would you like to see raw data?"))
    while answer.lower() =='yes':
        df_raw = df.sample(n=5)
        print(df_raw)
        answer = str(input("Would you like to see raw data again? (yes or no)"))
        if answer.lower() == 'no':
            break
        while answer.lower() not in ('yes','no'):
            answer = str(input("Incorrect selection. Enter yes or no?"))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
