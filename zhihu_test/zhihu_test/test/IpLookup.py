import urllib.request
import re
import json
def ipLookup(ip='127.0.0.1'):
    url='https://www.ip138.com/iplookup.asp?ip={0}&action=2'.format(ip)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    with urllib.request.urlopen(req) as response:
         the_page = response.read()
    response=the_page.decode("gb2312")
    result=re.compile('var ip_result =(.*);').search(response)
    return json.loads(result.group(1))

if __name__ == '__main__':
    print(ipLookup())