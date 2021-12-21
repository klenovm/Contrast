import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw

myImage = "image2.jpg"
newImage = 'newImage.jpg'

class Contr(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def on_click(self): #линейное контрастирование
        image = Image.open(myImage)  # Открываем изображение
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
        width = image.size[0]  # Определяем ширину
        height = image.size[1]  # Определяем высоту
        pix = image.load()  # Выгружаем значения пикселей
        ymin = 0
        ymax = 255
        gist = [0 for i in range(256)]
        print(type(pix[0, 0]))

        if type(pix[0,0]) is int: # проверка типа пискелей(монохромные или цветные)
            for i in range(width): #строим гистограмму
                for j in range(height):
                    gist[pix[i, j]] += 1
            xmin = -1
            xmax = -1
            for i in range(256): #находим макс и мин гистограммы
                if gist[i]>0:
                    xmax = i
                    if xmin<0:
                        xmin = i

            for i in range(width):
                for j in range(height):
                    y = pix[i,j]
                    y2 = (y-xmin)/(xmax-xmin)*(ymax-ymin)+ymin
                    draw.point((i,j), round(y2))

        else:
            for i in range(width):
                for j in range(height):
                    r, g, b = pix[i, j][0], pix[i, j][1], pix[i, j][2]
                    y = round(0.299 * r + 0.587 * g + 0.114 * b)
                    gist[y] += 1

            xmin = -1
            xmax = -1
            for i in range(256):
                if (xmin < 0) and gist[i] != 0:
                    xmin = i
                if gist[i] != 0:
                    xmax = i
            for i in range(width):
                for j in range(height):
                    r, g, b = pix[i, j][0], pix[i, j][1], pix[i, j][2]
                    y = 0.299 * r + 0.587 * g + 0.114 * b
                    y2 = (y - xmin) / (xmax - xmin) * (ymax - ymin) + ymin
                    if y == 0:
                        print('y = 0')
                        y = 0.0000001
                    k = y2 / y
                    r, g, b = round(pix[i, j][0]*k), round(pix[i, j][1]*k), round(pix[i, j][2]*k)
                    draw.point((i, j), (r, g, b))
        image.save(newImage, 'JPEG')
        del draw
        self.pixmap = QPixmap(newImage)
        self.pixmap = self.pixmap.scaledToWidth(600)
        self.pixmap = self.pixmap.scaledToHeight(330)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(190, 20)

        self.show()

    def on_click1(self): # нормализация
        image = Image.open(myImage)  # Открываем изображение
        draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
        width = image.size[0]  # Определяем ширину
        height = image.size[1]  # Определяем высоту
        pix = image.load()  # Выгружаем значения пикселей
        ymin = 0
        ymax = 255
        gist = [0 for i in range(256)]
        print(type(pix[0, 0]))

        if type(pix[0,0]) == int: # проверка типа пискелей(монохромные или цветные)
            for i in range(width):
                for j in range(height):
                    gist[pix[i, j]] += 1

            xmin = -1
            xmax = -1
            tmp = 0
            for i in range(256):
                if gist[i] * 3 < gist[i + 1]:
                    tmp = i
                    break
            for i in range(256):
                if (not gist[i] < tmp and xmin < 0):
                    xmin = i
                if (not gist[256 - i - 1] < tmp and xmax < 0):
                    xmax = 256 - i - 1
                if (xmin > 0) and (xmax > 0):
                    break
            # if xmin < 0:
            #     xmin = 0
            # if xmax < 0:
            #     xmax = 255
            for i in range(width):
                for j in range(height):
                    y = pix[i, j]
                    y2 = (y - xmin) / (xmax - xmin) * (ymax - ymin) + ymin
                    draw.point((i, j), round(y2))
        else:
            for i in range(width):
                for j in range(height):
                    r, g, b = pix[i, j][0], pix[i, j][1], pix[i, j][2]
                    y = round(0.299 * r + 0.587 * g + 0.114 * b)
                    gist[y] += 1
            xmin = -1
            xmax = -1
            tmp = 0
            for i in range(256):
                if gist[i] * 3 < gist[i + 1]:
                    tmp = i
                    break

            for i in range(256):
                if (not gist[i] < tmp and xmin<0):
                    xmin = i
                if (not gist[256 - i - 1] < tmp and xmax<0):
                    xmax = 256 - i - 1
                if (xmin > 0) and (xmax > 0):
                    break
            # if xmin < 0:
            #     xmin = 0
            # if xmax < 0:
            #     xmax = 255

            for i in range(width):
                for j in range(height):
                    r, g, b = pix[i, j][0], pix[i, j][1], pix[i, j][2]
                    y = 0.299 * r + 0.587 * g + 0.114 * b
                    y2 = (y - xmin) / (xmax - xmin) * (ymax - ymin) + ymin
                    if y == 0:
                        print('###', y2, '/', y)
                        y = 0.0000001
                    k = y2 / y
                    r, g, b = round(r * k), round(g * k), round(b * k)
                    draw.point((i, j), (r, g, b))

        image.save(newImage, 'JPEG')
        del draw
        self.pixmap = QPixmap(newImage)
        self.pixmap = self.pixmap.scaledToWidth(600)
        self.pixmap = self.pixmap.scaledToHeight(330)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(190, 20)

        self.show()

    def on_click2(self): #эквализация гистограммы
        image = Image.open(myImage)
        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]
        pix = image.load()
        print(type(pix[0, 0]))
        gist = [0 for i in range(256)]
        if type(pix[0, 0]) is int: # проверка типа пискелей(монохромные или цветные)
            for i in range(width):
                for j in range(height):
                    gist[pix[i,j]] += 1
            for i in range(255):
                gist[i] = gist[i]/(width*height)
            for i in range(1, 255):
                gist[i] += gist[i-1]
            for i in range(width):
                for j in range(height):
                    draw.point((i,j), round(gist[pix[i,j]]*255))
        else:
            for i in range(width):
                for j in range(height):
                    r, g, b = pix[i,j][0], pix[i,j][1], pix[i,j][2]
                    y = 0.299 * r + 0.587 * g + 0.114 * b
                    gist[round(y)] += 1
            for i in range(255):
                gist[i] = gist[i]/(width*height)
            for i in range(1, 255):
                gist[i] += gist[i-1]
            for i in range(width):
                for j in range(height):
                    r, g, b = pix[i,j][0], pix[i,j][1], pix[i,j][2]
                    y = 0.299 * r + 0.587 * g + 0.114 * b
                    y2 = gist[round(y)]*255
                    if y == 0:
                        print('###', y2, '/', y)
                        y = 0.0000001
                    k = y2/y
                    r, g, b = round(r*k), round(g*k), round(b*k)
                    draw.point((i, j), (r, g, b))

        image.save(newImage, 'JPEG')
        del draw
        self.pixmap = QPixmap(newImage)
        self.pixmap = self.pixmap.scaledToWidth(600)
        self.pixmap = self.pixmap.scaledToHeight(330)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(190, 20)

        self.show()

    def on_click3(self):  #показать стандартное изображение
        self.pixmap = QPixmap(myImage)
        self.pixmap = self.pixmap.scaledToWidth(600)
        self.pixmap = self.pixmap.scaledToHeight(330)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(190, 20)
        self.show()

    def initUI(self): #интерфейс
        global myImage
        self.resize(820, 380)
        self.setWindowTitle('Consrast')

        self.qbtn = QPushButton('Линейное контрастирование', self)
        self.qbtn.clicked.connect(self.on_click)
        self.qbtn.move(20, 140)
        self.qbtn1 = QPushButton('Нормализация', self)
        self.qbtn1.clicked.connect(self.on_click1)
        self.qbtn1.move(20, 170)
        self.qbtn2 = QPushButton('Эквализация гистограммы', self)
        self.qbtn2.clicked.connect(self.on_click2)
        self.qbtn2.move(20, 200)
        self.qbtn3 = QPushButton('Стандартное изображение', self)
        self.qbtn3.clicked.connect(self.on_click3)
        self.qbtn3.move(20, 60)

        self.imageLabel = QLabel(self)
        self.pixmap = QPixmap(myImage)
        self.pixmap = self.pixmap.scaledToWidth(600)
        self.pixmap = self.pixmap.scaledToHeight(330)
        self.imageLabel.setPixmap(self.pixmap)
        self.imageLabel.move(190, 20)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Contr()
    sys.exit(app.exec_())