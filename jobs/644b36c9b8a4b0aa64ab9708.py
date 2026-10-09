from manim import *

class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = "#071923"
        header = Text("PHYSLAB  |  UNT PHYSICS  |  KZ / RU / EN", font_size=18, color="#91AAB8")
        header.to_edge(UP, buff=0.3)
        rule = Line(LEFT * 6.5, RIGHT * 6.5, color="#25445A", stroke_width=2).shift(UP * 2.75)
        title = Text("WORKED EXAMPLE  |  KEEP ONE DATA SET", font_size=34, color="#EDF4F7", weight="BOLD")
        title.next_to(rule, DOWN, buff=0.35)
        self.add(header, rule)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1)
        given = Text("v0 = 2 m/s     a = 1.5 m/s²     t = 4 s", font_size=28, color="#91AAB8").shift(UP * 1.6)
        vcalc = Text("v = 2 + 1.5 × 4", font_size=41, color="#EDF4F7").move_to(UP * 0.6)
        vans = Text("v = 8 m/s", font_size=45, color="#35D8C2").move_to(DOWN * 0.15)
        scalc = Text("s = 2 × 4 + ½ × 1.5 × 4²", font_size=34, color="#EDF4F7").move_to(DOWN * 1.05)
        sans = Text("s = 8 + 12 = 20 m", font_size=41, color="#FFC857").move_to(DOWN * 1.95)
        check = Text("check: average v = 5 m/s; 5 × 4 = 20 m", font_size=23, color="#A78BFA").move_to(DOWN * 2.65)
        self.play(FadeIn(given), run_time=1)
        self.play(Write(vcalc), run_time=1)
        self.play(TransformFromCopy(vcalc, vans), run_time=1)
        self.play(Write(scalc), run_time=1)
        self.play(Write(sans), run_time=1)
        self.play(FadeIn(check), run_time=1)
        self.wait(36.0)
