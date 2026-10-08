from manim import *
import numpy as np

# Helper: dipole field E(r) for charges +q at +d/2, -q at -d/2
def dipole_E(rx, ry, d=2.0, q=1.0, k=1.0):
    r_plus = np.array([d/2.0, 0.0])
    r_minus = np.array([-d/2.0, 0.0])
    p = np.array([rx, ry])
    v_plus = p - r_plus
    v_minus = p - r_minus
    n_plus = np.linalg.norm(v_plus)
    n_minus = np.linalg.norm(v_minus)
    if n_plus < 0.15:
        n_plus = 0.15
    if n_minus < 0.15:
        n_minus = 0.15
    E = k * q * v_plus / n_plus**3 - k * q * v_minus / n_minus**3
    return E

# Compute a single field line (streamline) by integrating from a seed point.
# Integrate forward in tau; stop if we approach -q too closely or leave bounds.
def compute_field_line(seed, d=2.0, q=1.0, k=1.0, tau_max=8.0, step=0.05, sign=1):
    pts = [np.array(seed, dtype=float)]
    x, y = seed[0], seed[1]
    for _ in range(int(tau_max / step)):
        E = dipole_E(x, y, d, q, k)
        n = np.linalg.norm(E)
        if n < 1e-4:
            break
        # Forward from +q (sign=+1) toward -q, backward to trace back near +q
        if sign == 1:
            dx, dy = E / n * step
        else:
            dx, dy = -E / n * step
        x += dx
        y += dy
        if abs(x) > 4.5 or abs(y) > 3.5:
            break
        # Terminate when close to negative charge
        r_minus = np.array([-d/2.0, 0.0])
        if np.linalg.norm(np.array([x, y]) - r_minus) < 0.25:
            pts.append(np.array([x, y]))
            break
        pts.append(np.array([x, y]))
    return np.array(pts)


