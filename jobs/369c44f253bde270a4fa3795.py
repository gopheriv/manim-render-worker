from manim import *

# Synthetic QA011 only: identical source, isolated tournament candidates.
class CloudQA011(Scene):
    def construct(self):
        title = Text("Synthetic motion check", font="DejaVu Sans", font_size=30).to_edge(UP)
        circle = Circle(radius=1.3, color=BLUE)
        point = Dot(LEFT * 1.3, color=YELLOW)
        self.add(title, circle, point)
        self.play(point.animate.move_to(RIGHT * 1.3), run_time=1.5, rate_func=linear)
        self.wait(0.5)
