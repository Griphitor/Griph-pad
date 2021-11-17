import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv)
web = QWebEngineView()

def render(file_path:str):
    url = 'file:///%s' % file_path.replace("\\", "/")
    web.load(QUrl(url))
    web.show()
    app.exec_()
