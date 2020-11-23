"""
Détection et repérage d'objets avec OpenCV
- partant d'une image, on applique un masque pour filtrer certaines couleurs
- puis on recherche les contours de chaque forme ainsi trouvée
- puis on calcule les centres de chaque contour
- enfin on peut calculer la distance et l'angle de chaque centre dans un repère choisi
"""

import cv2
import numpy as np
from math import sqrt, atan, degrees, copysign
import os; os.chdir(r"C:\Users\Armand\Dropbox\ISEP\a1\AIR\Sandbox\OpenCV\object_detection")

def remove_null_contours(contours):
    """Filtre les contours en supprimant les contours nuls (artefacts)"""
    topop = []
    for _ in range(len(contours)):
        M = cv2.moments(contours[_])
        if M["m00"] == 0:
            topop.append(_)
    contours = np.delete(contours, topop, 0)
    return contours

def remove_tiny_contours(contours, min_contour_radius):
    """Filtre les contours en supprimant les contours qui ont un rayon inférieur à un rayon minimal donné"""
    topop = []
    for _ in range(len(contours)):
        contour = contours[_]
        contour = contour.tolist()
        contour = [_[0] for _ in contour]
        normes_contour = [sqrt(point[0] ** 2 + point[1] ** 2) for point in contour]
        contour_radius = max(normes_contour) - min(normes_contour)
        # print("Contour radius: {}".format(contour_radius))
        if contour_radius < min_contour_radius:
            topop.append(_)
    contours = np.delete(contours, topop, 0)
    return contours

def get_center(contour):
    """Calcule les coordonnées du centre d'un contour"""
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
    return cX, cY

def get_dist_and_rot(x, y):
    """Calcule la distance en cm et l'angle en degrés d'un point par rapport au centre d'un repère, en fonction de ses coordonnées dans ce repère"""
    dist_in_pixels = sqrt(x ** 2 + y ** 2)
    dist = dist_in_pixels / CM2PX
    rot = copysign(90-abs(degrees(atan(y / x))), x)
    return dist, rot


# Paramètres
image_name = "palets.jpg"
gui = True  # afficher ou non les images à chaque étape du procédé
CM2PX = 20  # longueur en cm * CM2PX = longueur en pixels
min_contour_radius = 10  # rayon minimal d'un contour pour qu'il soit pris en compte
major_version, minor_version, _ = cv2.__version__.split(".")  # le calcul des contours dépend de la version d'OpenCV

image = cv2.imread(image_name)  # colorspace = BGR
image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # colorspace = HSV
# print('target_hsv: {}'.format(frame_HSV))

# Calcul du masque
target_colour_RGB = (209, 72, 30)
target_colour_HSV = cv2.cvtColor(np.uint8([[target_colour_RGB]]), cv2.COLOR_RGB2HSV)[0][0]
print(f"target_colour_HSV: {target_colour_HSV}")
mask = cv2.inRange(image_HSV, (0, 130, 100), (9, 255, 255))  # masque exprimé dans le colorspace HSV
# # Optionnel: lisser le masque
# mask = cv2.GaussianBlur(mask, (5, 5), 0)
# mask = cv2.erode(mask, None, iterations=25)
bitwise_mask = cv2.bitwise_and(image, image, mask=mask)  # application du masque à l'image d'origine
if gui:
    cv2.imshow("image with mask", bitwise_mask), cv2.waitKey(0)

# Calcul des contours
findContours_param1 = cv2.RETR_EXTERNAL
findContours_param2 = cv2.CHAIN_APPROX_SIMPLE
if major_version == '4':
    contours, _ = cv2.findContours(mask, findContours_param1, findContours_param2)
else:
    _, contours, __ = cv2.findContours(mask, findContours_param1, findContours_param2)
# Filtrage des contours
contours = remove_null_contours(contours)
contours = remove_tiny_contours(contours, min_contour_radius)
print("Number of contours: {}".format(len(contours)))
if gui:
    for _ in range(len(contours)):
        cv2.drawContours(image, contours, _, (0, 255, 0), 3)
        cv2.imshow('', image), cv2.waitKey(0)

for contour in contours:
    x, y = get_center(contour)  # Calcul du centre du contour
    if gui:
        cv2.circle(image, (round(x), round(y)), 7, (0, 255, 0), -1)
        cv2.imshow('', image), cv2.waitKey(0)
    x, y = (x - image.shape[1] / 2, - y + image.shape[0])  # changement de repère pour placer le centre du repère en bas et au centre de l'image
    print(f"x: {x}, y: {y}, (dist, angle): {get_dist_and_rot(x, y)}")
