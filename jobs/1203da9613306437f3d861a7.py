from manim import *
class Owned1440Probec5171888(Scene):
    def construct(self):
        dot = Dot(color=BLUE).shift(LEFT * 2)
        self.add(dot)
        self.play(dot.animate.shift(RIGHT * 4), run_time=1.5, rate_func=linear)
        self.wait(0.5)
