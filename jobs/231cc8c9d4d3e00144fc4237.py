from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # ------------------ helpers ------------------
        LAMBDA_MIN_NM = 300.0
        LAMBDA_MAX_NM = 1100.0
        T_DEFAULT = 5800.0

        # Plot area (data coordinates: x in nm, y in arbitrary intensity)
        axes = Axes(
            x_range=[LAMBDA_MIN_NM, LAMBDA_MAX_NM, 200],
            y_range=[0, 1.05, 0.25],
            x_length=10.0,
            y_length=3.4,
            tips=False,
            stroke_opacity=0.55,
        )
        axes.move_to([0, -0.45, 0])

        x_label = MathTex(r"\lambda\ (\text{nm})", color=WHITE).scale(0.55)
        x_label.next_to(axes.x_axis, RIGHT, buff=0.15)
        y_label = MathTex(r"I(\lambda)", color=WHITE).scale(0.55)
        y_label.next_to(axes.y_axis, UP, buff=0.1)

        # Normalised curves so the visible plot stays inside [0, 1.05].
        def rj_curve(lam, T):
            return (T / T_DEFAULT) * (500.0 ** 4) / (lam ** 4)

        H_C_K = 1.438776877e7  # hc/k_B in nm·K
        peak_nm = 500.0
        def planck_raw(lam, T):
            x = H_C_K / (lam * T)
            return (1.0 / (lam ** 5)) / (math.exp(min(x, 700.0)) - 1.0)
        planck_norm = planck_raw(peak_nm, T_DEFAULT)
        def planck_curve(lam, T):
            return (T / T_DEFAULT) * planck_raw(lam, T) / planck_norm

        def plot_y(value):
            return min(value, 1.05)

        # ------------------ static filament + spectrum scaffolding ------------------
        filament = Line(LEFT * 2.4, RIGHT * 2.4, color=GREY_A, stroke_width=6)
        filament.move_to([0, -2.6, 0])
        filament_glow = Dot(filament.get_center(), color=ORANGE, radius=0.05)
        glow_halo = Circle(radius=0.55, color=ORANGE, fill_opacity=0.18,
                           stroke_opacity=0).move_to(filament.get_center())

        prism = Polygon(
            [-0.45, 0.0, 0], [0.45, 0.0, 0], [0.0, 0.85, 0],
            color=WHITE, fill_opacity=0.12, stroke_opacity=0.85
        )
        prism.move_to([0, -1.55, 0])

        # ------------------ BEAT A1.B1 | 0.00-2.46 s ------------------
        # Filament ignites, glow pulses, T readout ticks to 5800 K.
        T_tracker = ValueTracker(300.0)
        T_readout = always_redraw(
            lambda: VGroup(
                Text("T = ", color=WHITE).scale(0.32),
                DecimalNumber(T_tracker.get_value(), num_decimal_places=0,
                              color=WHITE).scale(0.32),
                Text(" K", color=WHITE).scale(0.32),
            ).arrange(RIGHT, buff=0.08).to_edge(LEFT, buff=0.5).shift(UP * 2.0)
        )
        self.add(filament, filament_glow, glow_halo, T_readout)
        self.play(
            T_tracker.animate.set_value(5800.0),
            filament_glow.animate.set_color(WHITE).scale(4.5),
            glow_halo.animate.scale(2.4).set_fill(opacity=0.55),
            run_time=2.1,
            rate_func=smooth,
        )
        self.wait(0.36)

        # ------------------ BEAT A1.B2 | 2.46-4.50 s ------------------
        # Light refracts through prism, fans into a continuous spectrum band.
        self.add(prism)
        ray_in = Line(filament.get_center(), prism.get_bottom(),
                      color=ORANGE, stroke_width=3, stroke_opacity=0.9)
        fan_lines = VGroup()
        for t in np.linspace(0, 1, 7):
            start = prism.get_top() + UP * 0.05
            end = start + rotate_vector(UP, -0.35 + 0.7 * t) * 1.6
            fan_lines.add(Line(start, end, color=ORANGE, stroke_width=2,
                               stroke_opacity=0.55))

        # Build spectrum band now (depends only on axes, which are constants)
        spectrum_lines = VGroup()
        for lam in np.linspace(LAMBDA_MIN_NM, LAMBDA_MAX_NM, 41):
            t = (lam - LAMBDA_MIN_NM) / (LAMBDA_MAX_NM - LAMBDA_MIN_NM)
            if t < 0.2:
                col = interpolate_color(PURPLE, BLUE, t / 0.2)
            elif t < 0.4:
                col = interpolate_color(BLUE, TEAL, (t - 0.2) / 0.2)
            elif t < 0.55:
                col = interpolate_color(TEAL, GREEN, (t - 0.4) / 0.15)
            elif t < 0.7:
                col = interpolate_color(GREEN, YELLOW, (t - 0.55) / 0.15)
            elif t < 0.85:
                col = interpolate_color(YELLOW, ORANGE, (t - 0.7) / 0.15)
            else:
                col = interpolate_color(ORANGE, RED, (t - 0.85) / 0.15)
            x = axes.x_axis.n2p(lam)[0]
            y = axes.y_axis.n2p(0.06)[1]
            seg = Line([x, y - 0.18, 0], [x, y + 0.18, 0],
                       color=col, stroke_width=4, stroke_opacity=0.85)
            spectrum_lines.add(seg)

        lambda_label = MathTex(r"\lambda\ (\text{nm})", color=WHITE).scale(0.45)
        lambda_label.next_to(spectrum_lines, RIGHT, buff=0.2)

        self.play(
            Create(ray_in),
            Create(fan_lines),
            FadeIn(spectrum_lines, lag_ratio=0.05),
            FadeIn(lambda_label),
            run_time=2.04,
        )

        # ------------------ BEAT A2.B1 | 4.50-6.79 s ------------------
        # Axes fade in: horizontal wavelength 300-1100 nm, vertical intensity.
        self.play(
            Create(axes, lag_ratio=0.01),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=1.6,
        )
        self.wait(0.69)

        # ------------------ BEAT A2.B2 | 6.79-10.00 s ------------------
        # Blue Rayleigh-Jeans curve drawn on top of the spectrum (linear ramp in UV).
        rj = axes.plot(
            lambda lam: plot_y(rj_curve(lam, T_DEFAULT)),
            x_range=[LAMBDA_MIN_NM, 1100.0, 1],
            color=BLUE, stroke_width=5,
        )
        rj_eq = MathTex(r"I_{\mathrm{RJ}}(\lambda)=\frac{2c k T}{\lambda^{4}}",
                        color=BLUE).scale(0.42)
        rj_eq.next_to(axes, RIGHT, buff=-1.0).shift(UP * 0.7)
        self.play(
            Create(rj),
            FadeIn(rj_eq, shift=LEFT * 0.2),
            run_time=2.6,
        )
        self.wait(0.61)

        # ------------------ BEAT A3.B1 | 10.00-13.00 s ------------------
        # Extend the blue curve past 300 nm (shoot upward) — UV catastrophe.
        arrow = Arrow(
            axes.c2p(310, 1.0), axes.c2p(310, 1.6),
            color=BLUE, stroke_width=6, max_tip_length_to_length_ratio=0.18,
            buff=0,
        )
        rj_uv = axes.plot(
            lambda lam: plot_y(rj_curve(lam, T_DEFAULT)),
            x_range=[300.0, 320.0, 1],
            color=BLUE, stroke_width=5,
        ).set_opacity(0.7)
        cat_label = MathTex(r"\lim_{\lambda\to 0} I_{\mathrm{RJ}}\to\infty",
                            color=BLUE).scale(0.45)
        cat_label.next_to(arrow.get_end(), UP, buff=0.15)
        self.play(
            Create(rj_uv),
            GrowArrow(arrow),
            FadeIn(cat_label, shift=UP * 0.15),
            run_time=1.8,
        )
        self.wait(1.2)

        # ------------------ BEAT A3.B2 | 13.00-17.50 s ------------------
        # Yellow Planck curve drawn, finite UV tail. Energy packets snap on
        # the wavelength axis at discrete steps.
        planck = axes.plot(
            lambda lam: plot_y(planck_curve(lam, T_DEFAULT)),
            x_range=[300.0, 1100.0, 1],
            color=YELLOW, stroke_width=5,
        )
        planck_eq = MathTex(
            r"I_{\mathrm{P}}(\lambda)=\frac{2hc^{2}}{\lambda^{5}}"
            r"\frac{1}{e^{hc/\lambda k T}-1}",
            color=YELLOW,
        ).scale(0.42)
        planck_eq.next_to(axes, DOWN, buff=0.2).shift(LEFT * 0.5)

        packet_targets = [340, 500, 660, 820, 980]
        packet_marks = VGroup(*[
            Square(side_length=0.10, fill_opacity=0.9, fill_color=GOLD,
                   stroke_opacity=0).move_to(axes.c2p(lm, 0.02))
            for lm in packet_targets
        ])

        self.play(
            Create(planck),
            LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in packet_marks],
                        lag_ratio=0.08),
            FadeIn(planck_eq, shift=UP * 0.1),
            run_time=3.9,
        )
        self.wait(0.6)

        # ------------------ BEAT A4.B1 | 17.50-21.94 s ------------------
        # Match measured spectrum to the yellow Planck curve; fade RJ to ghost;
        # peak marker "500 nm ≈ 5800 K".
        rj_ghost = rj.copy().set_opacity(0.25).set_stroke(width=2.5)
        rj_uv_ghost = rj_uv.copy().set_opacity(0.25).set_stroke(width=2.5)
        peak_dot = Dot(axes.c2p(500, planck_curve(500, T_DEFAULT)),
                       color=WHITE, radius=0.07)
        peak_line = DashedLine(
            axes.c2p(500, 0.0), axes.c2p(500, planck_curve(500, T_DEFAULT)),
            color=WHITE, stroke_width=2, dash_length=0.08,
        )
        peak_eq = MathTex(r"\lambda_{\mathrm{peak}}\approx 500\,\mathrm{nm}",
                          color=WHITE).scale(0.45)
        peak_eq.next_to(peak_dot, UP, buff=0.18)
        self.play(
            FadeOut(arrow),
            FadeOut(cat_label),
            Transform(rj, rj_ghost),
            Transform(rj_uv, rj_uv_ghost),
            Create(peak_line),
            FadeIn(peak_dot),
            FadeIn(peak_eq, shift=UP * 0.1),
            FadeOut(packet_marks),
            run_time=2.1,
        )
        self.wait(2.34)

        # ------------------ BEAT A4.B2 | 21.94-25.50 s ------------------
        # Inset showing three discrete energy packets E = hf on the filament.
        inset_box = Rectangle(width=2.4, height=1.2, color=WHITE,
                              stroke_opacity=0.7).round_corners(0.08)
        inset_box.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        inset_title = Text("E = hf", color=GOLD).scale(0.32)
        inset_title.next_to(inset_box, UP, buff=0.12)

        packet_inset = VGroup()
        for i in range(3):
            sq = Square(side_length=0.18, fill_opacity=0.9,
                        fill_color=GOLD, stroke_opacity=0)
            sq.move_to(inset_box.get_center() + LEFT * 0.7 + RIGHT * i * 0.7
                       + DOWN * 0.05)
            packet_inset.add(sq)
        arrows_in = VGroup()
        for sq in packet_inset:
            a = Arrow(filament.get_center() + UP * 0.1, sq.get_bottom(),
                      color=ORANGE, stroke_width=2, buff=0.05,
                      max_tip_length_to_length_ratio=0.25)
            arrows_in.add(a)
        ehf_eq = MathTex(r"E = h f", color=GOLD).scale(0.55)
        ehf_eq.move_to(inset_box.get_center())
        self.play(
            FadeIn(inset_box),
            FadeIn(inset_title),
            LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in packet_inset],
                        lag_ratio=0.15),
            LaggedStart(*[GrowArrow(a) for a in arrows_in], lag_ratio=0.15),
            FadeIn(ehf_eq),
            run_time=2.8,
        )
        self.wait(0.76)

        # ------------------ BEAT A5.B1 | 25.50-30.00 s ------------------
        # Hero frame: combine RJ (faded), Planck, measured spectrum, peak
        # marker, T readout, and the centered caption.
        hero_caption = Text("Planck resolves the UV catastrophe",
                            color=WHITE).scale(0.5)
        hero_caption.to_edge(UP, buff=0.4)
        hero_eq = MathTex(
            r"I_{\mathrm{P}}(\lambda)=\frac{2hc^{2}}{\lambda^{5}}"
            r"\frac{1}{e^{hc/\lambda k T}-1}",
            color=YELLOW,
        ).scale(0.45)
        hero_eq.next_to(hero_caption, DOWN, buff=0.15)

        self.play(
            spectrum_lines.animate.set_opacity(1.0),
            planck.animate.set_stroke(width=6),
            FadeIn(hero_caption, shift=DOWN * 0.1),
            FadeIn(hero_eq, shift=UP * 0.1),
            run_time=1.3,
        )
        self.wait(3.2)