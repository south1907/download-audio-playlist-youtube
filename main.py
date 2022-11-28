import requests
import json
import time

def download_by_url(url_need_download):
	url = 'https://srv10.y2mate.is/listFormats?url=' + url_need_download

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

with open('list_link.txt', 'r') as f:
	list_link = f.read().split('\n')


for link in list_link:
	print(link)
	download_by_url(link)


