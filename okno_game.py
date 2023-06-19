import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget, QMessageBox
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from log_game import Board
from log_game2 import Board2
from log_game3 import Board3

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(520, 680)
        MainWindow.setStyleSheet("background-color: rgb(245,255,250)")
        self.main_window = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 520, 150))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(180, 190, 160, 60))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_start.setFont(font)
        self.btn_start.setObjectName("btn_start")
        self.btn_settings = QtWidgets.QPushButton(self.centralwidget)
        self.btn_settings.setGeometry(QtCore.QRect(180, 290, 160, 60))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_settings.setFont(font)
        self.btn_settings.setObjectName("btn_settings")
        self.btn_rules = QtWidgets.QPushButton(self.centralwidget)
        self.btn_rules.setGeometry(QtCore.QRect(180, 390, 160, 60))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_rules.setFont(font)
        self.btn_rules.setObjectName("btn_rules")
        self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exit.setGeometry(QtCore.QRect(180, 490, 160, 60))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_exit.setFont(font)
        self.btn_exit.setObjectName("btn_exit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.music_player = QMediaPlayer()
        self.music_file = "Not.mp3"  # Замените на путь к вашему аудиофайлу
        self.music_playing = False

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.rules_dialog = None  # Переменная окна правил игры
        # Добавьте переменные QMediaPlayer
        
        self.add_functions()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главное меню"))
        self.label.setText(_translate("MainWindow", "Bomberman"))
        self.btn_start.setText(_translate("MainWindow", "Старт"))
        self.btn_settings.setText(_translate("MainWindow", "Настройки"))
        self.btn_rules.setText(_translate("MainWindow", "Правила"))
        self.btn_exit.setText(_translate("MainWindow", "Выход из игры"))

    def add_functions(self):
        self.btn_start.clicked.connect(lambda: self.open_yr_window())
        self.btn_settings.clicked.connect(lambda: self.start_settings())
        self.btn_rules.clicked.connect(lambda: self.pravila_game())
        self.btn_exit.clicked.connect(lambda: self.close_game())

    def open_yr_window(self):
        self.main_window.close()
        self.yrwindow = Ui_YRWindow(self.main_window)
        self.yrwindow.show()

    def start_settings(self):
        self.main_window.close()
        self.settings = SettingsWindow()
        self.settings.main_window = self.main_window
        self.settings.show()


    def close_game(self):
        reply = QMessageBox.question(
        self.main_window, "Выход", "Вы уверены, что хотите выйти из игры?", QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.main_window.close()
        else:
            self.main_window.show()
    
    def pravila_game(self):
        if not self.rules_dialog:  # Проверяем, существует ли уже окно правил игры
            self.rules_dialog = QMessageBox(self.main_window)
            self.rules_dialog.setWindowTitle("Правила игры")
            self.rules_dialog.setText("Цель игры - победить врагов, удалить стены и найти выход\n\n"
                                "1. Пользователь управляет персонажем Бомберменом на арене, похожей на лабиринт.\n"
                                "2. Пользователь может размещать бомбы, чтобы уничтожать препятствия и врагов\n"
                                "3. Бомбы могут нанести вред игроку, если он попал в зону поражения\n"
                                "4. Каждый уровень становится все сложнее из-за улучшения и увеличения кол-ва врагов\n"
                                "5. Игроки могут использовать стратегию, следить за врагами и взрывать с помощью бомб\n"
                                "6. При удалении стен появляются бонусы, который можно использовать для увеличения скорости игрока или дальности взрыва бомб\n"
                                "7. Очки начисляются за убитых врагов и сломанные стены\n\n"
                                "Удачи!")
            self.rules_dialog.setStandardButtons(QMessageBox.Ok)
        self.rules_dialog.exec_()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
            
        if key == Qt.Key_Z:
            self.toggle_music()
            return
        
    def toggle_music(self):
        if self.music_playing:
            self.music_player.stop()
            self.music_playing = False
        else:
            self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.music_file)))
            self.music_player.play()
            self.music_playing = True

