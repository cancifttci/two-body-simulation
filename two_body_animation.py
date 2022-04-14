import pygame
import time
import keyboard


class TwoBodyView:
    def __init__(self, file_name, speed):
        self._data = []
        self._state = 0
        self._status = True
        self._screen = pygame.display.set_mode([1000, 1000])
        self._speed = speed
        f = open(file_name, "r")
        lines = f.readlines()
        for line in lines:
            cols = line.split(",")
            self._data.append([(float(cols[0]), float(cols[1])), (float(cols[2]), float(cols[3]))])

    def set_status(self):
        if self._status is True:
            self._status = False
        else:
            self._status = True

    def start(self):
        print("Simulation Started")
        data = self._data

        pygame.init()
        pygame.display.set_caption('Two Body Movement Simulation')

        running = True
        number_of_orbit_points = 0
        start_state = data[0]
        for state in data[1:]:
            if round(state[0][0]) == round(start_state[0][0]):
                number_of_orbit_points += 5
                break
            number_of_orbit_points += 1

        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if keyboard.is_pressed("q"):
                running = False

            if keyboard.is_pressed("space"):
                time.sleep(0.2)
                orbit_points = []
                for i in range(self._status % number_of_orbit_points):
                    orbit_points.append(data[i])
                self.set_status()

            elif self._status is False and keyboard.is_pressed("r"):
                if self._state > 0:
                    self._state -= self._speed
                    self._screen.fill((0, 0, 0))

                    pygame.draw.circle(self._screen, (255, 0, 0), (500, 500), 2)
                    pygame.draw.line(self._screen, (255, 0, 0), (0, 500), (1000, 500), 1)
                    pygame.draw.line(self._screen, (255, 0, 0), (500, 0), (500, 1000), 1)

                    pygame.draw.circle(self._screen, (0, 0, 255),
                                       ((data[self._state][0][0] + 500), (data[self._state][0][1] + 500)), 10)
                    pygame.draw.circle(self._screen, (0, 255, 0),
                                       ((data[self._state][1][0] + 500), (data[self._state][1][1] + 500)), 10)

                    pygame.display.flip()
                    time.sleep(0.1)

            if self._status is not True:
                continue

            self._screen.fill((0, 0, 0))

            for i in range(self._state):
                pygame.draw.line(self._screen, (255, 255, 255),
                                 (data[i][0][0] + 500, data[i][0][1] + 500),
                                 (data[i + 1][0][0] + 500, data[i + 1][0][1] + 500), 1)
                pygame.draw.line(self._screen, (255, 255, 255),
                                 (data[i][1][0] + 500, data[i][1][1] + 500),
                                 (data[i + 1][1][0] + 500, data[i + 1][1][1] + 500), 1)

            pygame.draw.circle(self._screen, (255, 0, 0), (500, 500), 2)
            pygame.draw.line(self._screen, (255, 0, 0), (0, 500), (1000, 500), 1)
            pygame.draw.line(self._screen, (255, 0, 0), (500, 0), (500, 1000), 1)
            pygame.draw.circle(self._screen, (0, 0, 255),
                               ((data[self._state][0][0] + 500), (data[self._state][0][1] + 500)), 10)
            pygame.draw.circle(self._screen, (0, 255, 0),
                               ((data[self._state][1][0] + 500), (data[self._state][1][1] + 500)), 10)
            time.sleep(0.03)
            self._state += self._speed
            if self._state == len(data):
                self._state = 0

            pygame.display.flip()

        pygame.quit()


simulator = TwoBodyView(file_name="data.txt", speed=20)
simulator.start()
