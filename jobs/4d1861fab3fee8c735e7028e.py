from manim import *
import numpy as np
import math


def doppler(vs, f0=500.0, v=343.0):
    return f0 * v / (v - vs)


class AetherLabScene(Scene):
    def construct(self):
        PRIMARY = "#E74C3C"
        SECONDARY = "#3498DB"
        ACCENT = "#F1C40F"
        f0_val = 500.0
        v_sound = 343.0
        vs_val = 20.0

        # ------------------------------------------------------------------
        # BEAT A1.B1 | 0.00-2.50 s
        # ------------------------------------------------------------------
        title = Text("Doppler Effect", color=WHITE).scale(0.55).to_edge(UP, buff=0.25)

        # Thinner strip so the wave ribbon can dominate visually
        strip = Rectangle(width=10.5, height=0.9, stroke_width=0,
                          fill_color="#2C3E50", fill_opacity=1.0).shift(DOWN * 2.5)
        dashed = DashedLine(start=strip.get_left(), end=strip.get_right(),
                            dash_length=0.18, color=WHITE, stroke_width=2).move_to(strip)

        mic = VGroup(
            Circle(radius=0.16, color=WHITE, fill_opacity=1, stroke_color=WHITE),
            Line(UP * 0.16, DOWN * 0.45, color=WHITE, stroke_width=3),
            Line(LEFT * 0.18, RIGHT * 0.18, color=WHITE, stroke_width=3).shift(DOWN * 0.45),
        ).scale(0.7).move_to(strip.get_left() + RIGHT * 1.0 + UP * 0.05)

        van = VGroup(
            RoundedRectangle(width=0.9, height=0.45, corner_radius=0.06,
                             color=PRIMARY, fill_opacity=1, stroke_color=PRIMARY),
            Polygon(LEFT * 0.05, RIGHT * 0.05, RIGHT * 0.35, LEFT * 0.45,
                    color=PRIMARY, fill_opacity=1, stroke_color=PRIMARY).shift(UP * 0.18),
            Circle(radius=0.08, color=BLACK, fill_opacity=1).shift(LEFT * 0.28 + DOWN * 0.22),
            Circle(radius=0.08, color=BLACK, fill_opacity=1).shift(RIGHT * 0.28 + DOWN * 0.22),
        ).move_to(strip.get_right() + LEFT * 1.2 + UP * 0.05)

        # Sinusoidal wave ribbon (full waveform, not squiggle marks) — placed
        # to the LEFT of the van (the van is moving RIGHT, so emitted waves
        # pile up behind/below the strip from the observer's viewpoint).
        def make_ribbon(spacing):
            pts = []
            amp = 0.18
            # Build a single continuous polyline so it reads as one ribbon.
            n = 220
            x0 = -5.0
            x1 = 0.6
            xs = np.linspace(x0, x1, n)
            for i, x in enumerate(xs):
                # Use the spacing parameter to control wavelength.
                wavelength = spacing * 0.55
                y = amp * np.sin(2 * np.pi * (x - x0) / wavelength)
                pts.append([x, y, 0.0])
            ribbon_line = VMobject(stroke_color=PRIMARY, stroke_width=3)
            ribbon_line.set_points_as_corners([np.array(p) for p in pts])
            # Add a translucent fill below the curve to read as a band.
            fill_pts = list(pts) + [[x1, -amp * 0.6, 0.0], [x0, -amp * 0.6, 0.0]]
            fill = Polygon(*fill_pts, fill_color=PRIMARY, fill_opacity=0.18,
                           stroke_width=0)
            return VGroup(fill, ribbon_line)

        # Two ribbons: a relaxed one and a compressed one to be cross-faded.
        ribbon_relaxed = make_ribbon(spacing=0.45)
        ribbon_compressed = make_ribbon(spacing=0.22)
        for r in (ribbon_relaxed, ribbon_compressed):
            r.move_to(van.get_left() + LEFT * 0.05 + UP * 0.0)
        ribbon_compressed.set_opacity(0.0)

        self.play(
            FadeIn(title),
            FadeIn(strip), Create(dashed),
            FadeIn(mic), FadeIn(van),
            FadeIn(ribbon_relaxed),
            run_time=0.9,
        )

        van_start_x = van.get_center()[0]
        van_end_x = mic.get_center()[0] + 1.2
        self.play(
            van.animate.move_to([van_end_x, van.get_center()[1], 0]),
            ribbon_relaxed.animate.move_to([van_end_x - 1.2, van.get_center()[1], 0]),
            run_time=1.4, rate_func=smooth,
        )
        self.wait(0.2)

        # ------------------------------------------------------------------
        # BEAT A1.B2 | 2.50-5.00 s
        # ------------------------------------------------------------------
        vs_tracker = ValueTracker(vs_val)

        # Live counter positioned safely above the mic (well within frame).
        readout = always_redraw(
            lambda: DecimalNumber(
                doppler(vs_tracker.get_value(), f0_val, v_sound),
                num_decimal_places=0, color=ACCENT, font_size=34,
            ).move_to(mic.get_center() + UP * 0.95 + LEFT * 0.2)
        )
        hz_label = Text("Hz", color=ACCENT, font_size=22).next_to(readout, RIGHT, buff=0.1)
        freq_caption = Text("received f'", color=WHITE, font_size=22).next_to(readout, LEFT, buff=0.15)

        # Cross-fade from relaxed to compressed ribbon — physical visualization
        # of wavelength compression as the source speeds up.
        self.play(
            FadeIn(freq_caption), FadeIn(hz_label), FadeIn(readout),
            ribbon_compressed.animate.set_opacity(1.0),
            run_time=0.5,
        )
        self.play(vs_tracker.animate.set_value(28.0), run_time=1.6, rate_func=smooth)
        self.wait(0.4)

        # ------------------------------------------------------------------
        # BEAT A2.B1 | 5.00-8.00 s
        # ------------------------------------------------------------------
        van_dot = Dot(point=van.get_center(), color=PRIMARY, radius=0.06)
        mic_mini = VGroup(
            Circle(radius=0.08, color=WHITE, fill_opacity=1),
            Line(UP * 0.08, DOWN * 0.18, color=WHITE, stroke_width=2),
        ).scale(0.5).move_to(mic.get_center())

        # Axes shifted LEFT so the plot occupies the right two-thirds, but
        # the title/equation labels still have headroom on the right.
        axes = Axes(
            x_range=[0, 350, 50],
            y_range=[0, 1500, 250],
            x_length=6.4,
            y_length=3.6,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2,
                         "include_tip": False, "include_numbers": False},
        ).shift(RIGHT * 0.9 + UP * 0.3)
        x_label = Text("source speed v_s (m/s)", color=WHITE, font_size=20).next_to(axes.x_axis, DOWN, buff=0.25)
        y_label = Text("received f' (Hz)", color=WHITE, font_size=20).next_to(axes.y_axis, LEFT, buff=0.25).rotate(PI / 2)
        x_ticks = VGroup(*[
            Text(str(xv), color=GREY_A, font_size=16).next_to(axes.c2p(xv, 0), DOWN, buff=0.08)
            for xv in [0, 100, 200, 300]
        ])
        y_ticks = VGroup(*[
            Text(str(yv), color=GREY_A, font_size=16).next_to(axes.c2p(0, yv), LEFT, buff=0.08)
            for yv in [0, 500, 1000, 1500]
        ])

        # Subtle reference line (thin, low-opacity) — not a competing element.
        f0_line = DashedLine(
            start=axes.c2p(0, f0_val), end=axes.c2p(350, f0_val),
            color=ACCENT, stroke_width=2, dash_length=0.15,
        )
        f0_line.set_opacity(0.55)
        f0_tag = Text("f_0 = 500 Hz", color=ACCENT, font_size=22).next_to(
            axes.c2p(350, f0_val), LEFT, buff=0.15)

        # Clear the strip scene and build the plot.
        self.play(
            FadeOut(VGroup(strip, dashed, ribbon_relaxed, ribbon_compressed,
                           freq_caption, hz_label)),
            Transform(van, van_dot),
            Transform(mic, mic_mini),
            FadeIn(axes), FadeIn(x_label), FadeIn(y_label),
            FadeIn(x_ticks), FadeIn(y_ticks),
            Create(f0_line), FadeIn(f0_tag),
            run_time=1.0,
        )
        self.wait(2.0)

        # ------------------------------------------------------------------
        # BEAT A2.B2 | 8.00-11.00 s
        # ------------------------------------------------------------------
        curve = axes.plot(
            lambda x: doppler(min(x, 342.0), f0_val, v_sound),
            x_range=[0, 340], color=SECONDARY, stroke_width=4,
        )
        # Single equation, placed safely above the plot, LEFT-aligned to the
        # axes (away from the y-axis label).
        curve_label = MathTex("f' = \\frac{f_0\\, v}{v - v_s}",
                              color=SECONDARY, font_size=32)
        curve_label.next_to(axes, UP, buff=0.2).align_to(axes, LEFT).shift(RIGHT * 0.1)

        # Asymptote tag placed INSIDE the plot region (above-left of the
        # asymptote) so it never runs off the right edge.
        asymp = DashedLine(
            start=axes.c2p(340, 0), end=axes.c2p(340, 1500),
            color=PRIMARY, stroke_width=3, dash_length=0.12,
        )
        asymp_tag = Text("sound-speed limit v = 343 m/s", color=PRIMARY, font_size=20)
        asymp_tag.next_to(axes.c2p(340, 1320), UL, buff=0.12)

        self.play(Create(curve), run_time=1.0)
        self.play(Create(asymp), FadeIn(asymp_tag), FadeIn(curve_label), run_time=0.7)
        self.wait(1.3)

        # ------------------------------------------------------------------
        # BEAT A3.B1 | 11.00-15.00 s
        # ------------------------------------------------------------------
        x_cur, y_cur = 20.0, doppler(20.0, f0_val, v_sound)
        guideline = DashedLine(
            start=axes.c2p(x_cur, 0), end=axes.c2p(x_cur, y_cur),
            color=PRIMARY, stroke_width=2, dash_length=0.1,
        )
        marker = Dot(point=axes.c2p(x_cur, y_cur), color=ACCENT, radius=0.11)
        marker_label = Text("current: 530.6 Hz", color=ACCENT, font_size=22).next_to(
            marker, UR, buff=0.15)

        # Bottom readout — kept compact, placed safely inside the frame.
        bottom_readout = always_redraw(
            lambda: DecimalNumber(doppler(vs_tracker.get_value(), f0_val, v_sound),
                                  num_decimal_places=0, color=ACCENT, font_size=30)
            .move_to(DOWN * 3.2 + RIGHT * 2.5)
        )
        bottom_hz = Text("Hz", color=ACCENT, font_size=22).next_to(bottom_readout, RIGHT, buff=0.1)
        bottom_caption = Text("f' =", color=WHITE, font_size=24).next_to(bottom_readout, LEFT, buff=0.15)

        self.play(
            Create(guideline), FadeIn(marker, scale=1.4),
            FadeIn(marker_label),
            FadeIn(bottom_caption), FadeIn(bottom_hz), FadeIn(bottom_readout),
            run_time=1.0,
        )
        self.play(vs_tracker.animate.set_value(20.0), run_time=1.4, rate_func=linear)
        self.wait(1.6)

        # ------------------------------------------------------------------
        # BEAT A3.B2 | 15.00-19.00 s
        # ------------------------------------------------------------------
        sweeps = [
            (100, 588.0, 1.0, 0.4),
            (200, 714.0, 1.0, 0.4),
            (300, 1150.0, 1.0, 0.4),
        ]
        for vs_target, hz_text, run_t, _ in sweeps:
            new_label = Text(f"current: {hz_text:.0f} Hz", color=ACCENT, font_size=22).next_to(
                axes.c2p(vs_target, doppler(vs_target, f0_val, v_sound)), UR, buff=0.15)
            self.play(
                marker.animate.move_to(axes.c2p(vs_target, doppler(vs_target, f0_val, v_sound))),
                guideline.animate.put_start_and_end_on(
                    axes.c2p(vs_target, 0),
                    axes.c2p(vs_target, doppler(vs_target, f0_val, v_sound)),
                ),
                Transform(marker_label, new_label),
                vs_tracker.animate.set_value(vs_target),
                run_time=run_t, rate_func=linear,
            )
        self.wait(1.0)

        # ------------------------------------------------------------------
        # BEAT A4.B1 | 19.00-23.12 s
        # ------------------------------------------------------------------
        hero_x, hero_y = 20.0, doppler(20.0, f0_val, v_sound)
        hero_label = Text("v_s = 20 m/s  ->  f' = 530.6 Hz",
                          color=ACCENT, font_size=24).next_to(
            axes.c2p(hero_x, hero_y), UR, buff=0.18)

        # Hero thin strip at the very bottom — physically THIN.
        hero_strip = Rectangle(width=13.0, height=0.18, stroke_width=0,
                               fill_color="#2C3E50", fill_opacity=1.0).to_edge(DOWN, buff=0.12)
        hero_dash = DashedLine(start=hero_strip.get_left(), end=hero_strip.get_right(),
                               dash_length=0.2, color=WHITE, stroke_width=1.5).move_to(hero_strip)
        hero_van = VGroup(
            RoundedRectangle(width=0.32, height=0.14, corner_radius=0.03,
                             color=PRIMARY, fill_opacity=1, stroke_color=PRIMARY),
            Circle(radius=0.035, color=BLACK, fill_opacity=1).shift(LEFT * 0.10 + DOWN * 0.08),
            Circle(radius=0.035, color=BLACK, fill_opacity=1).shift(RIGHT * 0.10 + DOWN * 0.08),
        ).move_to(hero_strip.get_center() + LEFT * 4.5)
        hero_mic = VGroup(
            Circle(radius=0.07, color=WHITE, fill_opacity=1),
            Line(UP * 0.07, DOWN * 0.12, color=WHITE, stroke_width=1.6),
        ).scale(0.7).move_to(hero_strip.get_left() + RIGHT * 1.0)

        # Single equation, in the lower-left quadrant (well clear of axes).
        hero_eq = MathTex("f' = \\frac{f_0\\, v}{v - v_s}",
                          color=WHITE, font_size=34).to_corner(DL, buff=0.5)

        # Highlight the asymptote + "approaches infinity" tag, placed INSIDE.
        glow = DashedLine(
            start=axes.c2p(343, 0), end=axes.c2p(343, 1500),
            color=PRIMARY, stroke_width=5, dash_length=0.1,
        )
        inf_tag = Text("approaches infinity", color=PRIMARY, font_size=22).next_to(
            axes.c2p(340, 1100), UL, buff=0.12)

        self.play(
            FadeOut(VGroup(marker_label, bottom_caption, bottom_hz, bottom_readout)),
            marker.animate.move_to(axes.c2p(hero_x, hero_y)),
            guideline.animate.put_start_and_end_on(axes.c2p(hero_x, 0), axes.c2p(hero_x, hero_y)),
            FadeIn(hero_label),
            Transform(asymp, glow), FadeIn(inf_tag),
            FadeIn(hero_strip), FadeIn(hero_dash), FadeIn(hero_van), FadeIn(hero_mic),
            FadeIn(hero_eq),
            run_time=1.4,
        )
        self.wait(2.72)

        # ------------------------------------------------------------------
        # BEAT A4.B2 | 23.12-26.00 s
        # ------------------------------------------------------------------
        shock_van = hero_van.copy().move_to(hero_strip.get_right() + LEFT * 0.4)
        flash = Circle(radius=0.4, color=ACCENT, fill_opacity=0.8, stroke_width=0).move_to(shock_van)
        micro_ribbon = VGroup(*[
            Line(LEFT * 0.04, RIGHT * 0.04, color=PRIMARY, stroke_width=2)
            .shift(RIGHT * i * 0.05).move_to(shock_van.get_left() + LEFT * 0.1 + UP * 0.18)
            for i in range(6)
        ])
        # Spike readout — placed safely inside frame.
        spike = DecimalNumber(9999, color=PRIMARY, font_size=30).move_to(UP * 2.6 + RIGHT * 1.5)
        spike_lbl = Text("clipped", color=PRIMARY, font_size=22).next_to(spike, DOWN, buff=0.1)

        self.play(
            Transform(hero_van, shock_van),
            Flash(flash, color=ACCENT, flash_radius=0.7, line_length=0.22, num_lines=14),
            FadeIn(micro_ribbon),
            FadeIn(spike, scale=1.3), FadeIn(spike_lbl),
            run_time=1.1,
        )
        self.wait(1.3)
        self.play(
            FadeOut(spike), FadeOut(spike_lbl),
            FadeOut(micro_ribbon), FadeOut(flash),
            run_time=0.48,
        )

        # ------------------------------------------------------------------
        # BEAT A5.B1 | 26.00-30.00 s
        # ------------------------------------------------------------------
        # Recap composition: clean focal point = the equation at center,
        # supported by mic (left) and vs label (right). No stacked equations.
        recap_mic = VGroup(
            Circle(radius=0.12, color=WHITE, fill_opacity=1),
            Line(UP * 0.12, DOWN * 0.28, color=WHITE, stroke_width=2),
            Line(LEFT * 0.12, RIGHT * 0.12, color=WHITE, stroke_width=2).shift(DOWN * 0.28),
        ).scale(0.7).move_to(LEFT * 5.2 + DOWN * 0.2)
        recap_caption = Text("stationary observer", color=WHITE, font_size=22).next_to(
            recap_mic, DOWN, buff=0.2)
        recap_eq = MathTex("f' = \\frac{f_0\\, v}{v - v_s}",
                           color=ACCENT, font_size=46).move_to(UP * 0.4)
        vs_label = Text("v_s = 20 m/s", color=ACCENT, font_size=28).move_to(
            RIGHT * 4.2 + DOWN * 0.2)

        # Pre-build breathing curve overlays (subtle ±1% wobble).
        breath_phases = [0.0, 0.25, 0.5, 0.75]
        breath_curves = VGroup(*[
            axes.plot(
                lambda x, ph=ph: doppler(min(x, 342.0), f0_val, v_sound)
                * (1.0 + 0.01 * math.sin(2 * math.pi * ph / 2.0)),
                x_range=[0, 340], color=SECONDARY, stroke_width=4,
            )
            for ph in breath_phases
        ])
        # Hide the main static curve; overlays will become the visible curve.
        curve.set_opacity(0.0)
        for ov in breath_curves[1:]:
            ov.set_opacity(0.0)

        self.play(
            FadeOut(VGroup(hero_label, inf_tag, hero_van, hero_eq,
                           curve_label, f0_tag, f0_line, marker, guideline, asymp)),
            FadeIn(recap_mic), FadeIn(recap_caption),
            FadeIn(recap_eq), FadeIn(vs_label),
            run_time=0.7,
        )
        # Add overlay curves to the scene (already drawn, opacity 0).
        for ov in breath_curves:
            self.add(ov)

        # Lightweight updater: cross-fade between pre-built curve overlays
        # so the focal curve visibly breathes.
        breathe_t = ValueTracker(0.0)

        def breathe(m, dt):
            breathe_t.increment_value(dt)
            phase = (math.sin(2 * math.pi * breathe_t.get_value() / 2.0) + 1.0) * 0.5
            target_idx = int(phase * 3 + 0.5) % 4
            for i, ov in enumerate(breath_curves):
                if i == target_idx:
                    blend = 1.0 - abs(phase - (i / 3.0)) * 3.0
                    ov.set_opacity(max(0.0, min(1.0, blend)))
                else:
                    ov.set_opacity(0.0)

        breath_curves.add_updater(breathe)

        # Marker pulse — provides a second, smaller focal point on the curve.
        pulse_t = ValueTracker(0.0)
        recap_marker = Dot(point=axes.c2p(20.0, doppler(20.0, f0_val, v_sound)),
                           color=ACCENT, radius=0.11)
        self.play(FadeIn(recap_marker, scale=1.3), run_time=0.4)
        recap_marker.set_z_index(2)
        recap_marker.add_updater(lambda m, dt: (
            m.set_radius(0.10 + 0.02 * math.sin(2 * math.pi * pulse_t.get_value())),
            pulse_t.increment_value(dt),
        ))

        self.wait(3.3)