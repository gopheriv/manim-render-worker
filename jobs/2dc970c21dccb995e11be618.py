from manim import *
import math

h = 6.62607015e-34
c = 299792458.0
k_B = 1.380649e-23
b_Wien = 2.897771955e-3


def blackbody_lambda(lam_um, temperature):
    """Planck spectral radiance per wavelength, evaluated stably."""
    lam_m = lam_um * 1e-6
    exponent = h * c / (lam_m * k_B * temperature)
    if exponent > 700:
        return 0.0
    return (2 * h * c**2 / lam_m**5) / math.expm1(exponent)


def planck_relative(lam_um, temperature):
    """B_lambda divided by its own peak, so every curve is readable."""
    peak_um = b_Wien * 1e6 / temperature
    peak_radiance = blackbody_lambda(peak_um, temperature)
    return blackbody_lambda(lam_um, temperature) / peak_radiance


def rayleigh_jeans_relative(lam_um, temperature):
    """Classical B_lambda^RJ, shown on the same relative scale."""
    lam_m = lam_um * 1e-6
    peak_um = b_Wien * 1e6 / temperature
    peak_radiance = blackbody_lambda(peak_um, temperature)
    classical = 2 * c * k_B * temperature / lam_m**4
    return min(classical / peak_radiance, 1.16)


