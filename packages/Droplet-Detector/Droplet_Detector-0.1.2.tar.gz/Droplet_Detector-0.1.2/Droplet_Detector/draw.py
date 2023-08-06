import cv2  # type: ignore
import numpy as np
from Droplet_Detector.get_contours import get_contours  # type: ignore


def draw_contours_of_drops(img_path):
    # читаем пикчу и сохраняем копию

    img = cv2.imread(img_path)
    copy = img
    imgc = img.copy()
    print(type(imgc))

    img = cv2.medianBlur(img, 3)

    resize_times = 1.5
    img = cv2.resize(img, None, img, fx=1 / resize_times, fy=1 / resize_times)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # увеличиваем резкость изображения
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, kernel)

    # применяем маску собеля для выделения контуров
    sobel_f = cv2.Sobel(img, cv2.CV_64F, 2, 0, 7)
    abs_sobel_f = np.absolute(sobel_f)
    sobel = np.uint8(abs_sobel_f)
    print(type(sobel))

    # применяем размытие Гаусса для уменьшения шума
    img_blurred = (cv2.GaussianBlur(img, (2 * 2 + 1, 2 * 2 + 1), 0))

    # ещё ищем края
    canny = cv2.Canny(img_blurred, 40, 255,
                      L2gradient=True)
    # 50 - появляются шумы, но лучше отображаются контуры,
    # 100 - чуть меньше шума, чуть лучше контур

    # маску в чёрно-белый
    _, res = cv2.threshold(canny, 200, 255, cv2.THRESH_BINARY)

    # загружаем изображение и маску
    img = copy
    mask = cv2.convertScaleAbs(res)

    # проверка на размер изображений
    if img.shape[:2] != mask.shape[:2]:
        mask = cv2.resize(mask, img.shape[:2][::-1])

    # применяем маску к изображению
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    print(type(masked_img))

    # рисуем маску на изображении
    contours, hierarchy = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    cv2.fillPoly(mask, contours, (255, 255, 0))

    cn2 = get_contours(mask)

    cv2.drawContours(img, cn2, -1, (0, 255, 0), 1)

    filename = 'new_file/savedImage.jpg'
    cv2.imwrite(filename, img)
    return filename
