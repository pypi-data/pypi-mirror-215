import cv2  # type: ignore
import numpy as np
from Droplet_Detector.calculate import calculate_area  # type: ignore


def get_contours(img):
    copy = img

    img = cv2.medianBlur(img, 3)

    resize_times = 1.5
    img = cv2.resize(img, None, img, fx=1 / resize_times, fy=1 / resize_times)

    # увеличиваем резкость изображения
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, kernel)

    # применяем маску собеля для выделения контуров
    sobel_f = cv2.Sobel(img, cv2.CV_64F, 2, 0, -1)
    abs_sobel_f = np.absolute(sobel_f)
    sobel = np.uint8(abs_sobel_f)
    print(type(sobel))

    # применяем размытие Гаусса для уменьшения шума
    img_blurred = (cv2.GaussianBlur(img, (2 * 2 + 1, 2 * 2 + 1), 0))

    # ещё ищем края
    canny = cv2.Canny(img_blurred, 100, 255,
                      L2gradient=True)
    # 50 - появляются шумы, но лучше отображаются контуры,
    # 100 - чуть меньше шума, чуть лучше контур

    # маску в чёрно-белый
    _, res = cv2.threshold(canny, 200, 255, cv2.THRESH_BINARY)

    # загружаем изображение и маску
    img = copy

    mask = cv2.convertScaleAbs(res)

    # проверка на размер изображениЙ
    if img.shape[:2] != mask.shape[:2]:
        mask = cv2.resize(mask, img.shape[:2][::-1])

    mask += img

    contours, hierarchy = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    calculate_area(contours)

    cv2.fillPoly(mask, contours, (255, 255, 0))

    return contours
