from manim import *
import numpy as np

class AetherLabScene(Scene):
    def construct(self):
        v0 = 20.0
        g = 9.8
        th = np.pi / 4
        vx0 = v0 * np.cos(th)
        vy0 = v0 * np.sin(th)
        t_apex = vy0 / g
        H = vy0 ** 2 / (2 * g)
        T = 2 * vy0 / g
        R = v0 ** 2 / g

        def x_of(t):
            return vx0 * t
        def y_of(t):
            return vy0 * t - 0.5 * g * t * t
        def y_of_x(x):
            return x - (g / (2 * vx0 * vx0)) * x * x

        title = Text("Полёт мяча: 20 м/с, 45°", font_size=32)
        title.to_edge(UP, buff=0.3)
        title.set_z_index(10)

        axes = Axes(
            x_range=[0, 45, 10],
            y_range=[0, 12, 5],
            x_length=10.5,
            y_length=4.6,
            axis_config={"stroke_opacity": 0.35},
        )
        axes.scale_to_fit_width(12.0)
        axes.move_to(ORIGIN).shift(DOWN * 0.5)
        axes.set_z_index(0)
        xlab = Text("x, м", font_size=30).next_to(axes.x_axis, RIGHT, buff=0.2)
        ylab = Text("y, м", font_size=30).next_to(axes.y_axis, UP, buff=0.2)
        ground = Line(axes.c2p(0, 0), axes.c2p(45, 0), color=GREEN, stroke_opacity=0.6)
        ground.set_z_index(1)

        traj = axes.plot(lambda xx: y_of_x(xx), x_range=[0, R, 0.2], color=BLUE)
        traj.set_z_index(2)

        ball = Dot(color=YELLOW, radius=0.14)
        ball.set_z_index(5)
        ball.move_to(axes.c2p(0, 0))

        # BEAT A1.B1 | 0.00-4.00 s
        self.play(FadeIn(axes), FadeIn(title), FadeIn(ground), FadeIn(xlab), FadeIn(ylab), run_time=0.6)
        self.play(Create(traj), ball.animate.move_to(axes.c2p(R, 0)), run_time=2.8)
        self.wait(0.6)
        ball.move_to(axes.c2p(0, 0))

        # BEAT A2.B1 | 4.00-10.00 s
        p0 = axes.c2p(0, 0)
        sc = 0.09
        vx_arrow = Arrow(p0, axes.c2p(vx0 * sc * 4, 0), color=YELLOW, buff=0, stroke_width=6)
        vy_arrow = Arrow(p0, axes.c2p(0, vy0 * sc * 4), color=YELLOW, buff=0, stroke_width=6)
        v0_arrow = Arrow(p0, axes.c2p(vx0 * sc * 4, vy0 * sc * 4), color=WHITE, buff=0, stroke_width=5)
        l_vx = Text("vx=14,14 м/с", font_size=30).next_to(vx_arrow, DOWN, buff=0.15)
        l_vy = Text("vy=14,14 м/с", font_size=30).next_to(vy_arrow, LEFT, buff=0.15)
        l_ang = Text("45°", font_size=32).move_to(axes.c2p(6, 1.2))
        eq_decomp = MathTex(r"v_x=v_0\cos 45^\circ,\; v_y=v_0\sin 45^\circ", font_size=34)
        eq_decomp.to_edge(DOWN, buff=0.25)
        eq_decomp.set_z_index(10)
        comp_group = VGroup(vx_arrow, vy_arrow, v0_arrow, l_vx, l_vy, l_ang)
        self.play(LaggedStart(Create(vx_arrow), Create(vy_arrow), Create(v0_arrow), FadeIn(l_vx), FadeIn(l_vy), FadeIn(l_ang), FadeIn(eq_decomp), lag_ratio=0.15), run_time=2.0)
        self.wait(4.0)

        # BEAT A3.B1 | 10.00-14.50 s
        self.play(FadeOut(eq_decomp), FadeOut(comp_group), run_time=0.4)
        t_track = ValueTracker(0.0)
        t_label = Text("t =", font_size=32)
        t_label.to_corner(UR, buff=0.5)
        t_label.shift(DOWN * 0.6)
        t_num = DecimalNumber(0.0, num_decimal_places=2, color=WHITE, font_size=36)
        t_num.next_to(t_label, RIGHT, buff=0.15)
        t_unit = Text("с", font_size=30).next_to(t_num, RIGHT, buff=0.12)
        live_t = VGroup(t_label, t_num, t_unit)
        live_t.set_z_index(10)

        def ball_arrow_group():
            tt = t_track.get_value()
            xx = x_of(tt)
            yy = max(y_of(tt), 0)
            c = axes.c2p(xx, yy)
            b = Dot(c, color=YELLOW, radius=0.14)
            vyy = vy0 - g * tt
            k = 0.12
            ax = Arrow(c, c + RIGHT * vx0 * k * 0.35, color=YELLOW, buff=0, stroke_width=6)
            end2 = c + UP * vyy * k * 0.35
            if vyy >= 0.3:
                ay = Arrow(c, end2, color=YELLOW, buff=0, stroke_width=6)
            else:
                ay = Arrow(c, end2, color=GRAY, buff=0, stroke_width=4)
            tag = Text("vx vy", font_size=26).next_to(c, UP, buff=0.25)
            return VGroup(b, ax, ay, tag)

        flyer = always_redraw(ball_arrow_group)
        t_num.add_updater(lambda m: m.set_value(t_track.get_value()))
        t_num.next_to(t_label, RIGHT, buff=0.15)
        self.play(FadeIn(live_t), run_time=0.5)
        self.play(t_track.animate.set_value(t_apex), run_time=3.4, rate_func=linear)
        self.wait(0.6)

        # BEAT A3.B2 | 14.50-18.00 s
        apex_c = axes.c2p(x_of(t_apex), H)
        hero_dot = Dot(apex_c, color=RED, radius=0.2)
        hero_dot.set_z_index(6)
        self.play(Flash(hero_dot), Circumscribe(hero_dot, color=RED), FadeIn(hero_dot), run_time=0.8)
        h_line = DashedLine(axes.c2p(x_of(t_apex), 0), apex_c, color=YELLOW, dash_length=0.15)
        h_line.set_z_index(3)
        h_val = DecimalNumber(H, num_decimal_places=2, color=WHITE, font_size=34)
        h_pre = Text("H =", font_size=32)
        h_unit = Text("м", font_size=30)
        h_row = VGroup(h_pre, h_val, h_unit)
        h_row.arrange(RIGHT, buff=0.12)
        h_row.next_to(apex_c, RIGHT, buff=0.3)
        h_row.set_z_index(10)
        h_row.scale_to_fit_width(2.6)
        h_row.next_to(apex_c, RIGHT, buff=0.3)
        eq_H = MathTex(r"H=\frac{(v_0\sin\theta)^2}{2g}", font_size=34)
        eq_H.to_edge(DOWN, buff=0.25)
        eq_H.set_z_index(10)
        self.play(Create(h_line), FadeIn(h_row), FadeIn(eq_H), run_time=0.8)
        self.wait(1.9)

        # BEAT A4.B1 | 18.00-22.00 s
        flyer.clear_updaters()
        self.remove(flyer)
        t_num.clear_updaters()
        static_ball = Dot(apex_c, color=YELLOW, radius=0.14)
        static_ball.set_z_index(5)
        self.add(static_ball)
        eq_T = MathTex(r"T=\frac{2v_0\sin 45^\circ}{g}=2{,}89", font_size=36)
        eq_T.to_edge(DOWN, buff=0.25)
        eq_T.set_z_index(10)
        self.play(Transform(eq_H, eq_T), FadeOut(hero_dot), run_time=0.8)
        t_row_pre = Text("T = 2,89 с", font_size=32)
        t_row_pre.next_to(live_t, DOWN, buff=0.15)
        t_row_pre.set_z_index(10)
        self.play(FadeIn(t_row_pre), run_time=0.6)
        self.wait(2.6)

        # BEAT A4.B2 | 22.00-26.00 s
        eq_R = MathTex(r"R=\frac{v_0^2\sin 90^\circ}{g}=40{,}82", font_size=36)
        eq_R.to_edge(DOWN, buff=0.25)
        eq_R.set_z_index(10)
        land_c = axes.c2p(R, 0)
        land_tick = Line(land_c + UP * 0.25, land_c + DOWN * 0.25, color=YELLOW, stroke_width=6)
        land_tick.set_z_index(5)
        r_pre = Text("R =", font_size=32)
        r_val = DecimalNumber(R, num_decimal_places=2, color=WHITE, font_size=34)
        r_unit = Text("м", font_size=30)
        r_row = VGroup(r_pre, r_val, r_unit)
        r_row.arrange(RIGHT, buff=0.12)
        r_row.next_to(land_c, UP, buff=0.3)
        r_row.set_z_index(10)
        self.play(Transform(eq_H, eq_R), Create(land_tick), FadeIn(r_row), run_time=1.0)
        full_ball = Dot(land_c, color=YELLOW, radius=0.14)
        full_ball.set_z_index(5)
        self.play(Create(traj), full_ball.animate.move_to(land_c), run_time=0.6)
        self.wait(2.4)

        # BEAT A5.B1 | 26.00-30.00 s
        self.play(FadeOut(eq_H), FadeOut(t_row_pre), FadeOut(live_t), run_time=0.4)
        recap_title = Text("Парабола побеждает", font_size=34, color=YELLOW)
        recap_title.to_edge(UP, buff=0.3)
        recap_title.set_z_index(10)
        recap_title.scale_to_fit_width(5.5)
        recap_title.to_edge(UP, buff=0.3)
        info = Text("H=10,20 м  R=40,82 м  T=2,89 с", font_size=30)
        info.to_edge(DOWN, buff=0.3)
        info.set_z_index(10)
        self.play(FadeOut(title), FadeIn(recap_title), FadeIn(info), run_time=0.6)
        idle = ValueTracker(0.0)
        h_line.add_updater(lambda m: m.set_stroke(opacity=0.45 + 0.45 * np.sin(idle.get_value() * 4)))
        r_row.add_updater(lambda m, r=r_row.copy(): m.scale(1.0))
        r_tick_scale = ValueTracker(1.0)
        land_tick.add_updater(lambda m: m.set_stroke(width=6))
        self.play(idle.animate.set_value(6.0), run_time=3.0, rate_func=linear)
        h_line.clear_updaters()
        r_row.clear_updaters()
        land_tick.clear_updaters()
        self.wait(0.4)