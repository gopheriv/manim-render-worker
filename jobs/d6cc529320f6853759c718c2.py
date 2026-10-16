from manim import *

class PhysLabF154MovingDotProbe(Scene):
    def construct(self):
        dot = Dot(color=YELLOW)
        self.play(dot.animate.shift(RIGHT * 3), run_time=1.5)
        self.wait(0.5)
