1. Scraped the web for pokemon images using BeautifulSoup and Requests
2. Built a wrapper around Zernike_Moments function imported from mahotas library.
3. Indexed the database using Zernike_Moments and saved the file to disk. (the file is index.cpickle)
4. Found the edges of the GameBoy screen, croppedd the pokemon out of the screen while maintaining scale invariance.
5. The intensity of the image was modified to slightly make it bright.
6. The cropped image is indexed and euclidean distance used to compare the cropped image's feature vector to the ones in the database.
7. The name of the pokemon is displayed on the command line.

> Usage: 

In the command line, first run find_screen.py with your query image

example: `python find_screen.py -q query_marowak.png`


Only then run:

`python main_prog.py -q cropped.png -i index.cpickle`


Note: The second command is common irrespective of the pokemon being found.
