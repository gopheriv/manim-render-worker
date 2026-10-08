from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # Scene-wide background palette (dark tank feel)
        camera_bg = "#0B1220"
        tank_color = "#0E1A2B"
        source_color = "#3B82F6"
        ripple_color = "#60A5FA"
        screen_color = "#F8FAFC"
        accent = "#FACC15"

        self.camera.background_color = camera_bg

        # Build the wave tank (lower half of frame)
        tank = Rectangle(
            width=config.frame_width - 0.6,
            height=2.6,
            stroke_color="#1F2A44",
            stroke_width=2,
            fill_color=tank_color,
            fill_opacity=1.0,
        ).move_to(DOWN * 1.6)

        # Two cylindrical sources on the left, separated by d = 5 lambda units
        d_units = 5.0
        source_y = tank.get_center()[1]
        source_x_left = tank.get_left()[0] + 0.6
        src_gap = 1.6
        src1 = Circle(radius=0.18, color=source_color, fill_opacity=0.9,
                      stroke_width=2).move_to([source_x_left, source_y + src_gap / 2, 0])
        src2 = Circle(radius=0.18, color=source_color, fill_opacity=0.9,
                      stroke_width=2).move_to([source_x_left, source_y - src_gap / 2, 0])

        # Observation screen on the right
        screen_x = tank.get_right()[0] - 0.4
        obs_screen = Line(
            [screen_x, source_y - 1.15, 0],
            [screen_x, source_y + 1.15, 0],
            color=screen_color,
            stroke_width=4,
        )

        # Baseline ripple rings (concentric circles) for each source
        ring_proto = lambda n: Circle(
            radius=0.15 + 0.32 * n,
            stroke_opacity=max(0.0, 0.55 - 0.09 * n),
            stroke_width=1.5,
            color=ripple_color,
        )

        rings1 = VGroup(*[ring_proto(n) for n in range(8)])
        rings2 = VGroup(*[ring_proto(n) for n in range(8)])
        rings1.move_to(src1.get_center())
        rings2.move_to(src2.get_center())

        # Fringe strip on the screen (vertical bright bands)
        n_fringes = 9
        fringe_strip = VGroup()
        fringe_centers_x = []
        band_w = 0.10
        spacing = 0.32
        for i in range(n_fringes):
            bx = screen_x
            band = Rectangle(
                width=band_w,
                height=0.9,
                fill_color=accent,
                fill_opacity=0.0,
                stroke_color=accent,
                stroke_width=2,
            ).move_to([bx, source_y - 0.6 + i * spacing, 0])
            fringe_strip.add(band)
            fringe_centers_x.append(bx)

        # Live readout panel in upper-right
        readout_box = Rectangle(
            width=3.2, height=1.6,
            stroke_color="#334155",
            stroke_width=2,
            fill_color="#0F172A",
            fill_opacity=0.9,
        ).to_corner(UR).shift(DOWN * 0.4 + LEFT * 0.4)

        readout_title = Text("live readout", color="#E2E8F0",
                             font_size=22).move_to(readout_box.get_top() + DOWN * 0.25)

        I0_tracker = ValueTracker(1.0)
        d_tracker = ValueTracker(d_units)
        lam_tracker = ValueTracker(1.0)
        m_tracker = ValueTracker(4)

        def make_readout():
            I0_lbl = Text("I0 =", color="#CBD5E1", font_size=22)
            I0_num = DecimalNumber(I0_tracker.get_value(),
                                   num_decimal_places=2,
                                   color=accent, font_size=22)
            I0_unit = Text("W/m^2", color="#94A3B8", font_size=20)

            d_lbl = Text("d =", color="#CBD5E1", font_size=22)
            d_num = DecimalNumber(d_tracker.get_value(),
                                  num_decimal_places=1,
                                  color=accent, font_size=22)
            d_unit = Text("lam", color="#94A3B8", font_size=20)

            lam_lbl = Text("lam =", color="#CBD5E1", font_size=22)
            lam_num = DecimalNumber(lam_tracker.get_value(),
                                    num_decimal_places=1,
                                    color=accent, font_size=22)

            m_lbl = Text("bright m_max =", color="#CBD5E1", font_size=22)
            m_num = DecimalNumber(m_tracker.get_value(),
                                  num_decimal_places=0,
                                  color=accent, font_size=22)

            row1 = VGroup(I0_lbl, I0_num, I0_unit).arrange(RIGHT, buff=0.12)
            row2 = VGroup(d_lbl, d_num, d_unit).arrange(RIGHT, buff=0.12)
            row3 = VGroup(lam_lbl, lam_num).arrange(RIGHT, buff=0.12)
            row4 = VGroup(m_lbl, m_num).arrange(RIGHT, buff=0.12)

            stack = VGroup(row1, row2, row3, row4).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            stack.move_to(readout_box.get_center() + DOWN * 0.05)

            # Updaters for each number
            I0_num.add_updater(lambda m: m.set_value(I0_tracker.get_value()))
            d_num.add_updater(lambda m: m.set_value(d_tracker.get_value()))
            lam_num.add_updater(lambda m: m.set_value(lam_tracker.get_value()))
            m_num.add_updater(lambda m: m.set_value(m_tracker.get_value()))
            return stack, I0_num, d_num, lam_num, m_num

        readout_stack, I0_num, d_num, lam_num, m_num = make_readout()

        # Pulsing glow on each source and brightness on the fringe strip (idle loop drivers)
        phase = ValueTracker(0.0)

        source_pulse1 = always_redraw(lambda: Circle(
            radius=0.18 + 0.04 * (0.5 + 0.5 * math.cos(2 * math.pi * phase.get_value())),
            color=accent,
            stroke_width=3,
            stroke_opacity=0.6 + 0.4 * (0.5 + 0.5 * math.cos(2 * math.pi * phase.get_value())),
        ).move_to(src1.get_center()))
        source_pulse2 = always_redraw(lambda: Circle(
            radius=0.18 + 0.04 * (0.5 + 0.5 * math.cos(2 * math.pi * phase.get_value())),
            color=accent,
            stroke_width=3,
            stroke_opacity=0.6 + 0.4 * (0.5 + 0.5 * math.cos(2 * math.pi * phase.get_value())),
        ).move_to(src2.get_center()))

        # Reference labels (positioned absolutely, never stacked at the same coord)
        subtitle = Text("Two-source interference  d = 5 lambda",
                        color="#E2E8F0",
                        font_size=30).to_edge(UP, buff=0.35)

        # d = 5 lambda dimension label between the two sources
        d_dim = Brace(
            Line(src1.get_center() + DOWN * 0.22, src2.get_center() + DOWN * 0.22, stroke_opacity=0),
            direction=RIGHT,
            color="#94A3B8",
        )
        d_label = Text("d = 5 lambda", color="#E2E8F0",
                       font_size=28).next_to(d_dim, RIGHT, buff=0.15)

        # ============================ BEATS ============================

        # BEAT A1.B1 | 0.00-4.50 s
        # HOOK: tank + sources rise from the dark; concentric ripples cross.
        self.play(FadeIn(tank), run_time=0.6)
        self.play(FadeIn(src1), FadeIn(src2),
                  FadeIn(obs_screen), run_time=0.6)
        self.add(source_pulse1, source_pulse2)
        self.play(
            LaggedStart(*[FadeIn(r, scale=0.6) for r in rings1], lag_ratio=0.08),
            LaggedStart(*[FadeIn(r, scale=0.6) for r in rings2], lag_ratio=0.08),
            run_time=2.2,
        )
        self.play(phase.animate.set_value(0.6), run_time=1.1, rate_func=linear)

        # BEAT A2.B1 | 4.50-9.50 s
        # ESTABLISH: d = 5 lambda appears; fringe strip brightens.
        self.play(FadeIn(d_dim), FadeIn(d_label), run_time=0.6)
        bright_seq = []
        for i, band in enumerate(fringe_strip):
            bright_seq.append(band.animate.set_fill(opacity=0.0))
        # Light up the fringes left-to-right with measured brightness.
        self.play(
            LaggedStart(
                *[band.animate.set_fill(opacity=0.85) for band in fringe_strip],
                lag_ratio=0.12,
            ),
            FadeIn(readout_box),
            FadeIn(readout_title),
            FadeIn(readout_stack),
            run_time=2.6,
        )
        # Pulse the band group as a whole
        fringe_strip_pulse = VGroup(*fringe_strip)
        self.play(phase.animate.set_value(1.2), run_time=1.4, rate_func=linear)

        # BEAT A3.B1 | 9.50-13.50 s
        # EVOLVE: angle arc from source-midpoint to central bright fringe.
        # First clear what isn't needed for the angle detail.
        self.play(FadeOut(d_dim), FadeOut(d_label), run_time=0.4)

        midpoint = np.array([source_x_left, source_y, 0.0])
        target_fringe = fringe_strip[4].get_center()
        ray_line = Line(midpoint, target_fringe, color=WHITE, stroke_width=2)

        # Small angle arc near the midpoint
        arc_radius = 0.9
        arc = Arc(
            radius=arc_radius,
            start_angle=-PI / 2 + 0.18,
            angle=0.42,
            color=accent,
            stroke_width=3,
        ).move_arc_center_to(midpoint)

        theta_label = MathTex(r"\theta", color=accent, font_size=42).move_to(
            midpoint + RIGHT * 1.0 + UP * 0.15
        )

        I_live = ValueTracker(0.0)
        I_readout_num = DecimalNumber(
            I_live.get_value(),
            num_decimal_places=2,
            color=accent,
            font_size=30,
        )
        I_readout_lbl = Text("I(theta) / I0 =", color="#E2E8F0", font_size=24)
        I_readout_grp = VGroup(I_readout_lbl, I_readout_num).arrange(RIGHT, buff=0.15)
        I_readout_grp.next_to(fringe_strip[0], UP, buff=0.25)
        I_readout_num.add_updater(lambda m: m.set_value(I_live.get_value()))

        self.play(Create(ray_line), Create(arc), FadeIn(theta_label),
                  FadeIn(I_readout_grp), run_time=1.6)
        self.play(I_live.animate.set_value(4.0), run_time=2.0, rate_func=smooth)

        # BEAT A3.B2 | 13.50-17.50 s
        # EVOLVE: intensity equation types itself in.
        self.play(FadeOut(ray_line), FadeOut(arc), FadeOut(theta_label),
                  FadeOut(I_readout_grp), run_time=0.5)

        intensity_eq = MathTex(
            r"I(\theta)", r"=", r"2I_0\!\left(1+\cos\!\left(\tfrac{2\pi d\sin\theta}{\lambda}\right)\right)",
            color="#E2E8F0",
            font_size=36,
        )
        intensity_eq.move_to(DOWN * 0.55)

        # Highlight the live variables
        i0_hl = MathTex(r"I_0", color=accent, font_size=36).move_to(
            intensity_eq.get_center() + DOWN * 0.85 + LEFT * 2.0
        )
        d_hl = MathTex(r"d", color=accent, font_size=36).next_to(i0_hl, RIGHT, buff=0.6)
        lam_hl = MathTex(r"\lambda", color=accent, font_size=36).next_to(d_hl, RIGHT, buff=0.6)

        self.play(Write(intensity_eq), run_time=2.0)
        self.play(FadeIn(i0_hl), FadeIn(d_hl), FadeIn(lam_hl), run_time=1.0)
        self.play(phase.animate.set_value(1.8), run_time=0.6, rate_func=linear)

        # BEAT A4.B1 | 17.50-22.00 s
        # REVEAL: I(theta) vs sin(theta) plot; nine bright peaks to 4I0.
        self.play(
            FadeOut(intensity_eq), FadeOut(i0_hl),
            FadeOut(d_hl), FadeOut(lam_hl),
            run_time=0.5,
        )

        axes = Axes(
            x_range=[-0.55, 0.55, 0.2],
            y_range=[-0.5, 4.6, 1.0],
            x_length=5.6,
            y_length=2.6,
            tips=False,
            axis_config={"stroke_color": "#475569", "stroke_width": 2},
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)

        x_label = Text("sin(theta)", color="#E2E8F0", font_size=24).next_to(
            axes.x_axis.get_end(), RIGHT, buff=0.15
        )
        y_label = MathTex(r"I/I_0", color="#E2E8F0", font_size=28).next_to(
            axes.y_axis.get_end(), UP, buff=0.15
        )

        # Static spectrum: nine peaks to 4I0
        d_val = d_tracker.get_value()
        lam_val = lam_tracker.get_value()

        def I_curve(x):
            return 2.0 * (1.0 + math.cos(2 * math.pi * d_val * x / lam_val))

        spectrum = axes.plot(I_curve, color="#60A5FA", stroke_width=3)
        env_hi = axes.plot(lambda x: 4.0, color="#475569",
                           stroke_width=1.5, stroke_dasharray=[4, 4])
        env_lo = axes.plot(lambda x: 0.0, color="#475569",
                           stroke_width=1.5, stroke_dasharray=[4, 4])

        # Peak dots: sin(theta) = m * lam / d  for m = 0..4 (and negatives mirrored)
        peak_dots = VGroup()
        peak_labels = VGroup()
        m_max = 4
        for m_val in range(0, m_max + 1):
            for sign in ([1, -1] if m_val != 0 else [1]):
                tpos = sign * m_val * lam_val / d_val
                if abs(tpos) <= 0.5:
                    peak_dots.add(Dot(axes.c2p(tpos, 4.0),
                                      color=accent, radius=0.06))
                    lbl = MathTex(f"m={sign*m_val}", color=accent, font_size=22).next_to(
                        Dot(axes.c2p(tpos, 4.0)), UP, buff=0.1
                    )
                    peak_labels.add(lbl)
        # m=0 label centered
        peak_labels.add(MathTex(r"m=0", color=accent, font_size=22).next_to(
            Dot(axes.c2p(0.0, 4.0)), UP, buff=0.1
        ))
        peak_dots.add(Dot(axes.c2p(0.0, 4.0), color=accent, radius=0.07))

        nine_text = Text("nine bright peaks", color=accent, font_size=26).next_to(
            axes, UP, buff=0.15
        )

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.0)
        self.play(Create(spectrum), Create(env_hi), Create(env_lo), run_time=1.6)
        self.play(FadeIn(peak_dots), FadeIn(peak_labels), FadeIn(nine_text),
                  m_tracker.animate.set_value(4), run_time=1.0)

        # BEAT A4.B2 | 22.00-25.50 s
        # REVEAL: annotate central maximum with d sinθ = mλ; confirm nine fringes.
        self.play(FadeOut(nine_text), run_time=0.3)

        central_dot = peak_dots[-1]
        annotation = MathTex(r"d\sin\theta = m\lambda",
                             color=accent, font_size=36).next_to(central_dot, DOWN, buff=0.4)
        arrow = Arrow(annotation.get_top() + LEFT * 0.1,
                      central_dot.get_bottom() + UP * 0.05,
                      buff=0.05, color=accent, stroke_width=2)

        confirm_box = Rectangle(
            width=3.6, height=0.7,
            stroke_color=accent, stroke_width=2,
            fill_color="#0F172A", fill_opacity=0.85,
        ).to_edge(DOWN, buff=0.45)
        confirm_text = Text(
            "d = 5 lambda gives 9 bright fringes (m = 0, +/-1, +/-2, +/-3, +/-4)",
            color=accent, font_size=22,
        ).move_to(confirm_box.get_center())

        self.play(Create(arrow), Write(annotation), run_time=1.4)
        self.play(FadeIn(confirm_box), FadeIn(confirm_text), run_time=1.0)
        self.play(phase.animate.set_value(2.4), run_time=0.6, rate_func=linear)

        # BEAT A5.B1 | 25.50-30.00 s
        # RECAP: hero composition. Camera "pulls back" by scaling the whole scene.
        self.play(
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label),
            FadeOut(spectrum), FadeOut(env_hi), FadeOut(env_lo),
            FadeOut(peak_dots), FadeOut(peak_labels),
            FadeOut(arrow), FadeOut(annotation),
            FadeOut(confirm_box), FadeOut(confirm_text),
            run_time=0.6,
        )

        # Hero arrangement: sources on left, full fringe strip glowing,
        # compact intensity plot on the right, equation in the lower margin.
        hero_eq = MathTex(r"d\sin\theta = m\lambda",
                          color=accent, font_size=38).to_edge(DOWN, buff=0.35)

        # Mini intensity plot for the hero
        mini_axes = Axes(
            x_range=[-0.55, 0.55, 0.2],
            y_range=[-0.4, 4.4, 1.0],
            x_length=3.0, y_length=1.8,
            tips=False,
            axis_config={"stroke_color": "#475569", "stroke_width": 2},
        )
        mini_axes.to_corner(DR).shift(UP * 0.1 + LEFT * 0.2)
        mini_curve = mini_axes.plot(I_curve, color="#60A5FA", stroke_width=2.5)
        mini_env_hi = mini_axes.plot(lambda x: 4.0, color="#475569",
                                     stroke_width=1.2, stroke_dasharray=[3, 3])
        mini_env_lo = mini_axes.plot(lambda x: 0.0, color="#475569",
                                     stroke_width=1.2, stroke_dasharray=[3, 3])
        mini_plot = VGroup(mini_axes, mini_curve, mini_env_hi, mini_env_lo)

        hero_label = Text("hero: 9 bright fringes from d = 5 lambda",
                          color="#E2E8F0", font_size=26).next_to(hero_eq, UP, buff=0.3)

        # Re-show the d = 5 lambda dimension for the hero
        d_dim2 = Brace(
            Line(src1.get_center() + DOWN * 0.22,
                 src2.get_center() + DOWN * 0.22, stroke_opacity=0),
            direction=RIGHT, color="#94A3B8",
        )
        d_label2 = Text("d = 5 lambda", color="#E2E8F0",
                        font_size=28).next_to(d_dim2, RIGHT, buff=0.15)

        self.play(FadeIn(mini_plot), run_time=0.7)
        self.play(FadeIn(d_dim2), FadeIn(d_label2), run_time=0.5)
        self.play(Write(hero_eq), FadeIn(hero_label), run_time=1.0)

        # Idle loop: gentle ripple phase advance and fringe brightness breathing.
        self.play(
            phase.animate.set_value(3.0),
            *[band.animate.set_fill(opacity=max(0.0, 0.6 + 0.25 * math.cos(
                2 * math.pi * (0.4 * i + 0.0))))
              for i, band in enumerate(fringe_strip)],
            run_time=1.5,
            rate_func=linear,
        )

        # Keep the scene breathing through the final hold so last frames differ.
        for k in range(3):
            t_phase = 3.0 + 0.5 * (k + 1)
            self.play(
                phase.animate.set_value(t_phase),
                m_tracker.animate.set_value(4),
                run_time=0.4,
                rate_func=linear,
            )
            self.wait(0.1)