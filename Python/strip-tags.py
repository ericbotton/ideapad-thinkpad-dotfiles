# pylint: disable=invalid-name
#!/usr/bin/python3
""" ChatGTP: strip all html from web page and print text formatted """

from bs4 import BeautifulSoup
import requests

url = "https://ageofempires.fandom.com/wiki/Cheat_codes_(Age_of_Empires_III)" # Replace with the URL of the web page you want to extract text from
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Remove script and style elements
for script in soup(["script", "style"]):
    script.decompose()

# Get text
text = soup.get_text()

# Break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())

# Break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

# Drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

print(text)
