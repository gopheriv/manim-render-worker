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
            title.to_edge(UP, buff=0.35)
            title.scale_to_fit_width(5.8)

            axes = Axes(
                x_range=[0, 45, 10],
                y_range=[0, 13, 5],
                x_length=10.0,
                y_length=3.4,
                axis_config={"stroke_opacity": 0.4, "stroke_width": 3},
                tips=False,
            )
            axes.move_to(ORIGIN).shift(DOWN * 0.7)
            xlab = Text("x, м", font_size=24).next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
            ylab = Text("y, м", font_size=24).next_to(axes.y_axis.get_end(), UP, buff=0.15)
            ground = Line(axes.c2p(0, 0), axes.c2p(45, 0), color=GREEN, stroke_width=5, stroke_opacity=0.7)

            p0 = axes.c2p(0, 0)
            dir_vec = np.array([np.cos(45 * DEGREES), np.sin(45 * DEGREES), 0])
            barrel = Rectangle(width=1.1, height=0.34, color=GRAY_B, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
            barrel.rotate(45 * DEGREES)
            barrel.move_to(p0 + dir_vec * 0.45 + DOWN * 0.12)
            wheel1 = Circle(radius=0.18, color=GRAY_D, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
            wheel1.move_to(p0 + LEFT * 0.25 + DOWN * 0.28)
            wheel2 = Circle(radius=0.18, color=GRAY_D, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
            wheel2.move_to(p0 + RIGHT * 0.35 + DOWN * 0.28)
            base = Line(wheel1.get_center(), wheel2.get_center(), color=WHITE, stroke_width=4)
            cannon = VGroup(base, wheel1, wheel2, barrel)

            t_track = ValueTracker(0.0)
            t_pre = Text("t =", font_size=28)
            t_num = DecimalNumber(0.0, num_decimal_places=2, font_size=36)
            t_unit = Text("с", font_size=26)
            live_t = VGroup(t_pre, t_num, t_unit)
            live_t.arrange(RIGHT, buff=0.12)
            live_t.to_corner(UR, buff=0.55)
            live_t.shift(DOWN * 0.35)
            h_pre = Text("h =", font_size=28)
            h_num = DecimalNumber(0.0, num_decimal_places=2, font_size=36)
            h_unit = Text("м", font_size=26)
            live_h = VGroup(h_pre, h_num, h_unit)
            live_h.arrange(RIGHT, buff=0.12)
            live_h.next_to(live_t, DOWN, aligned_edge=RIGHT, buff=0.12)
            panel = SurroundingRectangle(VGroup(live_t, live_h), buff=0.18, color=GREY, stroke_opacity=0.6, fill_opacity=0.22)
            readout = VGroup(panel, live_t, live_h)
            t_num.add_updater(lambda m: m.set_value(t_track.get_value()))
            h_num.add_updater(lambda m: m.set_value(max(y_of(t_track.get_value()), 0)))

            # BEAT A1 HOOK 0-4s : cannon fires, ball rides tip of TracedPath
            self.play(FadeIn(axes), FadeIn(title), FadeIn(ground), FadeIn(xlab), FadeIn(ylab), FadeIn(cannon), FadeIn(readout), run_time=0.6)
            ball = Dot(p0, color=YELLOW, radius=0.15)
            ball.add_updater(lambda m: m.move_to(axes.c2p(x_of(t_track.get_value()), max(y_of(t_track.get_value()), 0))))
            trail = TracedPath(ball.get_center, stroke_color=BLUE, stroke_width=6, dissipating_time=0.1)
            flash = Star(n=5, outer_radius=0.35, inner_radius=0.17, color=ORANGE, fill_opacity=1).move_to(p0 + dir_vec * 1.1)
            self.add(ball, trail)
            self.play(FadeIn(flash, scale=0.5), run_time=0.2)
            self.play(FadeOut(flash, scale=1.5), t_track.animate.set_value(T), run_time=2.6, rate_func=linear)
            self.wait(0.6)
            ball.clear_updaters()
            self.remove(trail)
            full_demo = axes.plot(lambda xx: y_of_x(xx), x_range=[0, R, 0.5], color=BLUE, stroke_width=5)
            self.add(full_demo)
            self.remove(ball)
            t_track.set_value(0.0)

            # BEAT A2 4-10s : decomposition, offset labels, one focal at a time
            sc = 0.09
            vx_end = axes.c2p(vx0 * sc * 4, 0)
            vy_end = axes.c2p(0, vy0 * sc * 4)
            v_end = axes.c2p(vx0 * sc * 4, vy0 * sc * 4)
            vx_arrow = Arrow(p0, vx_end, color=YELLOW, buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.2)
            vy_arrow = Arrow(p0, vy_end, color=TEAL, buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.2)
            v0_arrow = Arrow(p0, v_end, color=WHITE, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.18)
            l_vx = Text("vx = 14.1 м/с", font_size=28).next_to(vx_arrow, DOWN, buff=0.35).shift(RIGHT * 0.6)
            l_vy = Text("vy = 14.1 м/с", font_size=28).next_to(vy_arrow, RIGHT, buff=0.45).shift(UP * 0.1)
            ang_arc = Arc(radius=0.75, start_angle=0, angle=45 * DEGREES, arc_center=p0, color=WHITE, stroke_width=4)
            l_ang = Text("45°", font_size=30).move_to(axes.c2p(6.0, 1.4))
            eq_decomp = MathTex(r"v_x=v_0\cos 45^\circ,\; v_y=v_0\sin 45^\circ", font_size=34)
            eq_decomp.to_edge(DOWN, buff=0.4)
            self.play(FadeOut(full_demo), Create(v0_arrow), FadeIn(l_ang), Create(ang_arc), run_time=0.8)
            self.wait(0.5)
            self.play(Create(vx_arrow), FadeIn(l_vx), Create(vy_arrow), FadeIn(l_vy), FadeIn(eq_decomp), run_time=1.2)
            self.wait(2.7)
            self.play(FadeOut(VGroup(vx_arrow, vy_arrow, v0_arrow, ang_arc, l_vx, l_vy, l_ang)), FadeOut(eq_decomp), run_time=0.4)

            # BEAT A3 flight 10-14.5s : vx constant length, vy shrinking, live t+h
            t_track.set_value(0.0)
            ball2 = Dot(p0, color=YELLOW, radius=0.15)
            ball2.add_updater(lambda m: m.move_to(axes.c2p(x_of(t_track.get_value()), max(y_of(t_track.get_value()), 0))))
            trail2 = TracedPath(ball2.get_center, stroke_color=BLUE, stroke_width=6)
            self.add(ball2, trail2)

            k = 0.055
            vx_len = vx0 * k
            def arrow_upd(m):
                tt = t_track.get_value()
                c = axes.c2p(x_of(tt), max(y_of(tt), 0))
                vyy = vy0 - g * tt
                m.become(VGroup())
                a1 = Arrow(c, c + RIGHT * vx_len, color=YELLOW, buff=0, stroke_width=7, max_tip_length_to_length_ratio=0.25)
                vy_vec = vyy * k
                if abs(vy_vec) < 0.12:
                    vy_vec = 0.12 if vyy >= 0 else -0.12
                col = YELLOW if vyy > 0.5 else (GRAY if abs(vyy) <= 0.5 else RED)
                a2 = Arrow(c, c + UP * vy_vec, color=col, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.35)
                lab = Text("vx const", font_size=22, color=YELLOW).next_to(a1.get_end(), RIGHT, buff=0.15)
                m.add(a1, a2, lab)
            vel = VGroup()
            vel.add_updater(arrow_upd)
            self.add(vel)
            self.play(t_track.animate.set_value(t_apex), run_time=3.0, rate_func=linear)
            self.wait(0.6)

            # BEAT apex hero 14.5-18s
            apex_c = axes.c2p(x_of(t_apex), H)
            hero_dot = Dot(apex_c, color=RED, radius=0.2)
            h_line = DashedLine(axes.c2p(x_of(t_apex), 0), apex_c, color=YELLOW, dash_length=0.15, stroke_width=3)
            h_row = Text("H = 10.20 м", font_size=30, color=YELLOW)
            h_row.next_to(apex_c, RIGHT, buff=0.4).shift(UP * 0.1)
            eq_H = MathTex(r"H=\frac{(v_0\sin\theta)^2}{2g}", font_size=36)
            eq_H.to_edge(DOWN, buff=0.4)
            self.play(FadeIn(hero_dot), Create(h_line), FadeIn(h_row), FadeIn(eq_H), run_time=1.2)
            self.wait(1.9)

            # BEAT T 18-22s
            eq_T = MathTex(r"T=\frac{2v_0\sin 45^\circ}{g}=2.89", font_size=36)
            eq_T.to_edge(DOWN, buff=0.4)
            t_row = Text("T = 2.89 с", font_size=28)
            t_row.next_to(readout, DOWN, buff=0.25)
            t_row.to_edge(RIGHT, buff=0.55)
            self.play(Transform(eq_H, eq_T), FadeOut(hero_dot), FadeIn(t_row), run_time=0.9)
            self.wait(2.6)

            # BEAT R 22-26s : continue to landing, ball ends at landing
            eq_R = MathTex(r"R=\frac{v_0^2\sin 90^\circ}{g}=40.82", font_size=36)
            eq_R.to_edge(DOWN, buff=0.4)
            land_c = axes.c2p(R, 0)
            land_tick = Line(land_c + UP * 0.3, land_c + DOWN * 0.3, color=YELLOW, stroke_width=7)
            r_row = Text("R = 40.82 м", font_size=30, color=YELLOW)
            r_row.next_to(land_c, UP, buff=0.45)
            self.play(Transform(eq_H, eq_R), Create(land_tick), FadeIn(r_row), run_time=0.8)
            self.play(t_track.animate.set_value(T), run_time=1.4, rate_func=linear)
            self.wait(1.6)

            # BEAT recap 26-30s : keep ball at landing, living pulse
            self.play(FadeOut(eq_H), FadeOut(t_row), run_time=0.4)
            vel.clear_updaters()
            self.remove(vel)
            ball2.clear_updaters()
            t_num.clear_updaters()
            h_num.clear_updaters()
            ball2.move_to(land_c)
            recap_title = Text("Парабола побеждает", font_size=34, color=YELLOW)
            recap_title.to_edge(UP, buff=0.35)
            recap_title.scale_to_fit_width(4.8)
            info = Text("H = 10.20 м   R = 40.82 м   T = 2.89 с", font_size=26)
            info.to_edge(DOWN, buff=0.4)
            self.play(FadeOut(title), FadeIn(recap_title), FadeIn(info), run_time=0.6)
            pulse = Circle(radius=0.2, color=YELLOW, stroke_width=4).move_to(land_c)
            pulse.add_updater(lambda m, dt: m.scale(1.03).set_stroke(opacity=max(m.get_stroke_opacity() - dt * 0.5, 0.1)))
            pulse2 = Circle(radius=0.15, color=ORANGE, stroke_width=3).move_to(land_c)
            self.add(pulse, pulse2)
            self.play(pulse.animate.scale(3.2).set_opacity(0.1), run_time=1.5)
            pulse.scale(0.35).set_stroke(opacity=0.9)
            self.play(pulse.animate.scale(3.0).set_opacity(0.1), ball2.animate.set_color(ORANGE), run_time=1.5)
            self.wait(0.4)