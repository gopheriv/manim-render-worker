from manim import *

class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = "#071923"
        header = Text("PHYSLAB  |  UNT PHYSICS  |  KZ / RU / EN", font_size=18, color="#91AAB8")
        header.to_edge(UP, buff=0.3)
        rule = Line(LEFT * 6.5, RIGHT * 6.5, color="#25445A", stroke_width=2).shift(UP * 2.75)
        title = Text("ACCELERATION: A CHANGE IN SPEED", font_size=34, color="#EDF4F7", weight="BOLD")
        title.next_to(rule, DOWN, buff=0.35)
        self.add(header, rule)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1)
        road = Line(LEFT * 5.5 + DOWN * 0.65, RIGHT * 5.5 + DOWN * 0.65, color="#91AAB8", stroke_width=4)
        bus = RoundedRectangle(width=1.3, height=0.58, corner_radius=0.12, fill_color="#35D8C2", fill_opacity=1, stroke_color="#35D8C2").move_to(LEFT * 4 + DOWN * 0.22)
        wheel1 = Circle(radius=0.13, color="#EDF4F7", fill_opacity=1).move_to(bus.get_center() + LEFT * 0.35 + DOWN * 0.3)
        wheel2 = Circle(radius=0.13, color="#EDF4F7", fill_opacity=1).move_to(bus.get_center() + RIGHT * 0.35 + DOWN * 0.3)
        speed = Text("v: 0  →  2  →  4  →  6 m/s", font_size=30, color="#FFC857").shift(UP * 0.45)
        ticks = VGroup(*[Text(f"{i} s", font_size=20, color="#91AAB8").move_to(LEFT * 4.4 + RIGHT * (i * 1.8) + DOWN * 1.15) for i in range(4)])
        accel = Text("same increase each second  →  constant a", font_size=25, color="#EDF4F7").shift(DOWN * 1.9)
        self.play(Write(speed), run_time=1)
        self.play(Create(road), FadeIn(bus), FadeIn(wheel1), FadeIn(wheel2), run_time=1)
        self.play(FadeIn(ticks), run_time=1)
        self.play(bus.animate.shift(RIGHT * 2), wheel1.animate.shift(RIGHT * 2), wheel2.animate.shift(RIGHT * 2), run_time=1)
        self.play(bus.animate.shift(RIGHT * 2), wheel1.animate.shift(RIGHT * 2), wheel2.animate.shift(RIGHT * 2), run_time=1)
        self.play(FadeIn(accel, shift=UP * 0.1), run_time=1)
        self.wait(36.0)
