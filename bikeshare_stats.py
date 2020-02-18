import time
import pandas as pd
import os.path


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

    # Initialize local variables
    cities = ['chicago','new york city','washington']
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    days = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    valid_city = False
    valid_month = False
    valid_day = False

    print("Hello! Welcome to explore bikeshare data for US cities: Chicago,New York and Washington.")

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:  
        # request input from user in the form of integer to the respective city selection
        city = input("Please enter the cityname that you would like to explore bikeshare data: ").lower()
        #check the selection is between 1 and 3. If not, ask again for the valid city
        if city in CITY_DATA: 
            # if city found, exit while loop  
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while not valid_month:  
        #request input from user for specific month to filter data or all for no filter. 
        month = input("Please enter the month between January and June that you would like filter the data or all for no filter : ").lower()
        # check for valid month in predefined list
        valid_month = month in months
        # check for valid month. If not ask again for valid month
        if not valid_month:
            print("The input does not match, Try again")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while not valid_day:  
        #request input from user for specific day to filter data or all for no filter
        day = input("Please enter the day name like Sunday, Monday...Saturday that you would like filter the data or all for no filter : ").lower()
        #check for valid day in perdefined list
        valid_day = day in days
        #check for valid day. If not asj again for valid day name
        if not valid_day:
            print("The input does not match, Try again")
            
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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    # initialize local variables
    start_time = time.time()
    
    # TO DO: display the most common month
    
    # find the most common month
    common_month = df['month'].mode()[0]
    # display the most common month
    print("The most common month: {}".format(common_month))

    # TO DO: display the most common day of week
    
    # extract day name from the Start Time column to create day name column
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    #find most common day name
    popular_day = df['day_of_week'].mode()[0]
    # display most common day name
    print("The most Popular day: {}".format(popular_day))

    # TO DO: display the most common start hour
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    #find most common hour
    common_hour = df['hour'].mode()[0]
    # display most common hour
    print("The most Popular Start Hour: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    # initialize local variables
    start_time = time.time()

    # TO DO: display most commonly used start station
    
    # extract most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()   
    # display most commonly used start station
    print("The most commonly used start station: {}".format(start_station))

    # TO DO: display most commonly used end station
    
    # extract most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    #display most commonly used end station
    print("The most commonly used end station: {}".format(end_station))

    # TO DO: display most frequent combination of start station and end station trip
    
    # extract most frequent combination of start and end station trip
    trip = df.groupby(['Start Station','End Station']).size().idxmax()
    # display most frequent combination of start and end station trip
    print("The most frequent combination of start station and end station trip: {}".format(trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    # initialize local variables
    start_time = time.time()

    # TO DO: display total travel time
    
    # calculate total travel time 
    total_travel_time = df['Trip Duration'].sum()
    # display total travel time 
    print("Total travel time is: {}".format(total_travel_time))

    # TO DO: display mean travel time
    
    # calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    # calculate mean travel time 
    print("Mean travel time is: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    
    # initializr local variables
    start_time = time.time()
    user_types = None
    gender = None
    common_birth_year = None
    
    # TO DO: Display counts of user types
    
    # check for 'User Type' column exists in bike share data
    if 'User Type' in df.columns:
        # if yes calculate stats and assign to user_types
        user_types = df['User Type'].value_counts()
    # check if user_types data found
    if user_types is None:
        # if not display data is not available
        print("User Types data is not available")
    else:
        # if yes, display the data
        print("Counts of user types: {}".format(user_types))

    # TO DO: Display counts of gender
    
    # check for 'Gender' column exists in bike share data
    if 'Gender' in df.columns:
        # if yes calculate stats and assign to geneder
        gender = df['Gender'].value_counts()
    # check if gender data found
    if gender is None:
        # if not display data is not available
        print("Gender data is not available")
    else:
        # if yes, display the data
        print("Counts of Gender: {}".format(gender))

    # TO DO: Display earliest, most recent, and most common year of birth
    
    # check for 'Birth Year' column exists in bike share data
    if 'Birth Year' in df.columns:
        # if yes calculate stats and assign to common_birth_year
        common_birth_year = df['Birth Year'].mode()[0]
    # check if common_birth_year data found
    if common_birth_year is None:
        # if not display data is not available
        print("Birth Year data is not available")
    else:
        # if yes, display the data
        print("The most common birth year is: {}".format(common_birth_year))
    
        early_birth_year = df['Birth Year'].min()
        print("The earliest birth year is: {}".format(early_birth_year))

        recent_birth_year = df['Birth Year'].max()
        print("The most recent birth year is: {}".format(recent_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    index1 = 0
    index2 = 5
    while True:
        # get the inputs 'city','month','day' from user to filter bikeshare data
        city, month, day = get_filters()
        #check if file exists 
        if os.path.exists(CITY_DATA[city]):
            # load the data from csv files to panda dataframe data structure for the given inputs from user
            df = load_data(city, month, day)
            
            # call to find time statistics 
            time_stats(df)
            # call to find station statistics
            station_stats(df)
            # call to find travel time statistics
            trip_duration_stats(df)
            # call to find user statistics
            user_stats(df)

            # task for asking user if they want see rawdata
            while True:
                # get the user input if they would like to rawdata
                display_rawdata = input('\nWould like to see rawdata in the incremental of 5 lines?  Enter yes or no. \n')
                if display_rawdata.lower() == 'yes' and len(df.index) >= index1:
                    # display first 5 rows of filtered bikeshare rawdata
                    print(df.iloc[index1:index2])
                    # increment indicies values by 5 to get next 5 rows
                    index1+=5
                    index2+=5
                else:
                    #if user input is no or all rows displayed then exit from this loop
                    break
            # check if user wants to see statistics for another set of inputs
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            # if yes, loop again. otherwise exit
            if restart.lower() != 'yes':
                break
        else:
            # if not, request ask for the data file to be placed in the current folder
            print("bikeshare data file not available in the current path. Please place the data file in the current path and then run this script")
            break


if __name__ == "__main__":
	main()
