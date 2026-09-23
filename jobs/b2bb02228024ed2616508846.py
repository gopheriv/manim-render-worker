from manim import *
import numpy as np
import math

# Physical constants (SI)
H_PLANCK = 6.62607015e-34
K_BOLTZ = 1.380649e-23
C_LIGHT = 2.99792458e8

# Helpers
def planck_blambda(lam_m, T):
    num = 2.0 * H_PLANCK * C_LIGHT ** 2 / (lam_m ** 5)
    expo = H_PLANCK * C_LIGHT / (lam_m * K_BOLTZ * T)
    return num / (math.exp(expo) - 1.0)

def rj_blambda(lam_m, T):
    return 2.0 * C_LIGHT * K_BOLTZ * T / (lam_m ** 4)

def wien_peak_nm(T):
    # Wien displacement: lambda_max * T = 2.897771955e-3 m K
    return 2.897771955e-3 / T * 1e9

def kelvin_to_rgb_hex(T):
    """Approximate blackbody color (2000-12000 K) → hex."""
    T = max(1000.0, min(12000.0, T))
    t = (T - 1000.0) / 11000.0
    # blend black->deep red->orange->white
    def smoothstep(a, b, x):
        x = np.clip((x - a) / (b - a), 0.0, 1.0)
        return x * x * (3 - 2 * x)
    r = smoothstep(0.0, 0.55, t) + 0.15 * smoothstep(0.55, 1.0, t)
    g = 0.05 * smoothstep(0.0, 0.45, t) + smoothstep(0.45, 1.0, t)
    b = smoothstep(0.45, 1.0, t)
    r, g, b = np.clip(r, 0, 1), np.clip(g, 0, 1), np.clip(b, 0, 1)
    return "#{:02X}{:02X}{:02X}".format(int(r*255), int(g*255), int(b*255))

NARRATION = (
    "A piece of metal, heated until it glows, becomes a perfect blackbody — and speaks to us in light.",
    "Plotting spectral radiance against wavelength reveals a curve that peaks, falls, and obeys a strict law.",
    "Crank the temperature up and the peak slides toward the blue, brighter and brighter — Wien's law in motion.",
    "Classical physics predicts a runaway ultraviolet catastrophe; only quantized oscillator energies, E = n h nu, tame the curve.",
    "Planck's law: B_lambda equals two h c squared over lambda to the fifth, divided by e to the h c over lambda k T, minus one.",
)


