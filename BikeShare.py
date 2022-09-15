import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    print('Hello! Let\'s explore some US bikeshare data! :)')
    print('-'*40)


    city = input('\n'+'Please, type one of these cities: (chicago, new york city, washington) '+'\n').lower()
    while city not in CITY_DATA:
        print("SORRY, Not valid input!" + '\n')
        city = input('\n'+'Please, type one of these cities: (chicago, new york city, washington) '+'\n').lower()

    filter_choice = input("\nWould you like to filter by (month or day or both or none)?\n").lower()
    while filter_choice not in ['month','day','both','none']:
        print("SORRY, Not valid input!" + '\n')
        filter_choice = input("\nWould you like to filter by (month or day or both or none)?\n").lower()


    if filter_choice == 'both':
        month = input('\n'+"Great job, now could you type one of first six months?"+'\n').lower()
        while month not in ['january','february','march','april','may','june']:
            print("SORRY, Not valid input!" + '\n')
            month = input('\n'+"Please, type one of first six months "+'\n').lower()

        day = input('\n'+"Finally, type one of week days: "+'\n').lower()
        while day not in ['saturday','sunday','monday','tuesday','wednesday','thursday','friday']:
            print("SORRY, Not valid input!" + '\n')
            day = input('\n'+"Please, type one of week days"+'\n').lower()

    elif filter_choice == 'none':
        month = 'all'
        day = 'all'

    elif filter_choice == 'month':
        month = input('\n'+"Great job, now could you type one of first six months?"+'\n').lower()
        while month not in ['january','february','march','april','may','june']:
            print("SORRY, Not valid input!" + '\n')
            month = input('\n'+"Please, type one of first six months "+'\n').lower()
        day = 'all'

    elif filter_choice == 'day':
        day = input('\n'+"Finally, type one of week days:"+'\n').lower()
        while day not in ['saturday','sunday','monday','tuesday','wednesday','thursday','friday']:
            print("SORRY, Not valid input!" + '\n')
            day = input('\n'+"Please, type one of week days"+'\n').lower()
        month = 'all'



    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])                      #reading the csv file for the specified city
    df['Start Time'] = pd.to_datetime(df['Start Time'])    #connverting the Start Time column to datetime object
    df['month'] = df['Start Time'].dt.month                #extracting the month data into a new column
    df['day_of_week'] = df['Start Time'].dt.day_name()  #extracting the day_of_week data into a new column


    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1                                        #converting the str month got by user into int
        df = df[df['month'] == month]                                        #filtering by month

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]                            #filtering by day


    return df


def time_stats(df):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    months_names = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month = months_names[most_common_month-1]
    print("Most Month: ",most_common_month)

    most_common_day = df['day_of_week'].mode()[0]
    print("Most Day: ",most_common_day)

    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("Most Hour: ",most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_startstation = df['Start Station'].mode()[0]
    print("Most Start Station:   ", most_common_startstation)

    most_common_endstation = df['End Station'].mode()[0]
    print("Most End Station:     ", most_common_endstation)

    df['comb'] = ['From:  '] + df['Start Station'] + ['  To:  '] + df['End Station']
    comb = df['comb'].mode()[0]
    print("Most Frequented Trip: ", comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_duration = (df['Trip Duration'].sum())/3600
    print("Total Travel Time (in hours):   ",trip_duration)

    trip_mean = (df['Trip Duration'].mean())/3600
    print("Average Travel Time (in hours): ",trip_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    Subscribers = df['User Type'].value_counts()[0]
    Customers = df['User Type'].value_counts()[1]
    print("Count of User Types: ")
    print("     Subscibers:      ",Subscribers)
    print("     Customers:       ",Customers)
    print("     Total:           ",Subscribers + Customers)

    if city != "washington":
        males = df['Gender'].value_counts()[0]
        females = df['Gender'].value_counts()[1]
        print("Count of Genders: ")
        print("     Males:           ",males)
        print("     Females:         ",females)
        print("     Total:           ",males + females)
    else:
        print("Oops, Washington city doesn't have Gender data")

    if city != "washington":
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common =  df['Birth Year'].mode()[0]
        print("Info of Birth Year: ")
        print("     Earliest Year:   ",int(earliest))
        print("     Recent Year:     ",int(recent))
        print("     Common Year:     ",int(common))
    else:
        print("Oops, Washington city doesn't have Year Birth data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    x = input("\nWould you like to see the raw data of the city?\nPlease Type (yes or no)\n").lower()
    while x not in ['yes','no']:
        print("SORRY, Not valid input!")
        x = input("\nWould you like to see the raw data of the city?\nPlease Type (yes or no)\n").lower()

    if x == 'yes':
        while x == 'yes':

            print("\nHere is the first 5 rows of the data:\n\n",df.head())
            x = input("\nWould you like to see more (yes or no)\n").lower()
            if x == 'yes':
                n = 5
                df.drop(index = df.index[0:n],inplace = True)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
