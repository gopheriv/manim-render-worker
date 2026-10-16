from manim import *
class AetherLabScene(Scene):
    def construct(self):
        equation = MathTex(r"\mathcal{L} + \theta_1")
        self.play(Write(equation), run_time=1.0)
        self.wait(0.5)