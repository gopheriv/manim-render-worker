from manim import *
import numpy as np

class AetherLabScene(Scene):
    def construct(self):
            # BEAT A1.B1 | 0.00-4.00 s
            title = Text("Горка энергии", font_size=34).to_edge(UP, buff=0.35)
            title.set_z_index(10)
            slope = Polygon(
                np.array([-5.5, 1.5, 0]), np.array([-0.5, -1.5, 0]),
                np.array([-0.5, -1.9, 0]), np.array([-5.5, 1.1, 0]),
                color=GRAY, fill_opacity=0.55, stroke_color=GRAY, stroke_width=3, stroke_opacity=0.35
            )
            flat = Rectangle(width=5.0, height=0.4, color=GRAY, fill_opacity=0.55, stroke_width=3, stroke_opacity=0.35).move_to(np.array([2.0, -1.7, 0]))
            slope.set_z_index(0)
            flat.set_z_index(0)
            top_pt = np.array([-4.9, 1.55, 0])
            bot_pt = np.array([-0.5, -1.15, 0])
            end_pt = np.array([3.6, -1.15, 0])
            block = Square(side_length=0.55, color=BLUE, fill_opacity=1, stroke_width=2).move_to(top_pt + np.array([0.15, 0.35, 0]))
            block.set_z_index(5)
            h_label = Text("Высота h = 5 м", font_size=30).next_to(block, UP, buff=0.2)
            h_label.set_z_index(10)
            m_label = Text("m = 2 кг", font_size=30).next_to(block, LEFT, buff=0.25)
            m_label.set_z_index(10)
            self.play(LaggedStart(Write(title), AnimationGroup(Create(slope), Create(flat), FadeIn(block, scale=0.6), FadeIn(h_label), FadeIn(m_label)), lag_ratio=0.4), run_time=2.2)
            self.wait(1.5)
            # BEAT A2.B1 | 4.00-7.00 s
            eq_pot = MathTex(r"E_{\text{pot}} = mgh").scale(0.85)
            eq_pot.to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
            eq_pot.set_z_index(10)
            calc_label = Text("2 × 9,8 × 5 = 98 Дж", font_size=30, color=TEAL).next_to(eq_pot, DOWN, buff=0.2)
            calc_label.set_z_index(10)
            self.play(Write(eq_pot), FadeIn(calc_label), run_time=1.0)
            self.wait(1.7)
            # BEAT A2.B2 | 7.00-10.00 s
            q_box = RoundedRectangle(width=5.2, height=0.9, corner_radius=0.15, color=TEAL, stroke_width=3).to_edge(DOWN, buff=0.5)
            q_box.set_z_index(10)
            q_text = Text("Куда исчезнет энергия внизу?", font_size=30).move_to(q_box.get_center())
            q_text.set_z_index(11)
            self.play(FadeOut(calc_label), Create(q_box), Write(q_text), run_time=1.0)
            self.wait(1.7)
            # BEAT A3.B1 | 10.00-14.00 s
            self.play(FadeOut(q_box), FadeOut(q_text), FadeOut(eq_pot), run_time=0.4)
            prog = ValueTracker(0.0)
            v_label = Text("v =", font_size=32).move_to(np.array([2.6, 1.8, 0]))
            v_label.set_z_index(10)
            v_num = DecimalNumber(0.0, num_decimal_places=1, color=WHITE, font_size=36)
            v_num.next_to(v_label, RIGHT, buff=0.15)
            v_num.set_z_index(10)
            v_unit = Text("м/с", font_size=30).next_to(v_num, RIGHT, buff=0.55)
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
            self.play(FadeIn(v_label), FadeIn(v_num), FadeIn(v_unit), run_time=0.5)
            self.play(prog.animate.set_value(1.0), run_time=2.8, rate_func=rate_functions.ease_in_quad)
            self.wait(0.4)
            # BEAT A3.B2 | 14.00-18.00 s
            block.clear_updaters()
            v_num.clear_updaters()
            bar_title = Text("Энергия", font_size=30).move_to(np.array([2.6, 0.7, 0]))
            bar_title.set_z_index(10)
            pe_back = Rectangle(width=0.7, height=2.0, color=GRAY, fill_opacity=0.15, stroke_width=2).move_to(np.array([1.9, -0.6, 0]))
            ke_back = Rectangle(width=0.7, height=2.0, color=GRAY, fill_opacity=0.15, stroke_width=2).move_to(np.array([3.1, -0.6, 0]))
            pe_small = Rectangle(width=0.7, height=0.06, color=BLUE, fill_opacity=1, stroke_width=1).align_to(pe_back, DOWN)
            ke_full = Rectangle(width=0.7, height=2.0, color=TEAL, fill_opacity=1, stroke_width=1).align_to(ke_back, DOWN)
            pe_full = Rectangle(width=0.7, height=2.0, color=BLUE, fill_opacity=1, stroke_width=1).align_to(pe_back, DOWN)
            ke_small = Rectangle(width=0.7, height=0.06, color=TEAL, fill_opacity=1, stroke_width=1).align_to(ke_back, DOWN)
            pe_bar = pe_small.copy()
            ke_bar = ke_full.copy()
            pe_cap = Text("пот", font_size=30).next_to(pe_back, DOWN, buff=0.15)
            ke_cap = Text("кин", font_size=30).next_to(ke_back, DOWN, buff=0.15)
            pe_cap.set_z_index(10)
            ke_cap.set_z_index(10)
            self.play(FadeIn(bar_title), FadeIn(pe_back), FadeIn(ke_back), FadeIn(pe_cap), FadeIn(ke_cap), FadeIn(pe_bar), FadeIn(ke_bar), run_time=0.6)
            self.play(AnimationGroup(Transform(pe_bar, pe_full), Transform(ke_bar, ke_small)), run_time=1.2)
            self.play(AnimationGroup(Transform(pe_bar, pe_small), Transform(ke_bar, ke_full)), run_time=1.6, rate_func=linear)
            self.wait(0.4)
            # BEAT A4.B1 | 18.00-26.00 s
            self.play(FadeOut(pe_bar), FadeOut(ke_bar), FadeOut(pe_back), FadeOut(ke_back), FadeOut(pe_cap), FadeOut(ke_cap), FadeOut(bar_title), FadeOut(v_label), FadeOut(v_num), FadeOut(v_unit), FadeOut(h_label), FadeOut(m_label), run_time=0.5)
            eq1 = MathTex(r"mgh = \frac{1}{2}mv^2").scale(0.9).move_to(ORIGIN + UP * 1.2)
            eq1.set_z_index(10)
            self.play(Write(eq1), run_time=1.0)
            self.wait(0.6)
            self.play(TransformMatchingTex(eq1, MathTex(r"v = \sqrt{2gh}").scale(0.9).move_to(ORIGIN + UP * 1.2)), run_time=1.0)
            self.wait(0.6)
            self.play(TransformMatchingTex(eq1, MathTex(r"v = \sqrt{2 \cdot 9{,}8 \cdot 5} = 9{,}9").scale(0.8).move_to(ORIGIN + UP * 1.2)), run_time=1.2)
            self.play(Flash(eq1), Circumscribe(eq1, color=TEAL), run_time=0.8)
            self.wait(1.6)
            # BEAT A5.B1 | 26.00-30.00 s
            self.play(FadeOut(eq1), FadeOut(title), FadeOut(slope), FadeOut(flat), FadeOut(block), run_time=0.4)
            hero_block = Square(side_length=0.7, color=BLUE, fill_opacity=1, stroke_width=2).move_to(np.array([1.5, -1.6, 0]))
            hero_block.set_z_index(5)
            hero_ground = Rectangle(width=11.0, height=0.4, color=GRAY, fill_opacity=0.5, stroke_width=2, stroke_opacity=0.35).move_to(np.array([0, -2.15, 0]))
            hero_ground.set_z_index(0)
            hero_v = Text("v = 9,9 м/с", font_size=44, color=YELLOW).move_to(np.array([1.5, -0.3, 0]))
            hero_v.set_z_index(10)
            hero_e = Text("Энергия сохранилась: 98 Дж", font_size=32, color=YELLOW).move_to(np.array([0, 1.6, 0]))
            hero_e.set_z_index(10)
            hero_ke_back = Rectangle(width=1.0, height=2.0, color=GRAY, fill_opacity=0.15, stroke_width=2).move_to(np.array([-3.5, 0.0, 0]))
            hero_ke_back.set_z_index(1)
            hero_bar = Rectangle(width=1.0, height=1.9, color=YELLOW, fill_opacity=1, stroke_width=1).align_to(hero_ke_back, DOWN)
            hero_bar.set_z_index(2)
            self.play(LaggedStart(AnimationGroup(FadeIn(hero_ground), FadeIn(hero_ke_back), FadeIn(hero_block), FadeIn(hero_e), FadeIn(hero_bar), FadeIn(hero_v)), hero_bar.animate.scale(1.06, about_edge=DOWN).set_rate_func(there_and_back), lag_ratio=0.25), run_time=3.6)