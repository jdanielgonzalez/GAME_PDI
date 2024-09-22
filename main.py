import cv2
import numpy as np
from game import (
    load_background,
    load_turtles,
    initialize_camera,
    get_frame,
    create_mask,
    clean_mask,
    binarize_mask,
    GameObject,
    draw_circle_and_turtle,
    overlay_medusa,
    Enemy  # Importar la clase Enemy
)

def main():
    desired_size = (960, 540)
    background = load_background('sea (1).jpg', desired_size)
    turtle_left, turtle_right = load_turtles('turtle_left.png', 'turtle_right.png')
    enemy_image = cv2.imread('basura.png', cv2.IMREAD_UNCHANGED)  # Carga con canal alfa

    cap = initialize_camera(960, 560)
    kernel = np.ones((10, 10), np.uint8)  # Definir el kernel aquí

    objects = []
    for _ in range(6):  # Crear 6 medusas
        pos = [np.random.randint(0, desired_size[0] - 50), np.random.randint(0, desired_size[1] - 50)]
        speed = [np.random.choice([-2, 2]), np.random.choice([-2, 2])]
        objects.append(GameObject(cv2.imread('medusa.png', cv2.IMREAD_UNCHANGED), pos, speed))

    enemies = []
    for _ in range(6):  # Crear 8 enemigos estáticos
        pos = [np.random.randint(0, desired_size[0] - 50), np.random.randint(0, desired_size[1] - 50)]
        enemies.append(Enemy(enemy_image, pos))

    cv2.namedWindow('Tapa con Fondo y Tortuga')

    while True:
        frame = get_frame(cap)
        if frame is None:
            print("No se pudo capturar la imagen de la cámara")
            break

        frame_resized = cv2.resize(frame, desired_size)
        hsv = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)

        mask = create_mask(hsv)
        cleaned_mask = clean_mask(mask, kernel)
        binary_mask = binarize_mask(cleaned_mask)

        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        combined = background.copy()

        # Mover y dibujar las medusas
        for obj in objects:
            obj.move(desired_size)
            combined = overlay_medusa(combined, obj)

            # Verificar si la medusa ha sido capturada
            if contours:
                for c in contours:
                    (x, y), radius = cv2.minEnclosingCircle(c)
                    center = (int(x), int(y))
                    if obj.is_caught(center, radius):  # Comprobar captura
                        print("Medusa capturada!")
                        break  # Salir si se captura la medusa

        # Dibujar enemigos y comprobar colisiones
        for enemy in enemies:
            enemy.draw(combined)
            # Verificar colisión con la tortuga
            if contours:
                for c in contours:
                    (x, y), radius = cv2.minEnclosingCircle(c)
                    center = (int(x), int(y))
                    if enemy.pos[0] <= center[0] <= enemy.pos[0] + enemy.size[0] and \
                       enemy.pos[1] <= center[1] <= enemy.pos[1] + enemy.size[1]:
                        print("¡Has chocado con un enemigo! ¡Perdiste!")
                        cap.release()
                        cv2.destroyAllWindows()
                        return  # Terminar el juego

        # Dibuja la tortuga
        combined = draw_circle_and_turtle(combined, contours, turtle_left, turtle_right, desired_size)

        cv2.imshow('Tapa con Fondo y Tortuga', combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
