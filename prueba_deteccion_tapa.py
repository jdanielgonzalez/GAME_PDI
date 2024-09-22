import cv2
import numpy as np

# Variables globales
color_space = 'HSV'  # Espacio de color por defecto

def nothing(x):
    pass

def create_trackbars_hsv():
    cv2.createTrackbar('H1', 'Mask', 0, 179, nothing)
    cv2.createTrackbar('S1', 'Mask', 100, 255, nothing)
    cv2.createTrackbar('V1', 'Mask', 100, 255, nothing)
    cv2.createTrackbar('H2', 'Mask', 179, 179, nothing)
    cv2.createTrackbar('S2', 'Mask', 255, 255, nothing)
    cv2.createTrackbar('V2', 'Mask', 255, 255, nothing)

def create_trackbars_lab():
    cv2.createTrackbar('L1', 'Mask', 0, 100, nothing)
    cv2.createTrackbar('A1', 'Mask', 150, 255, nothing)
    cv2.createTrackbar('A2', 'Mask', 255, 255, nothing)
    cv2.createTrackbar('B1', 'Mask', 0, 255, nothing)
    cv2.createTrackbar('B2', 'Mask', 255, 255, nothing)

def create_trackbars_ycrcb():
    cv2.createTrackbar('Y1', 'Mask', 0, 255, nothing)
    cv2.createTrackbar('Cr1', 'Mask', 140, 255, nothing)
    cv2.createTrackbar('Cr2', 'Mask', 255, 255, nothing)
    cv2.createTrackbar('Cb1', 'Mask', 0, 255, nothing)
    cv2.createTrackbar('Cb2', 'Mask', 255, 255, nothing)

def remove_trackbars():
    cv2.destroyWindow('Mask')  # Cierra la ventana de la máscara
    cv2.namedWindow('Mask')     # Vuelve a crear la ventana de la máscara

def detect_red(frame):
    global color_space

    if color_space == 'HSV':
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([cv2.getTrackbarPos('H1', 'Mask'), 
                                cv2.getTrackbarPos('S1', 'Mask'), 
                                cv2.getTrackbarPos('V1', 'Mask')])
        upper_red1 = np.array([cv2.getTrackbarPos('H2', 'Mask'), 
                                cv2.getTrackbarPos('S2', 'Mask'), 
                                cv2.getTrackbarPos('V2', 'Mask')])
        mask = cv2.inRange(hsv, lower_red1, upper_red1)

        print("HSV Lower:", lower_red1)
        print("HSV Upper:", upper_red1)

    elif color_space == 'LAB':
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
        lower_lab = np.array([cv2.getTrackbarPos('L1', 'Mask'), 
                              cv2.getTrackbarPos('A1', 'Mask'), 
                              0])  # B se mantiene fijo
        upper_lab = np.array([100, 
                              cv2.getTrackbarPos('A2', 'Mask'), 
                              255])  # B se mantiene fijo
        mask = cv2.inRange(lab, lower_lab, upper_lab)

        print("LAB Lower:", lower_lab)
        print("LAB Upper:", upper_lab)

    elif color_space == 'YCrCb':
        ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        lower_ycrcb = np.array([cv2.getTrackbarPos('Y1', 'Mask'), 
                                 cv2.getTrackbarPos('Cr1', 'Mask'), 
                                 0])  # Cb se mantiene fijo
        upper_ycrcb = np.array([255, 
                                 cv2.getTrackbarPos('Cr2', 'Mask'), 
                                 255])  # Cb se mantiene fijo
        mask = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

        print("YCrCb Lower:", lower_ycrcb)
        print("YCrCb Upper:", upper_ycrcb)

    return mask

def draw_circle(frame, contours):
    for c in contours:
        if cv2.contourArea(c) > 500:  # Filtra contornos pequeños
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            cv2.circle(frame, center, int(radius), (0, 255, 0), 2)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede abrir la cámara.")
        return
    
    global color_space
    cv2.namedWindow('Color Detection')
    cv2.namedWindow('Mask')

    create_trackbars_hsv()  # Crea trackbars para HSV

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Reflejar el frame
        frame = cv2.flip(frame, 1)

        mask = detect_red(frame)  # Detectar el color en el espacio actual
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        draw_circle(frame, contours)

        # Mostrar el frame y la máscara
        cv2.imshow('Color Detection', frame)
        cv2.imshow('Mask', mask)  # Mostrar la máscara

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('h'):  # Cambia a HSV
            color_space = 'HSV'
            remove_trackbars()
            create_trackbars_hsv()  # Crear trackbars para HSV
            print("Espacio de color cambiado a:", color_space)
        elif key == ord('l'):  # Cambia a LAB
            color_space = 'LAB'
            remove_trackbars()
            create_trackbars_lab()  # Crear trackbars para LAB
            print("Espacio de color cambiado a:", color_space)
        elif key == ord('y'):  # Cambia a YCrCb
            color_space = 'YCrCb'
            remove_trackbars()
            create_trackbars_ycrcb()  # Crear trackbars para YCrCb
            print("Espacio de color cambiado a:", color_space)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
