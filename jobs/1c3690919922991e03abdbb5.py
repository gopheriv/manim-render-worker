from manim import *

class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = "#071923"
        header = Text("PHYSLAB  |  UNT PHYSICS  |  KZ / RU / EN", font_size=18, color="#91AAB8")
        header.to_edge(UP, buff=0.3)
        rule = Line(LEFT * 6.5, RIGHT * 6.5, color="#25445A", stroke_width=2).shift(UP * 2.75)
        title = Text("NAME THE QUANTITIES", font_size=34, color="#EDF4F7", weight="BOLD")
        title.next_to(rule, DOWN, buff=0.35)
        self.add(header, rule)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1)
        v0 = Text("v0  initial velocity", font_size=29, color="#35D8C2").move_to(UP * 1.2 + LEFT * 2.5)
        v = Text("v  final velocity", font_size=29, color="#FFC857").move_to(UP * 0.4 + LEFT * 2.5)
        a = Text("a  үдеу (acceleration)", font_size=26, color="#FF7A90").move_to(DOWN * 0.4 + LEFT * 2.2)
        t = Text("t  time", font_size=29, color="#A78BFA").move_to(DOWN * 1.2 + LEFT * 2.5)
        s = Text("s  displacement (орын ауыстыру)", font_size=25, color="#EDF4F7").move_to(DOWN * 2.15 + LEFT * 0.5)
        axis = Arrow(RIGHT * 2.55 + UP * 1.35, RIGHT * 5.4 + UP * 1.35, color="#35D8C2", buff=0, stroke_width=4)
        marker = Dot(RIGHT * 2.55 + UP * 1.35, radius=0.09, color="#FFC857")
        axis_label = Text("chosen positive direction", font_size=18, color="#91AAB8").move_to(RIGHT * 3.95 + UP * 0.98)
        units = Text("v: m/s   a: m/s²\nt: s   s: m", font_size=23, color="#FFC857").move_to(RIGHT * 3.8 + DOWN * 0.35)
        distance = Text("distance = full path", font_size=21, color="#EDF4F7").move_to(RIGHT * 3.7 + DOWN * 1.55)
        self.play(Write(v0), Write(axis_label), run_time=1)
        self.play(Write(v), Create(axis), marker.animate.move_to(axis.get_end()), run_time=1)
        self.play(Write(a), FadeIn(units), run_time=1)
        self.play(Write(t), FadeIn(distance), run_time=1)
        self.play(Write(s), run_time=1)
        self.wait(37.0)
