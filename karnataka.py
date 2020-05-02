import requests, re, datetime, json, html

STATE = "karnataka"

with open(STATE + ".json") as f:
    l = json.loads(f.read())
urls = set([i['url'] for i in l])

URL = "https://covid19.karnataka.gov.in/new-page/Health%20Department%20Bulletin/en"
r = requests.get(URL)
m = re.findall("https.*?\.pdf", r.text)

for i in m:
    u = html.unescape(i)
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
