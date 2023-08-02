import pandas as pd
import numpy as np

def read_csv(stats_csv):
    df = pd.read_csv(stats_csv)\

    df['time_fox'] = df['time_fox'].apply(convert_time_values_to_seconds)
    df['time_brittany'] = df['time_brittany'].apply(convert_time_values_to_seconds)

    df = tries_and_time_comparison(df)

    return df

def tries_and_time_comparison(merged_df):
    df_copy = merged_df.copy()

    df_copy['tries_difference'] = np.nan
    df_copy['time_difference'] = np.nan

    # Calculate the Tries_Comparison column based on different conditions
    df_copy['tries_difference'] = np.where(
        (df_copy['tries_fox'].notna()) & (df_copy['tries_brittany'].notna()),   # Both not NaN
        df_copy['tries_fox'] - df_copy['tries_brittany'],
        np.nan  # Both are NaN
    )

    # Calculate the Time_Comparison column based on different conditions
    df_copy['time_difference'] = np.where(
        (df_copy['time_fox'].notna()) & (df_copy['time_brittany'].notna()),   # Both not NaN
        df_copy['time_fox'] - df_copy['time_brittany'],
        np.nan  # Both are NaN
    )

    # Brittany plays but not Fox
    mask = (df_copy['tries_fox'].isna()) & (df_copy['tries_brittany'].notna())
    df_copy.loc[mask, 'tries_difference'] = df_copy['tries_brittany']

    mask = (df_copy['time_fox'].isna()) & (df_copy['time_brittany'].notna())
    df_copy.loc[mask, 'time_difference'] = df_copy['time_brittany']

    # Fox plays but not Brittany
    mask = (df_copy['tries_fox'].notna()) & (df_copy['tries_brittany'].isna())
    df_copy.loc[mask, 'tries_difference'] = df_copy['tries_fox'] * -1

    mask = (df_copy['time_fox'].notna()) & (df_copy['time_brittany'].isna())
    df_copy.loc[mask, 'time_difference'] = df_copy['time_fox'] * -1

    df_copy = df_copy[['game_number', 'tries_difference', 'time_difference']]

    merged_df = pd.merge(merged_df, df_copy, on='game_number')

    return merged_df

def convert_time_values_to_seconds(time):
    if pd.isna(time):
        return np.nan

    minutes_seconds = str(time)
    minutes_seconds = minutes_seconds.split(':')

    minutes = int(minutes_seconds[0])
    seconds = int(minutes_seconds[1])

    # remove some of Brittany's bad data
    if minutes > 90:
        return None

    seconds = (minutes * 60) + seconds

    return seconds

def tally_scores(merged_df):
    fox_wins = merged_df[merged_df['tries_difference'] < 0]
    brittany_wins = merged_df[merged_df['tries_difference'] > 0]

    print(len(fox_wins))
    print(len(brittany_wins))

    return 0

def convert_seconds_to_minutes_seconds(seconds):
    minutes = seconds // 60
    seconds %= 60

    display_string = str(round(minutes)) + " min " + str(round(seconds)) + " sec"

    return display_string

def main():
    df = read_csv('csv/combined_stats.csv')

    tally_scores(df)

    return 0

if __name__ == "__main__":
    main()