from manim import *
import numpy as np

class AetherLabScene(Scene):
    def construct(self):
        v0 = 20.0
        g = 9.8
        vx0 = 14.142135623730951
        vy0 = 14.142135623730951
        T = 2.8861506634510334
        H = 10.204081632653061
        R = 40.816326530612244
        t_apex = 1.4430753317255165
        axes = Axes(x_range=[0, 45, 10], y_range=[0, 13, 5], x_length=11, y_length=5.2, axis_config={"stroke_opacity": 0.35, "stroke_width": 2}).shift(DOWN * 0.6)
        axes.set_z_index(0)
        x_lab = Text("x, м", font_size=30).next_to(axes.x_axis, RIGHT, buff=0.15)
        y_lab = Text("y, м", font_size=30).next_to(axes.y_axis, UP, buff=0.15)
        axes_group = VGroup(axes, x_lab, y_lab)
        ground = Line(axes.c2p(0, 0), axes.c2p(45, 0), color=GREEN, stroke_width=6)
        ground.set_z_index(1)
        def traj_y(x):
            return x * (vy0 / vx0) - g * x * x / (2 * vx0 * vx0)
        traj_green = axes.plot(traj_y, x_range=[0, R, 0.2], color=GREEN, stroke_width=6)
        traj_green.set_z_index(2)
        traj_yellow = axes.plot(traj_y, x_range=[0, R, 0.2], color=YELLOW, stroke_width=7)
        traj_yellow.set_z_index(2)
        def pos_at(t):
            x = vx0 * t
            y = vy0 * t - 0.5 * g * t * t
            return axes.c2p(x, max(y, 0))
        t_tracker = ValueTracker(0)
        # BEAT A1.B1 | 0.00-4.00 s
        cannon_base = Rectangle(width=1.1, height=0.5, color=GREY_D, fill_opacity=1).move_to(LEFT * 5.5 + DOWN * 3.0)
        cannon_bar = Rectangle(width=1.4, height=0.4, color=GREY_B, fill_opacity=1).move_to(LEFT * 4.8 + DOWN * 2.7).rotate(45 * DEGREES)
        cannon = VGroup(cannon_base, cannon_bar)
        ball0 = Dot(point=LEFT * 4.0 + DOWN * 2.2, color=WHITE, radius=0.18)
        title0 = Text("Пушка: бросок мяча", font_size=34).to_edge(UP, buff=0.4)
        v0_lab = Text("v0 = 20 м/с, 45°", font_size=30).next_to(ball0, UP, buff=0.25)
        v0_lab.set_z_index(5)
        self.play(FadeIn(cannon), FadeIn(ball0), FadeIn(title0), run_time=0.7)
        self.play(Flash(ball0, color=GREEN), FadeIn(v0_lab), ball0.animate.shift(UP * 0.8 + RIGHT * 0.8), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(cannon), FadeOut(ball0), FadeOut(v0_lab), FadeOut(title0), run_time=0.3)
        # BEAT A2.B1 | 4.00-10.00 s
        eq_traj = MathTex(r"x=v_0\cos\theta\,t,\; y=v_0\sin\theta\,t-\frac{gt^2}{2}", font_size=34)
        eq_traj.to_edge(UP, buff=0.3)
        eq_traj.set_z_index(5)
        sub_lab = Text("Парабола без воздуха", font_size=30).next_to(eq_traj, DOWN, buff=0.15)
        grp = VGroup(axes_group, ground, traj_green, eq_traj, sub_lab)
        grp.scale_to_fit_width(13.0 - 1)
        grp.move_to(ORIGIN + DOWN * 0.2)
        self.play(FadeIn(axes_group), FadeIn(ground), Create(traj_green), FadeIn(eq_traj), FadeIn(sub_lab), run_time=1.5)
        self.wait(4.2)
        self.play(FadeOut(sub_lab), run_time=0.3)
        # BEAT A3.B1 | 10.00-13.77 s
        t_tracker.set_value(0)
        t_title = Text("t, с:", font_size=30).to_edge(UP, buff=0.3).shift(LEFT * 3.5)
        t_num = DecimalNumber(0.0, num_decimal_places=2, color=WHITE, font_size=36)
        t_num.next_to(t_title, RIGHT, buff=0.2)
        t_num.add_updater(lambda m: m.set_value(t_tracker.get_value()))
        t_num.set_z_index(5)
        def flyer():
            t = t_tracker.get_value()
            p = pos_at(t)
            vy = vy0 - g * t
            ball = Dot(point=p, color=WHITE, radius=0.16)
            ball.set_z_index(4)
            vx_e = p + RIGHT * 0.9
            vy_len = np.clip(vy / vy0 * 1.1, -1.1, 1.1)
            a1 = Arrow(p, vx_e, color=BLUE, buff=0.05, stroke_width=5, max_tip_length_to_length_ratio=0.25)
            if abs(vy_len) < 0.08:
                a2 = VGroup()
            else:
                end2 = p + UP * vy_len
                a2 = Arrow(p, end2, color=GREEN, buff=0.05, stroke_width=5, max_tip_length_to_length_ratio=0.25)
            tag = Text("vx vy", font_size=24).next_to(ball, UP, buff=0.35)
            return VGroup(ball, a1, a2, tag)
        flyer_mob = always_redraw(flyer)
        self.play(FadeIn(t_title), FadeIn(t_num), FadeIn(flyer_mob), run_time=0.4)
        self.play(t_tracker.animate.set_value(t_apex), run_time=3.0, rate_func=linear)
        t_num.clear_updaters()
        self.remove(flyer_mob)
        ball_apex = Dot(point=pos_at(t_apex), color=WHITE, radius=0.16)
        ball_apex.set_z_index(4)
        self.add(ball_apex, t_num)
        # BEAT A3.B2 | 13.77-18.00 s
        apex_p = pos_at(t_apex)
        ground_p = axes.c2p(vx0 * t_apex, 0)
        h_line = DashedLine(ground_p, apex_p, color=BLUE, dash_length=0.12)
        h_line.set_z_index(3)
        h_lab = Text("H = 10.20 м", font_size=30, color=BLUE).next_to(h_line, RIGHT, buff=0.15)
        h_lab.set_z_index(5)
        eqH = MathTex(r"H=\frac{(v_0\sin\theta)^2}{2g}=10.20", font_size=32)
        eqH.next_to(eq_traj, DOWN, buff=0.1)
        eqH.set_z_index(5)
        self.play(Create(h_line), FadeIn(h_lab), FadeIn(eqH), Flash(apex_p), run_time=0.8)
        self.wait(3.1)
        self.play(FadeOut(eqH), run_time=0.3)
        # BEAT A4.B1 | 18.00-22.23 s
        eqT = MathTex(r"T=\frac{2v_0\sin\theta}{g}=2.89", font_size=36)
        eqT.to_edge(DOWN, buff=0.3)
        eqT.set_z_index(5)
        self.play(FadeIn(eqT), t_tracker.animate.set_value(T), ball_apex.animate.move_to(pos_at(T)), h_line.animate.set_opacity(0.35), run_time=1.2)
        self.wait(2.7)
        self.play(FadeOut(eqT), FadeOut(t_title), FadeOut(t_num), FadeOut(eq_traj), run_time=0.3)
        # BEAT A4.B2 | 22.23-26.00 s
        p0 = axes.c2p(0, 0)
        pR = axes.c2p(R, 0)
        r_arrow = DoubleArrow(p0, pR, color=RED, buff=0.05, stroke_width=6, max_tip_length_to_length_ratio=0.08)
        r_arrow.shift(DOWN * 0.35)
        r_arrow.set_z_index(3)
        eqR = MathTex(r"R=\frac{v_0^2\sin 2\theta}{g}=40.82", font_size=34)
        eqR.next_to(r_arrow, DOWN, buff=0.15)
        eqR.set_z_index(5)
        ball_end = Dot(point=pos_at(T), color=WHITE, radius=0.18)
        ball_end.set_z_index(4)
        self.play(Transform(traj_green, traj_yellow), FadeOut(ball_apex), FadeIn(ball_end), Create(r_arrow), FadeIn(eqR), run_time=1.0)
        self.play(Flash(pos_at(T)), Circumscribe(ball_end), run_time=0.7)
        self.wait(1.7)
        # BEAT A5.B1 | 26.00-30.00 s
        hero_box = Text("H = 10.20 м  •  T = 2.89 с  •  R = 40.82 м", font_size=30, color=WHITE)
        hero_box.to_edge(UP, buff=0.3)
        hero_box.set_z_index(5)
        hero_bg = SurroundingRectangle(hero_box, color=YELLOW, buff=0.15, stroke_width=3)
        self.play(FadeIn(hero_box), FadeIn(hero_bg), run_time=0.5)
        pulse = ValueTracker(0)
        ball_end.add_updater(lambda m: m.scale(1.0))
        ball_end.clear_updaters()
        r_num = DecimalNumber(R, num_decimal_places=2, color=YELLOW, font_size=34)
        r_num.next_to(eqR, RIGHT, buff=0.2)
        self.play(FadeIn(r_num), run_time=0.3)
        def pulse_ball():
            s = 1.0 + 0.18 * np.sin(pulse.get_value() * 2 * np.pi)
            d = Dot(point=pos_at(T), color=WHITE, radius=0.18 * s)
            d.set_z_index(4)
            return d
        pulse_ball_mob = always_redraw(pulse_ball)
        self.add(pulse_ball_mob)
        self.remove(ball_end)
        self.play(AnimationGroup(pulse.animate.set_value(3.0), r_arrow.animate.set_opacity(0.6), lag_ratio=0.0), run_time=3.0, rate_func=linear)
        self.wait(0.2)