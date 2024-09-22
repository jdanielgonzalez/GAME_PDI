# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 23:47:36 2024

@author: familia
"""

import cv2

# Capturar la cámara
cap = cv2.VideoCapture(0)

# Establecer el ancho y alto de la cámara a 1000x560
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)  # Ancho
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 560)  # Alto

# Verificar si se ha aplicado la resolución correctamente
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Resolución actual de la cámara: {width}x{height}")

# Mostrar el video en vivo para comprobar
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar la imagen de la cámara")
        break

    # Mostrar el frame en una ventana
    cv2.imshow('Cámara', frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
