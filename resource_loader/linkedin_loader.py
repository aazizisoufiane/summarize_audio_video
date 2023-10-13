import requests
from bs4 import BeautifulSoup

URL = 'YOUR_LINKEDIN_VIDEO_PAGE_URL'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(URL, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
video_tag = soup.find('video')

if video_tag:
    video_url = video_tag['src']
    video_data = requests.get(video_url, headers=headers, stream=True)

    with open('linkedin_video.mp4', 'wb') as file:
        for chunk in video_data.iter_content(chunk_size=1024 * 1024):
            file.write(chunk)
else:
    print("Video not found!")
