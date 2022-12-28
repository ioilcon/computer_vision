import cv2
import copy


def motion_detect():
    cap = cv2.VideoCapture(r'video.mov', cv2.CAP_ANY)                           # Считываем видео из файла
    ret, frame = cap.read()                                                     # Прочитать первый кадр
    gray_capture = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                      # Перевести в черный белый цвет
    window_size = 5                                                         # Применяем размытие Гаусса # Параметры фильтра Гаусса
    sigma = 5
    new_frame = cv2.GaussianBlur(gray_capture, (window_size, window_size), sigma)   # Свертка изображения с помощью фильтра Гаусса
    h = len(gray_capture)
    w = len(gray_capture[0])

    fourcc = cv2.VideoWriter_fourcc(*'XVID')                                # Подготовка файла для записи
    video_writer = cv2.VideoWriter("res.mov", fourcc, 25, (w, h))
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)                         # Подготовка окна
    while True:                                                           # Цикл до завершения изображения
        # cv2.imshow('frame', frame)
        old_frame = copy.deepcopy(new_frame)                                # Скопировать старый кадр
        ret, frame = cap.read()                                             # Считываем новый кадр
        if not ret:                                                         # Eсли чтение неуспешно, остановить цикл
            break

        gray_capture = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)              # Перевести в черный белый цвет
        new_frame = cv2.GaussianBlur(gray_capture,
                                     (window_size, window_size), sigma)     # Свертка изображения с помощью фильтра Гаусса
        # cv2.imshow('new_frame', new_frame)

        frame_dif = cv2.absdiff(old_frame, new_frame)                       # Найти разницу между двумя кадрами в отдельный фрейм

        cv2.imshow('frame_dif', frame_dif)

        # cv2.waitKey(0)
        retval, frame_dif = cv2.threshold(frame_dif, 50, 255,               # Провести операцию двоичного разделения для фрейма
                                          cv2.THRESH_BINARY)
        # cv2.imshow('retval', frame_dif)
        # cv2.imshow('frame_dif', frame_dif)

        contours, hier = cv2.findContours(frame_dif,                        # Найти контуры объектов для фрейма
                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:                                # Пройтись по контурам объектов для фрейма, найти контур площадью большей, чем наперед заданный параметр
            if 200 < cv2.contourArea(i):
                # Если нашли
                # print("find")
                video_writer.write(frame)
                continue
        if cv2.waitKey(0) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


motion_detect()