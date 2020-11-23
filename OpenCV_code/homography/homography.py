"""Homographie et transformation de perspective avec OpenCV"""

import cv2
import numpy as np
import os; os.chdir(r"C:\Users\Armand\Dropbox\ISEP\a1\AIR\Sandbox\OpenCV\homography")

# Coordonnées relevées sur l'image à transformer. Elles correspondent aux points rouges sur "grille_marqueurs.jpg"
pts_src = np.array([
    [103, 17], [191, 15], [279, 15], [368, 16], [457, 15], [545, 16], [633, 16],  # line 1
    [80, 75], [177, 77], [273, 78], [369, 79], [464, 79], [560, 77], [655, 78],  # line 2
    [56, 150], [160, 147], [265, 148], [369, 152], [472, 152], [577, 151], [681, 151],  # line 3
    [35, 205], [149, 207], [259, 204], [369, 205], [478, 208], [591, 207], [701, 207],  # line 4
    [13, 271], [134, 271], [253, 271], [370, 269], [486, 270], [606, 271], [685, 271],  # line 5
    [17, 385], [106, 385], [239, 384], [370, 382], [500, 383], [632, 385],  # line 6
])
pts_src_minimal = np.array([
    [103, 17], [191, 15], [500, 383], [632, 385],  # line 6
], dtype=np.float32)  # Version à 4 points

# Calcul des coordonnées correspondantes désirées
width, height = 720, 480
pts_dst = np.array([
    [width*0/6, height*0/13], [width*1/6, height*0/13], [width*2/6, height*0/13], [width*3/6, height*0/13], [width*4/6, height*0/13], [width*5/6, height*0/13], [width*6/6, height*0/13],  # line 1
    [width*0/6, height*3/13], [width*1/6, height*3/13], [width*2/6, height*3/13], [width*3/6, height*3/13], [width*4/6, height*3/13], [width*5/6, height*3/13], [width*6/6, height*3/13],  # line 2
    [width*0/6, height*6/13], [width*1/6, height*6/13], [width*2/6, height*6/13], [width*3/6, height*6/13], [width*4/6, height*6/13], [width*5/6, height*6/13], [width*6/6, height*6/13],  # line 3
    [width*0/6, height*8/13], [width*1/6, height*8/13], [width*2/6, height*8/13], [width*3/6, height*8/13], [width*4/6, height*8/13], [width*5/6, height*8/13], [width*6/6, height*8/13],  # line 4
    [width*0/6, height*10/13], [width*1/6, height*10/13], [width*2/6, height*10/13], [width*3/6, height*10/13], [width*4/6, height*10/13], [width*5/6, height*10/13], [width*17/18, height*10/13],  # line 5
    [width*1/18, height*13/13], [width*1/6, height*13/13], [width*2/6, height*13/13], [width*3/6, height*13/13], [width*4/6, height*13/13], [width*5/6, height*13/13],  # line 6
])
pts_dst_minimal = np.array([
    [width*0/6, height*0/13], [width*1/6, height*0/13], [width*4/6, height*13/13], [width*5/6, height*13/13],  # line 6
], dtype=np.float32)  # Version à 4 points


##################
# Calcul des matrices de transformations
homography_matrix = cv2.findHomography(pts_src, pts_dst)[0]  # matrice d'homographie à partir de deux ensembles de points mis en correspondance
print(homography_matrix)
print("\n")

perspective_matrix = cv2.getPerspectiveTransform(pts_src_minimal, pts_dst_minimal)
print(perspective_matrix)
print("\n")

# Transformation d'image ou de point en fonction d'une matrice de transformation
image = cv2.imread("grille.jpg")
im_out = cv2.warpPerspective(image, homography_matrix, (image.shape[1], image.shape[0]))  # image transformée
cv2.imwrite("grille_warped.jpg", im_out)

input_points = np.array([[(63, 242), (291, 110), (361, 252), (78, 386)]], dtype=np.float32)
warped_point = cv2.perspectiveTransform(input_points, perspective_matrix)[0]  # ensemble de points transformés
print(warped_point)
