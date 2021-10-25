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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while(True):
        city = input("Type name of City (chicago, new york city, washington) to filter for\n").lower()
        if(city in ['chicago', 'new york city', 'washington']):
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ""
    while(True):
        print("Type name of Month to Filter for (all, january, february, march, ... , june)")
        month = input()
        if(month in ['january', 'february', 'march', 'april', 'may', 'june','all']):
                     break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while(True):
        print("Type Name of Week day to filter for (all, sunday, monday, tuesday, wednesday, thursday, friday, saturday)")
        day = input()
        if(day in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']):
              break
              
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
        #days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        #day = days.index(day) + 1
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    mcm = df['month'].mode().values
    
    ## for handline more than one mode
    mcm = list(mcm) 
    for x in mcm:
        mcm[mcm.index(x)] = months[x - 1]
    print("most common month : ", mcm)

    # TO DO: display the most common day of week
    print("most common day of the week : ", df['day_of_week'].mode().values)

    # TO DO: display the most common start hour
    df['shour'] = pd.to_datetime(df['Start Time']).dt.hour
    print("most common start hour : ", df['shour'].mode().values)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("most common start station : ", df['Start Station'].mode().values)

    # TO DO: display most commonly used end station
    print("most common end station : ", df['End Station'].mode().values)

    # TO DO: display most frequent combination of start station and end station trip
    nf = df['Start Station'] + "%" + df['End Station']
    res = nf.mode().values
    res = list(res)
    for x in res:
        res[res.index(x)] = " (to) -> ".join(x.split("%"))
    print("most common combination of stations : ", res)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    diff = df['End Time'] - df['Start Time']
    total = pd.Timedelta(0)
    for x in diff:
        total = total + x

    print("Total Duration of all trips = ", total)
    
    # TO DO: display mean travel time
    print("Mean Travel Duration : ", diff.mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Number of Subscribers : ", sum(df['User Type'] == 'Subscriber'))
    print("Number of Customers : ", sum(df['User Type'] == 'Customer'))

    # TO DO: Display counts of gender
    if('Gender' in df):
        print("Number of Male Users : ", sum(df['Gender'] == 'Male'))
        print("Nunber of Female Users : ", sum(df['Gender'] == 'Female'))

    # TO DO: Display earliest, most recent, and most common year of birth
    if('Birth Year' in df):
        print("most common year of birth : ", df['Birth Year'].mode().values)
        print("most recent year of birth : ", df['Birth Year'].max())
        print("most earliest year of birth : ", df['Birth Year'].min())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while(view_data.lower() == 'yes'):
        print(df.iloc[start_loc:start_loc+5, :-3])
        start_loc += 5
        view_data = input('\nWould you like to view 5 more rows of individual trip data? Enter yes or no\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
