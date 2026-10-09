from manim import *
class AetherLabScene(Scene):
    def construct(self):
        dot = Dot(color=BLUE)
        self.play(FadeIn(dot), run_time=0.25)
        self.wait(0.25)
