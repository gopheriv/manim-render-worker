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
        v0 = Text("v0  initial velocity", font_size=31, color="#35D8C2").move_to(UP * 1.45 + LEFT * 1.3)
        v = Text("v  final velocity", font_size=31, color="#FFC857").move_to(UP * 0.6 + LEFT * 1.3)
        a = Text("a  acceleration / үдеу", font_size=31, color="#FF7A90").move_to(DOWN * 0.25 + LEFT * 1.3)
        t = Text("t  time", font_size=31, color="#A78BFA").move_to(DOWN * 1.1 + LEFT * 1.3)
        s = Text("s  displacement / орын ауыстыру", font_size=27, color="#EDF4F7").move_to(DOWN * 2.0 + LEFT * 0.1)
        axis = Arrow(LEFT * 4.6 + UP * 2.05, RIGHT * 4.6 + UP * 2.05, color="#35D8C2", buff=0, stroke_width=4)
        marker = Dot(LEFT * 4.6 + UP * 2.05, radius=0.09, color="#FFC857")
        axis_label = Text("chosen positive direction", font_size=20, color="#91AAB8").next_to(axis, UP, buff=0.12)
        units = Text("v: m/s     a: m/s²     t: s     s: m", font_size=26, color="#FFC857").move_to(RIGHT * 2.1 + DOWN * 0.2)
        distance = Text("distance = whole path", font_size=23, color="#EDF4F7").move_to(RIGHT * 2.1 + DOWN * 1.15)
        self.play(Write(v0), Write(axis_label), run_time=1)
        self.play(Write(v), Create(axis), marker.animate.move_to(axis.get_end()), run_time=1)
        self.play(Write(a), FadeIn(units), run_time=1)
        self.play(Write(t), FadeIn(distance), run_time=1)
        self.play(Write(s), run_time=1)
        self.wait(37.0)
