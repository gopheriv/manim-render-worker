from manim import *

class PhysLabCloudAcceptance20261013(Scene):
    def construct(self):
        self.camera.background_color = "#101828"
        title = Text("PhysLab cloud acceptance", font="DejaVu Sans", font_size=36).to_edge(UP)
        labels = VGroup(
            Text("ЕНТ физика", font="DejaVu Sans", font_size=28),
            Text("ҰБТ: ә ғ қ ң ө ұ ү һ і", font="DejaVu Sans", font_size=28),
            Text("UNT physics", font="DejaVu Sans", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        formula = MathTex(r"v=v_0+at", font_size=48).shift(RIGHT * 3 + UP)
        ball = Dot(LEFT * 2 + DOWN * 2, radius=0.2, color=BLUE_C)
        self.add(title, labels, formula, ball)
        self.play(ball.animate.shift(RIGHT * 4), run_time=3, rate_func=linear)
        self.wait(1)
