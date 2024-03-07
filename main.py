import requests
from bs4 import BeautifulSoup
import pylast
import csv


API_KEY = "API key here"
API_SECRET = "API secret here"
username = "username here"
password_hash = pylast.md5("password here")

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash
)


class Gig:
    def __init__(self, name, date, venue, link):
        self.name = name
        self.date = date
        self.venue = venue
        self.link = link


request = requests.get("https://www.ueaticketbookings.co.uk/whats-on/")
soup = BeautifulSoup(request.content, 'html.parser')
raw_gigs = soup.find_all("div", class_="event_item")

gig_list = []

for gig in raw_gigs:
    name = gig.find("a", class_="msl_event_name").text
    date = gig.find("dd", class_="msl_event_time").text
    venue = gig.find("dd", class_="msl_event_location").text
    link = gig.find("a", class_="msl_event_name", href=True)
    full_link = "https://www.ueaticketbookings.co.uk" + link['href']
    gig_listing = Gig(name, date, venue, full_link)
    gig_list.append(gig_listing)

print(len(gig_list))
final_gigs = []
for gig in gig_list:
    try:
        artist = network.get_artist(gig.name)
        tags = artist.get_top_tags(limit=5)
        tag_list = []
        for tag in tags:
            tag_list.append(tag.item.get_name())
        gig.genre = tag_list
        gig_details = [gig.name, gig.date, gig.venue, gig.genre, gig.link]
        final_gigs.append(str(gig_details))

    except:
        pass

final_output = '\n'.join(final_gigs)

with open("./Giglister/gigs.txt", 'w') as f:
    f.write(str(final_output))
    f.close()

# change to write a csv
# think its not working as they're now strings rather than a list
# with open("./Giglister/gigs.csv", 'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(final_output)
#     file.close()
