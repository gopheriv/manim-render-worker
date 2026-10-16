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

        title = Text("Полёт мяча: 20 м/с, 45°", font_size=30)
        title.to_edge(UP, buff=0.4)
        title.scale_to_fit_width(5.8)

        axes = Axes(
            x_range=[0, 45, 10],
            y_range=[0, 13, 5],
            x_length=10.0,
            y_length=3.5,
            axis_config={"stroke_opacity": 0.4, "stroke_width": 3},
            tips=False,
        )
        axes.move_to(ORIGIN).shift(DOWN * 0.65)
        xlab = Text("x, м", font_size=22).next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
        ylab = Text("y, м", font_size=22).next_to(axes.y_axis.get_end(), UP, buff=0.15)
        ground = Line(axes.c2p(0, 0), axes.c2p(45, 0), color=GREEN, stroke_width=4, stroke_opacity=0.6)

        traj_full = axes.plot(lambda xx: y_of_x(xx), x_range=[0, R, 1.0], color=BLUE, stroke_width=5)
        ball0 = Dot(axes.c2p(0, 0), color=YELLOW, radius=0.14)

        # BEAT A1.B1 | 0.00-4.00 s : full flight once, then clean up for continuity
        self.play(FadeIn(axes), FadeIn(title), FadeIn(ground), FadeIn(xlab), FadeIn(ylab), run_time=0.6)
        self.play(Create(traj_full), ball0.animate.move_to(axes.c2p(R, 0)), run_time=2.8, rate_func=linear)
        self.wait(0.6)
        # clear stale curve + ball so next reset to origin is intentional
        self.play(FadeOut(traj_full), FadeOut(ball0), run_time=0.3)

        # BEAT A2.B1 | 4.00-10.00 s : decomposition at origin, safe labels
        p0 = axes.c2p(0, 0)
        sc = 0.09
        vx_end = axes.c2p(vx0 * sc * 4, 0)
        vy_end = axes.c2p(0, vy0 * sc * 4)
        v_end = axes.c2p(vx0 * sc * 4, vy0 * sc * 4)
        vx_arrow = Arrow(p0, vx_end, color=YELLOW, buff=0, stroke_width=6)
        vy_arrow = Arrow(p0, vy_end, color=YELLOW, buff=0, stroke_width=6)
        v0_arrow = Arrow(p0, v_end, color=WHITE, buff=0, stroke_width=5)
        l_vx = Text("vx = 14.1 м/с", font_size=22).next_to(vx_arrow.get_center(), DOWN, buff=0.18)
        # placed to RIGHT of vertical arrow to avoid left-edge clip
        l_vy = Text("vy = 14.1 м/с", font_size=22).next_to(vy_arrow.get_center(), RIGHT, buff=0.2)
        ang_arc = Arc(radius=0.7, start_angle=0, angle=45 * DEGREES, arc_center=p0, color=WHITE, stroke_width=3)
        l_ang = Text("45°", font_size=26).move_to(axes.c2p(5.2, 1.0))
        eq_decomp = MathTex(r"v_x=v_0\cos 45^\circ,\; v_y=v_0\sin 45^\circ", font_size=30)
        eq_decomp.to_edge(DOWN, buff=0.4)
        comp_group = VGroup(vx_arrow, vy_arrow, v0_arrow, ang_arc, l_vx, l_vy, l_ang)
        self.play(
            LaggedStart(Create(vx_arrow), Create(vy_arrow), Create(v0_arrow), Create(ang_arc),
                        FadeIn(l_vx), FadeIn(l_vy), FadeIn(l_ang), FadeIn(eq_decomp), lag_ratio=0.15),
            run_time=2.0
        )
        self.wait(3.7)

        # BEAT A3.B1 | 10.00-14.50 s : progressive flight, owned readout
        self.play(FadeOut(eq_decomp), FadeOut(comp_group), run_time=0.4)
        t_track = ValueTracker(0.0)

        t_pre = Text("t =", font_size=26)
        t_num = DecimalNumber(0.0, num_decimal_places=2, font_size=32)
        t_unit = Text("с", font_size=24)
        live_t = VGroup(t_pre, t_num, t_unit)
        live_t.arrange(RIGHT, buff=0.12, aligned_y=ORIGIN)
        live_t.to_corner(UR, buff=0.7)
        live_t.shift(DOWN * 0.55)
        live_t.scale_to_fit_width(2.0)
        panel = SurroundingRectangle(live_t, buff=0.15, color=GREY, stroke_opacity=0.5, fill_opacity=0.25)
        readout = VGroup(panel, live_t)
        t_num.add_updater(lambda m: m.set_value(t_track.get_value()))

        def make_partial():
            tt = t_track.get_value()
            xe = max(x_of(tt), 0.01)
            return axes.plot(lambda xx: y_of_x(xx), x_range=[0, xe, 1.0], color=BLUE, stroke_width=5)

        def make_ball():
            tt = t_track.get_value()
            c = axes.c2p(x_of(tt), max(y_of(tt), 0))
            return Dot(c, color=YELLOW, radius=0.14)

        def make_varrow():
            tt = t_track.get_value()
            c = axes.c2p(x_of(tt), max(y_of(tt), 0))
            vyy = vy0 - g * tt
            k = 0.045
            a1 = Arrow(c, c + RIGHT * vx0 * k, color=YELLOW, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.25)
            col = YELLOW if vyy >= 0.3 else GRAY
            w = 6 if vyy >= 0.3 else 4
            a2 = Arrow(c, c + UP * vyy * k, color=col, buff=0, stroke_width=w, max_tip_length_to_length_ratio=0.3)
            return VGroup(a1, a2)

        part_traj = always_redraw(make_partial)
        fly_ball = always_redraw(make_ball)
        vel_arrows = always_redraw(make_varrow)

        self.play(FadeIn(readout), run_time=0.5)
        self.add(part_traj, fly_ball, vel_arrows)
        self.play(t_track.animate.set_value(t_apex), run_time=3.0, rate_func=linear)
        self.wait(0.6)

        # BEAT A3.B2 | 14.50-18.00 s : apex hero
        apex_c = axes.c2p(x_of(t_apex), H)
        hero_dot = Dot(apex_c, color=RED, radius=0.2)
        self.play(Flash(hero_dot), FadeIn(hero_dot), run_time=0.8)
        h_line = DashedLine(axes.c2p(x_of(t_apex), 0), apex_c, color=YELLOW, dash_length=0.15, stroke_width=3)
        h_pre = Text("H =", font_size=26)
        h_val = DecimalNumber(H, num_decimal_places=2, font_size=30)
        h_unit = Text("м", font_size=24)
        h_row = VGroup(h_pre, h_val, h_unit)
        h_row.arrange(RIGHT, buff=0.1, aligned_y=ORIGIN)
        h_row.scale_to_fit_width(2.0)
        h_row.next_to(apex_c, RIGHT, buff=0.25)
        # keep inside frame
        h_row.shift(LEFT * 0.2 + UP * 0.15)
        eq_H = MathTex(r"H=\frac{(v_0\sin\theta)^2}{2g}", font_size=32)
        eq_H.to_edge(DOWN, buff=0.4)
        self.play(Create(h_line), FadeIn(h_row), FadeIn(eq_H), run_time=0.8)
        self.wait(1.9)

        # BEAT A4.B1 | 18.00-22.00 s : time of flight
        eq_T = MathTex(r"T=\frac{2v_0\sin 45^\circ}{g}=2.89", font_size=32)
        eq_T.to_edge(DOWN, buff=0.4)
        self.play(Transform(eq_H, eq_T), FadeOut(hero_dot), run_time=0.8)
        t_row = Text("T = 2.89 с", font_size=26)
        t_row.next_to(readout, DOWN, buff=0.2)
        t_row.to_edge(RIGHT, buff=0.7)
        self.play(FadeIn(t_row), run_time=0.6)
        self.wait(2.6)

        # BEAT A4.B2 | 22.00-26.00 s : range
        eq_R = MathTex(r"R=\frac{v_0^2\sin 90^\circ}{g}=40.82", font_size=32)
        eq_R.to_edge(DOWN, buff=0.4)
        land_c = axes.c2p(R, 0)
        land_tick = Line(land_c + UP * 0.25, land_c + DOWN * 0.25, color=YELLOW, stroke_width=6)
        r_pre = Text("R =", font_size=26)
        r_val = DecimalNumber(R, num_decimal_places=2, font_size=30)
        r_unit = Text("м", font_size=24)
        r_row = VGroup(r_pre, r_val, r_unit)
        r_row.arrange(RIGHT, buff=0.1, aligned_y=ORIGIN)
        r_row.scale_to_fit_width(2.0)
        r_row.next_to(land_c, UP, buff=0.3)
        self.play(Transform(eq_H, eq_R), Create(land_tick), FadeIn(r_row), run_time=1.0)
        # continue flight to landing with same tracker
        self.play(t_track.animate.set_value(T), run_time=1.2, rate_func=linear)
        self.wait(1.8)

        # BEAT A5.B1 | 26.00-30.00 s : recap, living ending
        self.play(FadeOut(eq_H), FadeOut(t_row), FadeOut(readout), run_time=0.4)
        # reduce to 3 focal elements: axes+traj, recap title, info
        part_traj.clear_updaters()
        fly_ball.clear_updaters()
        vel_arrows.clear_updaters()
        t_num.clear_updaters()
        self.remove(part_traj, fly_ball, vel_arrows)
        traj_full2 = axes.plot(lambda xx: y_of_x(xx), x_range=[0, R, 1.0], color=BLUE, stroke_width=5)
        self.add(traj_full2)
        recap_title = Text("Парабола побеждает", font_size=32, color=YELLOW)
        recap_title.to_edge(UP, buff=0.4)
        recap_title.scale_to_fit_width(4.8)
        info = Text("H = 10.20 м   R = 40.82 м   T = 2.89 с", font_size=24)
        info.to_edge(DOWN, buff=0.4)
        self.play(FadeOut(title), FadeIn(recap_title), FadeIn(info), run_time=0.6)
        loop = ValueTracker(0.0)

        def loop_ball():
            tt = loop.get_value() % 1.0
            tcur = tt * T
            return Dot(axes.c2p(x_of(tcur), max(y_of(tcur), 0)), color=YELLOW, radius=0.14)

        mover = always_redraw(loop_ball)
        self.add(mover, h_line, h_row, r_row, land_tick)
        self.play(loop.animate.set_value(1.5), run_time=3.0, rate_func=linear)
        self.wait(0.4)