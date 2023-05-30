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
print(df)

# Save the DataFrame to a CSV file
df.to_csv('matching_games.csv', index=False)