class AetherLabScene(Scene):
    def construct(self):
        self.camera.background_color = "#0A1020"
        amber = "#FFB454"
        gold = "#FFD27A"
        cyan = "#75D6F5"
        coral = "#FF8878"
        muted = "#8792A8"
        white = "#F4F6FB"

        # BEAT A1.B1 | 0.00-2.00 s
        title = Text("Why hot objects glow", color=white, font_size=38, weight=BOLD)
        title.move_to(UP * 3.35)
        subtitle = Text("Thermal radiation carries a hidden spectrum", color=muted, font_size=26)
        subtitle.next_to(title, DOWN, buff=0.16)
        cavity = Rectangle(width=1.7, height=2.65, color=cyan, stroke_width=2, stroke_opacity=0.45)
        cavity.move_to(RIGHT * 4.25 + DOWN * 0.15)
        filament = Line(RIGHT * 4.25 + UP * 1.0, RIGHT * 4.25 + DOWN * 1.25, color=amber, stroke_width=6)
        self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(subtitle), Create(cavity), Create(filament), run_time=1.2)
        self.wait(0.8)

        # BEAT A1.B2 | 2.00-3.80 s
        self.play(filament.animate.set_color(gold).set_stroke(width=8), run_time=0.8)
        self.wait(1.0)

        # BEAT A1.B3 | 3.80-5.50 s
        temperature = Text("T = 3000 K", color=gold, font_size=30)
        temperature.move_to(RIGHT * 4.25 + DOWN * 2.05)
        self.play(FadeIn(temperature, shift=UP * 0.12), run_time=0.5)
        self.wait(1.2)

        # BEAT A2.B1 | 5.50-8.10 s
        axes = Axes(
            x_range=[0, 3.0, 0.5],
            y_range=[0, 1.2, 0.2],
            x_length=7.0,
            y_length=3.35,
            axis_config={"color": muted, "stroke_opacity": 0.65},
            tips=False,
        )
        axes.move_to(LEFT * 1.25 + DOWN * 0.55)
        x_label = Text("Wavelength (micrometers)", color=muted, font_size=26)
        x_label.next_to(axes.x_axis, DOWN, buff=0.18)
        y_label = Text("Relative radiance", color=muted, font_size=24)
        y_label.rotate(90 * DEGREES).next_to(axes.y_axis, LEFT, buff=0.2)
        rj_curve = axes.plot(
            lambda lam: rayleigh_jeans_relative(lam, 3000),
            x_range=[0.05, 3.0], color=cyan, stroke_width=3,
        )
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.3)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=0.9)
        self.play(Create(rj_curve), run_time=0.8)
        self.wait(0.6)

        # BEAT A2.B2 | 8.10-9.70 s
        uv_label = Text("Rayleigh-Jeans diverges as wavelength -> 0", color=cyan, font_size=25)
        uv_label.move_to(UP * 1.72 + LEFT * 1.1)
        uv_arrow = Arrow(
            uv_label.get_bottom(), axes.c2p(0.13, 1.1),
            color=cyan, buff=0.12, stroke_width=2.5,
        )
        self.play(FadeIn(uv_label, shift=DOWN * 0.1), Create(uv_arrow), run_time=0.5)
        self.wait(1.1)

        # BEAT A2.B3 | 9.70-11.50 s
        self.play(
            filament.animate.set_opacity(0.38), cavity.animate.set_opacity(0.25),
            temperature.animate.set_opacity(0.4),
            run_time=0.5,
        )
        self.wait(1.3)

        # BEAT A3.B1 | 11.50-14.50 s
        planck_curve = axes.plot(
            lambda lam: planck_relative(lam, 3000),
            x_range=[0.05, 3.0], color=amber, stroke_width=4,
        )
        self.play(FadeOut(uv_label), FadeOut(uv_arrow), run_time=0.25)
        self.play(Create(planck_curve), run_time=1.55)
        self.wait(1.2)

        # BEAT A3.B2 | 14.50-17.00 s
        peak_3000 = b_Wien * 1e6 / 3000
        peak_dot = Dot(color=gold, radius=0.085).move_to(axes.c2p(peak_3000, 1.0))
        guide_line = DashedLine(
            axes.c2p(peak_3000, 0), axes.c2p(peak_3000, 1.0),
            color=gold, stroke_width=2,
        )
        peak_label = Text("lambda_max = 0.97 um", color=gold, font_size=25)
        peak_label.move_to(LEFT * 1.25 + UP * 1.55)
        self.play(FadeIn(peak_dot), Create(guide_line), FadeIn(peak_label), run_time=0.7)
        self.wait(1.8)

        # BEAT A3.B3 | 17.00-19.00 s
        peak_4500 = b_Wien * 1e6 / 4500
        planck_4500 = axes.plot(
            lambda lam: planck_relative(lam, 4500),
            x_range=[0.05, 3.0], color=amber, stroke_width=4,
        )
        rj_4500 = axes.plot(
            lambda lam: rayleigh_jeans_relative(lam, 4500),
            x_range=[0.05, 3.0], color=cyan, stroke_width=3,
        )
        guide_4500 = DashedLine(
            axes.c2p(peak_4500, 0), axes.c2p(peak_4500, 1.0),
            color=gold, stroke_width=2,
        )
        peak_label_4500 = Text("lambda_max = 0.64 um", color=gold, font_size=25)
        peak_label_4500.move_to(LEFT * 1.25 + UP * 1.55)
        temperature_4500 = Text("T = 4500 K", color=gold, font_size=30)
        temperature_4500.move_to(temperature.get_center())
        self.play(
            Transform(planck_curve, planck_4500),
            Transform(rj_curve, rj_4500),
            peak_dot.animate.move_to(axes.c2p(peak_4500, 1.0)),
            Transform(guide_line, guide_4500),
            Transform(peak_label, peak_label_4500),
            Transform(temperature, temperature_4500),
            filament.animate.set_color(amber).set_opacity(0.85),
            run_time=1.2,
        )
        self.wait(0.8)

        # BEAT A4.B1 | 19.00-21.80 s
        self.play(
            planck_curve.animate.set_stroke(width=4.5),
            rj_curve.animate.set_stroke(opacity=0.82),
            run_time=1.0,
        )
        self.wait(1.8)

        # BEAT A4.B2 | 21.80-24.00 s
        equation = MathTex(
            r"B_{\lambda}(T)=\frac{2hc^2}{\lambda^5"
            r"\left(e^{hc/(\lambda k_BT)}-1\right)}",
            color=gold,
        ).scale(0.72)
        equation.move_to(UP * 2.7)
        self.play(FadeIn(equation, shift=DOWN * 0.12), run_time=0.8)
        self.wait(1.4)

        # BEAT A4.B3 | 24.00-25.50 s
        hero = Text("Quantization keeps the spectrum finite", color=white, font_size=30)
        hero.move_to(UP * 1.75)
        self.play(FadeOut(peak_label), FadeIn(hero, shift=DOWN * 0.1), peak_dot.animate.scale(1.22), run_time=0.5)
        self.play(peak_dot.animate.scale(1 / 1.22), run_time=0.2)
        self.wait(0.8)

        # BEAT A5.B1 | 25.50-27.30 s
        classical_planck_legend = VGroup(
            VGroup(Line(LEFT * 0.28, RIGHT * 0.28, color=cyan, stroke_width=4),
                   Text("Classical: diverges", color=cyan, font_size=25)).arrange(RIGHT, buff=0.18),
            VGroup(Line(LEFT * 0.28, RIGHT * 0.28, color=amber, stroke_width=4),
                   Text("Planck: finite", color=amber, font_size=25)).arrange(RIGHT, buff=0.18),
        ).arrange(RIGHT, buff=0.55).move_to(UP * 2.05)
        self.play(
            FadeOut(equation), FadeOut(hero),
            FadeOut(cavity), FadeOut(filament), FadeOut(temperature),
            FadeIn(classical_planck_legend), run_time=0.6,
        )
        self.wait(1.2)

        # BEAT A5.B2 | 27.30-29.00 s
        planck_6000 = axes.plot(
            lambda lam: planck_relative(lam, 6000),
            x_range=[0.05, 3.0], color=coral, stroke_width=3.5,
        )
        peak_6000 = b_Wien * 1e6 / 6000
        peak_dot_6000 = Dot(color=coral, radius=0.08).move_to(axes.c2p(peak_6000, 1.0))
        temp_legend = VGroup(
            VGroup(Line(LEFT * 0.25, RIGHT * 0.25, color=amber, stroke_width=4),
                   Text("4500 K - peak 0.64 um", color=amber, font_size=22)).arrange(RIGHT, buff=0.14),
            VGroup(Line(LEFT * 0.25, RIGHT * 0.25, color=coral, stroke_width=4),
                   Text("6000 K - peak 0.48 um", color=coral, font_size=22)).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(RIGHT * 4.45 + UP * 0.15)
        self.play(
            FadeOut(classical_planck_legend), FadeOut(rj_curve), Create(planck_6000),
            FadeIn(peak_dot_6000), FadeIn(temp_legend), run_time=0.9,
        )
        self.wait(0.8)

        # BEAT A5.B3 | 29.00-30.00 s
        final_title = Text("Hotter objects peak at shorter wavelengths", color=white, font_size=30)
        final_title.move_to(UP * 3.25)
        self.play(FadeIn(final_title, shift=DOWN * 0.1), peak_dot_6000.animate.scale(1.18), run_time=0.4)
        self.play(peak_dot_6000.animate.scale(1 / 1.18), run_time=0.2)
        self.wait(0.4)
