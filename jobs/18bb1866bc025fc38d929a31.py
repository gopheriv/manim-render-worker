"""
Blackbody Radiation: Planck's law, Wien's displacement, UV catastrophe.
Visual concept: a glowing rod heats through four temperatures while Planck
curves grow and shift blueward, then a divergent Rayleigh-Jeans curve
crashes off-screen at short wavelengths.
"""
from manim import *
import numpy as np
import math


def eq(tex, plain, size=34, color=WHITE, width=13.0):
    try:
        m = MathTex(tex, font_size=size, color=color)
    except Exception:
        m = Text(plain, font_size=int(size * 0.72), color=color)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


class AetherLabScene(Scene):
    def construct(self):
        # ===== Constants from brief =====
        b_const = 0.002898
        c_const = 2.998e8
        h_const = 6.626e-34
        k_const = 1.381e-23
        sigma_const = 5.67e-8
        x_max = 4.9651

        temps = [1000, 3000, 6000, 10000]
        lambda_max_nm = [2898, 966, 483, 289.8]
        rod_colors = ["#7F1D1D", "#F97316", "#FDE047", "#BFDBFE"]
        planck_colors = ["#EF4444", "#F97316", "#FACC15", "#60A5FA"]

        # ===== Beat 1: Title + Planck formula (0-4s) =====
        title = Text("Blackbody Radiation", color="#F8FAFC").scale(0.55).to_edge(UP)

        planck_eq = eq(
            r"B(\lambda, T) = \dfrac{2\,h\,c^{2}}{\lambda^{5}\!\left(e^{\,h c/(\lambda k T)} - 1\right)}",
            "B(λ,T) = 2hc² / [λ⁵(e^(hc/λkT) − 1)]",
            size=30, color="#22D3EE", width=11.5
        )
        planck_eq.next_to(title, DOWN, buff=0.25)

        self.play(
            Write(title),
            FadeIn(planck_eq, shift=UP * 0.15),
            run_time=1.4
        )
        self.wait(0.7)

        # ===== Beat 2: Stage reveal (rod + ribbon + axes) (4-8s) =====
        planck_eq.generate_target()
        planck_eq.target.scale(0.55).to_corner(UL, buff=0.35).shift(DOWN * 0.3)

        rod = Rectangle(width=0.55, height=4.2, fill_opacity=1.0,
                        fill_color=rod_colors[0], stroke_width=0).set_stroke(WHITE, 0.5)
        rod.move_to(np.array([-5.6, -0.4, 0.0]))
        rod_label = Text("T", color="#F8FAFC").scale(0.32).next_to(rod, DOWN, buff=0.08)
        rod_k = Text("1000 K", color="#F8FAFC").scale(0.30).next_to(rod_label, DOWN, buff=0.05)

        ribbon_width = 5.6
        ribbon_bg = Rectangle(width=ribbon_width, height=0.32,
                              fill_color="#111827", fill_opacity=1.0, stroke_width=0)
        ribbon_bg.move_to(np.array([-5.6, 3.05, 0.0]))

        grad_steps = 60
        grad_width = ribbon_width / grad_steps
        grad = VGroup()
        for i in range(grad_steps):
            t = i / (grad_steps - 1)
            if t < 0.25:
                col = interpolate_color(BLACK, "#7F1D1D", t / 0.25)
            elif t < 0.5:
                col = interpolate_color("#7F1D1D", "#F97316", (t - 0.25) / 0.25)
            elif t < 0.75:
                col = interpolate_color("#F97316", "#FDE047", (t - 0.5) / 0.25)
            else:
                col = interpolate_color("#FDE047", "#BFDBFE", (t - 0.75) / 0.25)
            seg = Rectangle(width=grad_width + 0.01, height=0.30,
                            fill_color=col, fill_opacity=1.0, stroke_width=0)
            seg.move_to(ribbon_bg.get_left() + np.array([grad_width * (i + 0.5), 0, 0]))
            grad.add(seg)
        grad.move_to(ribbon_bg.get_center())
        ribbon_caption = Text("perceived color", color="#94A3B8").scale(0.22)
        ribbon_caption.next_to(ribbon_bg, DOWN, buff=0.10)

        t_tracker = ValueTracker(0.05)
        ribbon_dot = always_redraw(lambda: Dot(
            ribbon_bg.get_left() + np.array([ribbon_width * t_tracker.get_value(), 0, 0]),
            color=WHITE, radius=0.09, stroke_width=1.5))

        axes = Axes(
            x_range=[200, 3200, 400],
            y_range=[0, 1.05, 0.25],
            x_length=9.0, y_length=3.6,
            tips=False,
            axis_config={"stroke_color": "#94A3B8", "stroke_width": 2,
                         "include_tip": False, "include_numbers": False}
        ).scale(0.85)
        axes.shift(np.array([2.5, -0.6, 0.0]))
        x_label = Text("λ (nm)", color="#94A3B8").scale(0.26).next_to(axes.x_axis, RIGHT, buff=0.15)
        y_label = Text("B(λ,T)", color="#94A3B8").scale(0.26).next_to(axes.y_axis, UP, buff=0.15)

        rod_group = VGroup(rod, rod_label, rod_k)
        ribbon_group = VGroup(ribbon_bg, grad, ribbon_caption)

        self.play(
            MoveToTarget(planck_eq),
            FadeIn(rod_group, shift=UP * 0.2),
            FadeIn(ribbon_group, shift=DOWN * 0.15),
            Create(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=1.6
        )
        self.add(ribbon_dot)
        self.wait(0.3)

        # ===== Beat 3: Quantum idea (8-13s) =====
        q1 = eq(r"E_{n} = n\,h\,\nu", "Eₙ = n·h·ν", size=30, color="#F8FAFC")
        q1.to_corner(UL, buff=0.4).shift(RIGHT * 4.5 + DOWN * 0.3)
        q2 = eq(
            r"\langle E \rangle = \dfrac{h\,\nu}{e^{\,h\nu/(k T)} - 1}",
            "⟨E⟩ = hν / (e^(hν/kT) − 1)",
            size=26, color="#22D3EE"
        )
        q2.next_to(q1, DOWN, buff=0.25).align_to(q1, LEFT)
        q2_note = Text("(→ kT classically — diverges)", color="#F59E0B").scale(0.24)
        q2_note.next_to(q2, DOWN, buff=0.14).align_to(q2, LEFT)

        self.play(
            FadeIn(q1, shift=RIGHT * 0.2),
            FadeIn(q2, shift=RIGHT * 0.2),
            FadeIn(q2_note),
            run_time=1.0
        )
        self.wait(0.7)
        self.play(FadeOut(q1), FadeOut(q2), FadeOut(q2_note), run_time=0.5)

        # ===== Beat 4: Heat through 4 temperatures (13-22s) =====
        def planck_curve(T, amp):
            def f(lam_nm):
                lam = lam_nm * 1e-9
                expo = h_const * c_const / (lam * k_const * T)
                if expo > 700:
                    return 0.0
                denom = math.expm1(expo)
                if denom <= 0:
                    return 0.0
                B = (2 * h_const * c_const ** 2) / (lam ** 5 * denom)
                return B * amp
            return f

        ref = (1000 ** 5)
        amps = [0.30 * (T ** 5) / ref for T in temps]

        curves = VGroup()
        peak_dots = VGroup()
        peak_val_labels = VGroup()
        for i, T in enumerate(temps):
            col = planck_colors[i]
            amp = amps[i]
            curve = axes.plot(planck_curve(T, amp), x_range=[220, 3000],
                              color=col, stroke_width=2.4)
            curves.add(curve)
            lam_pk = lambda_max_nm[i]
            y_pk = planck_curve(T, amp)(lam_pk)
            dot = Dot(axes.c2p(lam_pk, y_pk), color=WHITE, radius=0.07,
                      stroke_width=1.5)
            peak_dots.add(dot)
            pk_txt = Text(f"{lam_pk:g} nm", color=col).scale(0.24)
            pk_txt.next_to(axes.c2p(lam_pk, y_pk), UP, buff=0.10)
            peak_val_labels.add(pk_txt)

        new_rod = rod.copy().set_fill(rod_colors[0])

        self.play(
            Transform(rod, new_rod),
            Create(curves[0]),
            t_tracker.animate.set_value(0.05),
            FadeIn(peak_dots[0], scale=0.6),
            FadeIn(peak_val_labels[0], shift=UP * 0.1),
            run_time=1.6
        )
        self.wait(0.3)

        # Stages 2-4 consolidated: animate rod + label + ribbon + new curve together
        for i in range(1, 4):
            new_rod_i = rod.copy().set_fill(rod_colors[i])
            new_label_i = Text(f"{temps[i]} K", color="#F8FAFC").scale(0.30)
            new_label_i.next_to(rod_label, DOWN, buff=0.05)
            t_pos = 0.05 + 0.90 * (i / (len(temps) - 1))
            self.play(
                Transform(rod, new_rod_i),
                Transform(rod_k, new_label_i),
                t_tracker.animate.set_value(t_pos),
                Create(curves[i]),
                FadeIn(peak_dots[i], scale=0.6),
                FadeIn(peak_val_labels[i], shift=UP * 0.1),
                run_time=1.6
            )

        # ===== Beat 5: Wien's law (22-26s) =====
        self.play(FadeOut(peak_val_labels), run_time=0.4)

        wien_block = VGroup(
            eq(
                r"\dfrac{d B}{d\lambda} = 0 \;\;\Rightarrow\;\; x_{\max} \approx 4.9651",
                "dB/dλ = 0  →  x_max ≈ 4.9651",
                size=22, color="#F8FAFC", width=10
            ),
            eq(
                r"\lambda_{\max}\,T = \dfrac{h c}{x_{\max}\,k} = b \approx 2.898\times10^{-3}\,\text{m·K}",
                "λ_max·T = b ≈ 2.898×10⁻³ m·K",
                size=24, color="#F59E0B", width=10
            ),
            eq(
                r"B_{\text{peak}} \propto T^{5}, \quad F = \sigma\,T^{4},\ \sigma = 5.67\times10^{-8}",
                "B_peak ∝ T⁵,   F = σT⁴",
                size=22, color="#22D3EE", width=10
            ),
        ).arrange(DOWN, buff=0.22).to_edge(LEFT, buff=0.4).shift(UP * 1.2)

        self.play(FadeIn(wien_block, shift=UP * 0.15), run_time=1.2)
        self.wait(0.7)

        # ===== Beat 6: UV catastrophe (26-30s) =====
        self.play(
            FadeOut(wien_block),
            FadeOut(rod_group), FadeOut(ribbon_group), FadeOut(ribbon_caption),
            FadeOut(planck_eq),
            run_time=0.6
        )

        # Bring axes to center for the catastrophe
        axes.move_to(np.array([0.0, -0.3, 0.0]))
        x_label.next_to(axes.x_axis, RIGHT, buff=0.15)
        y_label.next_to(axes.y_axis, UP, buff=0.15)

        uv_title = Text("UV Catastrophe (T = 6000 K)", color="#EF4444").scale(0.34)
        uv_title.to_edge(UP, buff=0.4)

        def rj_curve(T, amp):
            def f(lam_nm):
                lam = lam_nm * 1e-9
                if lam <= 0:
                    return 0.0
                return 2 * c_const * k_const * T / (lam ** 4) * amp
            return f

        rj_amp = 1.4e-16
        rj = axes.plot(rj_curve(6000, rj_amp), x_range=[220, 3000],
                       color="#EF4444", stroke_width=2.4, use_smoothing=False)

        cmp = VGroup(
            Text("λ = 200 nm, T = 6000 K", color="#F8FAFC").scale(0.26),
            Text("B_RJ = 2 c k T / λ⁴ ≈ 3.10×10¹⁶", color="#EF4444").scale(0.26),
            Text("B_Planck ≈ 2.31×10¹¹", color="#22D3EE").scale(0.26),
            Text("RJ is ~1.34×10⁵ × larger  (UV catastrophe)", color="#F59E0B").scale(0.26),
        ).arrange(DOWN, buff=0.16).to_edge(LEFT, buff=0.5).shift(DOWN * 1.3)

        self.play(FadeIn(uv_title), Create(rj), run_time=1.4)
        self.play(FadeIn(cmp, shift=UP * 0.1), run_time=0.8)

        # Live tracer riding the RJ curve — keeps motion into the final seconds
        live_x = ValueTracker(220)
        live_dot = always_redraw(lambda: Dot(
            axes.c2p(live_x.get_value(), rj_curve(6000, rj_amp)(live_x.get_value())),
            color="#F8FAFC", radius=0.08))
        self.add(live_dot)
        self.play(live_x.animate.set_value(900), run_time=2.4, rate_func=linear)
        self.wait(0.3)