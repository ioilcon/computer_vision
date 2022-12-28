import numpy as np
import cv2
from matplotlib import pyplot as plt


def create_matr(n, q):
    matr = []
    for i in range(n):
        row = []
        for j in range(n):
            k = 1.0 / (2 * np.pi * (q ** 2)) * np.exp((-(i-n//2) ** 2 - (j-n//2) ** 2) / (2 * q ** 2))
            row.append(k)
        matr.append(row)
    return matr


def normalisation_matr(matr):
    sum = 0
    for i in range(len(matr)):
        for j in range(len(matr)):
            sum += matr[i][j]
    for i in range(len(matr)):
        for j in range(len(matr)):
            matr[i][j] /= sum
    return matr


def get_img():
    img = cv2.imread(r'carx7.jpg', flags=cv2.IMREAD_GRAYSCALE)
    h = int(img.shape[0])
    w = int(img.shape[1])
    return img, w, h


def show_img(img, img2):
    cv2.imshow('Display blur', img)
    cv2.imshow('Display origin', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


gray_picture, width, heigth = get_img()
copyFrame = cv2.GaussianBlur(gray_picture,(33,33),3.3)
cv2.imshow('Display origin', copyFrame)

# ________________________________________________lab_3___________________________________________
# gx = [[-1,0,1],[-2,0,2],[-1,0,1]]  # оператор Собеля
# gy = [[-1,-2,-1],[0,0,0],[1,2,1]]

# gx = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]  # оператор Прюитта
# gy = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]

gx = [[-1,0],[0,1]]  # оператор Робертса
gy = [[0, -1], [1, 0]]

a, b = 1, 1
# границы обхода
h_start, w_start = a, a
h_finish = heigth - a
w_finish = width - a

grad = []
dirs = []  # направления
dirs_pictures = []
max_len_picture = 0
border_picture = []
for i in range(h_start, h_finish):
    grad_row = []
    dirs_row = []
    dir_picture_row = []
    border_row = []
    for j in range(w_start, w_finish):
        newVal_gx = 0
        newVal_gy = 0
        for p_i in range(len(gx)):
            for p_j in range(len(gy)):
                newVal_gx = newVal_gx + copyFrame[i - 1 + p_i][j - 1 + p_j] * gx[p_i][p_j]
                newVal_gy = newVal_gy + copyFrame[i - 1 + p_i][j - 1 + p_j] * gy[p_i][p_j]
        if newVal_gx == 0:
            newVal_gx = 0.00000000000001
        len_grad = np.sqrt(newVal_gx ** 2 + newVal_gy ** 2)
        grad_row.append(len_grad)  # градиент - длина
        if len_grad > max_len_picture:
            max_len_picture = len_grad

        cur_tg = np.tan((newVal_gy / newVal_gx) / np.pi * 180)
        if cur_tg < -2.414 and newVal_gx * newVal_gy < 0 or cur_tg > 2.414 and newVal_gx * newVal_gy > 0:
            dirs_row.append(0) # 4 - 0
            dir_picture_row.append('|')
        elif cur_tg < -0.414 and newVal_gx * newVal_gy < 0:
            dirs_row.append(1) # 1 - 5
            dir_picture_row.append('/')
        elif cur_tg > -0.414 and newVal_gx * newVal_gy < 0 or cur_tg < 0.414 and newVal_gx * newVal_gy > 0:
            dirs_row.append(2) # 2 - 6
            dir_picture_row.append('-')
        elif cur_tg < 2.414 and newVal_gx * newVal_gy > 0:
            dirs_row.append(3)  # 3 - 7
            dir_picture_row.append('\\')
        else:
            dirs_row.append(2)
            dir_picture_row.append('-')
    grad.append(grad_row)
    dirs.append(dirs_row)
    dirs_pictures.append(dir_picture_row)

low_level = max_len_picture * (4/100)  # отрезает в процентах от яркости
high_level = max_len_picture * (16/100)  # что между ними проходит проверку(затираеть/красить)

for i in range(h_start + 1, h_finish - 2):
    for j in range(w_start + 1, w_finish - 2):
        if dirs[i][j] == 0:
            if grad[i + 1][j] < grad[i][j] and grad[i - 1][j] < grad[i][j]:
                copyFrame[i][j] = 0
            else:
                copyFrame[i][j] = 255
        elif dirs[i][j] == 1:
            if grad[i - 1][j + 1] < grad[i][j] and grad[i + 1][j - 1] < grad[i][j]:
                copyFrame[i][j] = 0
            else:
                copyFrame[i][j] = 255
        elif dirs[i][j] == 2:
            if grad[i][j - 1] < grad[i][j] and grad[i][j + 1] < grad[i][j]:
                copyFrame[i][j] = 0
            else:
                copyFrame[i][j] = 255
        elif dirs[i][j] == 3:
            if grad[i - 1][j - 1] < grad[i][j] and grad[i + 1][j + 1] < grad[i][j]:
                copyFrame[i][j] = 0
            else:
                copyFrame[i][j] = 255

for i in range(h_start + 1, h_finish - 2):
    for j in range(w_start + 1, w_finish - 2):
        if copyFrame[i][j] == 0:
            if grad[i][j] < low_level:
                copyFrame[i][j] = 255
            elif grad[i][j] < high_level:
                n = 0
                for p_i in range(2):
                    for p_j in range(2):
                        if copyFrame[p_i][p_j] == 0 and grad[p_i][p_j] > high_level:
                            n += 1
                if n == 0:
                    copyFrame[i][j] = 255

cv2.imshow('Display origin', copyFrame)
cv2.waitKey(10000000)
cv2.destroyAllWindows()