class Ui_YRWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.InitUi(self)
        self.main_window = main_window


    def InitUi(self, YRWindow):
        YRWindow.setObjectName("YRWindow")
        YRWindow.resize(520, 680)
        YRWindow.setStyleSheet("background-color: rgb(245,255,250)")

        self.centralwidget = QtWidgets.QWidget(YRWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 520, 75))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.izi_btn = QtWidgets.QPushButton(self.centralwidget)
        self.izi_btn.setGeometry(QtCore.QRect(160, 190, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.izi_btn.setFont(font)
        self.izi_btn.setObjectName("izi_btn")

        self.sl_btn = QtWidgets.QPushButton(self.centralwidget)
        self.sl_btn.setGeometry(QtCore.QRect(160, 450, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sl_btn.setFont(font)
        self.sl_btn.setObjectName("sl_btn")

        self.sr_btn = QtWidgets.QPushButton(self.centralwidget)
        self.sr_btn.setGeometry(QtCore.QRect(160, 320, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sr_btn.setFont(font)
        self.sr_btn.setObjectName("sr_btn")

        self.gl_btn = QtWidgets.QPushButton(self.centralwidget)
        self.gl_btn.setGeometry(QtCore.QRect(160, 550, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.gl_btn.setFont(font)
        self.gl_btn.setObjectName("gl_btn")

        self.music_player = QMediaPlayer()
        self.music_file = "Not.mp3"  # Замените на путь к вашему аудиофайлу
        self.music_playing = False

        YRWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(YRWindow)
        QtCore.QMetaObject.connectSlotsByName(YRWindow)
        self.add_functions()
        self.show()

    def retranslateUi(self, YRWindow):
        _translate = QtCore.QCoreApplication.translate
        YRWindow.setWindowTitle(_translate("YRWindow", "Выбор уровня"))
        self.label.setText(_translate("YRWindow", "Bomberman"))
        self.izi_btn.setText(_translate("YRWindow", "Лёгкий уровень"))
        self.sl_btn.setText(_translate("YRWindow", "Сложный уровень"))
        self.sr_btn.setText(_translate("YRWindow", "Средний уровень"))
        self.gl_btn.setText(_translate("YRWindow", "Главное меню"))

    def add_functions(self):
        self.izi_btn.clicked.connect(self.start_game)
        self.sr_btn.clicked.connect(self.start_game2)
        self.sl_btn.clicked.connect(self.start_game3)
        self.gl_btn.clicked.connect(self.menu)

    def menu(self):
        self.close()
        self.main_window.show()

    def start_game(self):
        self.close()
        self.board = GameWindow()
        self.board.show()
    
    def start_game2(self):
        self.close()
        self.board = GameWindow2()
        self.board.show()

    def start_game3(self):
        self.close()
        self.board = GameWindow3()
        self.board.show()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
            
        if key == Qt.Key_Z:
            self.toggle_music()
            return
        
    def toggle_music(self):
        if self.music_playing:
            self.music_player.stop()
            self.music_playing = False
        else:
            self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.music_file)))
            self.music_player.play()
            self.music_playing = True

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, SetWindow):
        SetWindow.setObjectName("SetWindow")
        self.main_window = MainWindow
        SetWindow.resize(520, 680)
        SetWindow.setStyleSheet("background-color: rgb(245,255,250);")
        self.centralwidget = QtWidgets.QWidget(SetWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelup = QtWidgets.QLabel(self.centralwidget)
        self.labelup.setGeometry(QtCore.QRect(100, 150, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.labelup.setFont(font)
        self.labelup.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.labelup.setTextFormat(QtCore.Qt.RichText)
        self.labelup.setAlignment(QtCore.Qt.AlignCenter)
        self.labelup.setObjectName("labelup")
        self.labelw = QtWidgets.QLabel(self.centralwidget)
        self.labelw.setGeometry(QtCore.QRect(320, 150, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(14)
        self.labelw.setFont(font)
        self.labelw.setStyleSheet("background-color: rgb(245,255,250);")
        self.labelw.setObjectName("labelw")
        self.labeldown = QtWidgets.QLabel(self.centralwidget)
        self.labeldown.setGeometry(QtCore.QRect(100, 210, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.labeldown.setFont(font)
        self.labeldown.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.labeldown.setAlignment(QtCore.Qt.AlignCenter)
        self.labeldown.setObjectName("labeldown")
        self.labels = QtWidgets.QLabel(self.centralwidget)
        self.labels.setGeometry(QtCore.QRect(320, 210, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.labels.setFont(font)
        self.labels.setObjectName("labels")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(100, 270, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(320, 270, 150, 48))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(100, 330, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(320, 330, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(100, 390, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(320, 390, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(100, 450, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(320, 450, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(100, 510, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(320, 510, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.btn_menu = QtWidgets.QPushButton(self.centralwidget)
        self.btn_menu.setGeometry(QtCore.QRect(160, 600, 200, 50))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(12)
        self.btn_menu.setFont(font)
        self.btn_menu.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.btn_menu.setObjectName("pushButton")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(0, 0, 520, 100))
        font = QtGui.QFont()
        font.setFamily("Forum")
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        SetWindow.setCentralWidget(self.centralwidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.music_player = QMediaPlayer()
        self.music_file = "Not.mp3"  # Замените на путь к вашему аудиофайлу
        self.music_playing = False

        self.retranslateUi(SetWindow)
        QtCore.QMetaObject.connectSlotsByName(SetWindow)
        self.add_functions()
        self.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Настройки"))
        self.labelup.setText(_translate("MainWindow", "Движение вверх"))
        self.labelw.setText(_translate("MainWindow", "W"))
        self.labeldown.setText(_translate("MainWindow", "Движение вниз"))
        self.labels.setText(_translate("MainWindow", "S"))
        self.label_5.setText(_translate("MainWindow", "Движение вправо"))
        self.label_6.setText(_translate("MainWindow", "D"))
        self.label_7.setText(_translate("MainWindow", "Движение влево"))
        self.label_8.setText(_translate("MainWindow", "A"))
        self.label_9.setText(_translate("MainWindow", "Поставить бомбу"))
        self.label_10.setText(_translate("MainWindow", "Space"))
        self.label_11.setText(_translate("MainWindow", "Пауза"))
        self.label_12.setText(_translate("MainWindow", "Esc или P"))
        self.label_13.setText(_translate("MainWindow", "Вкл/Выкл звук"))
        self.label_14.setText(_translate("MainWindow", "Z"))
        self.btn_menu.setText(_translate("MainWindow", "Назад в главное меню"))
        self.label_15.setText(_translate("MainWindow", "Bomberman"))

    def add_functions(self):
        self.btn_menu.clicked.connect(lambda: self.menu())

    def menu(self):
        self.close()
        self.main_window.show()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
            
        if key == Qt.Key_Z:
            self.toggle_music()
            return
        
    def toggle_music(self):
        if self.music_playing:
            self.music_player.stop()
            self.music_playing = False
        else:
            self.music_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.music_file)))
            self.music_player.play()
            self.music_playing = True

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Bomberman")
        self.grid_layout = QGridLayout()

        # Координаты внутренних стен
        inner_walls = [(2, 2), (2, 4), (2, 6), (2, 8), (2, 10),
                       (4, 2), (4, 4), (4, 6), (4, 8),  (4, 10),
                       (6, 2), (6, 4), (6, 6), (6, 8),  (6, 10)]

        self.board = Board(self, inner_walls=inner_walls) # Передача inner_walls в класс Board

        self.grid_layout.addWidget(self.board, 0, 0, Qt.AlignCenter)
        self.board.keyPressevent.connect(self.pause_esc)
        self.board.keyPressevent2.connect(self.start_game)
        self.board.keyPressevent3.connect(self.menu)
        central_widget = QWidget()
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)

        self.resize(620, 780)
        self.show()

    def menu(self):
        self.board.close()
        self.close()
        self.main_window = MainWindow
        self.main_window.show()

    def start_game(self):
        self.board.close()
        self.close()
        self.board2 = GameWindow()
        self.board2.show()
    
    def pause_esc(self):
        escape = QMessageBox()
        escape.setWindowTitle("Игра приостановлена")
        escape.setText("Выберите дальнейшее действие")
        escape.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Reset)

        new_button = escape.button(QMessageBox.Yes)
        new_button.setText("Новая игра")

        main_button = escape.button(QMessageBox.No)
        main_button.setText("Главное меню")

        resume_button = escape.button(QMessageBox.Reset)
        resume_button.setText("Продолжить")

        escape.exec()
        clicked_button = escape.clickedButton()

        if clicked_button == new_button:
            print('новая игра')
            self.start_game()
            self.board.resume()
        elif clicked_button == main_button:
            print('меню')
            self.menu()
        elif clicked_button == resume_button:
            self.board.resume()

    def keyPressEvent(self, event: QKeyEvent):
        self.board.keyPressEvent(event)

class GameWindow2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Bomberman")
        self.grid_layout = QGridLayout()

        # Координаты внутренних стен
        inner_walls = [(2, 2), (2, 4), (2, 6), (2, 8), (2, 10),
                       (4, 2), (4, 4), (4, 6), (4, 8),  (4, 10),
                       (6, 2), (6, 4), (6, 6), (6, 8),  (6, 10)]

        self.board = Board2(self, inner_walls=inner_walls)  # Передача inner_walls в класс Board

        self.grid_layout.addWidget(self.board, 0, 0, Qt.AlignCenter)
        self.board.keyPressevent4.connect(self.pause_esc)
        self.board.keyPressevent5.connect(self.start_game)
        self.board.keyPressevent6.connect(self.menu)
        central_widget = QWidget()
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)

        self.resize(620, 780)
        self.show()

    def menu(self):
        self.board.close()
        self.close()
        self.main_window = MainWindow
        self.main_window.show()

    def start_game(self):
        self.board.close()
        self.close()
        self.gboard = GameWindow2()
        self.gboard.show()
    
    def pause_esc(self):
        escape = QMessageBox()
        escape.setWindowTitle("Игра приостановлена")
        escape.setText("Выберите дальнейшее действие")
        escape.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Reset)

        new_button = escape.button(QMessageBox.Yes)
        new_button.setText("Новая игра")

        main_button = escape.button(QMessageBox.No)
        main_button.setText("Главное меню")

        resume_button = escape.button(QMessageBox.Reset)
        resume_button.setText("Продолжить")

        escape.exec()
        clicked_button = escape.clickedButton()

        if clicked_button == new_button:
            print('новая игра')
            self.start_game()
            self.board.resume()
        elif clicked_button == main_button:
            print('меню')
            self.menu()
        elif clicked_button == resume_button:
            self.board.resume()

    def keyPressEvent(self, event: QKeyEvent):
        self.board.keyPressEvent(event)

class GameWindow3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Bomberman")
        self.grid_layout = QGridLayout()

        # Координаты внутренних стен
        inner_walls = [(2, 2), (2, 4), (2, 6), (2, 8), (2, 10),
                       (4, 2), (4, 4), (4, 6), (4, 8),  (4, 10),
                       (6, 2), (6, 4), (6, 6), (6, 8),  (6, 10)]

        self.board = Board3(self, inner_walls=inner_walls)  # Передача inner_walls в класс Board

        self.grid_layout.addWidget(self.board, 0, 0, Qt.AlignCenter)
        self.board.keyPressevent7.connect(self.pause_esc)
        self.board.keyPressevent8.connect(self.start_game)
        self.board.keyPressevent9.connect(self.menu)
        central_widget = QWidget()
        central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(central_widget)

        self.resize(620, 780)
        self.show()

    def menu(self):
        self.board.close()
        self.close()
        self.main_window = MainWindow
        self.main_window.show()

    def start_game(self):
        self.board.close()
        self.close()
        self.gboard2 = GameWindow3()
        self.gboard2.show()
    
    def pause_esc(self):
        escape = QMessageBox()
        escape.setWindowTitle("Игра приостановлена")
        escape.setText("Выберите дальнейшее действие")
        escape.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Reset)

        new_button = escape.button(QMessageBox.Yes)
        new_button.setText("Новая игра")

        main_button = escape.button(QMessageBox.No)
        main_button.setText("Главное меню")

        resume_button = escape.button(QMessageBox.Reset)
        resume_button.setText("Продолжить")

        escape.exec()
        clicked_button = escape.clickedButton()

        if clicked_button == new_button:
            print('новая игра')
            self.start_game()
            # self.board.resume()
        elif clicked_button == main_button:
            print('меню')
            self.menu()
        elif clicked_button == resume_button:
            self.board.resume()

    def keyPressEvent(self, event: QKeyEvent):
        self.board.keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())