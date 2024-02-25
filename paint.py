from manim import *
from solve import solve
from solve import Body
class TESTS(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        axes.add_coordinates()
        self.play(Create(axes), run_time=5)
        self.move_camera(phi=45*DEGREES, theta=-45*DEGREES, run_time=3)
        self.begin_ambient_camera_rotation(rate=15*DEGREES, about="theta")
        self.wait(5)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=60*DEGREES, theta=-45*DEGREES, run_time=3)
        self.wait(2)
        self.move_camera(zoom=0.8)
        self.wait(5)
class NBODY(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        axes.add_coordinates()
        # mass, position(x, y, z), velocity(x, y, z)
        sol = solve([
            Body(1.1, *[-0.5, 1, 0], *[0.02, 0.02, 0.02]),
            Body(5.907, *[5.5, 4, 0.5], *[-1, 0, -0.1]),
            Body(1.425, *[0.2, 1, 1.5], *[0, -0.03, 0]),
            Body(2.425, *[0, 0, 0], *[0, 0, 0])
        ])
        return