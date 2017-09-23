import urllib2
import json

with open('windows.json') as f:
    windows = json.load(f)

wins = []
for window in windows:
    win = json.loads(window)
    wins.append(win)

for window in wins:
    url = window['image_url']
    fname = url.split('/')[-1]
    with open('img/' + fname, 'wb') as f:
        f.write(urllib2.urlopen(url).read())
