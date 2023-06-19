import sys
import random
from functools import partial
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget, QFrame, QSizePolicy,QMessageBox, QLabel
from PyQt5.QtGui import QPainter, QColor, QKeyEvent, QPixmap
from PyQt5.QtCore import Qt, QSize, QRect, QTimer, QUrl
from PyQt5 import QtCore, QtGui, QtWidgets

class Enemy:
    def __init__(self, row, col):
        self.enrow = row
        self.encol = col

class Vrag:
    def __init__(self, row, col):
        self.enrow = row
        self.encol = col

class Boss:
    def __init__(self, row, col):
        self.enrow = row
        self.encol = col

class Door:
    def __init__(self, row, col):
        self.drow = row
        self.dcol = col

class Board3(QFrame):

    keyPressevent7 = QtCore.pyqtSignal()
    keyPressevent8 = QtCore.pyqtSignal()
    keyPressevent9 = QtCore.pyqtSignal()

    def __init__(self, parent, inner_walls=None):
        super().__init__(parent)

        self.cell_size = 50
        self.num_rows = 9
        self.num_cols = 13
        self.inner_walls = inner_walls
        self.initBoard()
        self.score = 0
        self.en = 0
        self.explosion_cells = []
        self.bomb = None  # Текущая бомба
        self.open_door = False #Отслеживание двери
        #переменные для отслеживания паузы
        self.start = True
        self.stop = False
        self.paused = False # Переменная для отслеживания состояния паузы
        self.bomb_timer = QTimer(self)  # Таймер для взрыва бомбы
        self.enemy = Enemy(7, 11)  # Начальные координаты врага
        self.vrag = Vrag(5, 5)
        self.boss = Boss(1, 11)
        self.player = Player(1, 1)  # Начальные координаты игрока
        self.door = Door(7, 1) # координаты двери
        self.bomb_timer.timeout.connect(self.explodeBomb)

    def initBoard(self):
        self.setStyleSheet("background-color: #333333;")

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMinimumSize(self.num_cols * self.cell_size, self.num_rows * self.cell_size)
        self.setMaximumSize(self.num_cols * self.cell_size, self.num_rows * self.cell_size)

        self.flagwin = False
        self.flaggameover = False

        self.enemy_timer = QTimer(self)  # Таймер для перемещения врага
        self.enemy_timer.timeout.connect(self.moveEnemy)
        self.enemy_timer.start(500)  # Запуск таймера с интервалом 0.5 секунды

        self.vrag_timer = QTimer(self)  # Таймер для перемещения врага
        self.vrag_timer.timeout.connect(self.moveVrag)
        self.vrag_timer.start(500)  # Запуск таймера с интервалом 0.5 секунды

        self.boss_timer = QTimer(self)  # Таймер для перемещения врага
        self.boss_timer.timeout.connect(self.moveBoss)
        self.boss_timer.start(500)  # Запуск таймера с интервалом 0.5 секунды

        self.score = 0
        self.score_label = QLabel(self)
        self.score_label.setGeometry(10, self.height() - 30, 200, 20)
        self.score_label.setStyleSheet("color: white")
        self.score_label.setText("Счёт: 0")

        self.bricks = self.generateBricks()
        self.update()

    def updateScore(self):
        self.score_label.setText("Счёт: {}".format(self.score))

    def pause(self):
        if not self.start:
            return

        self.stop = not self.stop

        if self.stop:
            self.paused = True
            self.enemy_timer.stop()
            self.vrag_timer.stop()
            self.boss_timer.stop()
            self.bomb = None
        else:
            self.paused = False
            self.enemy_timer.start()
            self.vrag_timer.start()
            self.boss_timer.start()
            self.bomb = None

        self.update()

    def resume(self):
        if not self.start or not self.stop:
            return
 
        self.paused = False
        self.enemy_timer.start()
        self.bomb = None
        self.update()

    def removeEnemy(self):
        if self.enemy is not None:
            enemy_row = self.enemy.enrow
            enemy_col = self.enemy.encol
            self.enemy = None
            self.score += 1000
            self.en += 1
            # Удалить клетку, на которой находился враг, из списка кирпичных стен
            if (enemy_row, enemy_col) in self.bricks:
                self.bricks.remove((enemy_row, enemy_col))
            self.update()
            self.updateScore()
        self.gameWin()
        print(self.score)

    def removeBoss(self):
        if self.boss is not None:
            boss_row = self.boss.enrow
            boss_col = self.boss.encol
            self.boss = None
            self.score += 1000
            self.en += 1
            # Удалить клетку, на которой находился враг, из списка кирпичных стен
            if (boss_row, boss_col) in self.bricks:
                self.bricks.remove((boss_row, boss_col))
            self.updateScore()
            self.update()
        self.gameWin()
        print(self.score)

    def removeVrag(self):
        if self.vrag is not None:
            vrag_row = self.vrag.enrow
            vrag_col = self.vrag.encol
            self.vrag = None
            self.score += 1000
            self.en += 1
            # Удалить клетку, на которой находился враг, из списка кирпичных стен
            if (vrag_row, vrag_col) in self.bricks:
                self.bricks.remove((vrag_row, vrag_col))
            self.updateScore()
            self.update()
        self.gameWin()
        print(self.score)

    def isGrayWall(self, row, col):
        return (row, col) in self.inner_walls
    
    def isWall(self, row, col):
        return (row, col) in self.inner_walls

    def isBrickWall(self, row, col):
        return (row, col) in self.bricks

    def removeBrickWall(self, row, col):
        self.bricks.remove((row, col))
        self.score += 200
        print(self.score)
        self.updateScore()
        self.update()

    def playerHitByExplosion(self):
        return (self.player.row, self.player.col) in [(cell.row, cell.col) for cell in self.explosion_cells]

    def generateBricks(self):
        bricks = []
        available_cells = [(row, col) for row in range(1, self.num_rows - 1) for col in range(1, self.num_cols - 1)]
        num_bricks = min(len(available_cells), 20)  # Количество кирпичных блоков (здесь ограничено 10)

        for _ in range(num_bricks):
            brick_pos = random.choice(available_cells)
            bricks.append(brick_pos)
            available_cells.remove(brick_pos)

        return bricks

    def sizeHint(self):
        return QSize(self.num_cols * self.cell_size, self.num_rows * self.cell_size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(150, 150, 150))
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.drawCell(painter, row, col)
        self.drawPlayer(painter)  # Отрисовка игрока
        self.drawBomb(painter)  # Отрисовка бомбы
        self.drawExplosion(painter)  # Отрисовка взрыва

        if self.enemy is not None:
            self.drawEnemy(painter)

        if self.vrag is not None:
            self.drawVrag(painter)

        if self.boss is not None:
            self.drawBoss(painter)

        if self.flagwin == True:  
            self.drawDoor(painter)

    def drawDoor(self, painter):
        x = (self.width() - self.num_cols * self.cell_size) // 2 + self.door.dcol * self.cell_size
        y = (self.height() - self.num_rows * self.cell_size) // 2 + self.door.drow * self.cell_size
        self.door_texture = QPixmap("door.jpg")
        painter.drawPixmap(QRect(x, y, self.cell_size, self.cell_size), self.door_texture)

        if (self.door.drow, self.door.dcol) == (self.player.row, self.player.col):
                    print('тут проблема')
                    
                    self.opendoor()
                    return
        else:
            print("нет двери")

    def drawBoss(self, painter):
        x = (self.width() - self.num_cols * self.cell_size) // 2 + self.boss.encol * self.cell_size
        y = (self.height() - self.num_rows * self.cell_size) // 2 + self.boss.enrow * self.cell_size
        self.boss_texture = QPixmap("boss.png")
        painter.drawPixmap(QRect(x, y, self.cell_size, self.cell_size), self.boss_texture)

    def drawEnemy(self, painter):
        x = (self.width() - self.num_cols * self.cell_size) // 2 + self.enemy.encol * self.cell_size
        y = (self.height() - self.num_rows * self.cell_size) // 2 + self.enemy.enrow * self.cell_size
        self.vrag_texture = QPixmap("vrag.png")
        painter.drawPixmap(QRect(x, y, self.cell_size, self.cell_size), self.vrag_texture)

    def drawVrag(self, painter):
        x = (self.width() - self.num_cols * self.cell_size) // 2 + self.vrag.encol * self.cell_size
        y = (self.height() - self.num_rows * self.cell_size) // 2 + self.vrag.enrow * self.cell_size
        self.vrag_texture = QPixmap("vrag.png")
        painter.drawPixmap(QRect(x, y, self.cell_size, self.cell_size), self.vrag_texture)

    def moveEnemy(self):
        if self.enemy is not None:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Возможные направления движения
            valid_directions = []

            for direction in directions:
                next_row = self.enemy.enrow + direction[0]
                next_col = self.enemy.encol + direction[1]

                if (0 < next_row < self.num_rows - 1 and 0 < next_col < self.num_cols - 1) and \
                        (next_row, next_col) != (self.player.row, self.player.col) and \
                        not self.isWall(next_row, next_col) and \
                        not self.isBrickWall(next_row, next_col):
                    valid_directions.append(direction)
                if self.enemy is not None:
                    if (self.enemy.enrow, self.enemy.encol) == (self.player.row, self.player.col):
                        self.pause()
                        self.gameOver()
                        return

            if valid_directions:
                direction = random.choice(valid_directions)  # Случайный выбор направления из доступных
                self.enemy.enrow += direction[0]
                self.enemy.encol += direction[1]

            self.update()

    def moveVrag(self):
        if self.vrag is not None:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Возможные направления движения
            valid_directions = []

            for direction in directions:
                next_row = self.vrag.enrow + direction[0]
                next_col = self.vrag.encol + direction[1]

                if (0 < next_row < self.num_rows - 1 and 0 < next_col < self.num_cols - 1) and \
                        (next_row, next_col) != (self.player.row, self.player.col) and \
                        not self.isWall(next_row, next_col) and \
                        not self.isBrickWall(next_row, next_col):
                    valid_directions.append(direction)
                if self.vrag is not None:
                    if (self.vrag.enrow, self.vrag.encol) == (self.player.row, self.player.col):
                        self.pause()
                        self.gameOver()
                        return

            if valid_directions:
                direction = random.choice(valid_directions)  # Случайный выбор направления из доступных
                self.vrag.enrow += direction[0]
                self.vrag.encol += direction[1]

            self.update()

    def moveBoss(self):
        if self.boss is not None:
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Возможные направления движения
            valid_directions = []

            for direction in directions:
                next_row = self.boss.enrow + direction[0]
                next_col = self.boss.encol + direction[1]

                if (0 < next_row < self.num_rows - 1 and 0 < next_col < self.num_cols - 1) and \
                        (next_row, next_col) != (self.player.row, self.player.col) and \
                        not self.isWall(next_row, next_col):
                    valid_directions.append(direction)
                if self.boss is not None:
                    if (self.boss.enrow, self.boss.encol) == (self.player.row, self.player.col):
                        self.pause()
                        self.gameOver()
                        return

            if valid_directions:
                direction = random.choice(valid_directions)  # Случайный выбор направления из доступных
                self.boss.enrow += direction[0]
                self.boss.encol += direction[1]

            self.update()

    def drawExplosion(self, painter):
        for cell in self.explosion_cells:
            x = (self.width() - self.num_cols * self.cell_size) // 2 + cell.col * self.cell_size
            y = (self.height() - self.num_rows * self.cell_size) // 2 + cell.row * self.cell_size

            if self.isGrayWall(cell.row, cell.col):  # Проверка, является ли клетка серой стеной
                color = QColor(150, 150, 150)  # Серый цвет для серых стен
            elif 0 < cell.row < self.num_rows - 1 and 0 < cell.col < self.num_cols - 1:
                color = QColor(255, 255, 0)  # Желтый цвет для клеток взрыва
            else:
                continue  # Пропустить закрашивание клетки на периметре

            painter.fillRect(QRect(x, y, self.cell_size, self.cell_size), color)
            painter.drawRect(QRect(x, y, self.cell_size, self.cell_size))

    def drawBomb(self, painter):
        
        if self.bomb:
            bomb = self.bomb
            x = (self.width() - self.num_cols * self.cell_size) // 2 + bomb.col * self.cell_size
            y = (self.height() - self.num_rows * self.cell_size) // 2 + bomb.row * self.cell_size
            
            if not bomb.exploded:
                # Картинка при установке бомбы
                self.bomb_texture = QPixmap("bomb.jpg")
                painter.drawPixmap(QRect(x, y, self.cell_size, self.cell_size), self.bomb_texture)
            else:
                # Желтый квадрат при взрыве
                color = QColor(255, 255, 0)
                painter.fillRect(QRect(x, y, self.cell_size, self.cell_size), color)
                painter.drawRect(QRect(x, y, self.cell_size, self.cell_size))
                
                # Желтая клетка взрыва
                cell_x = (self.width() - self.num_cols * self.cell_size) // 2 + bomb.col * self.cell_size
                cell_y = (self.height() - self.num_rows * self.cell_size) // 2 + bomb.row * self.cell_size
                painter.fillRect(QRect(cell_x, cell_y, self.cell_size, self.cell_size), color)
                painter.drawRect(QRect(cell_x, cell_y, self.cell_size, self.cell_size))
                
                # Сбросить состояние бомбы после 2 секунд
                QTimer.singleShot(500, self.resetBomb)

    def opendoor(self):
        
        if self.open_door == True:
            print("Дверь открыта")
        else:
            self.open_door = True
            gameWin = QMessageBox()
            gameWin.setWindowTitle("Конец игры")
            gameWin.setText("Игра окончена. Вы победили! \n Вы набрали: " + str(self.score))
            gameWin.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            gameWin.setDefaultButton(QMessageBox.Yes)
            new_game_button = gameWin.button(QMessageBox.Yes)
            new_game_button.setText("Новая игра")
            main_menu_button = gameWin.button(QMessageBox.No)
            main_menu_button.setText("Главное меню")
            reply = gameWin.exec()

            if reply == QMessageBox.Yes:
                    self.keyPressevent8.emit()
            elif reply == QMessageBox.No:
                    self.keyPressevent9.emit()

            print("Game Win")

    def resetBomb(self):
        self.bomb = None
        self.explosion_cells = []
        self.update()

    def drawCell(self, painter, row, col):
        x = (self.width() - self.num_cols * self.cell_size) // 2 + col * self.cell_size
        y = (self.height() - self.num_rows * self.cell_size) // 2 + row * self.cell_size


        if row == 0 or row == self.num_rows - 1 or col == 0 or col == self.num_cols - 1:  # Внешние серые стены
            color = QColor(150, 150, 150)
            self.texture = QPixmap("texture.png")
            painter.fillRect(QRect(x, y, self.cell_size, self.cell_size), color)
            painter.drawPixmap(QRect(x, y, self.cell_size, self.cell_size), self.texture)
            painter.drawRect(QRect(x, y, self.cell_size, self.cell_size))
        elif self.inner_walls and (row, col) in self.inner_walls:  # Внутренние серые стены
            color = QColor(150, 150, 150)
            self.texture = QPixmap("texture.png")
            painter.fillRect(QRect(x, y, self.cell_size, self.cell_size), color)
            painter.drawPixmap(QRect(x, y, self.cell_size, self.cell_size), self.texture)
            painter.drawRect(QRect(x, y, self.cell_size, self.cell_size))
        elif (row, col) in self.bricks:  # Кирпичные блоки
            color = QColor(200, 100, 100)
            self.texture2 = QPixmap("texture2.jpg")
            painter.fillRect(QRect(x, y, self.cell_size, self.cell_size), color)
            painter.drawPixmap(QRect(x, y, self.cell_size, self.cell_size), self.texture2)
            painter.drawRect(QRect(x, y, self.cell_size, self.cell_size))
        
        else:  # Обычные пустые клетки
            color = QColor(255, 255, 255)
            painter.fillRect(QRect(x, y, self.cell_size, self.cell_size), color)
            painter.drawRect(QRect(x, y, self.cell_size, self.cell_size))

    def drawPlayer(self, painter):
        x = (self.width() - self.num_cols * self.cell_size) // 2 + self.player.col * self.cell_size
        y = (self.height() - self.num_rows * self.cell_size) // 2 + self.player.row * self.cell_size
        self.player_texture = QPixmap("player.png")
        painter.drawPixmap(QRect(x, y, self.cell_size, self.cell_size), self.player_texture)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key_P:
                self.pause()
                return
        if not self.paused:  # Проверка, не находится ли игра на паузе
            if key == Qt.Key_Escape:
                self.pause()
                self.keyPressevent7.emit()
                return

            if key == Qt.Key_Space:
                if self.bomb is None:
                    self.bomb = Bomb(self.player.row, self.player.col, self)
                    QTimer.singleShot(2000, partial(self.bomb.explode, self))
                    self.update()
            elif key == Qt.Key_W:
                next_row = self.player.row - 1
                if (next_row, self.player.col) not in self.inner_walls and (next_row, self.player.col) not in self.bricks and next_row > 0:
                    self.player.move_up()
            elif key == Qt.Key_S:
                next_row = self.player.row + 1
                if (next_row, self.player.col) not in self.inner_walls and (next_row, self.player.col) not in self.bricks and next_row < self.num_rows - 1:
                    self.player.move_down()
            elif key == Qt.Key_A:
                next_col = self.player.col - 1
                if (self.player.row, next_col) not in self.inner_walls and (self.player.row, next_col) not in self.bricks and next_col > 0:
                    self.player.move_left()
            elif key == Qt.Key_D:
                next_col = self.player.col + 1
                if (self.player.row, next_col) not in self.inner_walls and (self.player.row, next_col) not in self.bricks and next_col < self.num_cols - 1:
                    self.player.move_right()
        self.update()

    def gameWin(self):
        if self.flaggameover == True:
            print('jf')
        if self.en == 3:
            self.flagwin = True
            self.update()

    def gameOver(self):
        self.flaggameover = True
        if self.flagwin == True:
            print('Почти проиграл')
        else:
            game_over = QMessageBox()
            game_over.setWindowTitle("Конец игры")
            game_over.setText("Игра окончена. Выберите дальнейшее действие \n Вы набрали: " + str(self.score))
            game_over.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            game_over.setDefaultButton(QMessageBox.Yes)

            new_game_button = game_over.button(QMessageBox.Yes)
            new_game_button.setText("Новая игра")

            main_menu_button = game_over.button(QMessageBox.No)
            main_menu_button.setText("Главное меню")

            reply = game_over.exec()

            if reply == QMessageBox.Yes:
                self.keyPressevent8.emit()
            elif reply == QMessageBox.No:
                self.keyPressevent9.emit()
                
                
            print("Game Over")

    def placeBomb(self):
        self.bomb = Bomb(self.player.row, self.player.col)
        self.bomb_timer.start(2000)  # Запуск таймера на 2 секунды

    def explodeBomb(self):
        if self.bomb:
            self.bomb_timer.stop()  # Остановка таймера

            # Логика взрыва бомбы
            bomb = self.bomb
            self.bomb = None
            if self.enemy is not None:
                bomb.explode(self)

            if self.vrag is not None:
                bomb.explode(self)

            if self.boss is not None:
                bomb.explode(self)

