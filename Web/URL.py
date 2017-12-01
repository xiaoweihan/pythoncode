#coding=utf-8
import urlparse
import urllib
def main():
    url = 'https://www.hao123.com/'

    f = urllib.urlopen(url)

    print f.read()

    f.close()

if __name__ == '__main__':
    main()