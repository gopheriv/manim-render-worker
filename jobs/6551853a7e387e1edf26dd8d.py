from manim import *
class OwnedProfileProbe(Scene):
    def construct(self):
        dot = Dot(color=BLUE).shift(LEFT * 2)
        self.add(dot)
        self.play(dot.animate.shift(RIGHT * 4), run_time=1.5)
        self.wait(0.5)
