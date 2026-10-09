from manim import *

class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = "#071923"
        header = Text("PHYSLAB  |  UNT PHYSICS  |  KZ / RU / EN", font_size=18, color="#91AAB8")
        header.to_edge(UP, buff=0.3)
        rule = Line(LEFT * 6.5, RIGHT * 6.5, color="#25445A", stroke_width=2).shift(UP * 2.75)
        title = Text("CHOOSE THE MODEL", font_size=34, color="#EDF4F7", weight="BOLD")
        title.next_to(rule, DOWN, buff=0.35)
        self.add(header, rule)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1)
        condition = Text("straight line  +  constant acceleration", font_size=27, color="#35D8C2").shift(UP * 1.4)
        eq1 = Text("v = v0 + a t", font_size=48, color="#EDF4F7").move_to(UP * 0.25)
        eq2 = Text("s = v0 t + ½ a t²", font_size=43, color="#FFC857").move_to(DOWN * 0.85)
        axis = Text("a is signed along your chosen axis", font_size=25, color="#FF7A90").move_to(DOWN * 1.9)
        plus = Text("a > 0: velocity rises", font_size=19, color="#91AAB8").move_to(LEFT * 4.0 + UP * 0.35)
        minus = Text("a < 0: velocity falls", font_size=19, color="#91AAB8").move_to(RIGHT * 4.0 + UP * 0.35)
        self.play(FadeIn(condition), Write(eq1), run_time=1)
        self.play(eq1.animate.scale(1.06), run_time=1)
        self.play(Write(eq2), run_time=1)
        self.play(FadeIn(axis), run_time=1)
        self.play(FadeIn(plus), FadeIn(minus), run_time=1)
        self.wait(37.0)
