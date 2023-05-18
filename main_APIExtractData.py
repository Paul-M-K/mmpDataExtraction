from requests import post

response = post('https://api.igdb.com/v4/age_ratings', **{'headers': {'Client-ID': 'yizntsh128hmthcof1qurn2eashnvm', 'Authorization': 'Bearer lkvqnflz33l1bybwvqn1nuotoixt42'},'data': 'fields category,checksum,content_descriptions,rating,rating_cover_url,synopsis;'}).text
# print ("response: %s" % str(response.json()))

print(response)