class AetherLabScene(Scene):
    def construct(self):
        BLACK = "#000000"
        PRIMARY = "#FFD27F"
        SECONDARY = "#5FA8E0"
        ACCENT = "#FF6B5B"
        FACE = "#F8FAFC"

        camera_bg = "#0A0A12"
        self.camera.background_color = camera_bg

        # ---------- Persistence groups (act-lifetime mobjects) ----------
        hook_layer = VGroup()         # bell jar + coil + bloom + title
        readout_layer = VGroup()      # upper-left readouts
        plot_layer = VGroup()         # axes + Planck + ghost + Wien tick + annotation
        ladder_layer = VGroup()       # quantized ladder + packets
        triptych_layer = VGroup()     # hero frame composition
        recap_layer = VGroup()
        idle_layer = VGroup()

        # ============================================================
        # ACT 1 — HOOK  (≈4 s)
        # ============================================================
        bell = Circle(radius=1.6, color=PRIMARY, stroke_width=2, stroke_opacity=0.4).move_to(LEFT * 3.4)
        bell_base = Line(LEFT * 5.0 + DOWN * 1.7, RIGHT * 1.2 + DOWN * 1.7,
                         color=GREY_D, stroke_width=3).move_to([bell.get_x(), bell.get_y() - 1.6, 0])
        coil = ParametricFunction(
            lambda t: np.array([
                bell.get_x() + 0.85 * math.sin(8 * t),
                bell.get_y() + 0.45 * math.cos(8 * t) * 0.6,
                0.0
            ]),
            t_range=[0, TAU], color=GREY_E, stroke_width=6,
        )
        coil.move_to(bell.get_center())
        coil_start_x = coil.get_x()
        coil_start_y = coil.get_y()
        coil_width = coil.width
        coil_height = coil.height
        bloom_center = bell.get_center()
        bloom_radius_max = 1.7
        # Use a circle "glow" via concentric translucent discs
        bloom_cores = VGroup(*[
            Circle(radius=r, color="#FFE9B0", fill_opacity=0.05, stroke_width=0)
            for r in [1.7, 1.4, 1.1, 0.85]
        ]).move_to(bloom_center)
        halo = Circle(radius=bloom_radius_max, color="#FFEDC6", stroke_width=1,
                      stroke_opacity=0.0).move_to(bloom_center)
        hook_layer.add(bell, bell_base, coil, bloom_cores, halo)
        self.add(hook_layer)

        title_card = Text("Blackbody Radiation", color=PRIMARY, weight=BOLD).scale(0.7)
        title_card.move_to(ORIGIN)
        title_card.set_opacity(0)

        # Ignite coil — color & halo bloom
        coil_color_tracker = ValueTracker(5800.0)
        coil.set_color(kelvin_to_rgb_hex(coil_color_tracker.get_value()))

        def bloom_updater(mob):
            # halo radius modulated by a tracker; we handcraft shimmer visually below
            pass

        # Custom dynamic: re-color coil from a tracker each frame (cheap rebuild of color)
        coil.add_updater(lambda m: m.set_color(
            kelvin_to_rgb_hex(coil_color_tracker.get_value())
        ))
        # Coil brightness via opacity oscillating — done in idle loop later.
        # For "ignition", animate color and halo stroke opacity.
        halo_stroke = ValueTracker(0.0)
        halo.add_updater(lambda m: m.set_stroke(opacity=halo_stroke.get_value()))

        self.play(FadeIn(bell, scale=0.6), FadeIn(bell_base),
                  run_time=0.6)
        # Warm up by raising an "ignite" tracker
        ignite = ValueTracker(0.0)
        def color_at_ignite(v):
            # ramp 800K -> 5800K across [0,1]
            return 800.0 + v * 5000.0
        coil_color_tracker.set_value(color_at_ignite(0.0))
        coil_color_updater = coil_color_tracker
        coil_color_updater.add_updater(lambda tr: tr.set_value(
            color_at_ignite(ignite.get_value())
        ))
        self.play(ignite.animate.set_value(1.0),
                  halo_stroke.animate.set_value(0.6),
                  FadeIn(bloom_cores, scale=0.5),
                  run_time=2.2, rate_func=smooth)
        # Title whisper
        self.play(title_card.animate.set_opacity(1).scale(1.05).set_opacity(0).scale(1.0/1.05),
                  run_time=0.8, rate_func=smooth)
        # Actually we want a soft title fade-in/out (set opacity then to 0); redo cleanly:
        title_card.set_opacity(0)
        self.play(title_card.animate.set_opacity(1), run_time=0.6)
        self.play(title_card.animate.set_opacity(0).move_to(UP*0.2), run_time=0.6)
        # Remove ignite updater to stop further color drift during hook
        coil_color_updater.remove_updater(coil_color_updater.updaters[-1])

        # Readouts at upper-left
        temperature_tracker = ValueTracker(5800.0)
        peak_wl_tracker = ValueTracker(wien_peak_nm(5800.0))
        peak_rad_tracker = ValueTracker(planck_blambda(wien_peak_nm(5800.0)*1e-9, 5800.0))

        readout_anchor = UP * 2.6 + LEFT * 5.6
        def make_readout_block():
            head = Text("LIVE READOUTS", color=GREY_B).scale(0.28)
            head.next_to(readout_anchor, DOWN, buff=0.05).align_to(readout_anchor, LEFT)
            t_lbl = Text("temperature", color=GREY_B).scale(0.24)
            t_val = always_redraw(lambda: DecimalNumber(
                temperature_tracker.get_value(), num_decimal_places=0,
                color=FACE).scale(0.32))
            t_unit = Text("K", color=GREY_B).scale(0.22)
            t_row = VGroup(t_lbl, t_val, t_unit).arrange(RIGHT, buff=0.1).next_to(head, DOWN, buff=0.08, aligned_edge=LEFT)

            wl_lbl = Text("peak_wavelength", color=GREY_B).scale(0.24)
            wl_val = always_redraw(lambda: DecimalNumber(
                peak_wl_tracker.get_value(), num_decimal_places=0,
                color=FACE).scale(0.32))
            wl_unit = Text("nm", color=GREY_B).scale(0.22)
            wl_row = VGroup(wl_lbl, wl_val, wl_unit).arrange(RIGHT, buff=0.1).next_to(t_row, DOWN, buff=0.06, aligned_edge=LEFT)

            L_lbl = Text("spectral_radiance", color=GREY_B).scale(0.24)
            L_val = always_redraw(lambda: DecimalNumber(
                peak_rad_tracker.get_value() / 1e13, num_decimal_places=2,
                color=FACE).scale(0.32))
            L_unit = Text("×10¹³ W·m⁻³·sr⁻¹", color=GREY_B).scale(0.22)
            L_row = VGroup(L_lbl, L_val, L_unit).arrange(RIGHT, buff=0.1).next_to(wl_row, DOWN, buff=0.06, aligned_edge=LEFT)

            grp = VGroup(head, t_row, wl_row, L_row)
            return grp

        readouts = make_readout_block()
        readout_layer.add(readouts)
        self.play(FadeIn(readouts, shift=RIGHT*0.2), run_time=0.8)

        # ============================================================
        # ACT 2 — ESTABLISH  (≈6 s)
        # ============================================================
        # Transition hook_layer outward: coil to left third, plot slides in
        # First, fade out readouts into a new persistent placement
        # Keep readouts visible — just slide them up to corner for plot area.
        new_readout_pos = UP * 3.2 + LEFT * 5.7
        self.play(readouts.animate.scale(0.8).move_to(new_readout_pos),
                  coil.animate.scale(0.6).move_to(LEFT * 4.6),
                  bell.animate.scale(0.7).move_to(LEFT * 4.6),
                  bloom_cores.animate.scale(0.6).move_to(LEFT * 4.6),
                  halo.animate.scale(0.6).move_to(LEFT * 4.6),
                  bell_base.animate.scale(0.7).move_to(LEFT * 4.6 + DOWN * 1.1),
                  run_time=1.4)

        # Build plot axes
        ax = Axes(
            x_range=[200, 3000, 400],
            y_range=[0, 1.05e14, 2e13],
            x_length=7.2, y_length=3.8,
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 1.5,
                         "include_numbers": False},
        ).move_to(RIGHT * 1.6 + DOWN * 0.3)
        x_label = Text("wavelength (nm)", color=GREY_B).scale(0.28).next_to(ax.x_axis, DOWN, buff=0.18)
        y_label = Text("spectral radiance (W·m⁻³·sr⁻¹)", color=GREY_B).scale(0.24)
        y_label.rotate(PI/2).next_to(ax.y_axis, LEFT, buff=0.18)

        # Custom x-axis numbers (nm)
        x_num_pos = [400, 1000, 1600, 2200, 2800]
        x_nums = VGroup(*[
            Text(str(v), color=GREY_B, font="monospace").scale(0.22)
            .move_to(ax.c2p(v, 0) + DOWN * 0.22) for v in x_num_pos
        ])
        y_num_pos = [0, 2e13, 4e13, 6e13, 8e13, 1.0e14]
        def fmt(v):
            if v == 0:
                return "0"
            return f"{int(round(v/1e13))}×10¹³"
        y_nums = VGroup(*[
            Text(fmt(v), color=GREY_B, font="monospace").scale(0.20)
            .move_to(ax.c2p(200, v) + LEFT * 0.32) for v in y_num_pos
        ])

        plot_layer.add(ax, x_label, y_label, x_nums, y_nums)
        self.play(FadeIn(ax), FadeIn(x_label), FadeIn(y_label), FadeIn(x_nums), FadeIn(y_nums),
                  run_time=1.0)

        # Planck curve (T = 5800K)
        nm_to_xv = lambda nm: nm  # x is nm directly

        def planck_nm_to_y(nm, T):
            lam_m = nm * 1e-9
            return planck_blambda(lam_m, T)

        def rj_nm_to_y(nm, T):
            lam_m = nm * 1e-9
            return rj_blambda(lam_m, T)

        curve_max_for_T = 5800.0
        planck_curve = ax.plot(
            lambda nm: planck_nm_to_y(nm, 5800.0),
            x_range=[200, 3000, 8],
            color=PRIMARY, stroke_width=4,
        )
        rj_curve = ax.plot(
            lambda nm: rj_nm_to_y(nm, 5800.0),
            x_range=[200, 3000, 8],
            color=SECONDARY, stroke_width=1.5,
        )
        rj_curve.set_stroke(opacity=0.0)

        wien_x = always_redraw(lambda: peak_wl_tracker.get_value())
        wien_tick = always_redraw(lambda: Line(
            ax.c2p(wien_x.get_value(), 0),
            ax.c2p(wien_x.get_value(), ax.y_axis.y_range[1]),
            color=ACCENT, stroke_width=1.5, stroke_opacity=0.85,
        ))
        wien_label_text = "Wien peak: 500 nm"
        wien_label = always_redraw(lambda: Text(
            "{:.0f} nm".format(peak_wl_tracker.get_value()),
            color=ACCENT, weight=BOLD).scale(0.26).next_to(
            ax.c2p(wien_x.get_value(), ax.y_axis.y_range[1]*0.92), UP, buff=0.08))
        plot_layer.add(planck_curve, wien_tick, wien_label)

        self.play(Create(planck_curve), run_time=1.6)
        self.add(wien_tick, wien_label)

        # Ghost: equipartition dotted horizontal reference at kT ~ 4.07e-20 J → note as text
        eq_line = DashedLine(
            ax.c2p(200, planck_blambda(500e-9, 5800.0)*0.6),
            ax.c2p(3000, planck_blambda(500e-9, 5800.0)*0.6),
            color=GREY_A, stroke_width=1, dash_length=0.06,
        ).set_stroke(opacity=0.5)
        eq_label = Text("k_B T equipartition", color=GREY_A).scale(0.22).next_to(
            eq_line, RIGHT, buff=0.1).set_opacity(0.55)
        rj_curve.set_stroke(opacity=0.55)
        rj_curve.set_color(SECONDARY)
        plot_layer.add(rj_curve, eq_line, eq_label)
        self.play(FadeIn(rj_curve), FadeIn(eq_line), FadeIn(eq_label), run_time=0.9)

        # ============================================================
        # ACT 3 — EVOLVE  (≈9 s)
        # ============================================================
        # Animate temperature 3000 -> 7000 K in 500 K steps.
        # Each step: update coil color, recompute curve morph, update readouts.
        # We pick a small number of intermediate frames for speed, then a final flick.
        temps = list(range(3000, 7001, 500))  # 9 steps
        # Build successive curves
        step_curves = []
        for T in temps:
            c = ax.plot(lambda nm, T=T: planck_nm_to_y(nm, T),
                        x_range=[200, 3000, 8],
                        color=PRIMARY, stroke_width=4)
            step_curves.append(c)

        # Use a continuous ramp via a ValueTracker for temperature; smoothly step.
        # To keep within ~9 s we do ~9 sub-stages.
        current_curve = planck_curve
        for i, T in enumerate(temps):
            new_curve = step_curves[i]
            temperature_tracker.set_value(T)
            peak_wl_tracker.set_value(wien_peak_nm(T))
            peak_rad_tracker.set_value(planck_blambda(wien_peak_nm(T)*1e-9, T))
            # Coil color animates in parallel (handled by tracker color updater).
            self.play(Transform(current_curve, new_curve),
                      coil.animate.set_color(kelvin_to_rgb_hex(T)),
                      run_time=0.65, rate_func=linear)
            current_curve = new_curve
        # Replace last curve so it's properly colored with current value
        planck_curve = current_curve

        # Now add upward-diverging RJ ghost annotation
        # rj_curve already present with stroke opacity 0.55; bring to full
        rj_curve.set_stroke(opacity=0.9)
        uv_arrow = Arrow(
            ax.c2p(320, 6e13), ax.c2p(260, 1.05e14),
            color=ACCENT, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.18,
        )
        uv_label = Text("ultraviolet catastrophe", color=ACCENT, weight=BOLD).scale(0.26)
        uv_label.next_to(uv_arrow, UP, buff=0.12)
        plot_layer.add(uv_arrow, uv_label)
        self.play(FadeIn(uv_arrow, shift=UP*0.2), FadeIn(uv_label),
                  run_time=0.8)

        # ============================================================
        # ACT 4 — REVEAL  (≈7 s)
        # ============================================================
        # Wipe the plot, isolate the coil, then add ladder + packets + new curve.
        self.play(FadeOut(plot_layer, shift=UP*0.5), run_time=0.9)
        # Move coil to center-left
        self.play(coil.animate.move_to(LEFT * 5.0),
                  bell.animate.move_to(LEFT * 5.0).scale(1.0),
                  bloom_cores.animate.move_to(LEFT * 5.0),
                  halo.animate.move_to(LEFT * 5.0),
                  bell_base.animate.move_to(LEFT * 5.0 + DOWN * 1.3),
                  run_time=0.8)

        # Ladder — vertical evenly-spaced rungs at center
        n_rungs = 6
        ladder_x = LEFT * 1.6
        ladder_y0 = -2.1
        ladder_dy = 0.7
        rungs = VGroup()
        rung_labels = VGroup()
        for n in range(1, n_rungs + 1):
            y = ladder_y0 + (n-1) * ladder_dy
            rung = Line(ladder_x + LEFT*0.25 + UP*y, ladder_x + RIGHT*0.25 + UP*y,
                        color=ACCENT, stroke_width=4)
            rungs.add(rung)
            lbl = MathTex(r"E_{{{n}}} = n\,h\,\nu", color=ACCENT).scale(0.36)
            lbl.next_to(rung, RIGHT, buff=0.18)
            rung_labels.add(lbl)
        ladder_axis = DashedLine(ladder_x + DOWN*0.35, ladder_x + UP*(ladder_y0 + n_rungs*ladder_dy + 0.2),
                                 color=GREY_B, stroke_width=1).set_opacity(0.4)
        ladder_title = Text("quantized oscillators", color=ACCENT).scale(0.26).next_to(
            ladder_axis, UP, buff=0.05)
        ladder_layer.add(ladder_axis, rungs, rung_labels, ladder_title)
        self.play(FadeIn(ladder_axis), LaggedStart(*[FadeIn(r, shift=RIGHT*0.2) for r in rungs],
                                                    lag_ratio=0.12),
                  LaggedStart(*[FadeIn(l) for l in rung_labels], lag_ratio=0.10),
                  FadeIn(ladder_title, shift=UP*0.15),
                  run_time=1.6)

        # Packets hopping rung-to-rung then eject right
        packets = VGroup(*[Dot(color=ACCENT, radius=0.07, fill_opacity=1.0).move_to(
            ladder_x + RIGHT*0.0 + UP*(ladder_y0 + (i % n_rungs)*ladder_dy)) for i in range(5)])
        ladder_layer.add(packets)
        hop_path = []
        for i in range(5):
            hop_path.append(packets[i].animate.move_to(
                ladder_x + RIGHT*0.0 + UP*(ladder_y0 + (i+1)*0.55)))
        # Eject packets to the right
        eject_targets = [RIGHT * 3.2 + UP * (1.6 - i*0.4) for i in range(5)]

        self.play(LaggedStart(*hop_path, lag_ratio=0.15), run_time=1.0)
        self.play(LaggedStart(*[p.animate.move_to(t) for p, t in zip(packets, eject_targets)],
                               lag_ratio=0.18), run_time=0.9)

        # Build a fresh, larger Planck curve at right obeying full formula
        ax2 = Axes(
            x_range=[200, 3000, 400],
            y_range=[0, 1.4e14, 2e13],
            x_length=5.0, y_length=3.6,
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 1.2},
        ).move_to(RIGHT * 2.6 + DOWN * 0.05)
        x2_label = Text("λ (nm)", color=GREY_B).scale(0.24).next_to(ax2.x_axis, DOWN, buff=0.18)
        y2_label = Text("B_λ (W·m⁻³·sr⁻¹)", color=GREY_B).scale(0.22)
        y2_label.rotate(PI/2).next_to(ax2.y_axis, LEFT, buff=0.12)
        big_curve = ax2.plot(
            lambda nm: planck_nm_to_y(nm, 5800.0) * 1.25,
            x_range=[200, 3000, 6],
            color=PRIMARY, stroke_width=5,
        )
        big_tick = Line(ax2.c2p(500, 0), ax2.c2p(500, 1.35e14),
                        color=ACCENT, stroke_width=1.5).set_opacity(0.85)
        big_tick_label = Text("500 nm", color=ACCENT, weight=BOLD).scale(0.26).next_to(
            ax2.c2p(500, 1.32e14), UP, buff=0.05)

        triptych_layer.add(ax2, x2_label, y2_label, big_curve, big_tick, big_tick_label)

        equation = MathTex(
            r"B_\lambda(T) = \dfrac{2hc^2 / \lambda^5}",
            color=FACE,
        ).scale(0.42)
        # Two-line equation
        eq2 = MathTex(r"e^{\,hc / (\lambda k_B T)} - 1", color=FACE).scale(0.42)
        # Compose as a single typeset line using a fraction structure
        frac = MathTex(
            r"B_\lambda(T) \;=\;",
            r"{2 h c^{2} / \lambda^{5} \over e^{\,h c / (\lambda k_B T)} \;-\; 1}",
            color=FACE,
        ).scale(0.5)
        frac.next_to(ax2, DOWN, buff=0.45).move_to(DOWN * 2.8)

        self.play(FadeIn(ax2), FadeIn(x2_label), FadeIn(y2_label),
                  Create(big_curve), run_time=1.4)
        self.play(FadeIn(big_tick), FadeIn(big_tick_label), run_time=0.4)
        self.play(Write(frac), run_time=1.2)

        # Hero frame lock — coil + ladder + curve + equation
        self.wait(0.2)

        # ============================================================
        # ACT 5 — RECAP  (≈4 s)
        # ============================================================
        # Cross-dissolve everything to a small inset
        # Build recap composite (inset triptych compressed)
        old_layers = VGroup(hook_layer, ladder_layer, triptych_layer, readout_layer)
        # Don't include the readout_layer yet (we keep the live tracker values visible).
        # Fade out large triptych pieces but keep coil + live readouts running.
        big_fade = VGroup(ax2, x2_label, y2_label, big_curve, big_tick, big_tick_label, frac)
        self.play(FadeOut(big_fade, shift=DOWN*0.3),
                  FadeOut(rung_labels),
                  FadeOut(rungs),
                  FadeOut(ladder_axis),
                  FadeOut(ladder_title),
                  FadeOut(packets),
                  FadeOut(eq_line),
                  FadeOut(eq_label),
                  FadeOut(uv_arrow),
                  FadeOut(uv_label),
                  FadeOut(wien_label),
                  FadeOut(wien_tick),
                  FadeOut(plot_layer),
                  run_time=0.9)

        # Recap composition inset
        inset_box = Rectangle(width=4.6, height=2.6, stroke_color=GREY_B,
                              stroke_width=1.5).move_to(RIGHT * 2.3 + UP * 0.2)
        # Tiny axes inside inset
        ax_in = Axes(x_range=[200, 3000, 1], y_range=[0, 1.2e14, 1],
                     x_length=4.0, y_length=2.0, tips=False,
                     axis_config={"stroke_color": GREY_B, "stroke_width": 1}).move_to(inset_box.get_center())
        curve_in = ax_in.plot(lambda nm: planck_nm_to_y(nm, 5800.0) * 1.0,
                              x_range=[200, 3000, 8], color=PRIMARY, stroke_width=2.5)
        peak_in = Line(ax_in.c2p(500, 0), ax_in.c2p(500, 1.15e14),
                       color=ACCENT, stroke_width=1.3).set_opacity(0.85)
        wien_arrow = Arrow(ax_in.c2p(2000, 0.7e14), ax_in.c2p(500, 0.7e14),
                           color=ACCENT, buff=0, stroke_width=2.5,
                           max_tip_length_to_length_ratio=0.12)
        rj_tail = ax_in.plot(lambda nm: rj_nm_to_y(nm, 5800.0) * 0.45,
                             x_range=[200, 900, 8],
                             color=SECONDARY, stroke_width=1.5).set_stroke(opacity=0.7)
        rj_clip = DashedLine(ax_in.c2p(280, 0.0), ax_in.c2p(280, 1.15e14),
                             color=ACCENT, stroke_width=1, dash_length=0.05)
        clipped_lbl = Text("× suppressed", color=ACCENT).scale(0.20).next_to(rj_clip, UP, buff=0.05)

        recap_inset = VGroup(inset_box, ax_in, curve_in, peak_in, wien_arrow, rj_tail, rj_clip, clipped_lbl)
        recap_inset.move_to(RIGHT * 2.3 + UP * 0.2)
        self.play(FadeIn(recap_inset), run_time=0.7)

        banner = Text(
            "Quantized oscillators suppress the UV divergence — Planck's law wins.",
            color=PRIMARY, weight=BOLD,
        ).scale(0.36).next_to(inset_box, DOWN, buff=0.25).set_opacity(0)
        self.play(banner.animate.set_opacity(1), run_time=0.7)
        self.play(banner.animate.set_opacity(0).shift(DOWN*0.2), run_time=0.7)

        # ============================================================
        # IDLE LOOP (after recap, runs for the rest of budget ≈ 4 s)
        # ============================================================
        # Coil pulses with thermal flicker (opacity) and peak_wl breathes ±1 nm,
        # Planck curve shimmers (tail jitter via vertical jitter updater).
        # Build the canonical "final" Planck curve (in inset)
        T_now = temperature_tracker.get_value()
        # Persistent live curve in the inset: keep wave params live
        shimmer_t = ValueTracker(0.0)

        def live_curve_mob():
            base = ax_in.plot(lambda nm: planck_nm_to_y(nm, T_now) * 1.0,
                              x_range=[200, 3000, 8], color=PRIMARY, stroke_width=2.5)
            base.set_stroke(opacity=0.95)
            return base

        live_curve = always_redraw(live_curve_mob)
        # Replace static curve_in with the live version
        recap_layer.add(live_curve)
        self.add(live_curve)
        curve_in.become(live_curve)

        # Coil flicker: pulse opacity 0.9 -> 1.0 with 0.5 s period
        coil_flicker_phase = ValueTracker(0.0)
        coil.add_updater(lambda m: m.set_opacity(
            0.9 + 0.1 * math.sin(2 * PI * coil_flicker_phase.get_value() / 0.5)
        ))
        # peak_wl breathes ±1 nm
        breathe_phase = ValueTracker(0.0)
        peak_wl_tracker.add_updater(lambda tr: tr.set_value(
            wien_peak_nm(temperature_tracker.get_value())
            + 1.0 * math.sin(2 * PI * breathe_phase.get_value() / 1.0)
        ))

        idle_time = 3.4
        # Step the phase trackers smoothly via animate (no need to play many)
        self.play(coil_flicker_phase.animate.set_value(0.5),
                  breathe_phase.animate.set_value(1.0),
                  shimmer_t.animate.set_value(1.0),
                  run_time=idle_time, rate_func=linear)

        # Final stable pose — keep updaters running for a true idle loop.
        self.wait(0.8)