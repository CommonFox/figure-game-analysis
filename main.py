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

    df_copy['tries_fox'] = df_copy['tries_fox'] + df_copy['hints_fox']
    df_copy['tries_brittany'] = df_copy['tries_brittany'] + df_copy['hints_brittany']

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

def tally_scores(df):
    scores = {}

    fox_wins = df[df['tries_difference'] < 0]
    brittany_wins = df[df['tries_difference'] > 0]

    ties = df[df['tries_difference'] == 0]

    scores['fox'] = len(fox_wins) + len(ties[ties['time_difference'] < 0])
    scores['brittany'] = len(brittany_wins) + len(ties[ties['time_difference'] > 0])
    scores['tie'] = len(ties[ties['time_difference'] == 0])

    return scores

def number_of_games_played(df):
    games_played = {}

    games_played['fox'] = len(df[df['tries_fox'].notna()])
    games_played['brittany'] = len(df[df['tries_brittany'].notna()])

    return games_played

def convert_seconds_to_minutes_seconds(seconds):
    minutes = seconds // 60
    seconds %= 60

    display_string = str(round(minutes)) + " min " + str(round(seconds)) + " sec"

    return display_string

def find_averages(df):
    averages = {}

    averages['fox_tries'] = df['tries_fox'].mean()
    averages['fox_time'] = convert_seconds_to_minutes_seconds(df['time_fox'].mean())
    averages['fox_hints'] = df['hints_fox'].mean()

    averages['brittany_tries'] = df['tries_brittany'].mean()
    averages['brittany_time'] = convert_seconds_to_minutes_seconds(df['time_brittany'].mean())
    averages['brittany_hints'] = df['hints_brittany'].mean()

    return averages

def main():
    df = read_csv('csv/combined_stats.csv')

    scores = tally_scores(df)
    games_played = number_of_games_played(df)
    averages = find_averages(df)
    print(scores)
    print(games_played)
    print(averages)

    return 0

if __name__ == "__main__":
    main()