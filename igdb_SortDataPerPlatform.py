import json
import pandas as pd

# Load console data from JSON file
with open('platformsDataextract.json') as console_file:
    console_data = json.load(console_file)

# Load game data from JSON file
with open('gamerating.json') as game_file:
    game_data = json.load(game_file)

# Create an empty list to store the matching game data
matching_games_list = []

# Iterate through console data
for console in console_data:
    console_id = console['id']
    console_name = console['alternative_name']
    matching_games = [game for game in game_data if console_id in game['platforms']]

    # Append the matching game data to the list
    for game in matching_games:
        platform = [p for p in game['platforms'] if p == console_id]
        if platform:
            matching_games_list.append({
                'Console ID': console_id,
                'Console Name': console_name,
                'Game Name': game['name'],
                'rating': game['rating'],
                'rating_count': game['rating_count']
            })

# Create a DataFrame from the matching game data list
df = pd.DataFrame(matching_games_list)

# Print the DataFrame
# print(df)

# Iterate over unique groups
for group_value in df['Console ID'].unique():
    group_data = df[df['Console ID'] == group_value]  # Extract the data for the current group
    
    # Evaluate the group based on your criteria
    # Example: Calculate the mean of a specific column
    group_mean = group_data['rating'].mean()
    group_sum = group_data['rating_count'].sum()

    df = df.assign(weighted_rating = (df['rating']*df['rating_count'])/group_sum)
    
    # Print or perform any other desired actions with the evaluated group
    # print(f"Group {group_value}: Mean = {group_mean}: Sum = {group_sum}")

# Sort the DataFrame by 'ValueColumn' in descending order while keeping the groups intact
df_sorted = df.sort_values(by=['Console ID', 'weighted_rating'], ascending=[True, False])

# Remove duplicate rows based on all columns
df_no_duplicates = df_sorted.drop_duplicates()


print(df_no_duplicates)
# Save the DataFrame to a CSV file
df_no_duplicates.to_csv('matching_games.csv', index=False)
