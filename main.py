import sys
from PyQt6.QtWidgets import QApplication
from models.database import Database
from views.main_view import MainView

def main():
    Database()
    app = QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()