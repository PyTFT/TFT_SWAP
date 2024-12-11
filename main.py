from ui import MyMainWindow
from PySide6.QtWidgets import QApplication

app = QApplication([])
window = MyMainWindow()
window.show()
app.exec()