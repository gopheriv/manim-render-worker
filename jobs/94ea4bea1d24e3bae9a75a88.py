from manim import *

class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = "#071923"
        header = Text("PHYSLAB  |  UNT PHYSICS  |  KZ / RU / EN", font_size=18, color="#91AAB8")
        header.to_edge(UP, buff=0.3)
        rule = Line(LEFT * 6.5, RIGHT * 6.5, color="#25445A", stroke_width=2).shift(UP * 2.75)
        title = Text("READ A VELOCITY–TIME GRAPH", font_size=34, color="#EDF4F7", weight="BOLD")
        title.next_to(rule, DOWN, buff=0.35)
        self.add(header, rule)
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1)
        axes = Axes(x_range=[0, 4, 1], y_range=[0, 10, 2], x_length=6.4, y_length=4.0, tips=False, axis_config={"color": "#91AAB8", "include_numbers": True, "font_size": 20}).shift(LEFT * 2.0 + DOWN * 0.1)
        graph = Line(axes.c2p(0, 2), axes.c2p(4, 8), color="#35D8C2", stroke_width=5)
        marker = Dot(axes.c2p(0, 2), radius=0.09, color="#FF7A90")
        area_box = Polygon(axes.c2p(0, 0), axes.c2p(4, 0), axes.c2p(4, 2), axes.c2p(0, 2), fill_color="#FFC857", fill_opacity=0.6, stroke_width=0)
        area_tri = Polygon(axes.c2p(0, 2), axes.c2p(4, 2), axes.c2p(4, 8), fill_color="#35D8C2", fill_opacity=0.55, stroke_width=0)
        slope = Text("slope = (8 − 2) / 4 = 1.5 m/s²", font_size=24, color="#EDF4F7").move_to(RIGHT * 3.4 + UP * 1.4)
        areas = Text("area = 8 + 12 = 20 m", font_size=27, color="#FFC857").move_to(RIGHT * 3.4 + DOWN * 0.1)
        labels = Text("slope → a     area → displacement", font_size=21, color="#91AAB8").move_to(RIGHT * 3.25 + DOWN * 1.1)
        self.play(Create(axes), FadeIn(marker), run_time=1)
        self.play(FadeIn(area_box), Create(graph), marker.animate.move_to(graph.get_end()), run_time=1)
        self.play(FadeIn(area_tri), run_time=1)
        self.play(FadeIn(slope), run_time=1)
        self.play(FadeIn(areas), run_time=1)
        self.play(FadeIn(labels), run_time=1)
        self.wait(36.0)
