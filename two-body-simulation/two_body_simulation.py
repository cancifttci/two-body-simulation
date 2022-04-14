import math
import time


class TwoBodyModal:
    def __init__(self):
        self._store = []

    def get_states(self):
        return self._store

    def add_state(self, state):
        self._store.append([(state[0][0], state[0][1]), (state[1][0], state[1][1])])

    def get_last_state(self):
        return self._store[-1]

    def export_to_txt(self, file_name):
        f = open(file_name, "w")
        export_start = time.time()
        print("+Export Started...")
        for state in self._store:
            f.write(str(state[0][0])+","+str(state[0][1])+","+str(state[1][0])+","+str(state[1][1])+"\n")
        export_end = time.time()
        print("+Export Finished. ({} seconds)".format(round(export_end-export_start)))
        print("+"+str(len(self._store))+" state exported -> "+file_name)


class TwoBodyController:
    def __init__(self, mass_ratio=0.5, eccentricity=0.5, total_time=1000, step_size=0.01, method="runge-kutta"):
        self._mass_ratio = mass_ratio
        self._eccentricity = eccentricity
        self._t = total_time
        self._step_size = step_size
        self._method = method
        self._u = [0, 0, 0, 0]
        self._m1 = 1
        self._m2 = mass_ratio
        self._m12 = self._m1 + self._m2

        self._x1 = 0,
        self._y1 = 0

        self._x2 = 0,
        self._y2 = 0

    def get_method(self):
        return self._method

    def get_eccentricity(self):
        return self._eccentricity

    def get_mass_ratio(self):
        return self._mass_ratio

    def get_total_time(self):
        return self._t

    def get_step_size(self):
        return self._step_size

    def calculate_initial_state(self):
        return [(1, 0), (-1 * self._mass_ratio, 0)]

    def calculate_initial_velocity(self):
        return math.sqrt((1 + self._mass_ratio) * (1 + self._eccentricity))

    def derivative(self):
        du = [0.0, 0.0, 0.0, 0.0]

        r = self._u[0:2]
        rr = math.sqrt(math.pow(r[0], 2) + math.pow(r[1], 2))

        for i in range(2):
            du[i] = self._u[i + 2]
            du[i + 2] = -1 * (1 + self._mass_ratio) * r[i] / (math.pow(rr, 3))

        return du

    def runge_kutta(self):
        a = [self._step_size / 2, self._step_size / 2, self._step_size, 0]
        b = [self._step_size / 6, self._step_size / 3, self._step_size / 3, self._step_size / 6]
        u0 = []
        ut = []
        dimension = len(self._u)

        for i in range(dimension):
            u0.append(self._u[i])
            ut.append(0)

        for j in range(4):
            du = self.derivative()

            for i in range(dimension):
                self._u[i] = u0[i] + a[j] * du[i]
                ut[i] = ut[i] + b[j] * du[i]

        for i in range(dimension):
            self._u[i] = u0[i] + ut[i]

    def euler(self):
        u2 = self._u
        x = [0,0,0,0]
        y = self.derivative()
        for i in range(len(u2)):
            x[i] = u2[i] + self._step_size * y[i]

        for k in range(len(x)):
            self._u[k] = x[k]

    def update_position(self):
        if self._method == "euler":
            self.euler()
        else:
            self.runge_kutta()
        return self.calculate_new_position()

    def calculate_new_position(self):
        r = 150

        a1 = (self._m2 / self._m12) * r
        a2 = (self._m1 / self._m12) * r

        self._x1 = -1 * a2 * self._u[0]
        self._y1 = -1 * a2 * self._u[1]

        self._x2 = a1 * self._u[0]
        self._y2 = a1 * self._u[1]
        return [(self._x1, self._y1), (self._x2, self._y2)]

    def reset_state_to_initial_conditions(self):
        self._u[0] = 1
        self._u[1] = 0
        self._u[2] = 0
        self._u[3] = self.calculate_initial_velocity()


print("Two Body Movement Calculator")
method = input("Select calculation method(euler|runge-kutta):")
mass_ratio = float(input("Select Mass Ratio:"))
eccentricity = float(input("Select Eccentricity:"))
step_size = float(input("Select Step Size:"))
total_time = int(input("Select Total Time:"))

modal = TwoBodyModal()
controller = TwoBodyController(method=method, mass_ratio=mass_ratio,eccentricity=eccentricity,step_size=step_size,total_time=total_time)
controller.reset_state_to_initial_conditions()

total_time = 0
print("+Calculation Started... \n-Method: {}\n-Mass Ratio: {}\n-Eccentricity: {}\n-Total Time: {}\n-Step Size: {}".format(
    controller.get_method(),
    controller.get_mass_ratio(),
    controller.get_eccentricity(),
    controller.get_total_time(),
    controller.get_step_size()))

calculation_start = time.time()
while True:
    if total_time <= controller.get_total_time():
        new_state = controller.update_position()
        modal.add_state(new_state)
    else:
        break
    total_time += controller.get_step_size()
calculation_end = time.time()
print("+Calculation Finished. ({} seconds)".format(round(calculation_end-calculation_start)))
modal.export_to_txt("data.txt")

