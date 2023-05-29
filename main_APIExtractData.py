from requests import post



response = post('https://api.igdb.com/v4/platforms/', **{'headers': {'Client-ID': 'yizntsh128hmthcof1qurn2eashnvm', 'Authorization': 'Bearer lkvqnflz33l1bybwvqn1nuotoixt42'},'data': 'fields *; where name = "Nintendo Entertainment System"; limit 500;'}).text

# print ("response: %s" % str(response.json()))

print(response)
