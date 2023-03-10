from urllib.request import urlopen
from mastodon import Mastodon
import random
import html
from datetime import datetime
from time import sleep
import sys

test = "test" in sys.argv

mdon = Mastodon(access_token="mastodon.secret", api_base_url="https://botsin.space")

answers = {
    "WHERE": ["Under the sink", "China", "Scotland", "The international space station", "Germany", "Lower Brailes", "South Africa",
              "Egypt", "India", "Canada", "Japan", "New Zealand", "Paris", "Tokyo", "New York", "North Dakota", "Rio de Janeiro",
              "Casino Royale", "Yoghurt aisle at Asda", "In the middle of our street", "Sesame Street", "Falls from skies above",
              "Staffordshire", "Thuro", "PC World", "New Alresford", "Chicken Cottage", "Coventry", "Florence", "In the cupboard",
              "Next to the salt", "In the sky with diamonds", "New York", "The arctic", "The Netherlands", "The Nile", "Reddit",
              "BBC News", "The bathroom", "Thailand", "Barcelona", "Waterstones", "Dudley zoo"],
    "WHEN": ["Next week", "Next year", "Later today", "In six months", "In two months", "In a fortnight", "In 100 years",
             "In the year 3000", "Never"],
    "WHICH WAY": ["Straight ahead", "Behind you", "Left", "Right", "North", "South", "East", "West", "North-East", "North-West", "North-North-East"],
    "WHO": ["David Beckham", "Barack Obama", "Les Dennis", "Jeremy Corbyn", "Bill Gates", "Michael Jordan", "Michael Jackson",
            "Mick Herron", "Jackson Lamb", "Lovely Rita", "The Queen of France", "Postman Pat", "David Dimbleby", "Nicholas Lyndhurst",
            "Richard Madeley", "Orson Welles", "Le Chiffre", "Lassie", "Prue Leith", "Martine McCutcheon", "Gail Platt", "Ken Barlow",
            "Crazy Grace", "Andrew Neil", "Atomic Kittens", "Lisa from Steps", "Evil Dame Judi Dench", "Miss Piggy", "Girl from raisins box",
            "Neil Buchanan", "Wendy Warlock"],
    "HOW MUCH": ["$10", "A year", "50p", "£12", "A million", "13", "One"],
    "HOW LONG": ["A week", "Two days", "Six metres", "37 minutes", "Two years", "A furlong", "A lightyear"],
    "WHAT TIME": ["1", "2", "3 o'clock", "4 o'clock rock", "5", "6", "7 o'clock", "8 o'clock rock", "9", "10", "11 o'clock", "12 o'clock rock",
                  "Hammer time", "Chico time"],
    "WHAT": ["An egg", "A duck", "The moon", "Jesus", "A bacon sandwich", "Woolworths", "Magikarp", "The bible", "Pussycat", "Kitchen table",
             "Lucy", "Your wallet", "A cup of tea", "A haircut", "The seaside", "iPhone 4S"],
    "WHY": ["Because the Night", "Because We Want To", "Because You're Mine", "Because They're Young", "Because",
            "Because I Love You (The Postman Song)", "Because of You", "Because You Loved Me", "Because I Got High"],
    "HOW": ["With difficulty", "By trying hard", "With a Little Help from My Friends"],
    "DO": ["Yes", "No"],
    "DA": ["Yes", "No"],
    "CAN": ["Yes", "No"],
    "IS": ["Yes", "No"],
    "ARE": ["Yes", "No"],
    "AM": ["Yes", "No"],
    "HAVE": ["Yes", "No"],
    "WOULD": ["Yes", "No"],
    "WILL": ["Yes", "No"],
}


def is_question(q):
    if not q.endswith("?"):
        return False
    for word in answers:
        if word.upper() in q.upper():
            return True
    print(title)
    return False

done = [html.unescape(a["content"]) for a in mdon.account_statuses(mdon.me(), limit=7)]


i = 0
while True:
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
        toot = html.unescape(f"{title} (artist)")
        if is_question(title) and toot not in done:
            titles.append((title, artist, toot))
    if len(titles) >= max(1, 10 - i):
        break

    i += 1
    if not test:
        sleep(10)

if len(titles) == 0:
    raise RuntimeError("Song not found. This should never happen")

if test:
    for t in titles:
        print(t)

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

if test:
    print(f"if not testing, I would toot: {toot}: " + ", ".join(o))
else:
    poll = mdon.make_poll(o, 60*60*24)
    mdon.status_post(status=toot, poll=poll)

