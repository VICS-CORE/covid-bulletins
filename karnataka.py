import sys
import requests, re, datetime, json

if (sys.version_info[0] < 3):
    import HTMLParser
    unescape = HTMLParser.HTMLParser.unescape
else:
    import html
    unescape = html.unescape

STATE = "karnataka"

with open(STATE + ".json") as f:
    l = json.loads(f.read())
urls = set([i['url'] for i in l])

URL = "https://covid19.karnataka.gov.in/new-page/Media%20Bulletin/en"
r = requests.get(URL)
m = re.findall("https.*?\.pdf", r.text)

for i in m:
    u = unescape(i)
    try:
        print(u)
        if u in urls:
            print("Exists")
            continue
        # download & save
        r = requests.get(u)
        fn = u.split("/")[-1]
        with open(STATE + "/" + fn, "wb") as f:
            f.write(r.content)
        # mark saved
        l.append({
            "url": u,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        print(str(e))

with open(STATE + ".json", "w") as f:
    f.write(json.dumps(l, indent=2))
