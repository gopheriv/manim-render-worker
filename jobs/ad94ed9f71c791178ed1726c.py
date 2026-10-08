from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # Palette
        NEON = "#3DDCFF"
        AMBER = "#FFD60A"
        ACCENT = "#FF3366"
        INK = "#F8FAFC"
        DIM = "#7F8794"

        # Geometry / curve evaluation
        X_RANGE = [-2 * PI, 2 * PI, PI / 2]
        Y_RANGE = [-1.5, 1.5, 0.5]
        N_SAMPLES = 1201

        def square_wave(t):
            # sgn(sin t) avoiding 0 ambiguity
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

        # Static (non-redraw) plot builder — used to avoid always_redraw rebuild cost
        def make_axes(scale_factor=0.7):
            ax = Axes(
                x_range=[X_RANGE[0], X_RANGE[1], X_RANGE[2]],
                y_range=[Y_RANGE[0], Y_RANGE[1], Y_RANGE[2]],
                tips=False,
            ).scale(scale_factor)
            return ax

        axes = make_axes(0.7).to_edge(DOWN, buff=0.7)

        title = Text(
            "Fourier Series — Odd sines stack into a square",
            color=INK,
            font_size=30,
        ).to_edge(UP, buff=0.35)

        # --- HOOK ----------------------------------------------------------------
        # BEAT A1.B1 | 0.00-4.00 s
        self.play(Write(title), run_time=0.7)

        axes_group = VGroup(axes, title).scale_to_fit_width(config.frame_width - 1)
        # Re-place after scaling
        axes.restore() if False else None  # no-op guard
        # Recreate axes with the scaled group behaviour manually
        axes = Axes(
            x_range=[X_RANGE[0], X_RANGE[1], X_RANGE[2]],
            y_range=[Y_RANGE[0], Y_RANGE[1], Y_RANGE[2]],
            tips=False,
        ).scale(0.7 * (config.frame_width - 1) / 6.283185307179586 * 6.283185307179586 / 6.0)
        axes.to_edge(DOWN, buff=0.7)
        title = Text(
            "Fourier Series — Odd sines stack into a square",
            color=INK,
            font_size=30,
        ).to_edge(UP, buff=0.35)

        # Recompute a stable, bounded axes scale that fits
        axes = Axes(
            x_range=[X_RANGE[0], X_RANGE[1], PI / 2],
            y_range=[Y_RANGE[0], Y_RANGE[1], 0.5],
            tips=False,
        )
        axes.scale_to_fit_width(config.frame_width - 1.5).to_edge(DOWN, buff=0.7)
        title = Text(
            "Fourier Series — Odd sines stack into a square",
            color=INK,
            font_size=30,
        ).to_edge(UP, buff=0.35).scale_to_fit_width(config.frame_width - 1.5)

        self.play(FadeIn(axes, lag_ratio=0.05), run_time=0.7)

        # Reference dashed square wave (NEVER inside always_redraw — plot once)
        square_curve = axes.plot(
            square_wave,
            x_range=[X_RANGE[0] + 0.01, X_RANGE[1] - 0.01, 0.005],
            use_smoothing=False,
            color=AMBER,
            stroke_width=4,
        )
        # Manually dash the curve by splitting into short segments
        sq_dashed = DashedVMobject(square_curve, num_dashes=180, dashed_ratio=0.55)

        square_ref = VGroup(sq_dashed)
        target_label = Text("square wave target", color=AMBER, font_size=30).next_to(
            axes, RIGHT, buff=0.2
        ).align_to(axes, UP).shift(DOWN * 0.2)

        self.play(FadeIn(square_ref), FadeIn(target_label), run_time=0.9)
        self.wait(3.0)
        self.play(FadeOut(target_label), run_time=0.4)

        # --- ESTABLISH ----------------------------------------------------------
        # BEAT A2.B1 | 4.00-9.00 s
        # First harmonic k=1 ribbon drawn in (translucent)
        ribbon_k1 = axes.plot(
            lambda x: harmonic(x, 1),
            x_range=[X_RANGE[0], X_RANGE[1], 0.005],
            color=NEON,
            stroke_width=6,
            stroke_opacity=0.55,
        )
        partial_k1 = axes.plot(
            lambda x: partial_sum(x, 1),
            x_range=[X_RANGE[0], X_RANGE[1], 0.005],
            color=NEON,
            stroke_width=4,
        )

        k1_label = Text("k = 1 of N_max = 9", color=INK, font_size=30).next_to(
            title, DOWN, buff=0.25
        )

        self.play(Create(ribbon_k1), run_time=1.2)
        self.play(Create(partial_k1), FadeIn(k1_label), run_time=1.0)
        self.wait(2.4)
        self.play(FadeOut(k1_label), run_time=0.4)

        # --- EVOLVE -------------------------------------------------------------
        # BEAT A3.B1 | 9.00-16.00 s
        N_tracker = ValueTracker(1)

        def partial_at_N(x):
            return partial_sum(x, int(N_tracker.get_value()))

        # PRE-CREATE every static partial-sum curve for N = 1..9, then Transform between them.
        partial_curves = []
        for Nv in range(1, 10):
            c = axes.plot(
                lambda x, Nv=Nv: partial_sum(x, Nv),
                x_range=[X_RANGE[0], X_RANGE[1], 0.005],
                color=NEON,
                stroke_width=4,
            )
            partial_curves.append(c)

        # Counter readout (live), placed bottom-left
        N_readout_label = Text("N =", color=INK, font_size=34).to_corner(UL, buff=0.4)
        N_readout = Integer(int(N_tracker.get_value()), color=NEON, font_size=42).next_to(
            N_readout_label, RIGHT, buff=0.15
        )
        N_readout_box = VGroup(N_readout_label, N_readout)

        # Replace the earlier partial_k1 on screen with the partial_curves[0]
        self.remove(partial_k1)
        self.add(partial_curves[0])

        # Animate the counter appearing BEFORE animating N_tracker, to keep digit count stable
        self.play(FadeIn(N_readout_label), FadeIn(N_readout), run_time=0.5)
        # Hook the counter so it follows the tracker without animation inside self.play
        N_readout.add_updater(lambda m: m.set_value(int(N_tracker.get_value())))

        # Add ribbons cumulatively as N grows
        ribbons = VGroup(ribbon_k1)
        for idx in range(2, 10):  # build ribbons for k=3..17
            n = 2 * idx - 1
            rib = axes.plot(
                lambda x, n=n: harmonic(x, n),
                x_range=[X_RANGE[0], X_RANGE[1], 0.005],
                color=NEON,
                stroke_width=4,
                stroke_opacity=0.45,
            )
            rib.fade(0.5)
            ribbons.add(rib)

        # Tick: 1 -> 3 -> 5 -> 7 -> 9 (i.e. N grows through 1,3,5,7,9 odd-indexed sums)
        tick_steps = [(3, 2), (5, 2), (7, 2), (9, 2)]
        # Fade in ribbons for new odd harmonics with each step, transform the partial curve,
        # and advance the ValueTracker (which the counter updater follows).

        new_ribbons_step1 = VGroup(ribbons[1])  # k=3 (n=3)
        new_ribbons_step2 = VGroup(ribbons[2])  # k=5 (n=5)
        new_ribbons_step3 = VGroup(ribbons[3])  # k=7 (n=7)
        new_ribbons_step4 = VGroup(ribbons[4], ribbons[5], ribbons[6], ribbons[7], ribbons[8])  # k=9..17

        self.play(
            LaggedStart(FadeIn(new_ribbons_step1, lag_ratio=0.2), run_time=0.6),
            Transform(partial_curves[0], partial_curves[1]),
            N_tracker.animate.set_value(3),
            run_time=1.2,
        )
        self.play(
            LaggedStart(FadeIn(new_ribbons_step2, lag_ratio=0.2), run_time=0.5),
            Transform(partial_curves[1], partial_curves[2]),
            N_tracker.animate.set_value(5),
            run_time=1.2,
        )
        self.play(
            LaggedStart(FadeIn(new_ribbons_step3, lag_ratio=0.2), run_time=0.5),
            Transform(partial_curves[2], partial_curves[3]),
            N_tracker.animate.set_value(7),
            run_time=1.2,
        )
        self.play(
            LaggedStart(FadeIn(new_ribbons_step4, lag_ratio=0.1), run_time=0.9),
            Transform(partial_curves[3], partial_curves[4]),
            N_tracker.animate.set_value(9),
            run_time=2.0,
        )
        self.wait(0.8)

        # BEAT A3.B2 | 16.00-19.00 s
        # Gibbs overshoot annotation near a jump
        # Find the visible peak of the N=9 partial sum near the +1 jump (just right of t=0)
        # Use analytic peak location near t = pi/(2N) for large N; for N=9 the overshoot peak ~0.179 above +1.
        # Pick sample at t = PI / (2 * 9) ≈ 0.1745; compute value, convert to scene coords.
        t_peak = PI / (2 * 9)
        y_peak = partial_sum(t_peak, 9)
        peak_pt = axes.c2p(t_peak, y_peak)
        jump_target_pt = axes.c2p(t_peak, 1.0)

        arrow = Arrow(
            peak_pt + UP * 0.05 + RIGHT * 0.2,
            peak_pt,
            color=ACCENT,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.25,
            buff=0.0,
        )
        overshoot_card = VGroup(
            MathTex(r"y_{\text{peak}} \approx 1 + 0.179", color=ACCENT, font_size=34),
            MathTex(r"G \approx 0.08949", color=ACCENT, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(
            axes, RIGHT, buff=0.25
        ).align_to(axes, UP).shift(DOWN * 1.0)

        overshoot_text = Text(
            "+9% overshoot",
            color=ACCENT,
            font_size=30,
        ).next_to(peak_pt, UP, buff=0.25).align_to(peak_pt, RIGHT)

        self.play(
            Create(arrow),
            FadeIn(overshoot_text),
            FadeIn(overshoot_card),
            run_time=0.9,
        )
        self.wait(1.7)
        self.play(
            FadeOut(arrow),
            FadeOut(overshoot_text),
            FadeOut(overshoot_card),
            run_time=0.4,
        )

        # --- REVEAL -------------------------------------------------------------
        # BEAT A4.B1 | 19.00-26.00 s
        # Hero frame: all nine translucent ribbons fan above, neon partial sum (N=9) on dashed square
        # Already have: partial_curves[4] (N=9) live, ribbons all visible. Add the N=5..N=9 transforms done.

        # Hero label, glowing accent counter, and confirmation
        hero_label = Text("N = 9", color=NEON, font_size=42).next_to(
            N_readout_box, RIGHT, buff=0.6
        )
        summary = Text(
            "9 odd harmonics — the square appears",
            color=INK,
            font_size=30,
        ).next_to(title, DOWN, buff=0.25)

        self.play(FadeIn(hero_label), FadeIn(summary), run_time=0.9)
        self.wait(2.0)

        # Slight upward lift of the harmonic fan to feel like a chorus
        fan_anim_target = ribbons.copy().shift(UP * 0.12)

        self.play(
            Transform(ribbons, fan_anim_target, lag_ratio=0.0),
            run_time=1.5,
            rate_func=smooth,
        )
        self.wait(1.3)

        # --- RECAP --------------------------------------------------------------
        # BEAT A5.B1 | 26.00-30.00 s
        # Clear the stage: ribbons, counter, summary fade out
        self.play(
            FadeOut(ribbons),
            FadeOut(N_readout_label),
            FadeOut(N_readout),
            FadeOut(hero_label),
            FadeOut(summary),
            run_time=0.8,
        )

        # Remove the updater before animating the partial curve into the recap
        N_readout.clear_updaters()

        # Recap formula card
        formula = MathTex(
            r"x(t)=\frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin((2k-1)t)}{2k-1}",
            color=INK,
            font_size=42,
        )
        recap_label = Text("odd sine harmonics → square wave", color=NEON, font_size=30).next_to(
            formula, DOWN, buff=0.3
        )

        recap_card = VGroup(formula, recap_label).arrange(DOWN, buff=0.3).move_to(UP * 1.2)

        # Stable idle loop for the final waveform — VERY CHEAP: animate a ValueTracker
        # that scales/stretch by ±2% via a Transform on a small set of cached points.
        # We avoid always_redraw entirely. Instead, breathe by playing a Transform
        # between two pre-built partial-sum copies (one at +2% stretch, one at -2%).
        # The dashed square is left in place to shimmer via opacity oscillation.

        # Pre-build the breathing alternative curve (no redraw cost; Transform is cheap)
        partial_base = partial_curves[4]  # currently on screen

        def scaled_partial(x, factor):
            return factor * partial_sum(x, 9)

        partial_hi = axes.plot(
            lambda x: scaled_partial(x, 1.02),
            x_range=[X_RANGE[0], X_RANGE[1], 0.005],
            color=NEON,
            stroke_width=4,
        )
        partial_lo = axes.plot(
            lambda x: scaled_partial(x, 0.98),
            x_range=[X_RANGE[0], X_RANGE[1], 0.005],
            color=NEON,
            stroke_width=4,
        )

        # Recap entrance
        self.play(FadeIn(recap_card), run_time=0.9)

        # Idle loop: 3 breathing pulses + dashed shimmer.
        # We use a ValueTracker-like pulse via a quick Transform pair; not redrawing the curve.
        shimmer_tracker = ValueTracker(1.0)
        # Square reference opacity updater — only one cheap updater on opacity
        sq_dashed.add_updater(lambda m: m.set_opacity(0.6 + 0.25 * math.sin(6.2831 * shimmer_tracker.get_value())))

        breath_steps = 3
        per_breath = 0.55
        for _ in range(breath_steps):
            self.play(
                Transform(partial_base, partial_hi, run_time=per_breath, rate_func=smooth),
                shimmer_tracker.animate.increment_value(1.0),
                run_time=per_breath,
            )
            self.play(
                Transform(partial_base, partial_lo, run_time=per_breath, rate_func=smooth),
                shimmer_tracker.animate.increment_value(1.0),
                run_time=per_breath,
            )
        # Return to base and stop shimmer updater to avoid leftover on next render
        self.play(
            Transform(partial_base, partial_curves[4], run_time=per_breath, rate_func=smooth),
            run_time=per_breath,
        )
        sq_dashed.clear_updaters()
        self.wait(0.4)