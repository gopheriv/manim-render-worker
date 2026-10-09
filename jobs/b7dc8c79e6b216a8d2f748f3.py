from manim import *

class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = "#071923"
        header = Text("PHYSLAB  |  UNT PHYSICS  |  KZ / RU / EN", font_size=18, color="#91AAB8")
        header.to_edge(UP, buff=0.3)
        rule = Line(LEFT * 6.5, RIGHT * 6.5, color="#25445A", stroke_width=2).shift(UP * 2.75)
        title = Text("YOUR TURN  |  THEN CHECK", font_size=34, color="#EDF4F7", weight="BOLD")
        title.next_to(rule, DOWN, buff=0.35)
        self.add(header, rule)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1)
        question = Text("18 m/s  →  6 m/s   in   4 s", font_size=39, color="#EDF4F7").shift(UP * 1.25)
        prompt = Text("Find a and displacement s", font_size=28, color="#91AAB8").shift(UP * 0.35)
        a_calc = Text("a = (6 − 18) / 4 = −3 m/s²", font_size=35, color="#FF7A90").move_to(DOWN * 0.55)
        s_calc = Text("average v = 12 m/s  →  s = 48 m", font_size=32, color="#35D8C2").move_to(DOWN * 1.5)
        recap = Text("v = v0 + a t     |     s = v0 t + ½ a t²", font_size=30, color="#FFC857").move_to(DOWN * 2.5)
        check = Text("constant a  •  one axis  •  SI units", font_size=20, color="#91AAB8").move_to(DOWN * 3.1)
        velocity_drop = Line(RIGHT * 4.7 + UP * 1.35, RIGHT * 4.7 + DOWN * 0.15, color="#FF7A90", stroke_width=5)
        velocity_marker = Dot(RIGHT * 4.7 + UP * 1.35, radius=0.1, color="#FFC857")
        self.play(FadeIn(question), Write(prompt), Create(velocity_drop), FadeIn(velocity_marker), run_time=1)
        self.play(velocity_marker.animate.move_to(velocity_drop.get_end()), Write(a_calc), run_time=1)
        self.play(Write(s_calc), run_time=1)
        self.play(Write(recap), run_time=1)
        self.play(FadeIn(check), run_time=1)
        self.wait(36.0)
