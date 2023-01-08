import datetime
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York, or Washington ?\n").title()
    while city not in ["Chicago","New York","Washington"]:      
        city= input("Wrong answer !!\nWould you like to see data for Chicago, New York, or Washington ?\n").title()

    #get filter choice month , day , both and none
    filter_answer = input ('Would you like to filter the data by month, day, both, or not at all ? Type\"none\" for no time filter.\n').lower()
    while filter_answer not in ["month","day","both","none"]:
        filter_answer = input ('Wrong answer!!\nWould you like to filter the data by month, day, both, or not at all ? Type\"none\" for no time filter.\n').lower()
   
    # get user input for month (all, january, february, ... , june)
    months =('January','February','March','April','May','June')
    days = range (1,8)
    # When both is your choice
    if filter_answer == "both":
        month=input("Whitch month? Januray, February, March, April, May, or June?\n").title()
        while month not in months:
            month=input("Wrong answer!!\nWhitch month? Januray, February, March, April, May, or June?\n").title()
        day = int(input("Which day? please type your response as an integer (e.g., 1=Sunday).\n"))
        while day not in days:
            day = int(input("Wrong answer!!\nWhich day? please type your response as an integer (e.g., 1=Sunday).\n"))
# When month is your choice
    elif filter_answer == "month":
        month=input("Whitch month? Januray, February, March, April, May, or June?\n").title()
        while month not in months:
            month=input("Wrong answer!!\nWhitch month? Januray, February, March, April, May, or June?\n").title()
        day ="all"    
# when day is your choice:       
    elif filter_answer == "day":
        day = int(input("Which day? please type your response as an integer (e.g., 1=Sunday).\n"))
        while day not in days:
            day = int(input("Wrong answer!!\nWhich day? please type your response as an integer (e.g., 1=Sunday).\n"))
        month='all'
    else:
        day='all'
        month='all'    
    
    print('-'*40)
    return city, month, day, filter_answer 


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
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month =months.index(month)+1 
        
        # filter by month to create the new dataframe
        df = df[df['month']==month]
        

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days =['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        df =df[df['day_of_week']==days[day-1]]

         


    return df


def time_stats(df,filter_answer):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if filter_answer=='none' or filter_answer=='day' :
        print("The most popular month:{}, Counts:{}, Filter: \
{}".format(df['month'].value_counts().idxmax(),df['month'].value_counts().max(),filter_answer.strip().replace("none","all")))
          
    # display the most common day of week
    if filter_answer=='none'or filter_answer=='month' :
        print("The most popular day of week:{}, Counts:{}, Filter: \
{}".format(df['day_of_week'].value_counts().idxmax(),df['day_of_week'].value_counts().max(),filter_answer.strip().replace("none","all")))

    # display the most common start hour
    print("The most popular hour:{}, Counts:{}, Filter: \
{}".format(df['Start Time'].dt.hour.value_counts().idxmax(),df['Start Time'].dt.hour.value_counts().max(),filter_answer.strip().replace("none","all")))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,filter_answer):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station:{}, Counts:{}, Filter: {}".format(df['Start Station'].value_counts().idxmax(),df['Start Station'].value_counts().max(),filter_answer.strip().replace("none","all")))

    # display most commonly used end station
    print("The most common end station:{}, Counts:{}, Filter: {}".format(df['End Station'].value_counts().idxmax(),df['End Station'].value_counts().max(),filter_answer.strip().replace("none","all")))


    # display most frequent combination of start station and end station trip
    print("The most common trip from start to end: '{}', end station: '{}', Counts {}, Filter: {}".format(df.groupby(['Start Station','End Station']).size().idxmax()[0],df.groupby(['Start Station','End Station']).size().idxmax()[1],df.groupby(['Start Station','End Station']).size().max(),filter_answer.strip().replace("none","all")))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,filter_answer):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time, counts and average
    print("Total duration:{}, Counts:{}, average duration:{}, Filter: {}".format(df['Trip Duration'].sum(),df['Trip Duration'].count(),df['Trip Duration'].mean(),filter_answer.strip().replace("none","all")))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    
        

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User type ....") 
    print (df["User Type"].value_counts().to_string())
    
    if city != 'Washington':
        print("\nUser Gender ....") 
        print (df["Gender"].value_counts().to_string())


        print("\nDisplay more info about earliest, most recent, and most common year of birth")
        print ("Earliest year of birth : ",df["Birth Year"].min().astype(int))
        print ("The most recent year of birth: ",df["Birth Year"].max().astype(int))
        print ("The most common year of birth : ",df["Birth Year"].value_counts().idxmax().astype(int))
    
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def view_data(df,loc_value):
    
    while True:
        view_Q =input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        while view_Q not in ["yes","no"]:      
            view_Q= input("Wrong answer !!'\nWould you like to view 5 rows of individual trip data? Enter yes or no\n").lower()
        if view_Q=='yes':
            print(df.iloc[loc_value:loc_value+5].fillna("----"))
            
            loc_value+=5
        elif view_Q=='no':
            break
                
    


def main():
    while True:
        
        city, month, day, filter_answer = get_filters()
        df = load_data(city, month, day)

        time_stats(df,filter_answer)
        station_stats(df,filter_answer)
        trip_duration_stats(df,filter_answer)
        user_stats(df,city)
        loc_value =0
        view_data(df,loc_value)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
