import numpy as np

cube_dist = 40
cube_size = 30

cube_points = 20

screen_size = 40
screen_dist = 10


def Rx(theta):
    cs = np.cos(theta)
    sn = np.sin(theta)

    return np.array([[1, 0, 0], [0, cs, -sn], [0, sn, cs]])


def Ry(theta):
    cs = np.cos(theta)
    sn = np.sin(theta)

    return np.array([[cs, 0, sn], [0, 1, 0], [-sn, 0, cs]])


def Rz(theta):
    cs = np.cos(theta)
    sn = np.sin(theta)

    return np.array([[cs, -sn, 0], [sn, cs, 0], [0, 0, 1]])


A = 0
B = 0.5

print(chr(27) + "[2J")
while True:
    print("\x1b[H")

    light_coord_new = np.array([0, 0, -1]) / np.sqrt(1)

    screen = [[" " for _ in range(screen_size)] for __ in range(screen_size)]
    zbuffer = [[0 for _ in range(screen_size)] for __ in range(screen_size)]

    for x in np.linspace(0, cube_size, cube_points):
        for y in np.linspace(0, cube_size, cube_points):
            for z in np.linspace(0, cube_size, cube_points):
                if x == 0:
                    normal = np.array([-1, 0, 0])
                elif x == cube_size:
                    normal = np.array([1, 0, 0])

                elif y == 0:
                    normal = np.array([0, -1, 0])
                elif y == cube_size:
                    normal = np.array([0, 1, 0])

                elif z == 0:
                    normal = np.array([0, 0, -1])
                elif z == cube_size:
                    normal = np.array([0, 0, 1])

                else:
                    continue

                normal_new = normal @ Ry(A) @ Rz(B)
                coords = (
                    np.array([x, y, z])
                    - np.array([cube_size / 2, cube_size / 2, cube_size / 2])
                ) @ Ry(A) @ Rz(B) + np.array([0, 0, cube_dist])
                z_inv = 1 / coords[2]

                x_screen = int(screen_size / 2 + screen_dist * coords[0] * z_inv)
                y_screen = int(screen_size / 2 - screen_dist * coords[1] * z_inv)

                luminance = np.dot(normal_new, light_coord_new)
                if luminance > 0:
                    if z_inv > zbuffer[y_screen][x_screen]:
                        zbuffer[y_screen][x_screen] = z_inv
                        screen[y_screen][x_screen] = ".,-~:;=!*#$@"[int(luminance * 11)]

    for row in screen:
        for el in row:
            print(el, end="")
            print(el, end="")
        print()

    A += 0.1
    B += 0.1
