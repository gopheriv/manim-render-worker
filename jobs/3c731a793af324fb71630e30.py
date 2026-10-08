from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # Palette (only real Manim colors / hex)
        # ------------------------------------------------------------------
        NEON = "#3DDCFF"
        AMBER = "#FFD60A"
        ACCENT = "#FF3366"
        INK = "#F8FAFC"
        DIM = "#94A3B8"
        STAGE_BG = "#0B1020"

        # ------------------------------------------------------------------
        # Stage scaffold
        # ------------------------------------------------------------------
        X_RANGE = [-2 * PI, 2 * PI, PI / 2]
        Y_RANGE = [-1.5, 1.5, 0.5]
        STEP = 0.004

        # ------------------------------------------------------------------
        # Math helpers
        # ------------------------------------------------------------------
        def square_wave(t):
            s = math.sin(t)
            if s > 0:
                return 1.0
            if s < 0:
                return -1.0
            return 1.0

        def partial_sum(t, N):
            s = 0.0
            for k in range(1, N + 1):
                n = 2 * k - 1
                s += math.sin(n * t) / n
            return (4.0 / math.pi) * s

        def harmonic(t, n):
            return (4.0 / math.pi) * math.sin(n * t) / n

        # ------------------------------------------------------------------
        # Title
        # ------------------------------------------------------------------
        title = Text(
            "Fourier Series — Odd sines stack into a square",
            color=INK,
            font_size=30,
        )
        title.to_edge(UP, buff=0.35)
        title_w = min(config.frame_width - 1.5, title.width)
        if title.width > title_w:
            title.scale_to_fit_width(title_w)
            title.to_edge(UP, buff=0.35)

        # ------------------------------------------------------------------
        # Axes with full readable labels
        # ------------------------------------------------------------------
        axes = Axes(
            x_range=[X_RANGE[0], X_RANGE[1], X_RANGE[2]],
            y_range=[Y_RANGE[0], Y_RANGE[1], Y_RANGE[2]],
            x_axis_config={
                "include_numbers": False,
                "stroke_color": DIM,
                "stroke_width": 2,
            },
            y_axis_config={
                "include_numbers": True,
                "stroke_color": DIM,
                "stroke_width": 2,
                "decimal_number_config": {
                    "color": DIM,
                    "num_decimal_places": 1,
                    "font_size": 20,
                },
            },
            tips=False,
        )
        axes.scale_to_fit_width(config.frame_width - 1.6)
        axes.to_edge(DOWN, buff=0.95)

        # Custom x-axis labels
        x_tick_values = [-2 * PI, -PI, 0, PI, 2 * PI]
        x_tick_tex = [
            MathTex("-2\\pi", color=DIM, font_size=26),
            MathTex("-\\pi", color=DIM, font_size=26),
            MathTex("0", color=DIM, font_size=26),
            MathTex("\\pi", color=DIM, font_size=26),
            MathTex("2\\pi", color=DIM, font_size=26),
        ]
        x_ticks = VGroup()
        x_labels = VGroup()
        for v, tex in zip(x_tick_values, x_tick_tex):
            p = axes.c2p(v, 0)
            tick = Line(p + DOWN * 0.08, p + DOWN * 0.18, color=DIM, stroke_width=2)
            x_ticks.add(tick)
            lbl = tex.next_to(p, DOWN, buff=0.18)
            x_labels.add(lbl)
        x_axis_label = MathTex("x", color=DIM, font_size=28).next_to(
            x_labels, DOWN, buff=0.25
        )
        y_axis_label = MathTex("y", color=DIM, font_size=28).next_to(
            axes.c2p(0, Y_RANGE[1]), UP, buff=0.15
        )

        stage = VGroup(axes, x_ticks, x_labels, x_axis_label, y_axis_label)

        # ------------------------------------------------------------------
        # Static reference square wave (dashed amber)
        # ------------------------------------------------------------------
        square_curve = axes.plot(
            square_wave,
            x_range=[X_RANGE[0] + 0.01, X_RANGE[1] - 0.01, 0.01],
            use_smoothing=False,
            color=AMBER,
            stroke_width=4,
        )
        sq_dashed = DashedVMobject(square_curve, num_dashes=180, dashed_ratio=0.55)

        target_label = Text("square wave target", color=AMBER, font_size=26)
        # Place legend safely to the LEFT of the axes to never collide with the wave
        target_label.next_to(axes, LEFT, buff=0.25).align_to(axes, UP).shift(DOWN * 0.35)

        # ------------------------------------------------------------------
        # HOOK  (0.0 - 4.0 s)
        # ------------------------------------------------------------------
        self.play(FadeIn(stage), Write(title), run_time=0.9)
        self.play(FadeIn(sq_dashed), FadeIn(target_label), run_time=0.9)
        self.wait(1.8)
        self.play(FadeOut(target_label), run_time=0.4)

        # ------------------------------------------------------------------
        # ESTABLISH  (4.0 - 9.0 s) : first harmonic ribbon + N=1 partial
        # ------------------------------------------------------------------
        ribbon_k1 = axes.plot(
            lambda x: harmonic(x, 1),
            x_range=[X_RANGE[0], X_RANGE[1], STEP],
            color=NEON,
            stroke_width=6,
            stroke_opacity=0.55,
        )
        partial_k1 = axes.plot(
            lambda x: partial_sum(x, 1),
            x_range=[X_RANGE[0], X_RANGE[1], STEP],
            color=NEON,
            stroke_width=4,
        )
        k1_label = MathTex(r"\text{harmonic } k=1", color=INK, font_size=30)
        k1_label.next_to(title, DOWN, buff=0.25).align_to(title, LEFT)
        # square(x) marker — fits inside the frame at upper-left
        sx_label = Text("square(x)", color=AMBER, font_size=24).to_corner(
            UL, buff=0.45
        )

        self.add(sx_label)
        self.play(Create(ribbon_k1), run_time=1.2)
        self.play(Create(partial_k1), FadeIn(k1_label), run_time=1.0)
        self.wait(2.4)
        self.play(FadeOut(k1_label), FadeOut(sx_label), run_time=0.4)

        # ------------------------------------------------------------------
        # EVOLVE  (9.0 - 19.0 s) : N steps from 1 -> 3 -> 5 -> 7 -> 9
        # ------------------------------------------------------------------
        N_tracker = ValueTracker(1)

        partial_curves = []
        for Nv in range(1, 10):
            c = axes.plot(
                lambda x, Nv=Nv: partial_sum(x, Nv),
                x_range=[X_RANGE[0], X_RANGE[1], STEP],
                color=NEON,
                stroke_width=4,
            )
            partial_curves.append(c)

        N_readout_label = Text("N =", color=INK, font_size=34).to_corner(UL, buff=0.45)
        N_readout = Integer(1, color=NEON, font_size=42).next_to(
            N_readout_label, RIGHT, buff=0.15
        )
        N_readout_box = VGroup(N_readout_label, N_readout)

        # Counter readout starts blank; we add it now (keeps digits stable)
        self.remove(partial_k1)
        self.add(partial_curves[0])
        self.play(FadeIn(N_readout_label), FadeIn(N_readout), run_time=0.5)
        N_readout.add_updater(lambda m: m.set_value(int(N_tracker.get_value())))

        # Build all harmonic ribbons up front (k=1..9), but only add them in
        ribbons_list = []
        for idx in range(1, 10):
            n = 2 * idx - 1
            rib = axes.plot(
                lambda x, n=n: harmonic(x, n),
                x_range=[X_RANGE[0], X_RANGE[1], STEP],
                color=NEON,
                stroke_width=4,
                stroke_opacity=0.55,
            )
            ribbons_list.append(rib)

        step_groups = [
            [1],          # when going N=1 -> N=3, add k=2 (n=3)
            [2],          # N=3 -> N=5, add k=3 (n=5)
            [3],          # N=5 -> N=7, add k=4 (n=7)
            [4, 5, 6, 7, 8],  # N=7 -> N=9, add k=5..9 (n=9..17)
        ]
        next_targets = [3, 5, 7, 9]

        for add_idxs, target_N in zip(step_groups, next_targets):
            new_ribbons = VGroup(*[ribbons_list[i] for i in add_idxs])
            cur_idx = (target_N - 1) // 2 - 1   # current curve index for current N
            nxt_idx = cur_idx + 1              # target index for next N
            self.play(
                LaggedStart(*[FadeIn(r, lag_ratio=0.0) for r in new_ribbons], lag_ratio=0.15),
                Transform(partial_curves[cur_idx], partial_curves[nxt_idx]),
                N_tracker.animate.set_value(target_N),
                run_time=1.7 if target_N == 9 else 1.3,
                rate_func=smooth,
            )

        # Ribbon VGroup (single, for mass operations later)
        ribbons = VGroup(*ribbons_list)
        self.wait(0.8)

        # ------------------------------------------------------------------
        # GIBBS CLIMAX  (16.0 - 19.0 s) : overshoot annotation
        # ------------------------------------------------------------------
        t_peak = PI / (2 * 9)
        y_peak = partial_sum(t_peak, 9)
        peak_pt = axes.c2p(t_peak, y_peak)
        jump_pt = axes.c2p(0.0, 1.0)

        # Vertical accent guide between jump (y=1) and the overshoot peak
        guide = Line(
            axes.c2p(t_peak, 1.0),
            axes.c2p(t_peak, y_peak),
            color=ACCENT,
            stroke_width=3,
        )
        # Arrow pointing AT the peak from above-left
        arrow = Arrow(
            peak_pt + LEFT * 0.55 + UP * 0.55,
            peak_pt + LEFT * 0.05,
            color=ACCENT,
            stroke_width=5,
            buff=0.0,
            max_tip_length_to_length_ratio=0.22,
        )

        # Annotation card — short and wide so it doesn't overlap the waveform
        peak_eq = MathTex(
            r"y_{\max}\approx 1+0.17949\cdot \tfrac{2}{\pi}",
            color=ACCENT,
            font_size=30,
        )
        gibbs_eq = MathTex(
            r"G\;\approx\;0.08949\cdot\!\int|y|\,dx",
            color=ACCENT,
            font_size=30,
        )
        overshoot_card = VGroup(peak_eq, gibbs_eq).arrange(DOWN, buff=0.18)
        overshoot_card.to_edge(RIGHT, buff=0.45).shift(UP * 1.2)
        bg = BackgroundRectangle(overshoot_card, color="#000814", fill_opacity=0.55,
                                 stroke_opacity=0.0)
        card_group = VGroup(bg, overshoot_card)

        # A small "+9% overshoot" tag floating near the peak
        overshoot_text = Text(
            "+9% overshoot",
            color=ACCENT,
            font_size=24,
        )
        overshoot_text.next_to(peak_pt, UL, buff=0.15)

        self.play(
            Create(guide),
            Create(arrow),
            FadeIn(overshoot_text),
            FadeIn(card_group),
            run_time=1.1,
        )
        self.wait(1.4)
        self.play(
            FadeOut(guide),
            FadeOut(arrow),
            FadeOut(overshoot_text),
            FadeOut(card_group),
            run_time=0.5,
        )

        # ------------------------------------------------------------------
        # REVEAL  (19.0 - 26.0 s) : "N=9 — the square appears"
        # ------------------------------------------------------------------
        hero_label = MathTex("N=9", color=NEON, font_size=44).next_to(
            N_readout_box, RIGHT, buff=0.6
        )
        summary = Text(
            "9 odd harmonics — the square appears",
            color=INK,
            font_size=28,
        ).next_to(title, DOWN, buff=0.25)

        self.play(FadeIn(hero_label), FadeIn(summary), run_time=0.9)
        self.wait(1.6)

        # Subtle fan lift — keeps motion alive into RECAP
        fan_target = ribbons.copy().shift(UP * 0.12).set_opacity(0.85)
        self.play(
            Transform(ribbons, fan_target, lag_ratio=0.0),
            run_time=1.4,
            rate_func=smooth,
        )
        self.wait(1.0)

        # ------------------------------------------------------------------
        # RECAP  (26.0 - 30.0 s) : clear stage, keep dashed square + waveform + card
        # ------------------------------------------------------------------
        self.play(
            FadeOut(ribbons),
            FadeOut(N_readout_label),
            FadeOut(N_readout),
            FadeOut(hero_label),
            FadeOut(summary),
            run_time=0.8,
        )
        N_readout.clear_updaters()

        formula = MathTex(
            r"x(t)=\tfrac{4}{\pi}\sum_{k=1}^{\infty}\tfrac{\sin\!\big((2k-1)\,t\big)}{2k-1}",
            color=INK,
            font_size=40,
        )
        recap_label = Text(
            "odd sine harmonics → square wave",
            color=NEON,
            font_size=28,
        ).next_to(formula, DOWN, buff=0.28)

        recap_card = VGroup(formula, recap_label).arrange(DOWN, buff=0.18)
        recap_card.to_edge(UP, buff=1.1).scale_to_fit_width(config.frame_width - 1.6)

        # Live partial sum (final on-screen curve) — stays small in lower 60% of frame
        final_partial = axes.plot(
            lambda x: partial_sum(x, 9),
            x_range=[X_RANGE[0], X_RANGE[1], STEP],
            color=NEON,
            stroke_width=4,
        )
        self.add(final_partial)

        self.play(FadeIn(recap_card), run_time=0.8)

        # Living ending : a slow breathing Transform across two cached curves,
        # plus a gentle amber shimmer on the dashed square.
        partial_hi = axes.plot(
            lambda x: 1.02 * partial_sum(x, 9),
            x_range=[X_RANGE[0], X_RANGE[1], STEP],
            color=NEON,
            stroke_width=4,
        )
        partial_lo = axes.plot(
            lambda x: 0.98 * partial_sum(x, 9),
            x_range=[X_RANGE[0], X_RANGE[1], STEP],
            color=NEON,
            stroke_width=4,
        )
        shimmer = ValueTracker(0.0)
        sq_dashed.add_updater(
            lambda m: m.set_opacity(0.55 + 0.25 * math.sin(shimmer.get_value()))
        )

        for _ in range(2):
            self.play(
                Transform(final_partial, partial_hi, rate_func=smooth),
                shimmer.animate.increment_value(1.6),
                run_time=0.55,
            )
            self.play(
                Transform(final_partial, partial_lo, rate_func=smooth),
                shimmer.animate.increment_value(1.6),
                run_time=0.55,
            )
        self.play(
            Transform(final_partial, partial_curves[8], rate_func=smooth),
            run_time=0.5,
        )
        sq_dashed.clear_updaters()
        self.wait(0.4)