from manim import *
import numpy as np

class AetherLabScene(Scene):
    def construct(self):
        # BEAT A1.B1 | 0.00-4.00 s
        rail = Line(LEFT * 6.5, RIGHT * 6.5, color=GRAY, stroke_width=8).shift(DOWN * 1.8)
        rail2 = Line(LEFT * 6.5, RIGHT * 6.5, color=GRAY, stroke_width=2).shift(DOWN * 2.05)

        def make_cart(w, h, col):
            body = Rectangle(width=w, height=h, fill_color=col, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
            w1 = Circle(radius=0.12, fill_color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=2).move_to(body.get_bottom() + LEFT * w * 0.25 + DOWN * 0.1)
            w2 = Circle(radius=0.12, fill_color=BLACK, fill_opacity=1, stroke_color=WHITE, stroke_width=2).move_to(body.get_bottom() + RIGHT * w * 0.25 + DOWN * 0.1)
            return VGroup(body, w1, w2)

        cart1 = make_cart(1.8, 0.8, BLUE)
        cart1.move_to(DOWN * 1.15 + LEFT * 4.0)
        cart2 = make_cart(1.0, 0.6, ORANGE)
        cart2.move_to(DOWN * 1.25 + RIGHT * 1.5)

        lab1 = Text("m1=3 кг, v1=4 м/с", font_size=30, color=WHITE).next_to(cart1, UP, buff=0.15)
        lab2 = Text("m2=1 кг, стоит", font_size=30, color=WHITE).next_to(cart2, UP, buff=0.15)
        hook = Text("Тяжёлая тележка догоняет лёгкую", font_size=32, color=WHITE).to_edge(UP)
        hook.scale_to_fit_width(config.frame_width - 1.5)

        self.play(Create(rail), Create(rail2), FadeIn(cart1, shift=RIGHT * 1.0), FadeIn(cart2, shift=LEFT * 0.3), Write(hook), run_time=2.0)
        self.play(FadeIn(lab1), FadeIn(lab2), run_time=0.8)
        self.wait(1.2)

        # BEAT A2.B1 | 4.00-7.00 s
        p_tracker = ValueTracker(12.0)
        p_title = MathTex(r"p = m v", color=WHITE).scale(0.9)
        p_title.to_edge(UP, buff=0.2).shift(LEFT * 2.5)
        p_num = DecimalNumber(12.0, num_decimal_places=0, color=WHITE)
        p_num.scale(0.9)
        p_num.next_to(p_title, RIGHT, buff=0.25)
        p_unit = Text("кг·м/с", font_size=30, color=WHITE).next_to(p_num, RIGHT, buff=0.15)
        p_row = VGroup(p_title, p_num, p_unit)
        p_row.move_to(UP * 2.4)
        p_num.add_updater(lambda m: m.set_value(p_tracker.get_value()))
        hook2 = Text("Импульс до удара — двенадцать", font_size=30, color=BLUE).next_to(p_row, DOWN, buff=0.15)

        self.play(FadeOut(hook), FadeIn(p_title), FadeIn(p_num), FadeIn(p_unit), FadeIn(hook2), run_time=1.0)
        self.wait(2.0)

        # BEAT A2.B2 | 7.00-10.00 s
        plaque = Text("Удар упругий: что будет после?", font_size=30, color=WHITE)
        plaque_box = SurroundingRectangle(plaque, color=ORANGE, buff=0.2)
        plaque_grp = VGroup(plaque_box, plaque)
        plaque_grp.next_to(cart2, UP, buff=1.2)
        plaque_grp.move_to(RIGHT * 2.0 + UP * 0.6)
        self.play(FadeIn(plaque_grp, shift=UP * 0.2), run_time=1.0)
        self.wait(2.0)

        # BEAT A3.B1 | 10.00-14.00 s
        arr1 = Arrow(cart1.get_right(), cart1.get_right() + RIGHT * 1.2, color=BLUE, buff=0.05, stroke_width=6)
        arr1_lab = Text("4 м/с", font_size=30, color=WHITE).next_to(arr1, UP, buff=0.1)
        self.play(FadeOut(plaque_grp), FadeOut(hook2), FadeOut(lab1), FadeOut(lab2), FadeIn(arr1), FadeIn(arr1_lab), run_time=0.6)
        contact = cart2.get_left() + LEFT * 0.95
        self.play(cart1.animate.move_to(DOWN * 1.15 + LEFT * 0.55), cart2.animate.move_to(DOWN * 1.25 + RIGHT * 0.55), arr1.animate.shift(LEFT * 2.2), arr1_lab.animate.shift(LEFT * 2.2), run_time=2.0, rate_func=linear)
        flash_pt = (cart1.get_right() + cart2.get_left()) / 2
        flash = Flash(flash_pt, color=ORANGE, flash_radius=0.6)
        ring = Circumscribe(VGroup(cart1, cart2), color=ORANGE)
        self.play(flash, ring, run_time=0.6)
        self.wait(0.8)

        # BEAT A3.B2 | 14.00-18.00 s
        v1lab = Text("v1'=2 м/с", font_size=30, color=WHITE).next_to(cart1, UP, buff=0.15)
        v2lab = Text("v2'=6 м/с", font_size=30, color=WHITE).next_to(cart2, UP, buff=0.15)
        arr1b = Arrow(ORIGIN, RIGHT * 0.7, color=BLUE, buff=0).next_to(cart1, RIGHT, buff=0.05)
        arr2b = Arrow(ORIGIN, RIGHT * 1.6, color=ORANGE, buff=0).next_to(cart2, RIGHT, buff=0.05)
        self.play(FadeOut(arr1), FadeOut(arr1_lab), FadeIn(v1lab), FadeIn(v2lab), FadeIn(arr1b), FadeIn(arr2b), run_time=0.6)
        self.play(cart1.animate.shift(RIGHT * 1.2), v1lab.animate.shift(RIGHT * 1.2), arr1b.animate.shift(RIGHT * 1.2), cart2.animate.shift(RIGHT * 2.6), v2lab.animate.shift(RIGHT * 2.6), arr2b.animate.shift(RIGHT * 2.6), run_time=2.0, rate_func=linear)
        self.wait(1.4)

        # BEAT A4.B1 | 18.00-23.00 s
        eq1 = MathTex(r"m_1 v_1 = m_1 v_1' + m_2 v_2'", color=WHITE).scale(0.75)
        eq2 = Text("v1' = 2 м/с,  v2' = 6 м/с", color=WHITE, font_size=36).scale(0.75)
        eq3 = MathTex(r"3 \cdot 2 + 1 \cdot 6 = 12", color=WHITE).scale(0.8)
        calc_title = Text("Считаем по сохранению импульса", font_size=30, color=WHITE)
        calc = VGroup(calc_title, eq1, eq2, eq3).arrange(DOWN, buff=0.2)
        calc.scale_to_fit_width(config.frame_width - 2.0)
        calc.move_to(UP * 1.2)
        self.play(FadeOut(arr1b), FadeOut(arr2b), FadeIn(calc, shift=DOWN * 0.2), run_time=1.2)
        self.play(cart1.animate.shift(LEFT * 0.6 + DOWN * 0.2), cart2.animate.shift(LEFT * 1.0 + DOWN * 0.2), v1lab.animate.shift(LEFT * 0.6 + DOWN * 0.2), v2lab.animate.shift(LEFT * 1.0 + DOWN * 0.2), run_time=0.8)
        self.wait(3.0)

        # BEAT A4.B2 | 23.00-26.00 s
        self.play(FadeOut(eq1), run_time=0.4)
        after_row = VGroup(eq2, eq3)
        check = Text("Импульс после тоже двенадцать", font_size=30, color=WHITE).next_to(after_row, DOWN, buff=0.2)
        self.play(FadeIn(check, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)

        # BEAT A5.B1 | 26.00-30.00 s
        self.play(FadeOut(calc_title), FadeOut(eq2), FadeOut(eq3), FadeOut(check), FadeOut(v1lab), FadeOut(v2lab), FadeOut(p_title), FadeOut(p_num), FadeOut(p_unit), run_time=0.6)
        p_num.clear_updaters()
        hero_top = Text("p до = p после = 12 кг·м/с", font_size=36, color=WHITE)
        hero_top.to_edge(UP, buff=0.4)
        hero_top.scale_to_fit_width(config.frame_width - 1.5)
        hero_note = Text("Импульс сохранился", font_size=38, color=YELLOW)
        hero_note.next_to(hero_top, DOWN, buff=0.2)
        cart1.move_to(DOWN * 1.15 + LEFT * 1.6)
        cart2.move_to(DOWN * 1.25 + RIGHT * 0.8)
        hl1 = Text("v1'=2 м/с", font_size=30, color=WHITE).next_to(cart1, UP, buff=0.15)
        hl2 = Text("v2'=6 м/с", font_size=30, color=WHITE).next_to(cart2, UP, buff=0.15)
        hero_carts = VGroup(rail, rail2, cart1, cart2, hl1, hl2)
        self.play(FadeIn(hero_top), FadeIn(hero_note), FadeIn(hl1), FadeIn(hl2), Flash(hero_note, color=YELLOW), run_time=1.2)
        t_idle = ValueTracker(0.0)
        def note_upd(m):
            m.set_opacity(0.6 + 0.4 * abs(np.sin(t_idle.get_value() * 3.0)))
        hero_note.add_updater(note_upd)
        p2_tracker = ValueTracker(12.0)
        p2_num = DecimalNumber(12.0, num_decimal_places=0, color=WHITE).scale(0.7)
        p2_lab = Text("p = mv", font_size=30, color=WHITE)
        p2_grp = VGroup(p2_lab, p2_num).arrange(RIGHT, buff=0.2)
        p2_grp.next_to(hero_note, DOWN, buff=0.2)
        p2_num.add_updater(lambda m: m.set_value(p2_tracker.get_value()))
        self.add(p2_grp)
        self.play(t_idle.animate.set_value(4.0), cart1.animate.shift(RIGHT * 0.8), cart2.animate.shift(RIGHT * 0.8), hl1.animate.shift(RIGHT * 0.8), hl2.animate.shift(RIGHT * 0.8), p2_grp.animate.shift(RIGHT * 0.0), run_time=2.2, rate_func=linear)