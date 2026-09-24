from manim import *
import math

class AetherLabScene(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 6, 1], y_range=[0, 2, 0.5],
            x_length=8, y_length=4, tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        )
        curve = axes.plot(
            lambda x: 0.3 * x**3 / (math.exp(x) - 1),
            x_range=[0.08, 6], color=YELLOW, stroke_width=4,
        )
        heading = Text("BLACKBODY SPECTRUM", font_size=34, color=WHITE)
        formula = Text("I(x) = x^3 / (e^x - 1)", font_size=25, color=TEAL_A)
        heading.to_edge(UP)
        formula.to_edge(DOWN)
        axes.shift(DOWN * 0.45)
        curve.shift(DOWN * 0.45)
        self.play(Write(heading), run_time=1)
        self.play(Create(axes), Create(curve), FadeIn(formula), run_time=2)
        self.wait(1)
