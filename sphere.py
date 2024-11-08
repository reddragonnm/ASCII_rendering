import numpy as np

sphere_dist = 50
sphere_radius = 25

screen_size = 25
screen_dist = 15

theta_points = 100
phi_points = 100


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

    return np.array([[cs, -sn, 0], [sn, cs, 0], [0, 0, -1]])


i = 0.1
print(chr(27) + "[2J")
while True:
    print("\x1b[H")

    light_coord = np.array([np.sin(i), np.cos(i), -1], dtype=np.float64)
    light_coord_new = light_coord / np.linalg.norm(light_coord)

    screen = [[" " for _ in range(screen_size)] for __ in range(screen_size)]
    zbuffer = [[0 for _ in range(screen_size)] for __ in range(screen_size)]

    for theta in np.linspace(0, 2 * np.pi, theta_points):
        for phi in np.linspace(0, 2 * np.pi, phi_points):
            normal = np.matmul(
                np.array([np.cos(theta), np.sin(theta), 0]),
                Rx(phi),
            )
            coords = sphere_radius * normal + np.array([0, 0, sphere_dist])

            z_inv = 1 / coords[2]

            x_screen = int(screen_size / 2 + screen_dist * coords[0] * z_inv)
            y_screen = int(screen_size / 2 - screen_dist * coords[1] * z_inv)

            luminance = np.dot(normal, light_coord_new)
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
