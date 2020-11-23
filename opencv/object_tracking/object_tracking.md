# Tracking d'objet avec OpenCV

> Ce document se réfère à ce [programme d'exemple](../OpenCV_code/object_tracking/object_tracking.py).

Le tracking d'un objet consiste à suivre son évolution spatiale dans un flux vidéo au cours du temps.

On définit sur la première image du flux vidéo un cadre (rectangle) contenant l'objet d'intérêt et uniquement cet objet. Le tracking opère alors et tente de suivre cet objet à chaque nouvelle image, en faisant évoluer ce cadre.

> Ce cadre initial peut être défini soit à la main en renseignant des coordonnées, soit par l'intermédiaire de la fonction [selectROI](https://docs.opencv.org/3.4/d7/dfc/group__highgui.html#ga8daf4730d3adf7035b6de9be4c469af5) qui permet de définir le cadre via une GUI.

OpenCV propose plusieurs modes de tracking, qui correspondent à des algorithmes différents:

    'BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT'

Il semble par expérience que les modes ```KCF``` et ```CSRT``` fonctionnent le mieux. S'il se produit une erreur ```'Tracking failure'```, augmenter la surface du cadre initial (notamment avec KCF ?).

> Voir [Object Tracking](https://www.learnopencv.com/object-tracking-using-opencv-cpp-python) pour en savoir plus.
