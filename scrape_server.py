import http.server
import scrape_html as sh
import cgi, html
from http.client import responses

IPADDR=""
PORT = 9999
SERVER_NAME="Chadders HTTP Scrape Server"
SERVER_VERSION="1.0"
ENCODING="utf8"

def dictget(dict, key, idx=0, default_return=""):
  try:
    g = str(dict[bytes(key, ENCODING)][idx], ENCODING)

    if g == "":
      g = default_return

    return g
  except KeyError as e:
    return default_return

def opts(id,arr):
  r = ""
  for i in arr:
    r += f"<a href='#' onclick='pop({id},\"{i}\")'>{i}</a>,"

  return r.strip(",")

def wp(self, rq):
  self.server_version = f"{SERVER_NAME}/{SERVER_VERSION}"
#  self.sys_version = ""

  # enumerate the request headers
  #for hdr in self.headers:
  #  print(hdr,self.headers[hdr])

# set the return time here (in time.time() format or None if current time required), this is included in send_response() as the "Date" HTTP header
  self.date_time_string(None)

  # Set the HTTP response code 200 ("OK")
  self.send_response(200)

  # Can include headers directly by the send_header() method
  self.send_header("Content-Type", "text/html")

  resp = "<html>"
  resp += "<head>"
  resp += "<script>function pop(o,i) { o.value = i }</script>"
  resp += "<style>"
  resp += "a[href] {color: #336699; text-decoration: none;}"
  resp += "a[href]:hover {color: red;}"
  resp += "#url { width: 30% }"

  resp += "</style>"
  resp += "</head>"
  resp += "<body>"
  resp += f"<h1>{SERVER_NAME}</h1>"

  postvars = {}

  if rq == "POST":
    ctype, pdict = cgi.parse_header(self.headers['content-type'])

    #print(ctype)
    if ctype == 'multipart/form-data':
        postvars = cgi.parse_multipart(self.rfile, pdict)
    elif ctype == 'application/x-www-form-urlencoded':
        length = int(self.headers['content-length'])
        postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)

    #print(postvars)

  url = dictget(dict=postvars, key="url")
  selector = dictget(dict=postvars, key="selector")
  attr = dictget(dict=postvars, key="attr", default_return="*")

  URLS=["https://www.oratechinfo.co.uk","https://www.google.com"]
  SELECTORS=["input[type=password]", "img","body", "style", "head", "svg", "script", "span", "a[href]","div[id]","input[type=hidden]","meta","input[type=button]","button"]
  ATTRS=["*","content", "link", "alt", "title", "src", "style", "href", "id", "name", "class", "type", "value", "onclick", "onload", "onmouseover"]

  resp += "<form method='POST' action='/'>"
  resp += "URL:<input type='url' id='url' name='url' value='" + html.escape(url) + f"' placeholder='e.g. {URLS[0]}'>"
  resp += opts(id="url", arr=URLS) 
  resp += "<br/>SELECTOR:<input type='text' id='selector' name='selector' value='" + html.escape(selector) + f"' placeholder='e.g. {SELECTORS[0]}'>"
  resp += opts(id="selector", arr=SELECTORS)
  resp += "<br/>ATTRIBUTE<input type='text' id='attr' name='attr' value='" + html.escape(attr) + f"' placeholder='e.g. {ATTRS[0]}'>"
  resp += opts(id="attr", arr=ATTRS)
  resp += "<br/><input type='submit' value='Submit'></form>"

  if rq == "POST":    
    #print("abc", url, selector, attr)
    try:
      things, fresp = sh.scraper(url=url, selector=selector)

      status_code = fresp.getcode()
      status_desc = responses[status_code]

      resp += f"<h4>HTTP Response Code : {status_code} ({status_desc})</h4>"

      if len(things) == 0:
      	resp += "<h4>No selection matches</h4>"
      else:
        resp += "<ul>"
        for i in things: 
          if attr == "*":
            attribute = str(i)
          else:
            attribute = i.get(attr)          

          if attribute:
            resp += "<li>" + html.escape(attribute) + "</li>"
          else:
            resp += "<li></li>"          	
        resp += "</ul>"
    except Exception as e:
      resp += f"<h4><i>{e}</i></h4>"

  resp += "</body>"
  resp += "</html>"

  self.send_header("Content-Length", str(len(resp)))

  self.end_headers()

  self.wfile.write(bytes(resp, ENCODING))
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
       wp(self, 'GET')
    def do_POST(self):
       wp(self, 'POST')
try:
# can specify the address specifically, and it will only serve with addresses exactly that
#    server = http.server.HTTPServer(('10.100.4.221', PORT), MyHandler)
    print(f"Starting on ({IPADDR},{PORT})")
    server = http.server.HTTPServer((IPADDR, PORT), MyHandler)
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