class Bomb:
    
    def __init__(self, row, col,parent):
        self.row = row
        self.col = col
        self.board = parent
        self.color = QColor(0, 0, 0)  # Чёрный цвет при закладке бомбы
        self.exploded = False  # Флаг взрыва

    def getColor(self):
        return self.color

    def explode(self, inner_walls):
        print('boom!')
        explosion_cells = []
        
        if not self.exploded:
            self.exploded = True
            explosion_cells.append(ExplosionCell(self.row, self.col))  # Центральная клетка

            # Взрыв на 9 клеток
            for row in range(self.row - 1, self.row + 2):
                for col in range(self.col - 1, self.col + 2):
                    if 0 <= row < self.board.num_rows and 0 <= col < self.board.num_cols:
                        cell = ExplosionCell(row, col)
                        explosion_cells.append(cell)
                        if self.board.isBrickWall(row, col):
                            self.board.removeBrickWall(row, col)


        self.board.explosion_cells = explosion_cells
        self.exploded = True

        # Проверка столкновения с игроком
        if self.board.playerHitByExplosion():
            self.board.pause()
            self.board.gameOver()

        #Проверка столкновения с врагом
        if self.board.enemy is not None:
            enemy = self.board.enemy
            if (enemy.enrow, enemy.encol) in [(cell.row, cell.col) for cell in explosion_cells]:
                self.board.removeEnemy()

        #Проверка столкновения с врагом2
        if self.board.vrag is not None:
            vrag = self.board.vrag
            if (vrag.enrow, vrag.encol) in [(cell.row, cell.col) for cell in explosion_cells]:
                self.board.removeVrag()

        #Проверка столкновения с врагом2
        if self.board.boss is not None:
            boss = self.board.boss
            if (boss.enrow, boss.encol) in [(cell.row, cell.col) for cell in explosion_cells]:
                self.board.removeBoss()

class ExplosionCell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move_up(self):
        if self.row > 0:
            self.row -= 1

    def move_down(self):
        if self.row < 8:
            self.row += 1

    def move_left(self):
        if self.col > 0:
            self.col -= 1

    def move_right(self):
        if self.col < 12:
            self.col += 1
