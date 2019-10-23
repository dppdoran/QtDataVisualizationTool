import sys
import argparse
import pandas as pd
from PySide2.QtWidgets import QApplication, QMainWindow, QAction
from PySide2.QtCore import QDateTime, QTimeZone, Slot

def transform_date(utc, timezone=None):
    utc_format = "yyyy-MM-ddTHH:mm:ss.zzzZ"
    new_date = QDateTime().fromString(utc, utc_format)
    if timezone:
        new_date.setTimeZone(timezone)
    return new_date

def read_data(fname):
    # Read the csv data
    df = pd.read_csv(fname)

    # Remove incorrect magnitudes
    df = df.drop(df[df.mag < 0].index)
    magnitudes = df["mag"]

    # Local timezone
    timezone = QTimeZone(b"Europe/Berlin")

    # Get timestamps transformed to local timezone
    times = df["time"].apply(lambda x: transform_date(x, timezone))
    return times, magnitudes

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Earthquakes information")
        # Setup menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)
        self.status = self.statusBar()
        self.status.showMessage('Data loaded and plotted.')

        geometry = app.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    @Slot()
    def exit_app(self, checked):
        sys.exit()


if __name__ == '__main__':
    options = argparse.ArgumentParser()
    options.add_argument("-f", "--file", type=str, required=True)
    args = options.parse_args()
    data = read_data(args.file)
    print(data)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
