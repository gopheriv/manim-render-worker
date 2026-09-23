from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # ------------------------------------------------------------------
        # GLOBAL PALETTE  (kept consistent across all acts)
        # ------------------------------------------------------------------
        PRIMARY = "#FF7A1A"    # tungsten / amber / hero accent
        SECONDARY = "#1E90FF"  # blue-white filament & Rayleigh-Jeans sky
        ACCENT = "#FFE680"     # hero glow / Wien highlight
        WALL_COL = "#0B0F1A"   # darkened prism wall
        WALL_LIGHT = "#F8FAFC" # off-white wall before darkening

        # ------------------------------------------------------------------
        # BACKGROUND SCAFFOLDING — tall "prism wall" on the right
        # ------------------------------------------------------------------
        wall = Rectangle(
            width=5.2, height=5.6, stroke_color=WHITE, stroke_width=1
        ).set_fill(WALL_LIGHT, opacity=0.08)
        wall.to_edge(RIGHT, buff=0.15).shift(DOWN * 0.2)

        # faint dotted axes on the wall — only drawn, never filled
        wl_axis = DashedLine(
            start=wall.get_corner(DL) + UP * 0.25 + RIGHT * 0.05,
            end=wall.get_corner(DR) + UP * 0.25 + LEFT * 0.05,
            dash_length=0.08, color=WHITE,
        )
        rd_axis = DashedLine(
            start=wall.get_corner(DL) + UP * 0.25,
            end=wall.get_corner(DL) + UP * 0.25 + RIGHT * 4.8,
            dash_length=0.08, color=WHITE,
        ).rotate(90 * DEGREES)

        # wavelength tick labels (live, decimal driven) — built once, static
        ticks = VGroup()
        for nm in (0, 500, 1000, 1500, 2000, 2500):
            frac = nm / 2500.0
            pos = wl_axis.get_start() + (wl_axis.get_end() - wl_axis.get_start()) * frac
            t = Text(f"{nm}", color=WHITE).scale(0.22).next_to(pos, DOWN, buff=0.08)
            ticks.add(t)
        wl_labels = ticks

        wl_caption = Text("wavelength λ (nm)", color=WHITE).scale(0.28)
        wl_caption.next_to(wl_axis, DOWN, buff=0.35)

        rd_caption = Text("spectral radiance", color=WHITE).scale(0.28)
        rd_caption.rotate(90 * DEGREES).next_to(rd_axis, LEFT, buff=0.25)

        # ------------------------------------------------------------------
        # FILAMENTS — coiled tungsten on a shared rail (left of frame)
        # ------------------------------------------------------------------
        rail = Line(LEFT * 0.2 + UP * 1.6, LEFT * 5.6 + UP * 1.6,
                    stroke_width=2, color=GREY_B)
        filament_y = UP * 1.6

        def make_coil(color, center_x, radius=0.16, n_turns=6, height=0.55):
            coil = VGroup()
            for k in range(n_turns * 12):
                t = k / (n_turns * 12)
                y = height * (t - 0.5)
                x_off = radius * math.sin(2 * math.pi * n_turns * t)
                p = np.array([center_x + x_off, filament_y[1] + y, 0.0])
                dot = Dot(p, radius=0.012, color=color)
                coil.add(dot)
            stem_l = Line(np.array([center_x - 0.08, filament_y[1] - height / 2, 0]),
                          np.array([center_x - 0.08, filament_y[1] - height / 2 - 0.5, 0]),
                          stroke_width=2, color=GREY_B)
            stem_r = Line(np.array([center_x + 0.08, filament_y[1] - height / 2, 0]),
                          np.array([center_x + 0.08, filament_y[1] - height / 2 - 0.5, 0]),
                          stroke_width=2, color=GREY_B)
            return VGroup(coil, stem_l, stem_r)

        fil_red = make_coil("#B22222", -4.7)   # 3000 K — dim cherry
        fil_amb = make_coil(PRIMARY, -3.7)     # 5800 K — amber protagonist
        fil_blu = make_coil(SECONDARY, -2.7)   # 8000 K — blue-white

        # static temperature labels under each filament
        temp_red = DecimalNumber(3000, num_decimal_places=0, color="#B22222"
                                 ).scale(0.32).next_to(fil_red, DOWN, buff=0.15)
        temp_amb = DecimalNumber(5800, num_decimal_places=0, color=PRIMARY
                                 ).scale(0.32).next_to(fil_amb, DOWN, buff=0.15)
        temp_blu = DecimalNumber(8000, num_decimal_places=0, color=SECONDARY
                                 ).scale(0.32).next_to(fil_blu, DOWN, buff=0.15)

        # ------------------------------------------------------------------
        # PRISM  — triangular glass at frame center
        # ------------------------------------------------------------------
        prism = Polygon(
            np.array([-0.55, -0.65, 0]),
            np.array([0.55, -0.65, 0]),
            np.array([0.0, 0.75, 0]),
            color=WHITE, stroke_width=1.5,
        ).set_fill(BLUE_E, opacity=0.18)
        prism.move_to(np.array([-1.1, 1.6, 0]))

        slit = Rectangle(width=0.05, height=0.5, color=WHITE,
                         stroke_width=1, fill_opacity=0.6)
        slit.move_to(np.array([-1.7, 1.6, 0]))

        # light beams from filament → slit → prism → wall
        def beam(color, opacity):
            seg1 = Line(np.array([-3.7, 1.6, 0]), np.array([-1.7, 1.6, 0]),
                        stroke_width=3, color=color).set_opacity(opacity)
            seg2 = Line(np.array([-1.7, 1.6, 0]), np.array([-1.1, 1.6, 0]),
                        stroke_width=3, color=color).set_opacity(opacity)
            return VGroup(seg1, seg2)

        # ------------------------------------------------------------------
        # SPECTRAL SMEARS — rainbows on the wall (static, fade in)
        # ------------------------------------------------------------------
        wall_left = wall.get_left()[0] + 0.15
        wall_bottom = wall.get_bottom()[1] + 0.25
        wall_height = wall.height - 0.6
        wall_width = wall.width - 0.3

        def wl_to_x(nm):
            frac = 1.0 - nm / 2500.0
            return wall_left + wall_width * frac

        def color_for_nm(nm):
            if nm < 380:
                return interpolate_color(PURPLE, BLUE, (nm - 300) / 80)
            if nm < 450:
                return interpolate_color(BLUE, TEAL, (nm - 380) / 70)
            if nm < 520:
                return interpolate_color(TEAL, GREEN, (nm - 450) / 70)
            if nm < 580:
                return interpolate_color(GREEN, YELLOW, (nm - 520) / 60)
            if nm < 650:
                return interpolate_color(YELLOW, ORANGE, (nm - 580) / 70)
            return interpolate_color(ORANGE, ManimColor("#B22222"),
                                     min((nm - 650) / 200, 1.0))

        def make_smear(lambda_max, lambda_min, height_frac, opacity=0.55):
            grp = VGroup()
            steps = 20
            for k in range(steps):
                nm = lambda_min + (lambda_max - lambda_min) * (k / (steps - 1))
                w = (lambda_max - lambda_min) / steps * 1.05
                rect = Rectangle(
                    width=w / 50.0, height=wall_height * height_frac,
                    color=color_for_nm(nm), stroke_width=0,
                    fill_opacity=opacity,
                )
                x = wl_to_x(nm)
                rect.move_to(np.array([x, wall_bottom + wall_height * height_frac / 2, 0]))
                grp.add(rect)
            return grp

        smear_red = make_smear(2400, 600, height_frac=0.30, opacity=0.0)
        smear_amb = make_smear(1800, 380, height_frac=0.55, opacity=0.0)
        smear_blu = make_smear(900, 250, height_frac=0.70, opacity=0.0)

        # ------------------------------------------------------------------
        # PLANCK CURVES on the wall  (drawn against a normalized axis)
        # ------------------------------------------------------------------
        def planck(lam_m, T):
            h = 6.62607015e-34
            c = 2.99792458e8
            kB = 1.380649e-23
            x = h * c / (lam_m * kB * T)
            if x > 500:
                return 0.0
            return (2.0 * h * c * c) / (lam_m ** 5) / (math.exp(x) - 1.0)

        BPEAK = planck(500e-9, 5800.0)

        def planck_curve(T, color, opacity=1.0):
            pts = []
            for nm in np.linspace(250, 2500, 80):
                lam_m = nm * 1e-9
                B = planck(lam_m, T) / BPEAK
                x = wl_to_x(nm)
                y = wall_bottom + wall_height * 0.85 * max(B, 0.0)
                pts.append(np.array([x, y, 0]))
            return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
                pts
            ).set_opacity(opacity)

        curve_red = planck_curve(3000, ManimColor("#B22222"), opacity=0.0)
        curve_amb = planck_curve(5800, PRIMARY, opacity=0.0)
        curve_blu = planck_curve(8000, SECONDARY, opacity=0.0)

        # Rayleigh-Jeans curves
        def rj_curve(T, color, opacity=0.85, clip_y=2.4):
            pts = []
            for nm in np.linspace(250, 2500, 80):
                lam_m = nm * 1e-9
                c = 2.99792458e8
                kB = 1.380649e-23
                B = 2.0 * c * kB * T / (lam_m ** 5) / BPEAK
                yval = min(B, clip_y)
                x = wl_to_x(nm)
                y = wall_bottom + wall_height * 0.85 * yval
                pts.append(np.array([x, y, 0]))
            return DashedVMobject(
                VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(pts),
                num_dashes=60,
            ).set_opacity(opacity)

        rj_red = rj_curve(3000, ManimColor("#B22222"), opacity=0.0)
        rj_amb = rj_curve(5800, PRIMARY, opacity=0.0)
        rj_blu = rj_curve(8000, SECONDARY, opacity=0.0)

        # ------------------------------------------------------------------
        # WIEN MARKER — vertical line that walks left as temperature climbs
        # ------------------------------------------------------------------
        wien_x_tracker = ValueTracker(wl_to_x(500.0))  # start at 5800 K peak

        def wien_marker():
            x = wien_x_tracker.get_value()
            return Line(
                np.array([x, wall_bottom, 0]),
                np.array([x, wall_bottom + wall_height * 0.9, 0]),
                stroke_color=ACCENT, stroke_width=2.5,
            )

        wien_line = always_redraw(wien_marker)
        wien_label = always_redraw(lambda: MathTex(
            r"\lambda_{\max}\,T = 0.002898\ \mathrm{m\cdot K}",
            color=ACCENT,
        ).scale(0.32).next_to(
            np.array([wien_x_tracker.get_value(), wall_bottom, 0]), DOWN, buff=0.12
        ))

        # ------------------------------------------------------------------
        # TITLE
        # ------------------------------------------------------------------
        title = Text("Blackbody Radiation — Planck's Law", color=WHITE).scale(0.5)
        title.to_edge(UP, buff=0.25)

        # ==================================================================
        # ACT I — ESTABLISH
        # ==================================================================
        self.play(Write(title), run_time=1.0)
        self.play(
            Create(rail),
            FadeIn(fil_red, shift=RIGHT * 0.2),
            FadeIn(fil_amb, shift=RIGHT * 0.2),
            FadeIn(fil_blu, shift=RIGHT * 0.2),
            run_time=1.2,
        )
        self.play(FadeIn(slit, scale=0.6), FadeIn(prism, scale=0.6), run_time=0.6)

        # 3000 K red filament warms up
        self.play(
            fil_red.animate.set_opacity(1.0),
            FadeIn(temp_red, shift=UP * 0.2),
            smear_red.animate.set_opacity(0.55),
            Create(beam(ManimColor("#B22222"), 0.7)),
            run_time=1.4,
        )

        # 5800 K amber filament ignites
        self.play(
            fil_amb.animate.set_opacity(1.0),
            FadeIn(temp_amb, shift=UP * 0.2),
            smear_amb.animate.set_opacity(0.6),
            Create(beam(PRIMARY, 0.85)),
            run_time=1.2,
        )

        # 8000 K blue-white filament flares
        self.play(
            fil_blu.animate.set_opacity(1.0),
            FadeIn(temp_blu, shift=UP * 0.2),
            smear_blu.animate.set_opacity(0.6),
            Create(beam(SECONDARY, 0.85)),
            run_time=1.0,
        )

        # axes appear
        self.play(
            Create(wl_axis), Create(rd_axis),
            run_time=0.6,
        )
        self.play(FadeIn(wl_labels), FadeIn(wl_caption), FadeIn(rd_caption),
                  run_time=0.6)

        # ==================================================================
        # ACT II — EVOLVE
        # ==================================================================
        # Trace the three Planck curves directly on the wall
        self.play(
            Create(curve_red),
            Create(curve_amb),
            Create(curve_blu),
            run_time=2.0,
        )
        # Let curves take over
        self.play(
            smear_red.animate.set_opacity(0.18),
            smear_amb.animate.set_opacity(0.18),
            smear_blu.animate.set_opacity(0.18),
            run_time=0.6,
        )

        # Wien's marker walks with the live 0.002898 label
        self.play(FadeIn(wien_line), FadeIn(wien_label), run_time=0.6)
        self.play(
            wien_x_tracker.animate.set_value(wl_to_x(966)),
            run_time=1.0,
        )
        self.play(
            wien_x_tracker.animate.set_value(wl_to_x(362)),
            run_time=1.0,
        )
        self.play(
            wien_x_tracker.animate.set_value(wl_to_x(500)),
            run_time=0.8,
        )

        # Rayleigh-Jeans catastrophe overlay
        self.play(
            FadeIn(rj_red, shift=UP * 0.1),
            FadeIn(rj_amb, shift=UP * 0.1),
            FadeIn(rj_blu, shift=UP * 0.1),
            run_time=1.2,
        )

        # quantum cutoff flash on the amber curve's peak
        flash = Dot(
            np.array([wl_to_x(500), wall_bottom + wall_height * 0.85, 0]),
            color=ACCENT, radius=0.14,
        )
        self.play(
            curve_amb.animate.set_stroke(width=4.5),
            FadeIn(flash, scale=0.4),
            flash.animate.scale(1.8).set_opacity(0.0),
            run_time=0.8,
        )
        self.play(curve_amb.animate.set_stroke(width=3), run_time=0.2)

        # ==================================================================
        # ACT III — REVEAL
        # ==================================================================
        dim_group = VGroup(
            fil_red, fil_blu,
            smear_red, smear_blu,
            curve_red, curve_blu,
            rj_red, rj_blu,
            temp_red, temp_blu,
            beam(ManimColor("#B22222"), 0.7), beam(SECONDARY, 0.85),
            wl_labels, rd_caption,
        )
        self.play(
            dim_group.animate.set_opacity(0.18),
            wall.animate.set_fill(WALL_COL, opacity=0.85),
            run_time=1.0,
        )

        # brighten amber protagonist + curve
        self.play(
            fil_amb.animate.set_opacity(1.0),
            curve_amb.animate.set_stroke(width=4.5).set_opacity(1.0),
            run_time=0.6,
        )

        # Sun-glyph hero badge
        badge = VGroup(
            Circle(radius=0.42, color=ACCENT, stroke_width=2)
            .set_fill(PRIMARY, opacity=0.25),
            Text("☉", color=ACCENT).scale(0.7),
        ).next_to(curve_amb, UP, buff=0.6).shift(LEFT * 0.3)

        hero_caption = VGroup(
            MathTex(r"T = 5800\ \mathrm{K}", color=ACCENT).scale(0.38),
            MathTex(r"\lambda_{\max} \approx 500\ \mathrm{nm}", color=ACCENT).scale(0.38),
            Text("— our Sun", color=ACCENT).scale(0.32),
        ).arrange(DOWN, buff=0.1).next_to(badge, RIGHT, buff=0.25)

        self.play(FadeIn(badge, scale=0.6), Write(hero_caption), run_time=0.9)

        # Sweep the Rayleigh-Jeans tail off-wall
        self.play(
            rj_amb.animate.shift(RIGHT * 6).set_opacity(0),
            run_time=0.7,
        )

        # Final settle — wall darkens further
        self.play(
            wall.animate.set_fill(BLACK, opacity=0.75),
            run_time=0.4,
        )

        # ==================================================================
        # IDLE LOOP — keeps the scene alive after the hero frame
        # Three short drives using simple phase changes (no always_redraw
        # overload, no per-frame set_points_as_corners).
        # ==================================================================
        # photon dot, redrawn only when its phase tracker changes
        photon_phase = ValueTracker(0.0)
        photon = Dot(
            np.array([
                wall_left + (wall.get_right()[0] - 0.2 - wall_left) * 0.0,
                wall_bottom + 0.12, 0,
            ]),
            color=ACCENT, radius=0.06,
        ).set_opacity(0.9)
        photon.add_updater(lambda m: m.move_to(
            np.array([
                wall_left + (wall.get_right()[0] - 0.2 - wall_left) * photon_phase.get_value(),
                wall_bottom + 0.12, 0,
            ])
        ))
        self.add(photon)

        self.play(photon_phase.animate(rate_func=linear).set_value(1.0), run_time=2.0)
        self.play(photon_phase.animate(rate_func=linear).set_value(0.0), run_time=2.0)
        self.play(photon_phase.animate(rate_func=linear).set_value(1.0), run_time=2.0)

        self.wait(0.4)