import re


url = 'http://example.webscraping.com/places/default/view/Australia-1'
re.sub('[^/0-9a-zA-Z\-.,; _]', '_', url)