class AetherLabScene(Scene):
    def construct(self):
        # Palette
        RED_POS = "#FF5555"
        BLUE_NEG = "#5B9BFF"
        ACCENT = "#FFD86B"
        PLATE = "#1A1A22"
        DUST = "#E8E6DA"

        # Constants from spec
        d_val = 2.0
        q_val = 1.0
        k_val = 1.0
        tau_max = 8.0
        n_lines = 16

        # ---- Background plate ----
        plate = Circle(radius=2.8, color=GRAY, fill_color=PLATE, fill_opacity=1.0, stroke_width=2)
        plate.set_z_index(-3)
        plate.move_to(ORIGIN)

        # ---- Charge spheres ----
        pos_charge = Circle(radius=0.22, color=RED_POS, fill_color=RED_POS, fill_opacity=1.0)
        neg_charge = Circle(radius=0.22, color=BLUE_NEG, fill_color=BLUE_NEG, fill_opacity=1.0)
        pos_charge.move_to([d_val/2.0, 0, 0])
        neg_charge.move_to([-d_val/2.0, 0, 0])
        pos_label = MathTex("+q", color=WHITE, font_size=30).next_to(pos_charge, UP, buff=0.12)
        neg_label = MathTex("-q", color=WHITE, font_size=30).next_to(neg_charge, UP, buff=0.12)
        charges = VGroup(pos_charge, neg_charge, pos_label, neg_label)
        charges.set_z_index(2)

        # ---- Seed ring (16 markers) ----
        seed_ring = VGroup()
        for i in range(n_lines):
            ang = i * TAU / n_lines
            r = 2.55
            seed_ring.add(Dot([r*np.cos(ang), r*np.sin(ang), 0], radius=0.045, color=WHITE, fill_opacity=0.9))
        seed_ring.set_z_index(1)

        # ---- HUD ValueTrackers ----
        d_tr = ValueTracker(d_val)
        q_tr = ValueTracker(q_val)
        k_tr = ValueTracker(k_val)
        n_tr = ValueTracker(0)  # counts up 0 -> 16
        tau_tr = ValueTracker(0.0)

        def make_hud(label_text, tracker, unit=""):
            label = Text(label_text, font_size=28, color=GRAY_B)
            num = DecimalNumber(tracker.get_value(), num_decimal_places=1, font_size=28, color=WHITE)
            num.add_updater(lambda m: m.set_value(tracker.get_value()))
            if unit:
                u = Text(unit, font_size=24, color=GRAY_B)
                grp = VGroup(label, num, u).arrange(RIGHT, buff=0.15)
            else:
                grp = VGroup(label, num).arrange(RIGHT, buff=0.15)
            return grp

        hud_d = make_hud("d=", d_tr)
        hud_q = make_hud("q=", q_tr)
        hud_k = make_hud("k=", k_tr)
        hud_n = make_hud("n_lines=", n_tr)
        hud_tau = make_hud("tau_max=", tau_tr)
        hud_row = VGroup(hud_d, hud_q, hud_k, hud_n, hud_tau).arrange(RIGHT, buff=0.35)
        hud_row.scale_to_fit_width(config.frame_width - 1.2)
        hud_row.to_edge(UP, buff=0.35)
        for h in hud_row:
            for m in h:
                m.set_z_index(5)

        # =========================================================
        # BEAT A1.B1 | 0.00-2.50 s
        # Camera pushes in on the dark plate as the two charge
        # spheres fade up at +/- d/2; HUD digits count on.
        # =========================================================
        self.add(plate)
        self.add(hud_row)
        # Count-on for d, q, k
        d_tr.set_value(0.0)
        q_tr.set_value(0.0)
        k_tr.set_value(0.0)
        # Fade in charges
        self.play(
            FadeIn(charges, shift=UP*0.3),
            d_tr.animate.set_value(d_val),
            q_tr.animate.set_value(q_val),
            k_tr.animate.set_value(k_val),
            run_time=1.2,
        )
        self.wait(1.0)
        # Subtle halo around charges (used in idle later)
        halo_pos = Circle(radius=0.45, color=RED_POS, stroke_width=2).move_to(pos_charge.get_center())
        halo_neg = Circle(radius=0.45, color=BLUE_NEG, stroke_width=2).move_to(neg_charge.get_center())
        halo_pos.set_opacity(0.0)
        halo_neg.set_opacity(0.0)
        self.add(halo_pos, halo_neg)

        # =========================================================
        # BEAT A1.B2 | 2.50-4.00 s
        # Soft white ring of 16 seed dots blooms around the plate.
        # =========================================================
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.4) for d in seed_ring], lag_ratio=0.04),
            run_time=1.0,
        )
        self.wait(0.5)

        # =========================================================
        # BEAT A2.B1 | 4.00-7.00 s
        # Probe vector arrow at D2 with live |E| readout and the
        # superposition equation.
        # =========================================================
        probe_pos = np.array([1.4, 1.2, 0])
        E_vec = dipole_E(probe_pos[0], probe_pos[1])
        E_norm = np.linalg.norm(E_vec)
        E_hat = E_vec / E_norm
        arrow_scale = 0.7
        probe_arrow = Arrow(
            start=probe_pos,
            end=probe_pos + E_hat * arrow_scale,
            color=ACCENT,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.25,
        )
        probe_dot = Dot(probe_pos, radius=0.06, color=WHITE)
        probe_label = Text("probe", font_size=24, color=GRAY_B).next_to(probe_dot, UL, buff=0.08)
        # Live |E| readout
        E_tr = ValueTracker(E_norm)
        E_readout = DecimalNumber(E_tr.get_value(), num_decimal_places=3, font_size=26, color=ACCENT)
        E_readout.add_updater(lambda m: m.set_value(E_tr.get_value()))
        E_readout.next_to(probe_arrow.get_end(), UR, buff=0.12)
        # Equation
        eq_super = MathTex(
            r"\vec{E}=kq\frac{\vec{r}-\vec{r}_+}{|\vec{r}-\vec{r}_+|^3}-kq\frac{\vec{r}-\vec{r}_-}{|\vec{r}-\vec{r}_-|^3}",
            font_size=30, color=WHITE,
        )
        eq_super.set_z_index(5)
        eq_super.to_edge(DOWN, buff=0.45)
        eq_super.scale_to_fit_width(config.frame_width - 1.2)

        self.play(
            FadeIn(probe_dot, scale=0.5),
            Create(probe_arrow),
            FadeIn(probe_label),
            FadeIn(E_readout),
            FadeIn(eq_super, shift=UP*0.2),
            run_time=0.9,
        )
        # Animate probe along a small arc to show live E update
        arc_points = []
        for t in np.linspace(0, 1, 24):
            theta = np.pi/4 + 0.6 * np.sin(np.pi * t)
            rr = 1.6
            arc_points.append(np.array([rr*np.cos(theta), rr*np.sin(theta), 0]))
        probe_mover = ValueTracker(0.0)
        def upd_arrow(m):
            idx = int(probe_mover.get_value()) % len(arc_points)
            p = arc_points[idx]
            Ev = dipole_E(p[0], p[1])
            nv = np.linalg.norm(Ev)
            if nv < 1e-4:
                return
            m.put_start_and_end_on(p, p + (Ev/nv) * 0.7)
        def upd_dot(m):
            idx = int(probe_mover.get_value()) % len(arc_points)
            m.move_to(arc_points[idx])
        def upd_readout(m):
            idx = int(probe_mover.get_value()) % len(arc_points)
            p = arc_points[idx]
            Ev = dipole_E(p[0], p[1])
            E_tr.set_value(np.linalg.norm(Ev))
        def upd_label(m):
            idx = int(probe_mover.get_value()) % len(arc_points)
            m.next_to(arc_points[idx], UL, buff=0.08)
        probe_arrow.add_updater(upd_arrow)
        probe_dot.add_updater(upd_dot)
        probe_label.add_updater(upd_label)
        # readout updater via E_tr not direct on E_readout
        self.play(probe_mover.animate.set_value(len(arc_points) - 1), run_time=1.7, rate_func=linear)
        # Brief hold
        self.wait(0.2)
        # Clean up updaters before next act
        probe_arrow.clear_updaters()
        probe_dot.clear_updaters()
        probe_label.clear_updaters()
        E_readout.clear_updaters()

        # =========================================================
        # BEAT A2.B2 | 7.00-10.00 s
        # Probe arrow and HUD numbers fade; seed ring reframes stage.
        # =========================================================
        self.play(
            FadeOut(probe_arrow),
            FadeOut(probe_dot),
            FadeOut(probe_label),
            FadeOut(E_readout),
            FadeOut(eq_super),
            # HUD row fades down to just d, q, k (small)
            FadeOut(hud_n),
            FadeOut(hud_tau),
            run_time=0.8,
        )
        # Pulse the seed ring slightly to reframe
        self.play(seed_ring.animate.set_stroke(WHITE, width=0), run_time=0.2)  # no-op safety
        self.wait(1.7)

        # =========================================================
        # BEAT A3.B1 | 10.00-17.00 s
        # Dust particles emit from seeds and follow streamlines,
        # leaving glowing trails that snap into 16 field lines.
        # n_lines counter ticks 0 -> 16.
        # =========================================================
        # Pre-compute 16 field lines (analytic streamlines)
        field_lines = VGroup()
        for i in range(n_lines):
            ang = i * TAU / n_lines
            seed = [0.42 * np.cos(ang) + d_val/2.0, 0.42 * np.sin(ang)]
            pts_fwd = compute_field_line(seed, d=d_val, q=q_val, k=k_val, tau_max=tau_max, step=0.05, sign=1)
            pts_back = compute_field_line(seed, d=d_val, q=q_val, k=k_val, tau_max=tau_max*0.6, step=0.05, sign=-1)
            all_pts = np.vstack([pts_back[::-1], pts_fwd])
            line = VMobject(stroke_color=ACCENT, stroke_width=2.2, stroke_opacity=0.9)
            line.set_points_as_corners(all_pts)
            line.set_z_index(1)
            field_lines.add(line)

        # Dust particles: one per seed, animated along the forward streamline
        dust = VGroup()
        for i in range(n_lines):
            ang = i * TAU / n_lines
            seed = np.array([0.42 * np.cos(ang) + d_val/2.0, 0.42 * np.sin(ang), 0.0])
            d_dot = Dot(seed, radius=0.05, color=DUST, fill_opacity=1.0)
            d_dot.set_z_index(2)
            dust.add(d_dot)

        # Make tau_max equation visible briefly
        tau_eq = MathTex(r"\tau_{max}=8.0", font_size=30, color=ACCENT)
        tau_eq.to_edge(DOWN, buff=0.45)

        # Animate: n_lines counts up 0->16, dust moves and trails form lines
        # We'll do a LaggedStart of small moves per particle and reveal lines gradually
        # Build per-particle MoveAlongPath paths
        moves = []
        creates = []
        for i in range(n_lines):
            ang = i * TAU / n_lines
            seed = [0.42 * np.cos(ang) + d_val/2.0, 0.42 * np.sin(ang)]
            pts_fwd = compute_field_line(seed, d=d_val, q=q_val, k=k_val, tau_max=tau_max, step=0.05, sign=1)
            path_pts = [np.array([p[0], p[1], 0.0]) for p in pts_fwd]
            if len(path_pts) > 2:
                moves.append(MoveAlongPath(dust[i], VMobject().set_points_as_corners(path_pts), run_time=4.0, rate_func=linear))
            # Create line near end of motion
            creates.append(Create(field_lines[i], run_time=1.2))

        # Animate n_lines counter
        n_tr.set_value(0.0)
        # Bring in dust, run all particles together (LaggedStart)
        self.play(FadeIn(dust, scale=0.3), run_time=0.4)
        self.add(tau_eq)
        # Run particles + counter + staggered line creates
        self.play(
            LaggedStart(*moves, lag_ratio=0.02),
            n_tr.animate.set_value(float(n_lines)),
            LaggedStart(*creates, lag_ratio=0.04),
            run_time=5.6,
        )
        # Hold then fade dust, but keep field lines
        self.play(FadeOut(dust), run_time=0.5)

        # =========================================================
        # BEAT A3.B2 | 17.00-20.00 s
        # 16 lines complete and gently breathe; tau_max settles in HUD.
        # =========================================================
        # Bring tau_max HUD back
        hud_tau2 = make_hud("tau_max=", tau_tr)
        hud_tau2[0].set_color(GRAY_B)
        for m in hud_tau2:
            m.set_z_index(5)
        # place at the end of remaining hud row
        remaining = VGroup(hud_d, hud_q, hud_k, hud_n)
        hud_full = VGroup(remaining, hud_tau2).arrange(RIGHT, buff=0.35)
        hud_full.scale_to_fit_width(config.frame_width - 1.2)
        hud_full.to_edge(UP, buff=0.35)
        self.play(
            FadeIn(hud_tau2, shift=DOWN*0.1),
            tau_tr.animate.set_value(8.0),
            run_time=0.8,
        )
        # Gentle breathe: stroke opacity oscillation via updater (but we must
        # ensure final frames differ). Add a small upater-based pulse.
        pulse_phase = ValueTracker(0.0)
        def pulse_updater(m):
            ph = pulse_phase.get_value()
            m.set_stroke(opacity=0.7 + 0.25 * np.sin(ph))
        for line in field_lines:
            line.add_updater(pulse_updater)
        self.play(pulse_phase.animate.set_value(TAU), run_time=2.0, rate_func=linear)

        # =========================================================
        # BEAT A4.B1 | 20.00-26.00 s
        # Camera dollies to 3/4 angle (via slight group rotation),
        # dashed axis line, two short tangent arrows showing mirror
        # symmetry, annotation near B2.
        # =========================================================
        # Remove hud temporarily to declutter
        self.play(FadeOut(tau_eq), run_time=0.2)
        # Stop pulse on lines before manipulating
        for line in field_lines:
            line.clear_updaters()
        # Dashed dipole axis
        axis_line = DashedLine(start=[-3.2, 0, 0], end=[3.2, 0, 0], color=GRAY_B, stroke_width=2, dash_length=0.15)
        axis_line.set_z_index(0)
        # Tangent arrows at two symmetric probe points (mirror about y-axis)
        # Point above-right of +q and above-left of -q
        def arrow_at(p, color):
            Ev = dipole_E(p[0], p[1])
            nv = np.linalg.norm(Ev)
            if nv < 1e-4:
                return Arrow(p, p + RIGHT*0.3, color=color, buff=0, stroke_width=4)
            return Arrow(p, p + (Ev/nv)*0.6, color=color, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        p1 = np.array([1.8, 1.4, 0])
        p2 = np.array([-1.8, 1.4, 0])
        tan1 = arrow_at(p1, ACCENT)
        tan2 = arrow_at(p2, ACCENT)
        sym_dots = VGroup(Dot(p1, radius=0.05, color=WHITE), Dot(p2, radius=0.05, color=WHITE))
        # Annotation
        annot = MathTex(r"\vec{E}_{axis}\approx\frac{2k\vec{p}}{r^3},\ \vec{p}=q\vec{d}", font_size=30, color=ACCENT)
        annot.set_z_index(5)
        annot.move_to([-3.4, 2.2, 0])  # near B2

        # Slight 3/4 tilt via rotation of the main scene group
        scene_group = VGroup(plate, charges, field_lines, halo_pos, halo_neg, seed_ring, axis_line, tan1, tan2, sym_dots)
        # Add elements to scene_group references; ensure already in scene
        # (these were already added via individual play calls)

        self.play(
            Create(axis_line),
            FadeIn(tan1), FadeIn(tan2), FadeIn(sym_dots),
            FadeIn(annot, shift=RIGHT*0.2),
            run_time=1.0,
        )
        # Subtle dolly: scale group slightly and tilt
        tilt_group = VGroup(plate, charges, field_lines, halo_pos, halo_neg, seed_ring, axis_line, tan1, tan2, sym_dots, annot)
        self.play(
            tilt_group.animate.rotate(0.12).scale(0.96),
            run_time=1.5,
        )
        # Add halos pulsing
        halo_pos.set_opacity(0.0)
        halo_neg.set_opacity(0.0)
        halo_phase = ValueTracker(0.0)
        def halo_upd_pos(m):
            m.set_opacity(0.35 + 0.25 * np.sin(halo_phase.get_value()))
        def halo_upd_neg(m):
            m.set_opacity(0.35 + 0.25 * np.sin(halo_phase.get_value() + np.pi))
        halo_pos.add_updater(halo_upd_pos)
        halo_neg.add_updater(halo_upd_neg)
        self.play(halo_phase.animate.set_value(2*PI), run_time=2.5, rate_func=linear)

        # =========================================================
        # BEAT A5.B1 | 26.00-30.00 s
        # All UI clears; only charges + 16 field lines remain
        # centered; main equation types in beneath; live counters
        # d=2.0, q=1.0, n_lines=16, tau_max=8.0 above.
        # =========================================================
        # Clear halos and updaters
        halo_pos.clear_updaters()
        halo_neg.clear_updaters()
        # Remove everything except plate, charges, field_lines
        # (hud row is still present; we keep it but compact)
        # First, build the hero composition group and clear extras
        # Remove annotations, axis, tangents, seeds, halo
        self.play(
            FadeOut(tilt_group),
            run_time=0.6,
        )
        # Hero group: charges + field lines centered
        hero = VGroup(charges, field_lines)
        # Ensure centered
        hero.move_to(ORIGIN)
        # Recenter plate visually behind
        plate.move_to(ORIGIN)
        # Main equation beneath
        main_eq = MathTex(
            r"\vec{E}(\vec{r})=kq\!\left(\frac{\vec{r}-\vec{r}_+}{|\vec{r}-\vec{r}_+|^3}-\frac{\vec{r}-\vec{r}_-}{|\vec{r}-\vec{r}_-|^3}\right)",
            font_size=34, color=WHITE,
        )
        main_eq.set_z_index(5)
        main_eq.next_to(hero, DOWN, buff=0.35)
        main_eq.scale_to_fit_width(config.frame_width - 1.2)

        # Compact HUD above
        hud_compact = VGroup(hud_d, hud_q, hud_n, hud_tau2).arrange(RIGHT, buff=0.4)
        hud_compact.scale_to_fit_width(config.frame_width - 1.2)
        hud_compact.to_edge(UP, buff=0.35)
        for h in hud_compact:
            for m in h:
                m.set_z_index(5)
        # Ensure hud_n and hud_tau2 still updating
        hud_n[1].add_updater(lambda m: m.set_value(n_tr.get_value()))
        hud_tau2[1].add_updater(lambda m: m.set_value(tau_tr.get_value()))
        hud_d[1].add_updater(lambda m: m.set_value(d_tr.get_value()))
        hud_q[1].add_updater(lambda m: m.set_value(q_tr.get_value()))

        # Type-in effect: reveal equation part by part
        eq_parts = VGroup()
        parts = [
            r"\vec{E}(\vec{r})",
            r"=",
            r"kq",
            r"\!\left(\frac{\vec{r}-\vec{r}_+}{|\vec{r}-\vec{r}_+|^3}",
            r"-",
            r"\frac{\vec{r}-\vec{r}_-}{|\vec{r}-\vec{r}_-|^3}\right)",
        ]
        cur = MathTex(parts[0], font_size=34, color=WHITE)
        cur.move_to(main_eq.get_center())
        self.play(FadeIn(cur), run_time=0.2)
        for p in parts[1:]:
            new = MathTex(parts[0] if p == "=" else (cur.get_tex_string() + p), font_size=34, color=WHITE)
            new.move_to(main_eq.get_center())
            self.play(Transform(cur, new), run_time=0.18)
        # Place final equation
        self.play(Transform(cur, main_eq), run_time=0.2)

        # Idle loop: halos breathing + line pulse (must change final 3 frames)
        # Re-create halos since we removed tilt_group
        halo_pos = Circle(radius=0.45, color=RED_POS, stroke_width=2).move_to(pos_charge.get_center())
        halo_neg = Circle(radius=0.45, color=BLUE_NEG, stroke_width=2).move_to(neg_charge.get_center())
        halo_pos.set_z_index(1)
        halo_neg.set_z_index(1)
        self.add(halo_pos, halo_neg)
        idle_phase = ValueTracker(0.0)
        def idle_halo_pos(m):
            m.set_opacity(0.35 + 0.30 * np.sin(idle_phase.get_value()))
        def idle_halo_neg(m):
            m.set_opacity(0.35 + 0.30 * np.sin(idle_phase.get_value() + np.pi))
        halo_pos.add_updater(idle_halo_pos)
        halo_neg.add_updater(idle_halo_neg)
        # Field line gentle pulse in brightness
        def idle_line(m):
            m.set_stroke(opacity=0.75 + 0.20 * np.sin(idle_phase.get_value() * 1.2))
        for line in field_lines:
            line.add_updater(idle_line)
        # Run idle for remaining time (RECAP window 4s; we already used ~1.2s typing)
        # Budget: ~2.5s idle
        self.play(idle_phase.animate.set_value(3 * TAU), run_time=2.6, rate_func=linear)
        self.wait(0.4)