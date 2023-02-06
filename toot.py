from urllib.request import urlopen
from mastodon import Mastodon
#from songs import load_songs
import random
from datetime import datetime
from time import sleep

mdon = Mastodon(access_token="mastodon.secret", api_base_url="https://botsin.space")

answers = {
    "WHERE": ["Under the sink", "China", "Scotland", "The international space station", "Germany", "Lower Brailes", "South Africa",
              "Egypt", "India", "Canada", "Japan", "New Zealand", "Paris", "Tokyo", "New York", "North Dakota", "Rio de Janeiro"],
    "WHEN": ["Next week", "Next year", "Later today", "In six months", "In two months", "In a fortnight", "In 100 years",
             "In the year 3000", "Never"],
    "WHICH WAY": ["Straight ahead", "Behind you", "Left", "Right", "North", "South", "East", "West", "North-East", "North-West", "North-North-East"],
    "WHO": ["David Beckham", "Barack Obama", "Les Dennis", "Jeremy Corbyn", "Bill Gates", "Michael Jordan", "Michael Jackson",
            "Mick Herron", "Jackson Lamb"],
    "HOW MUCH": ["$10", "A year", "50p", "£12", "A million", "13", "One"],
    "HOW LONG": ["A week", "Two days", "Six metres", "37 minutes", "Two years", "A furlong", "A lightyear"],
    "WHAT": ["An egg", "A duck", "The moon", "Jesus", "A bacon sandwich", "Woolworths", "Magikarp", "The bible"],
    "WHY": ["Why not?", "Because the Night", "Because We Want To", "Because You're Mine", "Because They're Young", "Because",
            "Because I Love You (The Postman Song)", "Because of You", "Because You Loved Me"],
    "HOW": ["With difficulty", "By trying hard", "With a Little Help from My Friends"],
    "DO": ["Yes", "No"],
    "CAN": ["Yes", "No"],
    "IS": ["Yes", "No"],
    "ARE": ["Yes", "No"],
    "AM": ["Yes", "No"],
    "HAVE": ["Yes", "No"],
}


def is_question(q):
    if q.startswith("BECAUSE"):
        print(q)
    if not q.endswith("?"):
        return False
    for word in answers:
        if word.upper() in q.upper():
            return True
    print(title)
    return False


for i in range(50):
    y = random.randrange(1952, datetime.now().year + 1)
    m = random.randrange(1, 13)
    d = random.randrange(1, 32)

    url = f"https://www.officialcharts.com/charts/singles-chart/{y}{'0' if m < 10 else ''}{m}{'0' if d < 10 else ''}{d}/"
    print(url)
    with urlopen(url) as f:
        page = f.read().decode("utf-8")
    titles = []
    for t in page.split("<div class=\"track\">")[1:]:
        title = t.split("<div class=\"title\">")[1].split(">")[1].split("<")[0]
        artist = t.split("<div class=\"artist\">")[1].split(">")[1].split("<")[0]
        if is_question(title):
            titles.append((title, artist))
    if len(titles) >= max(1, 10 - i):
        break

    sleep(10)

if len(titles) == 0:
    raise ValueError("Song not found")

q = random.choice(titles)

for word, options in answers.items():
    if q[0].upper().startswith(word.upper()):
        answers = options
        break
else:
    for word, options in answers.items():
        if word.upper() in q[0].upper():
            answers = options
            break
    else:
        raise RuntimeError("This should never happen")
o = []
for i in range(4):
    if len(answers) > 0:
        o.append(random.choice(answers))
        answers.remove(o[-1])

poll = mdon.make_poll(o, 60*60*24)
mdon.status_post(status=f"{q[0]} ({q[1]})", poll=poll)

