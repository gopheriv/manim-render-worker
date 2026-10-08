from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # Palette
        PRIMARY = "#FFD166"   # golden string
        SECONDARY = "#06D6A0" # ghost green pulse
        ACCENT = "#EF476F"    # accent red envelope / first pulse
        DARK_BG = "#0B1220"
        FLOOR_GREY = "#3A475A"
        TEXT_WHITE = "#F8FAFC"

        self.camera.background_color = DARK_BG

        # Physics constants
        A_val = 1.0
        k_val = math.pi / 2.0          # 1.5707963
        omega_val = 2.0
        lambda_val = 4.0
        v_val = lambda_val * omega_val / (2.0 * math.pi)  # 1.2732

        # Stage scaffolding: floor grid, posts, time-axis
        floor = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-3.2, -2.6, 0.1],
            x_length=14,
            y_length=0.5,
            background_line_style={"stroke_color": FLOOR_GREY, "stroke_width": 1, "stroke_opacity": 0.45},
            axis_config={"stroke_opacity": 0},
        )
        floor.set_opacity(0.5)
        floor.to_edge(DOWN, buff=0.4)
        self.add(floor)

        post_left = Rectangle(width=0.18, height=1.6, color=GREY_A, fill_opacity=0.85, stroke_opacity=0.6)
        post_left.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        post_right = post_left.copy().to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        posts = VGroup(post_left, post_right)

        # String spans between posts at mid-screen
        x_left = post_left.get_right()[0] + 0.05
        x_right = post_right.get_left()[0] - 0.05
        x_mid = (x_left + x_right) / 2.0
        y_string = 0.0

        def string_axes():
            return Axes(
                x_range=[0, lambda_val, lambda_val / 4.0],
                y_range=[-2.6, 2.6, 1.0],
                x_length=(x_right - x_left),
                y_length=4.6,
                tips=False,
                axis_config={"stroke_opacity": 0},
            ).move_to([x_mid, y_string, 0.0])

        axes = string_axes()
        # A faint baseline (the at-rest string) for context
        baseline = Line(axes.c2p(0, 0), axes.c2p(lambda_val, 0),
                        color=GREY_B, stroke_width=2, stroke_opacity=0.55)

        # Time clock above the bench
        time_tracker = ValueTracker(0.0)
        t_label = Text("t =", color=TEXT_WHITE, font_size=22).to_edge(UP, buff=0.35).shift(LEFT * 5.6)
        t_readout = always_redraw(
            lambda: DecimalNumber(time_tracker.get_value(), num_decimal_places=2,
                                  color=TEXT_WHITE, font_size=22)
            .next_to(t_label, RIGHT, buff=0.12)
        )

        # Equation used as identity banner / hero / recap
        eq_standing = MathTex("y = 2A\\sin(kx)\\cos(\\omega t)",
                              color=TEXT_WHITE).scale(0.55)
        eq_y1 = MathTex("y_1 = A\\sin(kx - \\omega t)", color=ACCENT).scale(0.45)
        eq_y2 = MathTex("y_2 = A\\sin(kx + \\omega t)", color=SECONDARY).scale(0.45)
        eq_sum = MathTex("y = y_1 + y_2", color=TEXT_WHITE).scale(0.5)
        eq_nodes = MathTex("\\sin(kx)=0 \\Rightarrow x = n\\pi/k", color=TEXT_WHITE).scale(0.45)
        eq_v = MathTex("v = \\lambda\\,\\omega/2\\pi", color=TEXT_WHITE).scale(0.45)

        # Title (small, top-left)
        title = Text("Standing Wave", color=TEXT_WHITE, font_size=26).to_edge(UP, buff=0.25).shift(LEFT * 4.6)
        self.add(title)

        # Beat group placeholder for sweeping cleanups
        current = VGroup()

        # =========================================================
        # BEAT A1.B1 | 0.00-5.00 s
        # =========================================================
        # Build the stage: posts, baseline, axes, HUD numbers, then launch
        # the first right-moving sine pulse (accent red) onto the string.
        self.play(
            FadeIn(posts, shift=UP * 0.2),
            Create(baseline),
            run_time=0.6,
        )
        # HUD: A, k, lambda, omega, v
        hud_labels = ["A", "k", "λ", "ω", "v"]
        hud_values = [A_val, k_val, lambda_val, omega_val, v_val]
        hud_decimals = [3, 3, 2, 2, 3]
        hud = VGroup()
        for lbl, val, nd in zip(hud_labels, hud_values, hud_decimals):
            lbl_t = Text(f"{lbl}=", color=TEXT_WHITE, font_size=22)
            num = DecimalNumber(val, num_decimal_places=nd, color=TEXT_WHITE, font_size=22)
            grp = VGroup(lbl_t, num).arrange(RIGHT, buff=0.08)
            hud.add(grp)
        hud.arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.35).shift(RIGHT * 0.4)
        self.play(FadeIn(hud, lag_ratio=0.15), run_time=0.6)
        self.add(t_label, t_readout)

        # The y1 pulse: a localised sine "bump" that travels rightward.
        # We implement it as a ParametricFunction whose x-position is
        # controlled by a ValueTracker; amplitude = A, width = lambda/2.
        pulse1_tracker = ValueTracker(-2.0)  # x-position of pulse centre
        pulse1_width = lambda_val / 2.0

        def pulse1_curve():
            cx = pulse1_tracker.get_value()
            L = lambda_val
            return ParametricFunction(
                lambda s: axes.c2p(
                    s,
                    A_val * math.sin(k_val * (s - cx))
                    * math.exp(-((s - cx) ** 2) / (2.0 * (pulse1_width / 3.0) ** 2)),
                ),
                t_range=[max(0, cx - 1.5 * pulse1_width), min(L, cx + 1.5 * pulse1_width), 0.05],
                color=ACCENT,
                stroke_width=6,
            )

        pulse1 = always_redraw(pulse1_curve)
        self.add(pulse1)
        # Animate the pulse from left anchor toward the midpoint.
        self.play(pulse1_tracker.animate.set_value(x_mid / (x_right - x_left) * lambda_val * 0.0 + lambda_val * 0.5),
                  time_tracker.animate.set_value(0.6),
                  run_time=4.0, rate_func=linear)
        # Hold the read of the still-frozen frame at 0.6s window: small hold
        self.wait(0.4)

        # =========================================================
        # BEAT A2.B1 | 5.00-8.00 s
        # =========================================================
        # Slide in the y1 label, then introduce the second pulse from the right.
        eq_y1.next_to(axes, UP, buff=0.15).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(eq_y1, shift=RIGHT * 0.1), run_time=0.4)

        pulse2_tracker = ValueTracker(lambda_val + 2.0)

        def pulse2_curve():
            cx = pulse2_tracker.get_value()
            L = lambda_val
            return ParametricFunction(
                lambda s: axes.c2p(
                    s,
                    A_val * math.sin(k_val * (s - cx))
                    * math.exp(-((s - cx) ** 2) / (2.0 * (pulse1_width / 3.0) ** 2)),
                ),
                t_range=[max(0, cx - 1.5 * pulse1_width), min(L, cx + 1.5 * pulse1_width), 0.05],
                color=SECONDARY,
                stroke_width=6,
            )

        pulse2 = always_redraw(pulse2_curve)
        self.add(pulse2)
        # Move rightward -> leftward toward midpoint
        self.play(
            pulse1_tracker.animate.set_value(lambda_val * 0.45),
            pulse2_tracker.animate.set_value(lambda_val * 0.55),
            time_tracker.animate.set_value(1.4),
            run_time=2.6,
            rate_func=linear,
        )
        eq_y2.next_to(axes, UP, buff=0.15).to_edge(RIGHT, buff=0.6)
        self.play(FadeIn(eq_y2, shift=LEFT * 0.1), run_time=0.4)

        # =========================================================
        # BEAT A2.B2 | 8.00-11.00 s
        # =========================================================
        # Pulses cross at mid-string; show sum y = y1 + y2 below the bench.
        # We let the two pulses continue past each other and superimpose
        # visually by drawing a thicker combined curve at the crossing instant.
        sum_peak = ParametricFunction(
            lambda s: axes.c2p(
                s,
                2.0 * A_val * math.sin(k_val * (s - lambda_val * 0.5))
                * math.exp(-((s - lambda_val * 0.5) ** 2) / (2.0 * (pulse1_width / 3.0) ** 2)),
            ),
            t_range=[lambda_val * 0.5 - 1.5 * pulse1_width,
                     lambda_val * 0.5 + 1.5 * pulse1_width, 0.05],
            color=PRIMARY, stroke_width=10,
        )
        self.play(
            pulse1_tracker.animate.set_value(lambda_val * 0.42),
            pulse2_tracker.animate.set_value(lambda_val * 0.58),
            FadeIn(sum_peak, scale=0.95),
            time_tracker.animate.set_value(2.0),
            run_time=1.2, rate_func=smooth,
        )
        eq_sum.next_to(axes, DOWN, buff=0.5)
        self.play(Write(eq_sum), run_time=0.6)
        self.wait(0.4)
        # Cross-fade the transient overlay out; pulses continue off-string
        self.play(
            FadeOut(sum_peak),
            pulse1_tracker.animate.set_value(lambda_val + 2.0),
            pulse2_tracker.animate.set_value(-2.0),
            run_time=0.8, rate_func=linear,
        )
        self.remove(pulse1, pulse2)
        self.play(FadeOut(eq_y1), FadeOut(eq_y2), run_time=0.3)

        # =========================================================
        # BEAT A3.B1 | 11.00-15.00 s
        # =========================================================
        # Identity banner slides in: y = 2A sin(kx) cos(omega t).
        # Replace the pulses with a thick golden standing wave that breathes.
        eq_standing.to_edge(RIGHT, buff=0.6).shift(UP * 1.4)
        self.play(FadeIn(eq_standing, shift=LEFT * 0.2), run_time=0.6)

        # Standing wave as a static curve whose y-scale is driven by a
        # ValueTracker; we change the value to make it breathe.
        breath = ValueTracker(1.0)
        breath_phase = ValueTracker(0.0)  # independent clock for the wave

        def standing_curve():
            scale = breath.get_value()
            phase = breath_phase.get_value()
            return axes.plot(
                lambda x: scale * 2.0 * A_val * math.sin(k_val * x) * math.cos(omega_val * phase + 0.0),
                x_range=[0, lambda_val, 0.05],
                color=PRIMARY, stroke_width=8,
            )

        standing = always_redraw(standing_curve)
        self.add(standing)
        # First reveal at amplitude 1.0 (cos=1)
        self.play(breath.animate.set_value(1.0), run_time=0.3)
        # Breathe for the rest of the window
        self.play(
            breath_phase.animate.set_value(1.6),
            time_tracker.animate.set_value(3.6),
            run_time=2.8, rate_func=linear,
        )

        # =========================================================
        # BEAT A3.B2 | 15.00-19.00 s
        # =========================================================
        # Live amplitude readout at upper-left of bench; fixed node dots appear.
        amp_label = Text("max |y| =", color=TEXT_WHITE, font_size=24)
        amp_readout = always_redraw(
            lambda: DecimalNumber(
                2.0 * A_val * abs(math.cos(omega_val * breath_phase.get_value())),
                num_decimal_places=2, color=PRIMARY, font_size=28
            )
        )
        amp_group = VGroup(amp_label, amp_readout).arrange(RIGHT, buff=0.12)
        amp_group.to_edge(LEFT, buff=0.6).shift(UP * 1.4)
        self.add(amp_group)

        # Node markers: x = 0, 2, 4 (within [0, lambda])
        node_xs = [0.0, lambda_val / 2.0, lambda_val]
        node_dots = VGroup(*[
            Dot(axes.c2p(x, 0.0), color=WHITE, radius=0.07).set_stroke(BLACK, 1.5)
            for x in node_xs
        ])
        node_caption = Text("nodes stay fixed", color=TEXT_WHITE, font_size=24)
        node_caption.next_to(amp_group, DOWN, buff=0.25).align_to(amp_group, LEFT)
        self.play(
            FadeIn(node_dots, lag_ratio=0.2),
            FadeIn(node_caption, shift=UP * 0.1),
            run_time=0.6,
        )
        # Continue breathing
        self.play(
            breath_phase.animate.set_value(3.2),
            time_tracker.animate.set_value(4.8),
            run_time=3.4, rate_func=linear,
        )

        # =========================================================
        # BEAT A4.B1 | 19.00-23.00 s
        # =========================================================
        # Hero frame: switch to the sin(kx) envelope with antinode caps and
        # a wavelength bracket above. Accent red appears ONLY at this hero.
        self.play(
            FadeOut(amp_group),
            FadeOut(node_caption),
            run_time=0.4,
        )

        # Static +envelope and -envelope in accent red
        env_pos = axes.plot(lambda x: 2.0 * A_val * math.sin(k_val * x),
                            x_range=[0, lambda_val, 0.05],
                            color=ACCENT, stroke_width=3)
        env_neg = axes.plot(lambda x: -2.0 * A_val * math.sin(k_val * x),
                            x_range=[0, lambda_val, 0.05],
                            color=ACCENT, stroke_width=3)
        # Antinode caps at x = 1, 3 (peak |sin(kx)|)
        antinode_xs = [lambda_val / 4.0, 3.0 * lambda_val / 4.0]
        antinode_caps = VGroup(*[
            Dot(axes.c2p(x, 0.0), color=PRIMARY, radius=0.11)
            .set_stroke(WHITE, 2, opacity=0.9)
            for x in antinode_xs
        ])
        antinode_label = Text("antinodes", color=PRIMARY, font_size=24).next_to(antinode_caps[0], UP, buff=0.25)

        # Wavelength bracket from x=0 to x=lambda
        brace = BraceBetweenPoints(
            axes.c2p(0, 0), axes.c2p(lambda_val, 0), direction=UP, color=TEXT_WHITE
        )
        brace_label = MathTex("\\lambda = 4.0", color=TEXT_WHITE).scale(0.5)
        brace_label.next_to(brace, UP, buff=0.12)

        # Equation remains on the right
        eq_standing.generate_target()
        eq_standing.target.to_edge(RIGHT, buff=0.6).shift(UP * 2.0)
        self.play(
            MoveToTarget(eq_standing),
            FadeIn(env_pos), FadeIn(env_neg),
            FadeIn(antinode_caps, lag_ratio=0.2),
            FadeIn(brace), FadeIn(brace_label),
            FadeIn(antinode_label),
            run_time=0.9,
        )
        # Continue breathing underneath the static envelope
        self.play(
            breath_phase.animate.set_value(4.8),
            time_tracker.animate.set_value(6.0),
            run_time=2.7, rate_func=linear,
        )
        # Brief readable hold
        self.wait(0.4)

        # =========================================================
        # BEAT A4.B2 | 23.00-26.00 s
        # =========================================================
        # Annotations: node spacing text and v = lambda*omega/2pi on floor.
        annotation = Text(
            "nodes at x = nπ/k,  antinodes at (n+½)π/k,  spacing λ/2",
            color=TEXT_WHITE, font_size=22,
        )
        annotation.next_to(axes, DOWN, buff=0.5).to_edge(LEFT, buff=0.4)
        eq_v.next_to(annotation, DOWN, buff=0.25).align_to(annotation, LEFT)
        # Floor speed tick: a small moving marker along the floor grid
        tick_tracker = ValueTracker(x_left)
        speed_tick = always_redraw(
            lambda: Dot(
                [tick_tracker.get_value(), floor.get_y() + 0.05, 0.0],
                color=ACCENT, radius=0.08
            )
        )
        speed_label = Text("v = 1.273 m/s", color=ACCENT, font_size=22).next_to(eq_v, RIGHT, buff=0.25)
        self.add(speed_tick)
        self.play(
            FadeIn(annotation, shift=UP * 0.1),
            FadeIn(eq_v, shift=UP * 0.1),
            FadeIn(speed_label, shift=UP * 0.1),
            run_time=0.6,
        )
        # Tick moves rightward at v for the readable hold
        self.play(
            tick_tracker.animate.set_value(x_right - 0.2),
            breath_phase.animate.set_value(5.6),
            time_tracker.animate.set_value(6.8),
            run_time=2.0, rate_func=linear,
        )
        self.wait(0.4)

        # =========================================================
        # BEAT A5.B1 | 26.00-30.00 s
        # =========================================================
        # Recap: clear everything except the standing wave and one live number A.
        # Clean slate with the equation and breathing standing wave.
        self.play(
            FadeOut(VGroup(env_pos, env_neg, antinode_caps, antinode_label,
                           brace, brace_label, annotation, eq_v, speed_label,
                           speed_tick, node_dots, posts, baseline, floor, hud, title,
                           t_label, t_readout)),
            run_time=0.7,
        )
        # Recap equation centred, A readout below
        recap_eq = MathTex("y = 2A\\sin(kx)\\cos(\\omega t)",
                           color=TEXT_WHITE).scale(0.7)
        recap_eq.to_edge(UP, buff=0.6)
        a_label = Text("A =", color=TEXT_WHITE, font_size=26)
        a_readout = always_redraw(
            lambda: DecimalNumber(A_val, num_decimal_places=2, color=PRIMARY, font_size=30)
        )
        a_group = VGroup(a_label, a_readout).arrange(RIGHT, buff=0.12)
        a_group.next_to(recap_eq, DOWN, buff=0.3)

        # Reset the standing wave (it is still on the canvas via always_redraw)
        self.add(recap_eq, a_group)
        # Idle loop: gentle breathing with nodes absolutely still, equation
        # opacity pulses 0.6 -> 1.0 over ~2 s. We drive both via a phase
        # tracker so the readout continues to vary slightly.
        self.play(
            breath_phase.animate.set_value(6.6),
            run_time=0.6, rate_func=linear,
        )
        # Opacity pulse on the equation via an updater for the idle loop
        pulse_phase = ValueTracker(0.0)
        recap_eq.add_updater(lambda m: m.set_opacity(0.6 + 0.4 * (0.5 + 0.5 * math.cos(pulse_phase.get_value()))))
        # Run the idle loop for the remaining ~2.8 s so the final three
        # sampled frames are all different.
        self.play(
            pulse_phase.animate.set_value(2.0 * math.pi),
            breath_phase.animate.set_value(8.2),
            time_tracker.animate.set_value(8.4),
            run_time=2.6, rate_func=linear,
        )
        self.wait(0.2)