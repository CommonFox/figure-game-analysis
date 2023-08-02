import pandas as pd
import numpy as np

def read_csv(fox_stats, brittany_stats):
    df_fox_stats = pd.read_csv(fox_stats)
    df_brittany_stats = pd.read_csv(brittany_stats)

    df_fox_stats['Time'] = df_fox_stats['Time'].apply(convert_time_values_to_seconds)
    df_brittany_stats['Time'] = df_brittany_stats['Time'].apply(convert_time_values_to_seconds)

    merged_df = pd.merge(df_fox_stats, df_brittany_stats, on=['Game #', 'Date'], suffixes=('_fox', '_brittany'))
    merged_df = merged_df.drop(['Player_fox', 'Player_brittany'], axis=1)

    merged_df = tries_and_time_comparison(merged_df)

    return merged_df

def tries_and_time_comparison(merged_df):
    df_copy = merged_df.copy()

    df_copy['Tries_Comparison'] = np.nan
    df_copy['Time_Comparison'] = np.nan

    # Calculate the Tries_Comparison column based on different conditions
    df_copy['Tries_Comparison'] = np.where(
        (df_copy['Tries_fox'].notna()) & (df_copy['Tries_brittany'].notna()),   # Both not NaN
        df_copy['Tries_fox'] - df_copy['Tries_brittany'],
        np.nan  # Both are NaN
    )

    # Calculate the Time_Comparison column based on different conditions
    df_copy['Time_Comparison'] = np.where(
        (df_copy['Time_fox'].notna()) & (df_copy['Time_brittany'].notna()),   # Both not NaN
        df_copy['Time_fox'] - df_copy['Time_brittany'],
        np.nan  # Both are NaN
    )

    # Brittany plays but not Fox
    mask = (df_copy['Tries_fox'].isna()) & (df_copy['Tries_brittany'].notna())
    df_copy.loc[mask, 'Tries_Comparison'] = df_copy['Tries_brittany']

    mask = (df_copy['Time_fox'].isna()) & (df_copy['Time_brittany'].notna())
    df_copy.loc[mask, 'Time_Comparison'] = df_copy['Time_brittany']

    # Fox plays but not Brittany
    mask = (df_copy['Tries_fox'].notna()) & (df_copy['Tries_brittany'].isna())
    df_copy.loc[mask, 'Tries_Comparison'] = df_copy['Tries_fox'] * -1

    mask = (df_copy['Time_fox'].notna()) & (df_copy['Time_brittany'].isna())
    df_copy.loc[mask, 'Time_Comparison'] = df_copy['Time_fox'] * -1

    df_copy = df_copy[['Game #', 'Tries_Comparison', 'Time_Comparison']]

    merged_df = pd.merge(merged_df, df_copy, on='Game #')

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

def tally_scores(merged_df):
    fox_wins = merged_df[merged_df['Tries_Comparison'] < 0]
    brittany_wins = merged_df[merged_df['Tries_Comparison'] > 0]

    print(len(fox_wins))
    print(len(brittany_wins))

    return 0

def convert_seconds_to_minutes_seconds(seconds):
    minutes = seconds // 60
    seconds %= 60

    display_string = str(round(minutes)) + " min " + str(round(seconds)) + " sec"

    return display_string

def main():
    df = read_csv('csv/fox_stats.csv', 'csv/brittany_stats.csv')

    tally_scores(df)

    return 0

if __name__ == "__main__":
    main()