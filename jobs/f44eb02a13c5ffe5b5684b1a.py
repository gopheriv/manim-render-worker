from manim import *
import numpy as np

class AetherLabScene(Scene):
    def construct(self):
        # BEAT A1.B1 | 0.00-4.00 s : hill + block + safe labels
        title = Text("Горка энергии", font_size=34).to_edge(UP, buff=0.35)
        title.set_z_index(10)
        slope = Polygon(
            np.array([-5.2, 1.2, 0]), np.array([-0.8, -1.3, 0]),
            np.array([-0.8, -1.7, 0]), np.array([-5.2, 0.8, 0]),
            color=GRAY, fill_opacity=0.55, stroke_color=GRAY, stroke_width=3, stroke_opacity=0.35
        )
        flat = Rectangle(width=4.2, height=0.4, color=GRAY, fill_opacity=0.55, stroke_width=3, stroke_opacity=0.35).move_to(np.array([1.9, -1.5, 0]))
        slope.set_z_index(0)
        flat.set_z_index(0)
        top_pt = np.array([-4.6, 1.25, 0])
        bot_pt = np.array([-0.8, -0.95, 0])
        end_pt = np.array([3.2, -0.95, 0])
        block = Square(side_length=0.55, color=BLUE, fill_opacity=1, stroke_width=2).move_to(top_pt + np.array([0.15, 0.35, 0]))
        block.set_z_index(5)
        # safe, centered labels — never at frame edge
        h_label = Text("Высота h = 5 м", font_size=26).move_to(np.array([-2.6, 2.15, 0]))
        h_label.set_z_index(10)
        m_label = Text("m = 2 кг", font_size=26).move_to(np.array([-2.6, 1.55, 0]))
        m_label.set_z_index(10)
        self.play(LaggedStart(Write(title), AnimationGroup(Create(slope), Create(flat), FadeIn(block, scale=0.6), FadeIn(h_label), FadeIn(m_label)), lag_ratio=0.4), run_time=2.2)
        self.wait(1.5)
        # BEAT A2.B1 | 4.00-7.00 s : potential energy, kept inside right zone
        eq_pot = MathTex(r"E_{\text{pot}} = mgh").scale(0.8)
        eq_pot.move_to(np.array([3.2, 2.0, 0]))
        eq_pot.set_z_index(10)
        calc_label = Text("2 × 9,8 × 5 = 98 Дж", font_size=24, color=TEAL).move_to(np.array([3.2, 1.3, 0]))
        calc_label.set_z_index(10)
        self.play(Write(eq_pot), FadeIn(calc_label), run_time=1.0)
        self.wait(1.7)
        # BEAT A2.B2 | 7.00-10.00 s : question
        q_box = RoundedRectangle(width=5.0, height=0.85, corner_radius=0.15, color=TEAL, stroke_width=3).to_edge(DOWN, buff=0.5)
        q_box.set_z_index(10)
        q_text = Text("Куда исчезнет энергия внизу?", font_size=26).move_to(q_box.get_center())
        q_text.set_z_index(11)
        self.play(FadeOut(calc_label), Create(q_box), Write(q_text), run_time=1.0)
        self.wait(1.7)
        # BEAT A3.B1 | 10.00-14.00 s : slide with live speed
        prog = ValueTracker(0.0)
        v_label = Text("v =", font_size=30).move_to(np.array([2.4, 2.2, 0]))
        v_label.set_z_index(10)
        v_num = DecimalNumber(0.0, num_decimal_places=1, color=WHITE, font_size=34)
        v_num.next_to(v_label, RIGHT, buff=0.15)
        v_num.set_z_index(10)
        v_unit = Text("м/с", font_size=26).next_to(v_num, RIGHT, buff=0.35)
        v_unit.set_z_index(10)
        def block_pos():
            p = prog.get_value()
            if p < 0.6:
                q = p / 0.6
                base = top_pt * (1 - q) + bot_pt * q
                return base + np.array([0.15, 0.35, 0])
            else:
                q = (p - 0.6) / 0.4
                base = bot_pt * (1 - q) + end_pt * q
                return base + np.array([0.0, 0.35, 0])
        block.add_updater(lambda m: m.move_to(block_pos()))
        v_num.add_updater(lambda m: m.set_value(9.9 * prog.get_value()))
        self.play(FadeOut(q_box), FadeOut(q_text), FadeOut(eq_pot), FadeIn(v_label), FadeIn(v_num), FadeIn(v_unit), run_time=0.6)
        self.play(prog.animate.set_value(1.0), run_time=2.8, rate_func=rate_functions.ease_in_quad)
        self.wait(0.4)
        # BEAT A3.B2 | 14.00-18.00 s : energy bars on right, speed on top — no overlap
        block.clear_updaters()
        v_num.clear_updaters()
        bar_title = Text("Энергия", font_size=26).move_to(np.array([3.8, 1.4, 0]))
        bar_title.set_z_index(10)
        pe_back = Rectangle(width=0.65, height=1.7, color=GRAY, fill_opacity=0.15, stroke_width=2).move_to(np.array([3.3, -0.1, 0]))
        ke_back = Rectangle(width=0.65, height=1.7, color=GRAY, fill_opacity=0.15, stroke_width=2).move_to(np.array([4.4, -0.1, 0]))
        pe_small = Rectangle(width=0.65, height=0.06, color=BLUE, fill_opacity=1, stroke_width=1).align_to(pe_back, DOWN)
        ke_full = Rectangle(width=0.65, height=1.7, color=TEAL, fill_opacity=1, stroke_width=1).align_to(ke_back, DOWN)
        pe_full = Rectangle(width=0.65, height=1.7, color=BLUE, fill_opacity=1, stroke_width=1).align_to(pe_back, DOWN)
        ke_small = Rectangle(width=0.65, height=0.06, color=TEAL, fill_opacity=1, stroke_width=1).align_to(ke_back, DOWN)
        pe_bar = pe_small.copy()
        ke_bar = ke_full.copy()
        pe_cap = Text("пот", font_size=24).next_to(pe_back, DOWN, buff=0.12)
        ke_cap = Text("кин", font_size=24).next_to(ke_back, DOWN, buff=0.12)
        pe_cap.set_z_index(10)
        ke_cap.set_z_index(10)
        self.play(v_label.animate.move_to(np.array([0.0, 2.5, 0])), v_num.animate.move_to(np.array([0.9, 2.5, 0])), v_unit.animate.move_to(np.array([1.9, 2.5, 0])), FadeIn(bar_title), FadeIn(pe_back), FadeIn(ke_back), FadeIn(pe_cap), FadeIn(ke_cap), FadeIn(pe_bar), FadeIn(ke_bar), run_time=0.8)
        self.play(AnimationGroup(Transform(pe_bar, pe_full), Transform(ke_bar, ke_small)), run_time=1.2)
        self.play(AnimationGroup(Transform(pe_bar, pe_small), Transform(ke_bar, ke_full)), run_time=1.6, rate_func=linear)
        self.wait(0.4)
        # BEAT A4.B1 | 18.00-26.00 s : clean derivation center-left, bars fully removed
        self.play(FadeOut(pe_bar), FadeOut(ke_bar), FadeOut(pe_back), FadeOut(ke_back), FadeOut(pe_cap), FadeOut(ke_cap), FadeOut(bar_title), FadeOut(v_label), FadeOut(v_num), FadeOut(v_unit), FadeOut(h_label), FadeOut(m_label), run_time=0.5)
        eq1 = MathTex(r"mgh = \frac{1}{2}mv^2").scale(0.9).move_to(np.array([-2.0, 1.0, 0]))
        eq1.set_z_index(10)
        eq2 = MathTex(r"v = \sqrt{2gh}").scale(0.9).move_to(np.array([-2.0, 0.0, 0]))
        eq2.set_z_index(10)
        self.play(LaggedStart(Write(eq1), FadeIn(eq2), lag_ratio=0.6), run_time=2.0)
        self.wait(0.6)
        eq3 = MathTex(r"v = \sqrt{2 \cdot 9{,}8 \cdot 5} = 9{,}9").scale(0.75).move_to(np.array([-2.0, -1.0, 0]))
        eq3.set_z_index(10)
        box = SurroundingRectangle(eq3, color=TEAL, buff=0.15)
        box.set_z_index(10)
        self.play(Write(eq3), run_time=1.2)
        self.play(Create(box), Circumscribe(eq3, color=TEAL), run_time=0.8)
        self.wait(1.6)
        # BEAT A5.B1 | 26.00-30.00 s : hero conclusion — fresh objects, no reuse
        self.play(FadeOut(eq1), FadeOut(eq2), FadeOut(eq3), FadeOut(box), FadeOut(title), FadeOut(slope), FadeOut(flat), FadeOut(block), run_time=0.4)
        hero_ground = Rectangle(width=11.0, height=0.4, color=GRAY, fill_opacity=0.5, stroke_width=2, stroke_opacity=0.35).move_to(np.array([0, -2.15, 0]))
        hero_ground.set_z_index(0)
        hero_block = Square(side_length=0.7, color=BLUE, fill_opacity=1, stroke_width=2).move_to(np.array([1.5, -1.6, 0]))
        hero_block.set_z_index(5)
        hero_e = Text("Энергия сохранилась: 98 Дж", font_size=30, color=YELLOW).move_to(np.array([0, 1.8, 0]))
        hero_e.set_z_index(10)
        hero_v = Text("v = 9,9 м/с", font_size=42, color=YELLOW).move_to(np.array([1.5, -0.3, 0]))
        hero_v.set_z_index(10)
        hero_ke_back = Rectangle(width=1.0, height=1.8, color=GRAY, fill_opacity=0.15, stroke_width=2).move_to(np.array([-3.5, 0.1, 0]))
        hero_ke_back.set_z_index(1)
        hero_bar = Rectangle(width=1.0, height=1.7, color=YELLOW, fill_opacity=1, stroke_width=1).align_to(hero_ke_back, DOWN)
        hero_bar.set_z_index(2)
        hero_cap = Text("кинетическая", font_size=22).next_to(hero_ke_back, DOWN, buff=0.12)
        hero_cap.set_z_index(10)
        self.play(FadeIn(hero_ground), FadeIn(hero_ke_back), FadeIn(hero_cap), FadeIn(hero_block), FadeIn(hero_e), FadeIn(hero_bar), FadeIn(hero_v), run_time=1.2)
        self.play(hero_block.animate.shift(RIGHT * 2.0), hero_bar.animate.scale(1.08, about_edge=DOWN).set_rate_func(there_and_back), hero_v.animate.shift(RIGHT * 1.0), run_time=2.4, rate_func=linear)