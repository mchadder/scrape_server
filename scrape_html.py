# sudo apt-get install python3-pip
# sudo pip install beautifulsoup4

# sudo pip install -U beautifulsoup4 (to ensure the latest version is installed)

def scraper(url="", selector=""):

  if url == "":
    url = "https://www.oratechinfo.co.uk"

  if selector == "":
    selector = "a[href]"
    #selector = "input"

  USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"

  HEADERS = { 'User-Agent' : USER_AGENT,
              'Cookie': 'PREF=12345' }

  from bs4 import BeautifulSoup
  import urllib.request

  req = urllib.request.Request(url, data=None, headers=HEADERS)
  f = urllib.request.urlopen(req)

  #print(f)

  html = f.read().decode('utf-8')

  soup = BeautifulSoup(html, "html.parser")

# .title returns the HTML <title> tag
#print(soup.title)

# .title.string returns the text of the <title> tag
#print(soup.title.string)

# Print formatted HTML output 
#print(soup.prettify())

# ~= : containing word
# |= : starts with
# ^= : begins with
# $= : ends with
# *= : substring

# bs4 (4.6) only supports the :nth-of-type pseudoclass

  items = soup.select(selector)
#items = soup.select("a[href],link[href]")
#items = soup.select('a[href^="http"]')

  return (items, f)

def printem(inp):
  print("HTTP Response Code: " + str(inp[1].getcode()))
  for i in inp[0]:
    print(i.get("href"))

if __name__ == "__main__": 
  printem(scraper())
