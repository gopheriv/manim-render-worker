from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
            # Palette
            PRIMARY = "#FFD166"   # golden string / standing wave
            SECONDARY = "#06D6A0" # ghost green pulse (right-moving in act 2)
            ACCENT = "#EF476F"    # accent red pulse (left-moving in act 2)
            DARK_BG = "#0B1220"
            FLOOR_GREY = "#3A475A"
            TEXT_WHITE = "#F8FAFC"
            DIM_WHITE = "#CBD5E1"
            GREY_A = "#3A475A"
            GREY_B = "#94A3B8"

            self.camera.background_color = DARK_BG

            # Physics constants
            A_val = 1.0
            k_val = math.pi / 2.0
            omega_val = 2.0
            lambda_val = 4.0
            v_val = lambda_val * omega_val / (2.0 * math.pi)

            # Stage: floor grid + anchor posts placed in upper-middle band so
            # the composition occupies multiple vertical rows (R1-R6) rather
            # than collapsing everything to R4.
            floor = NumberPlane(
                x_range=[-7, 7, 1],
                y_range=[-2.9, -2.4, 0.1],
                x_length=14,
                y_length=0.45,
                background_line_style={"stroke_color": FLOOR_GREY, "stroke_width": 1, "stroke_opacity": 0.5},
                axis_config={"stroke_opacity": 0},
            )
            floor.set_opacity(0.55)
            floor.to_edge(DOWN, buff=0.35)
            self.add(floor)

            # String sits in the upper band so the lower band hosts text annotations.
            string_y = 1.2
            post_left = Rectangle(width=0.16, height=2.0, color=GREY_A,
                                  fill_opacity=0.9, stroke_opacity=0.6)
            post_right = post_left.copy()
            post_left.move_to([-5.6, string_y - 0.3, 0.0])
            post_right.move_to([5.6, string_y - 0.3, 0.0])
            posts = VGroup(post_left, post_right)

            x_left = post_left.get_right()[0] + 0.05
            x_right = post_right.get_left()[0] - 0.05
            x_mid = (x_left + x_right) / 2.0

            # Local axes that span the string, in physics units [0, lambda] x [-A, A].
            axes = Axes(
                x_range=[0, lambda_val, lambda_val / 4.0],
                y_range=[-2.0, 2.0, 1.0],
                x_length=(x_right - x_left),
                y_length=3.4,
                tips=False,
                axis_config={"stroke_opacity": 0},
            ).move_to([x_mid, string_y, 0.0])

            baseline = Line(axes.c2p(0, 0), axes.c2p(lambda_val, 0),
                            color=GREY_B, stroke_width=2, stroke_opacity=0.6)

            # HUD parameter strip — bold, bright, easy to read on dark bg
            hud = VGroup()
            for lbl in ["A=1.000", "k=1.571", "λ=4.00", "ω=2.00", "v=1.273"]:
                t = Text(lbl, color=TEXT_WHITE, font_size=22, weight=BOLD)
                hud.add(t)
            hud.arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.3)
            # Backplate for the HUD so the white-on-dark always has contrast
            hud_back = Rectangle(
                width=hud.width + 0.6, height=hud.height + 0.25,
                stroke_opacity=0, fill_color="#111B2E", fill_opacity=0.85
            ).move_to(hud.get_center())
            self.add(hud_back, hud)

            # Time readout
            time_tracker = ValueTracker(0.0)
            t_label = Text("t =", color=TEXT_WHITE, font_size=22, weight=BOLD)
            t_readout = always_redraw(
                lambda: DecimalNumber(time_tracker.get_value(), num_decimal_places=2,
                                      color=TEXT_WHITE, font_size=22)
                .next_to(t_label, RIGHT, buff=0.12)
            )
            t_group = VGroup(t_label, t_readout).arrange(RIGHT, buff=0.12)
            t_group.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.5)
            # Fade in t_group in its own play BEFORE any ValueTracker animations
            # that change the readout's digit count, to avoid unequal zip lengths
            # inside Animation.interpolate_mobject.
            self.add(t_group)

            # Title (top-left, separate from HUD strip so it doesn't compete)
            title = Text("Standing Wave", color=TEXT_WHITE, font_size=30, weight=BOLD)
            title.to_edge(LEFT, buff=0.5).shift(DOWN * 0.55 + LEFT * 0.0)
            # Actually position under the HUD on the left
            title.next_to(hud, DOWN, buff=0.35).align_to(hud, LEFT)
            self.add(title)

            # =========================================================
            # ACT 1 — HOOK: a localized right-moving sine pulse
            # =========================================================
            # Build the stage pieces
            self.play(
                FadeIn(posts, shift=UP * 0.15),
                Create(baseline),
                run_time=0.5,
            )

            # The pulse: a localized bump of width ~lambda/2 traveling along x.
            # x is the pulse centre in physics units (string spans [0, lambda]).
            pulse1_tracker = ValueTracker(-1.2)  # start off-string to the left
            pulse_width = lambda_val / 2.0

            def pulse1_curve():
                cx = pulse1_tracker.get_value()
                L = lambda_val
                sigma = pulse_width / 2.4
                lo = max(0.0, cx - 1.4 * pulse_width)
                hi = min(L, cx + 1.4 * pulse_width)
                if hi <= lo:
                    hi = lo + 0.01
                return ParametricFunction(
                    lambda s: axes.c2p(
                        s,
                        A_val * math.sin(k_val * (s - cx))
                        * math.exp(-((s - cx) ** 2) / (2.0 * sigma ** 2)),
                    ),
                    t_range=[lo, hi, 0.04],
                    color=ACCENT,
                    stroke_width=7,
                )

            pulse1 = always_redraw(pulse1_curve)
            self.add(pulse1)

            # Narration caption underneath the bench
            caption1 = Text(
                "right-moving sine pulse on the string",
                color=ACCENT, font_size=24, weight=BOLD,
            )
            caption1.to_edge(DOWN, buff=0.9).shift(LEFT * 0.3)
            self.play(FadeIn(caption1, shift=UP * 0.1), run_time=0.4)

            # Animate pulse from off-left, ONTO the string, traveling to mid.
            self.play(
                pulse1_tracker.animate.set_value(lambda_val * 0.5),
                time_tracker.animate.set_value(0.8),
                run_time=4.0, rate_func=linear,
            )
            # Hold at mid-string so the bump is clearly visible
            self.wait(0.4)

            # =========================================================
            # ACT 2 — A second pulse from the right meets the first
            # =========================================================
            # Right-moving (green) pulse incoming from the right.
            pulse2_tracker = ValueTracker(lambda_val + 1.2)

            def pulse2_curve():
                cx = pulse2_tracker.get_value()
                L = lambda_val
                sigma = pulse_width / 2.4
                lo = max(0.0, cx - 1.4 * pulse_width)
                hi = min(L, cx + 1.4 * pulse_width)
                if hi <= lo:
                    hi = lo + 0.01
                return ParametricFunction(
                    lambda s: axes.c2p(
                        s,
                        A_val * math.sin(k_val * (s - cx))
                        * math.exp(-((s - cx) ** 2) / (2.0 * sigma ** 2)),
                    ),
                    t_range=[lo, hi, 0.04],
                    color=SECONDARY,
                    stroke_width=7,
                )

            pulse2 = always_redraw(pulse2_curve)
            self.add(pulse2)

            # Update caption
            self.play(
                FadeOut(caption1),
                FadeIn(Text(
                    "two counter-propagating pulses about to meet",
                    color=TEXT_WHITE, font_size=24, weight=BOLD,
                ).to_edge(DOWN, buff=0.9).shift(LEFT * 0.3), shift=UP * 0.1),
                run_time=0.4,
            )

            # Drive both pulses toward the center — pulse1 slightly left of mid,
            # pulse2 slightly right of mid, so they visibly approach each other.
            self.play(
                pulse1_tracker.animate.set_value(lambda_val * 0.46),
                pulse2_tracker.animate.set_value(lambda_val * 0.54),
                time_tracker.animate.set_value(1.6),
                run_time=2.4, rate_func=linear,
            )

            # Crossing moment: superimpose the sum curve in PRIMARY (golden)
            sum_peak = ParametricFunction(
                lambda s: axes.c2p(
                    s,
                    2.0 * A_val * math.sin(k_val * (s - lambda_val * 0.5))
                    * math.exp(-((s - lambda_val * 0.5) ** 2) / (2.0 * (pulse_width / 2.4) ** 2)),
                ),
                t_range=[lambda_val * 0.5 - 1.4 * pulse_width,
                         lambda_val * 0.5 + 1.4 * pulse_width, 0.04],
                color=PRIMARY, stroke_width=11,
            )
            self.play(
                FadeIn(sum_peak, scale=0.9),
                time_tracker.animate.set_value(2.0),
                run_time=0.4,
            )
            # Brief readable hold on the crossing
            self.wait(0.4)

            # Pulses continue past each other, ghosts fade out gracefully.
            self.play(
                pulse1_tracker.animate.set_value(lambda_val + 1.2),
                pulse2_tracker.animate.set_value(-1.2),
                FadeOut(sum_peak),
                time_tracker.animate.set_value(2.6),
                run_time=1.2, rate_func=linear,
            )
            self.remove(pulse1, pulse2)

            # =========================================================
            # ACT 3 — Standing wave reveals and breathes
            # =========================================================
            # Clear the bottom caption before the standing wave reveal.
            # Use Group (not VGroup) so non-VMobject submobjects (ValueTrackers,
            # updater-controlled mobjects) are accepted without TypeError.
            self.play(
                FadeOut(Group(*self.mobjects)),
                run_time=0.0001,
            )
            # Rebuild a clean stage for acts 3-4
            self.camera.background_color = DARK_BG
            floor = NumberPlane(
                x_range=[-7, 7, 1],
                y_range=[-2.9, -2.4, 0.1],
                x_length=14, y_length=0.45,
                background_line_style={"stroke_color": FLOOR_GREY, "stroke_width": 1, "stroke_opacity": 0.5},
                axis_config={"stroke_opacity": 0},
            )
            floor.set_opacity(0.55).to_edge(DOWN, buff=0.35)
            self.add(floor)
            post_left = Rectangle(width=0.16, height=2.0, color=GREY_A, fill_opacity=0.9, stroke_opacity=0.6)
            post_right = post_left.copy()
            post_left.move_to([-5.6, string_y - 0.3, 0.0])
            post_right.move_to([5.6, string_y - 0.3, 0.0])
            posts = VGroup(post_left, post_right)
            x_left = post_left.get_right()[0] + 0.05
            x_right = post_right.get_left()[0] - 0.05
            x_mid = (x_left + x_right) / 2.0
            axes = Axes(
                x_range=[0, lambda_val, lambda_val / 4.0],
                y_range=[-2.0, 2.0, 1.0],
                x_length=(x_right - x_left),
                y_length=3.4,
                tips=False,
                axis_config={"stroke_opacity": 0},
            ).move_to([x_mid, string_y, 0.0])
            baseline = Line(axes.c2p(0, 0), axes.c2p(lambda_val, 0),
                            color=GREY_B, stroke_width=2, stroke_opacity=0.6)
            self.add(posts, baseline)

            # HUD rebuild
            hud = VGroup()
            for lbl in ["A=1.000", "k=1.571", "λ=4.00", "ω=2.00", "v=1.273"]:
                hud.add(Text(lbl, color=TEXT_WHITE, font_size=22, weight=BOLD))
            hud.arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.3)
            hud_back = Rectangle(
                width=hud.width + 0.6, height=hud.height + 0.25,
                stroke_opacity=0, fill_color="#111B2E", fill_opacity=0.85,
            ).move_to(hud.get_center())
            self.add(hud_back, hud)

            # Rebuild the time readout with fresh trackable references and
            # restore its visual position. We add it directly (it will be
            # redrawn by always_redraw once the tracker moves).
            time_tracker = ValueTracker(2.6)
            t_label = Text("t =", color=TEXT_WHITE, font_size=22, weight=BOLD)
            t_readout = always_redraw(
                lambda: DecimalNumber(time_tracker.get_value(), num_decimal_places=2,
                                      color=TEXT_WHITE, font_size=22)
                .next_to(t_label, RIGHT, buff=0.12)
            )
            t_group = VGroup(t_label, t_readout).arrange(RIGHT, buff=0.12)
            t_group.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.5)
            self.add(t_group)

            title = Text("Standing Wave", color=TEXT_WHITE, font_size=30, weight=BOLD)
            title.next_to(hud, DOWN, buff=0.35).align_to(hud, LEFT)
            self.add(title)

            # Standing wave equation banner
            eq_standing = MathTex("y = 2A\\sin(kx)\\cos(\\omega t)",
                                  color=TEXT_WHITE).scale(0.6)
            eq_standing.to_edge(RIGHT, buff=0.6).shift(UP * 1.5)
            self.add(eq_standing)

            # Standing wave with a "ghost" trace of the two parent pulses
            # fading out, to echo act 2 and make the transition legible.
            ghost1 = ParametricFunction(
                lambda s: axes.c2p(s, A_val * math.sin(k_val * (s - lambda_val * 0.3))
                                   * math.exp(-((s - lambda_val * 0.3) ** 2) / (2.0 * (pulse_width / 2.4) ** 2))),
                t_range=[0, lambda_val, 0.05], color=ACCENT, stroke_width=2,
            )
            ghost2 = ParametricFunction(
                lambda s: axes.c2p(s, A_val * math.sin(k_val * (s - lambda_val * 0.7))
                                   * math.exp(-((s - lambda_val * 0.7) ** 2) / (2.0 * (pulse_width / 2.4) ** 2))),
                t_range=[0, lambda_val, 0.05], color=SECONDARY, stroke_width=2,
            )

            # Breathing standing wave
            breath = ValueTracker(1.0)
            breath_phase = ValueTracker(0.0)

            def standing_curve():
                scale = breath.get_value()
                phase = breath_phase.get_value()
                return axes.plot(
                    lambda x: scale * 2.0 * A_val * math.sin(k_val * x)
                    * math.cos(omega_val * phase),
                    x_range=[0, lambda_val, 0.05],
                    color=PRIMARY, stroke_width=9,
                )

            standing = always_redraw(standing_curve)
            self.add(ghost1, ghost2, standing)

            caption3 = Text(
                "travelling waves fade  →  standing wave locks in",
                color=TEXT_WHITE, font_size=24, weight=BOLD,
            )
            caption3.to_edge(DOWN, buff=0.9)
            self.play(FadeIn(caption3, shift=UP * 0.1), run_time=0.4)
            # Ghosts fade, standing wave holds and breathes
            self.play(
                FadeOut(ghost1), FadeOut(ghost2),
                breath_phase.animate.set_value(1.6),
                time_tracker.animate.set_value(3.4),
                run_time=2.4, rate_func=linear,
            )
            self.wait(0.4)
            self.play(FadeOut(caption3), run_time=0.4)

            # =========================================================
            # ACT 4 — Annotate nodes, antinodes, wavelength
            # =========================================================
            # Node dots at x = 0, 2, 4
            node_xs = [0.0, lambda_val / 2.0, lambda_val]
            node_dots = VGroup(*[
                Dot(axes.c2p(x, 0.0), color=WHITE, radius=0.075).set_stroke(BLACK, 1.5)
                for x in node_xs
            ])
            node_label = Text("nodes (fixed)", color=TEXT_WHITE, font_size=22, weight=BOLD)
            node_label.next_to(node_dots[0], DOWN, buff=0.25)

            # Antinodes at x = 1, 3
            antinode_xs = [lambda_val / 4.0, 3.0 * lambda_val / 4.0]
            antinode_dots = VGroup(*[
                Dot(axes.c2p(x, 0.0), color=PRIMARY, radius=0.11).set_stroke(WHITE, 2, opacity=0.9)
                for x in antinode_xs
            ])
            antinode_label = Text("antinodes", color=PRIMARY, font_size=22, weight=BOLD)
            antinode_label.next_to(antinode_dots[0], UP, buff=0.25)

            # Wavelength bracket
            brace = BraceBetweenPoints(
                axes.c2p(0, 0), axes.c2p(lambda_val, 0), direction=UP, color=TEXT_WHITE,
            )
            brace_label = MathTex("\\lambda = 4.0", color=TEXT_WHITE).scale(0.55)
            brace_label.next_to(brace, UP, buff=0.12)

            self.play(
                FadeIn(node_dots, lag_ratio=0.2),
                FadeIn(node_label, shift=UP * 0.1),
                FadeIn(antinode_dots, lag_ratio=0.2),
                FadeIn(antinode_label, shift=DOWN * 0.1),
                FadeIn(brace), FadeIn(brace_label),
                run_time=0.8,
            )

            # Continue breathing with annotations in place
            self.play(
                breath_phase.animate.set_value(3.4),
                time_tracker.animate.set_value(4.6),
                run_time=2.8, rate_func=linear,
            )

            # Bottom annotation: node spacing rule, on its own row
            annotation = Text(
                "nodes at x = nπ/k,   antinodes at (n + ½)π/k,   spacing = λ/2",
                color=TEXT_WHITE, font_size=22, weight=BOLD,
            )
            annotation.to_edge(DOWN, buff=0.45)

            # Speed tick moving along the floor in accent red, with a label
            tick_tracker = ValueTracker(x_left)
            speed_tick = always_redraw(
                lambda: Dot([tick_tracker.get_value(), floor.get_y() + 0.04, 0.0],
                            color=ACCENT, radius=0.085)
            )
            speed_label = Text("v = 1.273 m/s", color=ACCENT, font_size=22, weight=BOLD)
            speed_label.next_to(node_label, RIGHT, buff=0.4)

            self.play(
                FadeIn(annotation, shift=UP * 0.1),
                FadeIn(speed_label, shift=UP * 0.1),
                run_time=0.5,
            )
            self.add(speed_tick)
            self.play(
                tick_tracker.animate.set_value(x_right - 0.15),
                breath_phase.animate.set_value(5.0),
                time_tracker.animate.set_value(5.8),
                run_time=2.4, rate_func=linear,
            )
            self.wait(0.4)

            # =========================================================
            # ACT 5 — Recap: equation + breathing wave + live A readout
            # =========================================================
            # Clear everything except floor, posts, baseline, axes, standing wave
            self.play(
                FadeOut(VGroup(node_dots, node_label, antinode_dots, antinode_label,
                               brace, brace_label, annotation, speed_label, speed_tick,
                               eq_standing, hud, hud_back, t_group, title)),
                run_time=0.6,
            )

            # Recap equation centered high
            recap_eq = MathTex("y = 2A\\sin(kx)\\cos(\\omega t)",
                               color=TEXT_WHITE).scale(0.85)
            recap_eq.to_edge(UP, buff=0.55)

            # Live A and max|y| readout (DecimalNumber does NOT accept weight=)
            a_label = Text("A =", color=TEXT_WHITE, font_size=26, weight=BOLD)
            a_readout = always_redraw(
                lambda: DecimalNumber(A_val, num_decimal_places=3,
                                      color=PRIMARY, font_size=30)
            )
            a_group = VGroup(a_label, a_readout).arrange(RIGHT, buff=0.12)
            a_group.next_to(recap_eq, DOWN, buff=0.3).align_to(recap_eq, LEFT).shift(RIGHT * 0.3)

            max_label = Text("max |y| =", color=TEXT_WHITE, font_size=26, weight=BOLD)
            max_readout = always_redraw(
                lambda: DecimalNumber(
                    2.0 * A_val * abs(math.cos(omega_val * breath_phase.get_value())),
                    num_decimal_places=3, color=PRIMARY, font_size=30,
                )
            )
            max_group = VGroup(max_label, max_readout).arrange(RIGHT, buff=0.12)
            max_group.next_to(a_group, DOWN, buff=0.25).align_to(a_group, LEFT)

            self.play(FadeIn(recap_eq, shift=DOWN * 0.1), run_time=0.5)
            self.add(a_group, max_group)

            # Recap caption at the very bottom
            recap_caption = Text(
                "standing wave: fixed nodes, oscillating antinodes",
                color=PRIMARY, font_size=24, weight=BOLD,
            )
            recap_caption.to_edge(DOWN, buff=0.45)
            self.play(FadeIn(recap_caption, shift=UP * 0.1), run_time=0.4)

            # Idle loop: keep the wave breathing and the live readouts ticking
            # so the last sampled frames are visibly different.
            self.play(
                breath_phase.animate.set_value(6.6),
                time_tracker.animate.set_value(6.6),
                run_time=0.7, rate_func=linear,
            )
            # Gentle opacity pulse on recap_eq via updater
            pulse_phase = ValueTracker(0.0)
            recap_eq.add_updater(
                lambda m: m.set_opacity(0.7 + 0.3 * (0.5 + 0.5 * math.cos(pulse_phase.get_value())))
            )
            self.play(
                pulse_phase.animate.set_value(2.0 * math.pi),
                breath_phase.animate.set_value(8.2),
                time_tracker.animate.set_value(8.4),
                run_time=2.4, rate_func=linear,
            )
            self.wait(0.3)