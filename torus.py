import numpy as np

torus_dist = 20
torus_radius1 = 2
torus_radius2 = 1

screen_size = 35
screen_dist = screen_size * torus_dist * 3 / (8 * (torus_radius1 + torus_radius2))

theta_points = 90
phi_points = 90


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
B = 0

i = 0.1
print(chr(27) + "[2J")
while True:
    print("\x1b[H")

    light_coord = np.array([0, 1, -1]) / np.sqrt(2)

    screen = [[" " for _ in range(screen_size)] for __ in range(screen_size)]
    zbuffer = [[0 for _ in range(screen_size)] for __ in range(screen_size)]

    for theta in np.linspace(0, 2 * np.pi, theta_points):
        for phi in np.linspace(0, 2 * np.pi, phi_points):
            normal = (
                np.array([np.cos(theta), np.sin(theta), 0]) @ Ry(phi) @ Rx(A) @ Rz(B)
            )
            coords = np.array(
                [
                    torus_radius1 + torus_radius2 * np.cos(theta),
                    torus_radius2 * np.sin(theta),
                    0,
                ]
            ) @ Ry(phi) @ Rx(A) @ Rz(B) + np.array([0, 0, torus_dist])

            z_inv = 1 / coords[2]

            x_screen = int(screen_size / 2 + screen_dist * coords[0] * z_inv)
            y_screen = int(screen_size / 2 - screen_dist * coords[1] * z_inv)

            luminance = np.dot(normal, light_coord)
            if luminance > 0:
                if z_inv > zbuffer[y_screen][x_screen]:
                    zbuffer[y_screen][x_screen] = z_inv
                    screen[y_screen][x_screen] = ".,-~:;=!*#$@"[int(luminance * 11)]

    for row in screen:
        for el in row:
            print(el, end="")
            print(el, end="")
        print()

    i += 0.07
    A += 0.1
    B += 0.1
