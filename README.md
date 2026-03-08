Best Places Crime Score Lookup
A command-line tool that pulls violent and property crime scores from bestplaces.net by zip code. This data is commonly needed when rating certain classes of business in carrier portals.
How It Works

Enter a zip code
The tool looks up the city and state automatically
It scrapes the crime score page for that location
It returns the violent crime and property crime scores

Requirements

Python 3
Google Chrome

Installation
bashpip install pyzipcode selenium
Usage
bashpython best_places.py
You'll be prompted to enter a zip code. The tool validates the input, looks up the location, and prints the crime scores for that area.
Libraries Used

pyzipcode — converts zip codes to city/state
selenium — automates the browser to scrape crime score data from bestplaces.net
