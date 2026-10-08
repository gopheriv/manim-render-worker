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
        title = Text("Doppler Effect", color=WHITE).scale(0.5).to_edge(UP, buff=0.25)

        strip = Rectangle(width=12.0, height=1.4, stroke_width=0,
                          fill_color="#2C3E50", fill_opacity=1.0).shift(DOWN * 2.6)
        dashed = DashedLine(start=strip.get_left() + UP * 0.0, end=strip.get_right(),
                            dash_length=0.18, color=WHITE, stroke_width=2).move_to(strip)
        mic = VGroup(
            Circle(radius=0.16, color=WHITE, fill_opacity=1, stroke_color=WHITE),
            Line(UP * 0.16, DOWN * 0.45, color=WHITE, stroke_width=3),
            Line(LEFT * 0.18, RIGHT * 0.18, color=WHITE, stroke_width=3).shift(DOWN * 0.45),
        ).scale(0.7).move_to(strip.get_left() + RIGHT * 1.0 + UP * 0.15)

        van = VGroup(
            RoundedRectangle(width=0.9, height=0.45, corner_radius=0.06,
                             color=PRIMARY, fill_opacity=1, stroke_color=PRIMARY),
            Polygon(LEFT * 0.05, RIGHT * 0.05, RIGHT * 0.35, LEFT * 0.45,
                    color=PRIMARY, fill_opacity=1, stroke_color=PRIMARY).shift(UP * 0.18),
            Circle(radius=0.08, color=BLACK, fill_opacity=1).shift(LEFT * 0.28 + DOWN * 0.22),
            Circle(radius=0.08, color=BLACK, fill_opacity=1).shift(RIGHT * 0.28 + DOWN * 0.22),
        ).move_to(strip.get_right() + LEFT * 1.2 + UP * 0.05)

        # pre-build once
        ribbon = VGroup()
        for i in range(12):
            crest = Arc(radius=0.18, start_angle=0, angle=PI, color=PRIMARY,
                        stroke_width=2).rotate(PI / 2).shift(RIGHT * (i * 0.30))
            trough = Arc(radius=0.18, start_angle=PI, angle=PI, color=PRIMARY,
                         stroke_width=2).rotate(PI / 2).shift(RIGHT * (i * 0.30 + 0.15))
            ribbon.add(VGroup(crest, trough))
        ribbon.set_stroke(opacity=0.7)
        ribbon.next_to(van, RIGHT, buff=0.05).align_to(van, DOWN)

        # Combined intro: strip + dashed + mic + van + ribbon in one play
        self.play(
            FadeIn(strip), Create(dashed),
            FadeIn(mic), FadeIn(van),
            FadeIn(ribbon, lag_ratio=0.05),
            run_time=0.9,
        )

        van_start_x = van.get_center()[0]
        van_end_x = mic.get_center()[0] + 1.2
        self.play(
            van.animate.move_to([van_end_x, van.get_center()[1], 0]),
            ribbon.animate.shift(LEFT * (van_start_x - van_end_x)),
            run_time=1.4, rate_func=smooth,
        )
        self.wait(0.2)

        # ------------------------------------------------------------------
        # BEAT A1.B2 | 2.50-5.00 s
        # ------------------------------------------------------------------
        vs_tracker = ValueTracker(vs_val)

        # Single updater-controlled readout; fade in number BEFORE first tracker change
        readout = always_redraw(
            lambda: DecimalNumber(
                doppler(vs_tracker.get_value(), f0_val, v_sound),
                num_decimal_places=0, color=ACCENT, font_size=34,
            ).next_to(mic, UP, buff=0.35)
        )
        hz_label = Text("Hz", color=ACCENT, font_size=22).next_to(mic, UP, buff=0.35).shift(RIGHT * 0.95)
        freq_label = Text("f' (Hz)", color=WHITE, font_size=22).next_to(mic, UP, buff=0.35).shift(LEFT * 1.2)
        freq_caption = Text("received f'", color=WHITE, font_size=22)

        # Fade in number and labels together, then animate tracker afterwards
        self.play(
            FadeIn(freq_label), FadeIn(hz_label), FadeIn(freq_caption),
            FadeIn(readout),
            run_time=0.5,
        )
        # small compression effect: pull ribbon crests ahead of van
        for crest in ribbon:
            crest.shift(LEFT * 0.03)
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

        axes = Axes(
            x_range=[0, 350, 50],
            y_range=[0, 1500, 250],
            x_length=6.2,
            y_length=4.2,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2,
                         "include_tip": False, "include_numbers": False},
        ).to_edge(RIGHT, buff=0.6).shift(UP * 0.2)
        x_label = Text("source speed v_s (m/s)", color=WHITE, font_size=20).next_to(axes.x_axis, DOWN, buff=0.25)
        y_label = Text("received frequency f' (Hz)", color=WHITE, font_size=20).next_to(axes.y_axis, LEFT, buff=0.25).rotate(PI / 2)
        x_ticks = VGroup(*[
            Text(str(xv), color=GREY_A, font_size=16).next_to(axes.c2p(xv, 0), DOWN, buff=0.08)
            for xv in [0, 100, 200, 300]
        ])
        y_ticks = VGroup(*[
            Text(str(yv), color=GREY_A, font_size=16).next_to(axes.c2p(0, yv), LEFT, buff=0.08)
            for yv in [0, 500, 1000, 1500]
        ])

        f0_line = DashedLine(
            start=axes.c2p(0, f0_val), end=axes.c2p(350, f0_val),
            color=ACCENT, stroke_width=3, dash_length=0.15,
        )
        f0_tag = Text("f_0 = 500 Hz", color=ACCENT, font_size=24).next_to(axes.c2p(340, f0_val), RIGHT, buff=0.1)

        # Single play: clear strip scene + build axes/labels/f0 reference
        self.play(
            FadeOut(VGroup(strip, dashed, ribbon, freq_label, hz_label, freq_caption)),
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
        curve_label = MathTex("f' = \\frac{f_0\\, v}{v - v_s}", color=SECONDARY, font_size=32)
        curve_label.next_to(axes, UP, buff=0.15).align_to(axes, LEFT).shift(RIGHT * 0.2)

        asymp = DashedLine(
            start=axes.c2p(340, 0), end=axes.c2p(340, 1500),
            color=PRIMARY, stroke_width=3, dash_length=0.12,
        )
        asymp_tag = Text("sound-speed limit v=343 m/s", color=PRIMARY, font_size=20)
        asymp_tag.next_to(axes.c2p(340, 1500), UP, buff=0.15).align_to(axes.c2p(340, 1500), LEFT).shift(LEFT * 0.2)

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
        marker_label = Text("current van: 530.6 Hz", color=ACCENT, font_size=22).next_to(marker, UR, buff=0.15)

        # Bottom readout as second live updater (kept; brief and essential recap)
        bottom_readout = always_redraw(
            lambda: DecimalNumber(doppler(vs_tracker.get_value(), f0_val, v_sound),
                                  num_decimal_places=0, color=ACCENT, font_size=30)
            .move_to(DOWN * 3.2 + LEFT * 4.0)
        )
        bottom_hz = Text("Hz", color=ACCENT, font_size=22).next_to(DOWN * 3.2 + LEFT * 3.1, buff=0)
        bottom_caption = Text("f'", color=WHITE, font_size=22).next_to(DOWN * 3.2 + LEFT * 4.8, buff=0)

        # Combine: guideline + marker + labels + readouts in one play
        self.play(
            Create(guideline), FadeIn(marker, scale=1.4),
            FadeIn(marker_label),
            FadeIn(bottom_caption), FadeIn(bottom_hz), FadeIn(bottom_readout),
            run_time=1.0,
        )
        # tracker animates AFTER readouts are visible
        self.play(vs_tracker.animate.set_value(20.0), run_time=1.4, rate_func=linear)
        self.wait(1.6)

        # ------------------------------------------------------------------
        # BEAT A3.B2 | 15.00-19.00 s
        # ------------------------------------------------------------------
        sweeps = [
            (100, 588.0, 1.0, 0.5),
            (200, 714.0, 1.0, 0.4),
            (300, 1150.0, 1.0, 0.3),
        ]
        prev_x = 20.0
        for vs_target, hz_text, run_t, tracker_t in sweeps:
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
            prev_x = vs_target
        self.wait(1.0)

        # ------------------------------------------------------------------
        # BEAT A4.B1 | 19.00-23.12 s
        # ------------------------------------------------------------------
        hero_x, hero_y = 20.0, doppler(20.0, f0_val, v_sound)
        hero_label = Text("vs=20 m/s, f'=530.6 Hz", color=ACCENT, font_size=24).next_to(
            axes.c2p(hero_x, hero_y), UR, buff=0.18)

        glow = DashedLine(
            start=axes.c2p(343, 0), end=axes.c2p(343, 1500),
            color=PRIMARY, stroke_width=5, dash_length=0.1,
        )
        inf_tag = Text("approaches infinity", color=PRIMARY, font_size=24).next_to(
            axes.c2p(343, 1300), RIGHT, buff=0.1)

        hero_strip = Rectangle(width=14.0, height=0.4, stroke_width=0,
                               fill_color="#2C3E50", fill_opacity=1.0).to_edge(DOWN, buff=0.05)
        hero_dash = DashedLine(start=hero_strip.get_left(), end=hero_strip.get_right(),
                               dash_length=0.2, color=WHITE, stroke_width=2).move_to(hero_strip)
        hero_van = VGroup(
            RoundedRectangle(width=0.45, height=0.22, corner_radius=0.04,
                             color=PRIMARY, fill_opacity=1, stroke_color=PRIMARY),
            Circle(radius=0.05, color=BLACK, fill_opacity=1).shift(LEFT * 0.15 + DOWN * 0.12),
            Circle(radius=0.05, color=BLACK, fill_opacity=1).shift(RIGHT * 0.15 + DOWN * 0.12),
        ).move_to(hero_strip.get_center() + LEFT * 4.0)
        hero_mic = VGroup(
            Circle(radius=0.08, color=WHITE, fill_opacity=1),
            Line(UP * 0.08, DOWN * 0.14, color=WHITE, stroke_width=2),
        ).scale(0.6).move_to(hero_strip.get_left() + RIGHT * 1.0)
        side_caption = MathTex("f' = \\frac{f_0\\, v}{v - v_s}", color=WHITE, font_size=30).to_corner(UL, buff=0.5)

        # Combined hero play
        self.play(
            FadeOut(VGroup(marker_label, bottom_caption, bottom_hz, bottom_readout)),
            marker.animate.move_to(axes.c2p(hero_x, hero_y)),
            guideline.animate.put_start_and_end_on(axes.c2p(hero_x, 0), axes.c2p(hero_x, hero_y)),
            FadeIn(hero_label),
            Transform(asymp, glow), FadeIn(inf_tag),
            FadeIn(hero_strip), FadeIn(hero_dash), FadeIn(hero_van), FadeIn(hero_mic),
            FadeIn(side_caption),
            run_time=1.4,
        )
        self.wait(2.72)

        # ------------------------------------------------------------------
        # BEAT A4.B2 | 23.12-26.00 s
        # ------------------------------------------------------------------
        shock_van = hero_van.copy().move_to(hero_strip.get_right() + LEFT * 0.5)
        flash = Circle(radius=0.5, color=ACCENT, fill_opacity=0.8, stroke_width=0).move_to(shock_van)
        micro_ribbon = VGroup(*[
            Line(LEFT * 0.04, RIGHT * 0.04, color=PRIMARY, stroke_width=2)
            .shift(RIGHT * i * 0.05).move_to(shock_van.get_left() + LEFT * 0.1 + UP * 0.15)
            for i in range(6)
        ])
        spike = DecimalNumber(9999, color=PRIMARY, font_size=30).move_to(UP * 2.5 + RIGHT * 3.0)
        spike_lbl = Text("clipped", color=PRIMARY, font_size=22).next_to(spike, DOWN, buff=0.1)

        self.play(
            Transform(hero_van, shock_van),
            Flash(flash, color=ACCENT, flash_radius=0.8, line_length=0.25, num_lines=14),
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
        recap_mic = VGroup(
            Circle(radius=0.12, color=WHITE, fill_opacity=1),
            Line(UP * 0.12, DOWN * 0.28, color=WHITE, stroke_width=2),
            Line(LEFT * 0.12, RIGHT * 0.12, color=WHITE, stroke_width=2).shift(DOWN * 0.28),
        ).scale(0.7).move_to(DOWN * 2.6 + LEFT * 5.5)
        recap_caption = Text("stationary observer", color=WHITE, font_size=22).next_to(recap_mic, DOWN, buff=0.15)
        recap_eq = MathTex("f' = \\frac{f_0\\, v}{v - v_s}", color=WHITE, font_size=44).move_to(UP * 1.0)
        vs_label = Text("v_s = 20 m/s", color=ACCENT, font_size=26).move_to(DOWN * 2.6 + RIGHT * 1.5)

        # pre-build breathing curve points ONCE (no per-frame rebuild)
        breath_phases = [0.0, 0.25, 0.5, 0.75]
        breath_curves = VGroup(*[
            axes.plot(
                lambda x, ph=ph: doppler(min(x, 342.0), f0_val, v_sound) * (1.0 + 0.01 * math.sin(2 * math.pi * ph / 2.0)),
                x_range=[0, 340], color=SECONDARY, stroke_width=4,
            )
            for ph in breath_phases
        ])
        original_curve = breath_curves[0]
        original_curve_pts = original_curve.get_points().copy()

        self.play(
            FadeOut(VGroup(hero_label, inf_tag, hero_van, side_caption)),
            FadeIn(recap_mic), FadeIn(recap_caption),
            FadeIn(recap_eq), FadeIn(vs_label),
            run_time=0.7,
        )

        # Single updater: breathe the curve via pre-built point sets (Transform-style swap)
        breathe_t = ValueTracker(0.0)
        idx_tracker = [0]

        def pick_curve():
            t = breathe_t.get_value()
            i = int((math.sin(2 * math.pi * t / 2.0) + 1.0) * 1.5) % 4
            if i != idx_tracker[0]:
                idx_tracker[0] = i
                return breath_curves[i]
            return None

        # Use a lightweight updater that simply nudges opacity of overlay sets
        overlays = [c for c in breath_curves]
        for i, ov in enumerate(overlays):
            if i != 0:
                ov.set_opacity(0.0)
                self.add(ov)

        def breathe(m, dt):
            breathe_t.increment_value(dt)
            phase = (math.sin(2 * math.pi * breathe_t.get_value() / 2.0) + 1.0) * 0.5
            target_idx = int(phase * 3 + 0.5)
            for i, ov in enumerate(overlays):
                if i == target_idx:
                    target = 1.0 - abs(phase - (i / 3.0)) * 3.0
                    ov.set_opacity(max(0.0, min(1.0, target)))
                else:
                    ov.set_opacity(0.0)

        curve.add_updater(breathe)

        # Pulse marker radius (second live updater)
        pulse_t = ValueTracker(0.0)
        marker.set_z_index(2)
        marker.add_updater(lambda m, dt: (
            m.set_radius(0.10 + 0.02 * math.sin(2 * math.pi * pulse_t.get_value())),
            pulse_t.increment_value(dt),
        ))

        self.wait(3.3)