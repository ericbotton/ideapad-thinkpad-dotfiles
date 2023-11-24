from urllib.request import urlopen

url = input("Enter the html url: ")
# url = "https://www.ign.com/articles/2006/12/21/neverwinter-nights-2-item-id-datasbase-752101"

page = urlopen(url)
print('HTTPResponse object  ' + page)

html_bytes = page.read()
html = html_bytes.decode("utf-8")
html

'''
print(html)
'''
print("''' new file '''\n", file=open('/Users/Owner/html.txt', 'a'))
print(html, file=open('/Users/Owner/html.txt', 'a'))
