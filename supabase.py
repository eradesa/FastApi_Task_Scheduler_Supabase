#import urlparse

from urllib.parse import urlparse

#url = "https://www.example.com/path/to/page.html?query=string#fragment"




url = "https://tdhsckeqhmxbovyuumtp.supabase.co" # replace with your Supabase URL
result = urlparse(url)
database = result.path[1:]
user = result.username
password = result.password
host = result.hostname
port = result.port

parsed_url = urlparse(url)

print(parsed_url.scheme)  # prints "https"
print(parsed_url.netloc)  # prints "www.example.com"
print(parsed_url.path)    # prints "/path/to/page.html"
print(port)   # prints "query=string"
print(database)  # prints "fragment"