import json
import urllib.request
import string
import random
import time

count = 1

#https://developers.google.com/youtube/v3/docs
API_KEY = 'Enter_Google_Developer_API_KEY'

#MAKE SURE TO INCREMENT SEED EACH TIME
#random.seed(1)
#random.seed(2)
random.seed(3)

for i in range(0,100):

    random_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

    urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,random_id)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))

    for data in results['items']:
        videoId = (data['id']['videoId'])
        print(videoId)
        #store your ids

    time.sleep(10)
