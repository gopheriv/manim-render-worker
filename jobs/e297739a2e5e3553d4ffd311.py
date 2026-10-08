from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # Palette
        PRIMARY = "#FFD166"   # golden string / standing wave
        SECONDARY = "#06D6A0" # green pulse (right-moving)
        ACCENT = "#EF476F"    # reserved for REVEAL climax (envelope / antinode markers)
        DARK_BG = "#0B1220"
        FLOOR_GREY = "#3A475A"
        TEXT_WHITE = "#F8FAFC"
        DIM_WHITE = "#CBD5E1"
        GREY_A = "#3A475A"
        GREY_B = "#94A3B8"
        COOL = "#7DD3FC"      # secondary travelling pulse colour (calmer than red)
        DIM_EQ = "#E2E8F0"

        self.camera.background_color = DARK_BG

        # Physics constants
        A_val = 1.0
        k_val = math.pi / 2.0
        omega_val = 2.0
        lambda_val = 4.0
        v_val = lambda_val * omega_val / (2.0 * math.pi)

        # ---- Floor (kept off-frame in later acts so the wave owns R3-R5) ----
        floor = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-2.9, -2.4, 0.1],
            x_length=14,
            y_length=0.45,
            background_line_style={"stroke_color": FLOOR_GREY, "stroke_width": 1,
                                   "stroke_opacity": 0.5},
            axis_config={"stroke_opacity": 0},
        )
        floor.set_opacity(0.55).to_edge(DOWN, buff=0.35)

        # ---- Anchor posts ----
        post_left = Rectangle(width=0.16, height=2.0, color=GREY_A,
                              fill_opacity=0.9, stroke_opacity=0.6)
        post_right = post_left.copy()
        post_left.move_to([-5.6, 0.9, 0.0])
        post_right.move_to([5.6, 0.9, 0.0])
        posts = VGroup(post_left, post_right)

        x_left = post_left.get_right()[0] + 0.05
        x_right = post_right.get_left()[0] - 0.05
        x_mid = (x_left + x_right) / 2.0

        # ---- Local axes over the string ----
        axes = Axes(
            x_range=[0, lambda_val, lambda_val / 4.0],
            y_range=[-2.0, 2.0, 1.0],
            x_length=(x_right - x_left),
            y_length=3.4,
            tips=False,
            axis_config={"stroke_opacity": 0},
        ).move_to([x_mid, 1.2, 0.0])

        baseline = Line(axes.c2p(0, 0), axes.c2p(lambda_val, 0),
                        color=GREY_B, stroke_width=2, stroke_opacity=0.6)

        # ---- Top HUD strip (parametrics) ----
        hud = VGroup()
        for lbl in ["A=1.000", "k=1.571", "λ=4.00", "ω=2.00", "v=1.273"]:
            hud.add(Text(lbl, color=TEXT_WHITE, font_size=22, weight=BOLD))
        hud.arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.3)
        hud_back = Rectangle(
            width=hud.width + 0.6, height=hud.height + 0.25,
            stroke_opacity=0, fill_color="#111B2E", fill_opacity=0.85,
        ).move_to(hud.get_center())
        hud_layer = VGroup(hud_back, hud)

        # ---- Time readout (left, same row as HUD) ----
        time_tracker = ValueTracker(0.0)
        t_label = Text("t =", color=TEXT_WHITE, font_size=22, weight=BOLD)
        t_readout = always_redraw(
            lambda: DecimalNumber(
                time_tracker.get_value(), num_decimal_places=2,
                color=TEXT_WHITE, font_size=22,
            ).next_to(t_label, RIGHT, buff=0.12)
        )
        t_group = VGroup(t_label, t_readout).arrange(RIGHT, buff=0.12)
        t_group.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.5)

        # ---- Title ----
        title = Text("Standing Wave", color=TEXT_WHITE, font_size=30, weight=BOLD)
        title.next_to(hud, DOWN, buff=0.35).align_to(hud, LEFT)

        # ---- Layout regions (so text never overlaps the wave) ----
        # R1-R2: HUD + title strip.   R3-R5: wave band.   R6-R7: captions.
        # The wave spans roughly y in [-1.7, 1.7] centred at y=1.2,
        # so captions must live BELOW y = -1.85 or in upper-left of R1.

        # Add the static stage layers
        self.add(floor, posts, baseline, hud_layer, t_group, title)

        # =========================================================
        # ACT 1 — HOOK: right-moving sine pulse (COOL colour, NOT accent)
        # =========================================================
        caption1 = Text(
            "right-moving sine pulse on the string",
            color=COOL, font_size=24, weight=BOLD,
        )
        caption1.to_edge(DOWN, buff=0.5)
        self.play(
            FadeIn(posts, shift=UP * 0.15),
            Create(baseline),
            FadeIn(caption1, shift=UP * 0.1),
            run_time=0.6,
        )

        pulse1_tracker = ValueTracker(-1.2)
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
                color=COOL,
                stroke_width=7,
            )

        pulse1 = always_redraw(pulse1_curve)
        self.add(pulse1)
        self.play(
            pulse1_tracker.animate.set_value(lambda_val * 0.5),
            time_tracker.animate.set_value(0.8),
            run_time=4.0, rate_func=linear,
        )
        self.wait(0.3)

        # =========================================================
        # ACT 2 — Counter-propagating pulse meets the first
        # =========================================================
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

        caption2 = Text(
            "counter-propagating pulse approaches",
            color=SECONDARY, font_size=24, weight=BOLD,
        )
        caption2.to_edge(DOWN, buff=0.5)
        self.play(
            FadeOut(caption1),
            FadeIn(caption2, shift=UP * 0.1),
            run_time=0.4,
        )

        # Drive both pulses toward a clearly visible approach / overlap
        self.play(
            pulse1_tracker.animate.set_value(lambda_val * 0.50),
            pulse2_tracker.animate.set_value(lambda_val * 0.50),
            time_tracker.animate.set_value(1.6),
            run_time=2.4, rate_func=linear,
        )
        self.wait(0.2)

        # CROSSING MOMENT — overlay the summed (constructive) transient so
        # the audience sees the two pulses literally combine and double.
        sum_peak = ParametricFunction(
            lambda s: axes.c2p(
                s,
                2.0 * A_val * math.sin(k_val * (s - lambda_val * 0.5))
                * math.exp(-((s - lambda_val * 0.5) ** 2)
                           / (2.0 * (pulse_width / 2.4) ** 2)),
            ),
            t_range=[
                lambda_val * 0.5 - 1.4 * pulse_width,
                lambda_val * 0.5 + 1.4 * pulse_width, 0.04,
            ],
            color=PRIMARY, stroke_width=11,
        )
        crossing_caption = Text(
            "y₁ + y₂  →  constructive peak (2A)",
            color=PRIMARY, font_size=24, weight=BOLD,
        )
        crossing_caption.to_edge(DOWN, buff=0.5)
        self.play(
            FadeOut(caption2),
            FadeIn(sum_peak, scale=0.9),
            FadeIn(crossing_caption, shift=UP * 0.1),
            time_tracker.animate.set_value(2.0),
            run_time=0.5,
        )
        self.wait(0.5)

        # Continue past each other and fade
        self.play(
            pulse1_tracker.animate.set_value(lambda_val + 1.2),
            pulse2_tracker.animate.set_value(-1.2),
            FadeOut(sum_peak),
            FadeOut(crossing_caption),
            time_tracker.animate.set_value(2.8),
            run_time=1.4, rate_func=linear,
        )
        self.remove(pulse1, pulse2)

        # =========================================================
        # ACT 3 — REVEAL: standing wave locked in (accent reserved)
        # =========================================================
        # Clear only the caption contents (stage stays put)
        reveal_caption = Text(
            "travelling waves → standing wave locks in",
            color=TEXT_WHITE, font_size=24, weight=BOLD,
        )
        reveal_caption.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(reveal_caption, shift=UP * 0.1), run_time=0.4)

        ghost1 = ParametricFunction(
            lambda s: axes.c2p(
                s,
                A_val * math.sin(k_val * (s - lambda_val * 0.3))
                * math.exp(-((s - lambda_val * 0.3) ** 2)
                           / (2.0 * (pulse_width / 2.4) ** 2)),
            ),
            t_range=[0, lambda_val, 0.05],
            color=COOL, stroke_width=2,
        )
        ghost2 = ParametricFunction(
            lambda s: axes.c2p(
                s,
                A_val * math.sin(k_val * (s - lambda_val * 0.7))
                * math.exp(-((s - lambda_val * 0.7) ** 2)
                           / (2.0 * (pulse_width / 2.4) ** 2)),
            ),
            t_range=[0, lambda_val, 0.05],
            color=SECONDARY, stroke_width=2,
        )

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

        self.play(
            FadeOut(ghost1), FadeOut(ghost2),
            breath_phase.animate.set_value(1.6),
            time_tracker.animate.set_value(3.4),
            run_time=2.4, rate_func=linear,
        )
        self.wait(0.3)

        # =========================================================
        # ACT 4 — Annotate nodes, antinodes, λ  (no overlap with the wave)
        # =========================================================
        self.play(FadeOut(reveal_caption), run_time=0.3)

        node_xs = [0.0, lambda_val / 2.0, lambda_val]
        node_dots = VGroup(*[
            Dot(axes.c2p(x, 0.0), color=WHITE, radius=0.075).set_stroke(BLACK, 1.5)
            for x in node_xs
        ])
        node_label = Text("nodes (fixed)", color=TEXT_WHITE,
                          font_size=22, weight=BOLD)
        # Place beneath the floor, well clear of the wave band
        node_label.next_to(floor, UP, buff=0.05).align_to(node_dots[0], LEFT).shift(DOWN*0.05)

        antinode_xs = [lambda_val / 4.0, 3.0 * lambda_val / 4.0]
        antinode_dots = VGroup(*[
            Dot(axes.c2p(x, 0.0), color=ACCENT, radius=0.11)
            .set_stroke(WHITE, 2, opacity=0.9)
            for x in antinode_xs
        ])
        antinode_label = Text("antinodes", color=ACCENT,
                              font_size=22, weight=BOLD)
        antinode_label.next_to(antinode_dots[0], DOWN, buff=0.45)

        # λ bracket: lift above the highest reachable antinode, never crossing
        # the live standing wave (we keep it pinned to baseline amplitude).
        brace = BraceBetweenPoints(
            axes.c2p(0, 0), axes.c2p(lambda_val, 0),
            direction=DOWN, color=TEXT_WHITE,
        )
        brace_label = MathTex("\\lambda = 4.0", color=TEXT_WHITE).scale(0.55)
        brace_label.next_to(brace, DOWN, buff=0.12)

        eq_standing = MathTex(
            "y = 2A\\sin(kx)\\cos(\\omega t)",
            color=DIM_EQ,
        ).scale(0.6)
        # Park the equation at upper-left so it never crosses the wave curve
        eq_standing.to_edge(LEFT, buff=0.5).shift(UP * 0.05)

        self.play(
            FadeIn(node_dots, lag_ratio=0.2),
            FadeIn(node_label, shift=UP * 0.1),
            FadeIn(antinode_dots, lag_ratio=0.2),
            FadeIn(antinode_label, shift=DOWN * 0.1),
            FadeIn(brace), FadeIn(brace_label),
            FadeIn(eq_standing, shift=RIGHT * 0.1),
            run_time=0.9,
        )

        # Keep breathing — annotations stay put; pair with travelling dot in COOL
        annotation = Text(
            "nodes at nπ/k,   antinodes at (n+½)π/k,   spacing = λ/2",
            color=TEXT_WHITE, font_size=22, weight=BOLD,
        )
        annotation.to_edge(DOWN, buff=0.25)

        tick_tracker = ValueTracker(x_left)
        speed_tick = always_redraw(
            lambda: Dot(
                [tick_tracker.get_value(), floor.get_y() + 0.04, 0.0],
                color=COOL, radius=0.085,
            )
        )
        speed_label = MathTex("v = 1.273", color=COOL).scale(0.6)
        speed_label.next_to(brace_label, RIGHT, buff=0.6).align_to(brace_label, DOWN)

        self.play(
            FadeIn(annotation, shift=UP * 0.1),
            FadeIn(speed_label, shift=UP * 0.1),
            run_time=0.5,
        )
        self.add(speed_tick)
        self.play(
            tick_tracker.animate.set_value(x_right - 0.15),
            breath_phase.animate.set_value(3.4),
            time_tracker.animate.set_value(4.6),
            run_time=2.8, rate_func=linear,
        )
        self.wait(0.3)

        # =========================================================
        # ACT 5 — REVEAL climax: ACCENT envelope + live readouts, wave breathes
        # =========================================================
        # Sweep act-4 furniture away but KEEP floor, posts, baseline, axes,
        # HUD, time readout, and the breathing standing wave.
        self.play(
            FadeOut(VGroup(
                node_dots, node_label, antinode_dots, antinode_label,
                brace, brace_label, eq_standing, annotation,
                speed_label, speed_tick,
            )),
            run_time=0.5,
        )

        # ACCENT envelope: 2|cos(ωt)| — the breath-shape that doubles the antinode
        envelope_phase = ValueTracker(0.0)

        def envelope_curve():
            amp = 2.0 * A_val * abs(math.cos(omega_val * envelope_phase.get_value()))
            return axes.plot(
                lambda x: amp * abs(math.sin(k_val * x)),
                x_range=[0, lambda_val, 0.05],
                color=ACCENT, stroke_width=4,
            )

        envelope_top = always_redraw(envelope_curve)
        envelope_bot = always_redraw(
            lambda: axes.plot(
                lambda x: -2.0 * A_val * abs(math.cos(omega_val * envelope_phase.get_value()))
                * abs(math.sin(k_val * x)),
                x_range=[0, lambda_val, 0.05],
                color=ACCENT, stroke_width=4,
            )
        )
        self.add(envelope_top, envelope_bot)

        # Recap equation centered high — well clear of envelope
        recap_eq = MathTex(
            "y = 2A\\sin(kx)\\cos(\\omega t)",
            color=TEXT_WHITE,
        ).scale(0.85)
        recap_eq.to_edge(LEFT, buff=0.6).shift(UP * 0.6)

        # Make the equation's amplitude factor literally update
        a_factor = DecimalNumber(2.0 * A_val, num_decimal_places=3,
                                 color=PRIMARY, font_size=46)
        a_factor.move_to(recap_eq[0][4].get_center())  # the "2" before A
        # Hide the static "2" inside the equation so a_factor stands in
        highlight_box = SurroundingRectangle(
            recap_eq[0][4], color=ACCENT, buff=0.04, stroke_width=2,
        )

        def update_a_factor(mob):
            target = recap_eq[0][4]
            mob.move_to(target.get_center())
            val = 2.0 * A_val
            mob.set_value(val)

        a_factor.add_updater(update_a_factor)

        # Live readouts anchored to a clean column on the right
        a_label = Text("A =", color=TEXT_WHITE, font_size=26, weight=BOLD)
        a_readout = DecimalNumber(A_val, num_decimal_places=3,
                                  color=PRIMARY, font_size=30)
        a_group = VGroup(a_label, a_readout).arrange(RIGHT, buff=0.12)
        a_group.to_edge(RIGHT, buff=0.8).shift(UP * 0.9)

        max_label = Text("max |y| =", color=TEXT_WHITE, font_size=26, weight=BOLD)
        max_readout = always_redraw(
            lambda: DecimalNumber(
                2.0 * A_val * abs(math.cos(omega_val * envelope_phase.get_value())),
                num_decimal_places=3, color=ACCENT, font_size=30,
            ).next_to(max_label, RIGHT, buff=0.12)
        )
        max_group = VGroup(max_label, max_readout).arrange(RIGHT, buff=0.12)
        max_group.next_to(a_group, DOWN, buff=0.25).align_to(a_group, LEFT)

        recap_caption = Text(
            "nodes fixed · antinodes oscillate  ↔  envelope breathes in ACCENT",
            color=ACCENT, font_size=22, weight=BOLD,
        )
        recap_caption.to_edge(DOWN, buff=0.35)

        self.add(a_factor, highlight_box)
        self.play(
            FadeIn(recap_eq, shift=DOWN * 0.1),
            FadeIn(recap_caption, shift=UP * 0.1),
            FadeIn(a_group, shift=LEFT * 0.1),
            FadeIn(max_group, shift=LEFT * 0.1),
            run_time=0.7,
        )
        self.wait(0.3)

        # Sweep envelope_phase through a full visible breath cycle so the
        # last sampled frames are unambiguously different from frame 5.
        breath_phase.set_value(8.2)
        envelope_phase.set_value(0.0)
        self.play(
            envelope_phase.animate.set_value(math.pi / omega_val),  # 2A → 0
            breath_phase.animate.set_value(8.2 + math.pi / 2.0),
            time_tracker.animate.set_value(8.4),
            run_time=1.4, rate_func=linear,
        )
        self.play(
            envelope_phase.animate.set_value(math.pi),  # 0 → 2A again
            breath_phase.animate.set_value(8.2 + math.pi),
            time_tracker.animate.set_value(8.8),
            run_time=1.4, rate_func=linear,
        )

        # Final living hold: keep the envelope visibly breathing while
        # the readout numbers tick. Two more samples at distinct phases.
        self.play(
            envelope_phase.animate.set_value(4.0 * math.pi / omega_val),
            breath_phase.animate.set_value(8.2 + 2.0 * math.pi),
            time_tracker.animate.set_value(9.4),
            run_time=1.8, rate_func=linear,
        )
        self.play(
            envelope_phase.animate.set_value(5.0 * math.pi / omega_val),
            breath_phase.animate.set_value(8.2 + 2.5 * math.pi),
            time_tracker.animate.set_value(10.0),
            run_time=1.4, rate_func=linear,
        )
        self.wait(0.3)