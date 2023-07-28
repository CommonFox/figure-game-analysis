import pandas as pd

def read_csv(fox_stats, brittany_stats):
    df_fox_stats = pd.read_csv(fox_stats)
    df_brittany_stats = pd.read_csv(brittany_stats)

    return df_fox_stats, df_brittany_stats

def convert_time_values_to_seconds(time):
    if pd.isna(time):
        return None

    minutes_seconds = str(time)
    minutes_seconds = minutes_seconds.split(':')

    seconds = (int(minutes_seconds[0]) * 60) + int(minutes_seconds[1])

    return seconds


def main():
    df_fox_stats, df_brittany_stats = read_csv('csv/fox_stats.csv', 'csv/brittany_stats.csv')

    df_fox_stats['Time'] = df_fox_stats['Time'].apply(convert_time_values_to_seconds)
    df_brittany_stats['Time'] = df_brittany_stats['Time'].apply(convert_time_values_to_seconds)

    print(df_brittany_stats.head())

    return 0

if __name__ == "__main__":
    main()