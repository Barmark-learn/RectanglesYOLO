import math
import random
from PIL import Image, ImageDraw
import numpy as np


class Rectangle:
    def __init__(self):
        pass

    # Функция для вращения прямоугольника. Используем матрицу поворота.
    def rotate_rect(self, w, h, theta, center_rotate=(0, 0)):
        cos, sin = math.cos(theta), math.sin(theta)
        coord_rect = [(w / 2.0, h / 2.0), (w / 2.0, -h / 2.0), (-w / 2.0, -h / 2.0), (-w / 2.0, h / 2.0)]
        # Возвращаем список с координатами вершин повернутого прямоугольника
        return [(cos * x - sin * y + center_rotate[0], sin * x + cos * y + center_rotate[1]) for (x, y) in coord_rect]

    # Функция проверки длины и цвета внутреннего прямоугольника
    def check_len_color(self, r, g, b):
        flag_length = True
        while flag_length:
            # Генерируем случайным образом координаты верхней левой вершины и нижней правой
            x1 = random.randrange(0, 640)
            y1 = random.randrange(0, 480)
            x2 = random.randrange(0, 640)
            y2 = random.randrange(0, 480)
            # Генерируем случайным образом цвет внутреннего прямоугольника
            r_extra = random.randrange(0, 256)
            g_extra = random.randrange(0, 256)
            b_extra = random.randrange(0, 256)
            # Делаем проверку на длину стороны прямоугольника и на различие его цвета с цветом фона
            if (150 <= abs(y2 - y1) <= 250) and (150 <= abs(x2 - x1) <= 250) and (r_extra != r or g_extra != g
                                                                                  or b_extra != b):
                flag_length = False
        # Возвращаем координаты внутреннего прямоугольника и его цвет
        return x1, y1, x2, y2, r_extra, g_extra, b_extra

    # Функция для проверки на выход внутреннего повернутого прямоугольника за границы изображения
    def check_border(self, x_1, x_2, y_1, y_2, angle, x_centr, y_centr):
        flag_abroad = True
        while flag_abroad:
            # Получаем список с координатами вершин повернутого прямоугольника
            xy = self.rotate_rect(abs(x_2 - x_1), abs(y_2 - y_1), angle * math.pi / 180,
                                  center_rotate=(x_centr, y_centr))
            # Проверяем координаты на выход за пределы основного изображения
            for el in xy:
                if el[0] > 640 or el[0] < 0 or el[1] > 480 or el[1] < 0:
                    # Если нашли координату выходящую за рамки, генерируем новые координаты центра и выходим из цикла
                    x_centr = random.randrange(0, 640)
                    y_centr = random.randrange(0, 480)
                    flag = False
                    break
                else:
                    flag = True
            if flag:
                flag_abroad = False
        return xy

    def creator(self):
        # Задаем случайный цвет основного прямоугольного фона
        r_main = random.randrange(0, 256)
        g_main = random.randrange(0, 256)
        b_main = random.randrange(0, 256)
        # Случайным образом выбираем координаты центра поворота внутреннего прямоугольника
        x_centr = random.randrange(0, 640)
        y_centr = random.randrange(0, 480)
        # Создаем основной прямоугольный фон
        rectangle_main = Image.new('RGB', (640, 480), color=(r_main, g_main, b_main))
        # Получаем координаты верхней левой и нижней правой вершины внутреннего прямоугольника и его цвет
        x_1, y_1, x_2, y_2, r_inner, g_inner, b_inner = self.check_len_color(r_main, g_main, b_main)
        # Задаем случайный угол поворота от 0 до 89
        angle = random.randrange(0, 90)
        # Получем список с координатами повернутого внутреннего прямоугольника
        xy = self.check_border(x_1, x_2, y_1, y_2, angle, x_centr, y_centr)
        # Список c координатами х и у внутреннего прямоугольника
        x_coord = [el[0] for el in xy]
        y_coord = [el[1] for el in xy]
        # Получаем координаты описывающего прямоугольника
        x_max, x_min = max(x_coord), min(x_coord)
        y_max, y_min = max(y_coord), min(y_coord)
        # Отрисовываем на основном фоне полученный прямоугольник
        pencil = ImageDraw.Draw(rectangle_main)
        pencil.polygon(xy, fill=(r_inner, g_inner, b_inner))
        # Отрисовка описывающего прямоугольника
        pencil.rectangle((x_min, y_min, x_max, y_max), outline='red')
        return rectangle_main, x_min, y_min, x_max, y_max, abs(x_max - x_min), abs(y_max - y_min), xy


rec = Rectangle()
im, x_box, y_box, _, _, w_box, h_box, rect_coord = rec.creator()
print('Описывающий прямоугольник:', f'x = {int(x_box)}', f'y = {int(y_box)}', f'w = {int(w_box)}', f'h = {int(h_box)}',
      sep='\n')
print('Координаты углов:', f'x1 = {int(rect_coord[0][0])}', f'y1 = {int(rect_coord[0][1])}',
      f'x2 = {int(rect_coord[1][0])}', f'y2 = {int(rect_coord[1][1])}', f'x3 = {int(rect_coord[2][0])}',
      f'y3 = {int(rect_coord[2][1])}', f'x4 = {int(rect_coord[3][0])}', f'y4 = {int(rect_coord[3][1])}', sep='\n')

'''# Часть кода для получения нампи массива для Yolo
new_lst = []
rec = Rectangle()
im, _, _, _, _, _, _, coord = rec.creator()
im.show()
print(coord)
for i in range(2500):
    im, _, _, _, _, _, _, coord = rec.creator()
    name = f'rectangle/Data{i}.jpg'
    coord_vert = name + ' ' + str(int(coord[0])) + ',' + str(int(coord[1])) + ',' + str(int(coord[2])) + ',' + \
                 str(int(coord[3])) + ',' + '0'
    new_lst.append(coord)
    im.save(f'D:/pythonProject1/Rectangles_for_vert/rectangle/Data{i}.jpg')
arr_rectangle = np.array(new_lst)
print(arr_rectangle.shape)
np.save('D:/pythonProject1/Rectangles_for_vert/rectangle.npy', arr_rectangle)'''
