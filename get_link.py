import requests
import json

url = "https://www.youtube.com/playlist?list=PLez4BA028nWRic8Aa2hbiVdhmP_yiHxNO"

payload={}
headers = {
  'Cookie': 'GPS=1; VISITOR_INFO1_LIVE=u6WG0FlH32U; YSC=5svkkAU85F8'
}

response = requests.request("GET", url, headers=headers, data=payload)
text_html = response.text

def find_string_by_from_end(str_data, str_from, str_end):
	from_index = str_data.find(str_from)
	if from_index > 0:
		end_index = str_data.find(str_end, from_index)

		if end_index > 0:
			return str_data[from_index:end_index]

	return ''
	
find_from = '{"responseContext":{"serviceTrackingParams":'
find_end = ';</script>'

data_web = find_string_by_from_end(text_html, find_from, find_end)
data_json = json.loads(data_web)

data = data_json['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

for item in data:
	print('https://www.youtube.com/watch?v=' + item['playlistVideoRenderer']['videoId'])