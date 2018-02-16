from bs4 import BeautifulSoup
import argparse
import requests


ap = argparse.ArgumentParser()
ap.add_argument("-p","--pokemon_list", required = True, help = "Path to where the raw Pokemon HTML resides")
ap.add_argument("-s","--sprites", required = True, help = "Path where the sprites will be stored")
args = vars(ap.parse_args())

# we use BeautifulSoup to parse the raw HTML and identify all the <a> tags
# parse the text in them and add them to a list
# Subsequently we will be using these names to download the sprites
soup = BeautifulSoup(open(args["pokemon_list"]).read())
names =[]

for link in soup.findAll("a"):

	names.append(link.text)


for name in names:

	parsedName = name.lower()

	parsedName = parsedName.replace("'", "")


	parsedName = parsedName.replace(". ", "-")

	if name.find(u'\u2640') != -1:
		parsedName = "nidoran-f"
	elif name.find(u'\u2642') != -1:
		parsedName = "nidoran-m"

	print ("[x] downloading %s" % (name))
	# construct the URL to download the sprite
	# These 2 lines are the bulk of the matter
	url  = "http://img.pokemondb.net/sprites/red-blue/normal/%s.png" % (parsedName)
	r = requests.get(url)

	# handling errors
	if r.status_code != 200:
		#print "[x] error downloading %s" % (name)
		print ("[x] error downloading %s"% name)
		continue

	f = open("%s%s.png" % (args["sprites"], parsedName), "wb")
	f.write(r.content)
	f.close()
