import cv2  # type: ignore
from Droplet_Detector.do_xslx import do_df  # type: ignore

sum_area_s = 0


def get_sum():
    return sum_area_s


def update_sum(new_value):
    global sum_area_s
    sum_area_s = new_value


def calculate_area(contours):
    # global sum_area_s
    all_area = 0

    for contour in contours:
        all_area += cv2.contourArea(contour)
    do_df(contours)
    update_sum(all_area)
    return all_area
