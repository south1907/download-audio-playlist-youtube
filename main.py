import requests
import json
import time

def download_by_url(url_need_download):
	url = 'https://srv11.y2mate.is/listFormats?url=' + url_need_download

	payload={}
	headers = {
	  'Accept': 'application/json, text/javascript, */*; q=0.01',
	  'Referer': 'https://en.y2mate.is/'
	}

	response = requests.request("GET", url, headers=headers, data=payload)

	data = json.loads(response.text)
	if data is not None and 'error' in data:
		check_status = data['error']

		if check_status == False:
			file_name = data['formats']['basename']

			audios = data['formats']['audio']
			audio = audios[0]

			link_convert = audio['url']

			# request convert 
			response = requests.request("GET", link_convert, headers=headers, data=payload)
			data_convert = json.loads(response.text)

			while True:
				# getLink
				get_link = data_convert['url']
				response = requests.request("GET", get_link, headers=headers, data=payload)
				data_get_link = json.loads(response.text)
				if 'url' in data_get_link and data_get_link['url'] != '':
					final_url_audio = data_get_link['url']
					print('Have url: '+ final_url_audio +', downloading')
					r = requests.get(final_url_audio)  
					with open('audios/'+ file_name +'.mp3', 'wb') as f:
					    f.write(r.content)
					break
				else:
					print('converting, sleep 1s and continue')
					time.sleep(1)

def find_string_by_from_end(str_data, str_from, str_end):
	from_index = str_data.find(str_from)
	if from_index > 0:
		end_index = str_data.find(str_end, from_index)

		if end_index > 0:
			return str_data[from_index:end_index]

	return ''

with open('link_playlist.txt', 'r') as f:
	url = f.read()

payload={}
headers = {
  'Cookie': 'GPS=1; VISITOR_INFO1_LIVE=u6WG0FlH32U; YSC=5svkkAU85F8'
}

response = requests.request("GET", url, headers=headers, data=payload)
text_html = response.text
	
find_from = '{"responseContext":{"serviceTrackingParams":'
find_end = ';</script>'

data_web = find_string_by_from_end(text_html, find_from, find_end)
data_json = json.loads(data_web)

data = data_json['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

for item in data:
	link = 'https://www.youtube.com/watch?v=' + item['playlistVideoRenderer']['videoId']

	print(link)
	download_by_url(link)


