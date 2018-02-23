__license__ = 'GPL v3'
__copyright__ = '2018 cove9988@gmail.com'
from urllib3 import ProxyManager, make_headers
from bs4 import BeautifulSoup
import re
import datetime
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys


def get_page(url, proxy, header):
    http = ProxyManager(proxy_url = proxy, headers=header)
    r = http.request('GET', url)
    return BeautifulSoup(r.data, 'lxml')


def news_header(soup):
    lns = "<p><h3>Click on a news title to remove anyone you don't want read, keep the rest of them and click the submit button to read them all </h3></p>"
    # not in a day different timezone
    news_date = 'news/' + datetime.datetime.today().strftime('%Y/%m')
    links = soup.find_all(href=re.compile(news_date))
    button_line = '''<b><button onclick="style.display = 'none'"> '''
    for l in links:
        lns = lns + button_line + l.prettify() + '</button></b>'
    return lns


def load_browser(lns, url):
    app = QApplication(sys.argv)
    view = QWebEngineView()
    view.setWindowTitle = url
    html = '''<!DOCTYPE html> 
    <html> 
        <body> '''  + lns +  ''' 
    <p><input type='submit' name='a1' value='get all news on list' onclick='button.style.display = "none";'></p>
        </body>
    </html>'''
    view.show()
    view.setHtml(html)
    # view.setUrl(QUrl(url))
    app.exec()


if __name__ == '__main__':
    url = "http://www.wenxuecity.com"
    proxy = "http://your.company.proxy:8080"
    default_headers = make_headers(proxy_basic_auth='usrname:pwd')
    soup = get_page(url, proxy, default_headers)
    lns = news_header(soup)
    load_browser(lns, url)
