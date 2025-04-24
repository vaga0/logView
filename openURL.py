from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

def create_web_view(parent, url):
    browser = QWebEngineView(parent)
    browser.setUrl(QUrl(url))
    return browser