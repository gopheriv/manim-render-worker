from manim import *
class AetherLabScene(Scene):
    def construct(self):
        dot = Dot()
        self.play(FadeIn(dot), run_time=0.5)
        self.wait(0.25)
