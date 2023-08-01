import pandas as pd

def read_csv(fox_stats, brittany_stats):
    df_fox_stats = pd.read_csv(fox_stats)
    df_brittany_stats = pd.read_csv(brittany_stats)

    df_fox_stats['Time'] = df_fox_stats['Time'].apply(convert_time_values_to_seconds)
    df_brittany_stats['Time'] = df_brittany_stats['Time'].apply(convert_time_values_to_seconds)

    merged_df = pd.merge(df_fox_stats, df_brittany_stats, on=['Game #', 'Date'], suffixes=('_fox', '_brittany'))
    merged_df = merged_df.drop(['Player_fox', 'Player_brittany'], axis=1)

    return merged_df

def convert_time_values_to_seconds(time):
    if pd.isna(time):
        return None

    minutes_seconds = str(time)
    minutes_seconds = minutes_seconds.split(':')

    minutes = int(minutes_seconds[0])
    seconds = int(minutes_seconds[1])

    # remove some of Brittany's bad data
    if minutes > 90:
        return None

    seconds = (minutes * 60) + seconds

    return seconds

def convert_seconds_to_minutes_seconds(seconds):
    minutes = seconds // 60
    seconds %= 60

    display_string = str(round(minutes)) + " min " + str(round(seconds)) + " sec"

    return display_string

def main():
    df = read_csv('csv/fox_stats.csv', 'csv/brittany_stats.csv')

    print(df.head(50))

    return 0

if __name__ == "__main__":
    main()