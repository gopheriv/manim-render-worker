from manim import *
import numpy as np

# Helper: integrate a single dipole field line via RK2 (midpoint)
def integrate_field_line(seed_xy, rp, rm, k=1.0, q=1.0, tau_max=8.0, dt=0.02):
    pts = [np.array([seed_xy[0], seed_xy[1], 0.0], dtype=float)]
    r = pts[-1].copy()
    tau = 0.0
    while tau < tau_max:
        def E(p):
            dp = p - rp
            dm = p - rm
            np_ = np.linalg.norm(dp)
            nm_ = np.linalg.norm(dm)
            if np_ < 1e-3 or nm_ < 1e-3:
                return np.zeros(3)
            return k * q * dp / (np_ ** 3) - k * q * dm / (nm_ ** 3)
        k1 = E(r)
        k2 = E(r + 0.5 * dt * k1)
        r = r + dt * k2
        # Clip to a generous box to keep math stable
        if abs(r[0]) > 3.4 or abs(r[1]) > 2.4:
            break
        pts.append(r.copy())
        tau += dt
    return np.array(pts)


def make_streamline(theta, rp, rm, tau_max=8.0):
    # Seed a tiny offset outward from +q (rp) along direction theta
    seed = rp + 0.18 * np.array([np.cos(theta), np.sin(theta), 0.0])
    pts = integrate_field_line(seed[:2], rp, rm, tau_max=tau_max)
    return pts


class AetherLabScene(Scene):
    def construct(self):
        # Geometry constants from the spec
        d = 2.0
        rp = np.array([-d / 2, 0.0, 0.0])
        rm = np.array([d / 2, 0.0, 0.0])
        k = 1.0
        q = 1.0
        n_lines = 16
        tau_max = 8.0

        # ---- Persistent scene scaffolding ----
        # Graphite grid (subtle background)
        grid = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            background_line_style={"stroke_color": GRAY, "stroke_width": 1, "stroke_opacity": 0.25},
        )
        grid.set_opacity(0.4)
        grid.set_z_index(-2)

        # Charge spheres
        radius = 0.35
        sphere_pos = Circle(radius=radius, color=BLUE, fill_opacity=0.85, stroke_width=0)
        sphere_neg = Circle(radius=radius, color=RED, fill_opacity=0.85, stroke_width=0)
        sphere_pos.move_to(rp)
        sphere_neg.move_to(rm)
        # Inner highlight to give the metal a sheen
        highlight_p = Dot(rp + np.array([0.10, 0.12, 0.0]), radius=0.10, color=WHITE, fill_opacity=0.55)
        highlight_n = Dot(rm + np.array([0.10, 0.12, 0.0]), radius=0.10, color=WHITE, fill_opacity=0.55)

        dipole = VGroup(sphere_pos, sphere_neg, highlight_p, highlight_n)

        # Trackers for live readouts
        q_tracker = ValueTracker(1.0)
        d_tracker = ValueTracker(2.0)
        n_tracker = ValueTracker(16)
        tau_tracker = ValueTracker(0.0)
        E_sample_tracker = ValueTracker(0.0)

        # Variable labels (corner anchored)
        var_box = VGroup()
        q_label = Text("q =", font_size=30, color=WHITE).move_to(5.7 * RIGHT + 3.3 * UP)
        q_num = DecimalNumber(1.0, num_decimal_places=1, font_size=30, color=BLUE)
        q_num.add_updater(lambda m: m.set_value(q_tracker.get_value()))
        q_num.next_to(q_label, RIGHT)
        d_label = Text("d =", font_size=30, color=WHITE).next_to(q_num, RIGHT, buff=0.45)
        d_num = DecimalNumber(2.0, num_decimal_places=1, font_size=30, color=RED)
        d_num.add_updater(lambda m: m.set_value(d_tracker.get_value()))
        d_num.next_to(d_label, RIGHT)
        n_label = Text("n =", font_size=30, color=WHITE).next_to(d_num, RIGHT, buff=0.45)
        n_num = DecimalNumber(16, num_decimal_places=0, font_size=30, color=YELLOW)
        n_num.add_updater(lambda m: m.set_value(n_tracker.get_value()))
        n_num.next_to(n_label, RIGHT)
        var_box.add(q_label, q_num, d_label, d_num, n_label, n_num)
        var_box.to_edge(UP, buff=0.35).to_edge(RIGHT, buff=0.35)

        # |E| readout (lower-left)
        E_text = Text("|E| =", font_size=30, color=WHITE).to_edge(LEFT, buff=0.6).to_edge(DOWN, buff=0.6)
        E_num = DecimalNumber(0.0, num_decimal_places=3, font_size=30, color=BLUE)
        E_num.add_updater(lambda m: m.set_value(E_sample_tracker.get_value()))
        E_num.next_to(E_text, RIGHT, buff=0.15)
        # τ readout (lower-right)
        tau_text = Text("τ =", font_size=30, color=WHITE).next_to(E_num, RIGHT, buff=0.8)
        tau_num = DecimalNumber(0.0, num_decimal_places=2, font_size=30, color=YELLOW)
        tau_num.add_updater(lambda m: m.set_value(tau_tracker.get_value()))
        tau_num.next_to(tau_text, RIGHT, buff=0.15)
        readout_box = VGroup(E_text, E_num, tau_text, tau_num)

        # Sample point for |E| along axis
        sample_tracker = ValueTracker(2.5)
        sample_dot = always_redraw(
            lambda: Dot(
                [sample_tracker.get_value(), 0, 0],
                radius=0.06, color=YELLOW
            )
        )

        # Pre-compute the 16 streamlines (only used when revealed)
        thetas = np.linspace(0.05, 2 * np.pi - 0.05, n_lines, endpoint=False)
        all_pts = [make_streamline(th, rp, rm, tau_max=tau_max) for th in thetas]

        def streamline_vmobject(idx, color=BLUE, stroke_w=2.4):
            pts = all_pts[idx]
            vm = VMobject(stroke_color=color, stroke_width=stroke_w)
            vm.set_points_as_corners(pts)
            return vm

        streamlines = VGroup(*[streamline_vmobject(i, color=BLUE) for i in range(n_lines)])

        # Pre-compute an 8-thread subset for A3.B1
        half = streamlines[:8]

        # Compass-like dial (corner)
        dial = VGroup()
        dial_outer = Circle(radius=0.32, color=WHITE, stroke_width=2)
        dial_tick = Line(ORIGIN, 0.28 * UP, color=WHITE, stroke_width=2)
        dial.add(dial_outer, dial_tick)
        dial.move_to(2.6 * LEFT + 2.7 * UP)
        dial_label = Text("field dial", font_size=20, color=GRAY_A).next_to(dial, DOWN, buff=0.1)

        # Seed points (8 around +q)
        seed_thetas = np.linspace(0, 2 * np.pi, 8, endpoint=False) + np.pi / 8
        seeds = VGroup(*[
            Dot(rp + 0.20 * np.array([np.cos(t), np.sin(t), 0.0]),
                radius=0.045, color=BLUE)
            for t in seed_thetas
        ])

        # Separation arrow (BLUE) between spheres
        sep_arrow = Arrow(rp + 0.4 * RIGHT, rm - 0.4 * RIGHT,
                          buff=0, color=BLUE, stroke_width=3, max_tip_length_to_length_ratio=0.12)
        sep_label = MathTex(r"\mathbf{r}-\mathbf{r}_+", font_size=30, color=BLUE).next_to(sep_arrow, UP, buff=0.12)

        # Equation (recap version)
        eq_main = MathTex(
            r"\mathbf{E}(\mathbf{r})=kq\!\left(\frac{\mathbf{r}-\mathbf{r}_+}{|\mathbf{r}-\mathbf{r}_+|^3}-\frac{\mathbf{r}-\mathbf{r}_-}{|\mathbf{r}-\mathbf{r}_-|^3}\right)",
            font_size=34,
        )
        eq_main.set_color_by_tex(r"\mathbf{r}_+", BLUE)
        eq_main.set_color_by_tex(r"\mathbf{r}_-", RED)
        eq_main.to_edge(LEFT, buff=0.45).shift(1.0 * UP)

        # Equation (shorter, used in A2.B2)
        eq_short = MathTex(
            r"\mathbf{E}(\mathbf{r})=kq\frac{\Delta\mathbf{r}_+}{|\Delta\mathbf{r}_+|^3}-kq\frac{\Delta\mathbf{r}_-}{|\Delta\mathbf{r}_-|^3}",
            font_size=30,
        )
        eq_short.set_color_by_tex(r"\Delta\mathbf{r}_+", BLUE)
        eq_short.set_color_by_tex(r"\Delta\mathbf{r}_-", RED)
        eq_short.to_edge(LEFT, buff=0.4).shift(1.2 * UP)

        # Auxiliary plot: |E| along axis, lower-right (F5 area)
        plot_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 3, 1],
            x_length=4.2,
            y_length=2.3,
            tips=False,
            axis_config={"color": GRAY, "stroke_opacity": 0.7, "include_numbers": False},
        )
        plot_axes.move_to(3.4 * RIGHT + 2.2 * DOWN)
        plot_xlabel = Text("x", font_size=22, color=GRAY_A).next_to(plot_axes.x_axis, RIGHT, buff=0.1)
        plot_ylabel = Text("|E|", font_size=22, color=GRAY_A).next_to(plot_axes.y_axis, UP, buff=0.1)
        plot_title = Text("|E| along axis", font_size=22, color=GRAY_A).next_to(plot_axes, UP, buff=0.1)

        def axis_E(x):
            # Along x-axis, by = 0
            rx = np.array([x, 0.0, 0.0])
            dp = rx - rp
            dm = rx - rm
            npsq = max(float(np.dot(dp, dp)), 1e-4)
            nmsq = max(float(np.dot(dm, dm)), 1e-4)
            Ex = k * q * (dp[0] / npsq ** 1.5 - dm[0] / nmsq ** 1.5)
            return abs(Ex)

        def plusq_E(x):
            rx = np.array([x, 0.0, 0.0])
            dp = rx - rp
            npsq = max(float(np.dot(dp, dp)), 1e-4)
            Ex = k * q * dp[0] / npsq ** 1.5
            return abs(Ex)

        curve_total = plot_axes.plot(axis_E, x_range=[-2.8, 2.8, 0.05], color=BLUE, stroke_width=2.6)
        curve_plusq = plot_axes.plot(plusq_E, x_range=[-2.8, 2.8, 0.05], color=YELLOW, stroke_width=1.6, stroke_opacity=0.7)
        plot_group = VGroup(plot_axes, plot_xlabel, plot_ylabel, plot_title, curve_total, curve_plusq)

        # Hero annotation
        hero_annotation = Text(
            "Dipole field — source to sink",
            font_size=34, color=YELLOW
        )
        hero_annotation.to_edge(DOWN, buff=0.55)

        # =================================================
        # BEAT A1.B1 | 0.00-2.00 s
        # =================================================
        # Show graphite grid then materialize the two spheres
        self.add(grid)
        self.play(FadeIn(grid, run_time=0.35))
        # The grid acts as our lab surface; reveal the spheres with a soft FadeIn
        self.play(
            FadeIn(sphere_pos, scale=0.6),
            FadeIn(sphere_neg, scale=0.6),
            FadeIn(highlight_p),
            FadeIn(highlight_n),
            run_time=0.55,
        )
        # A faint 'hair' sprouts at the positive pole to hint at field emergence
        hint_arrows = VGroup(*[
            Arrow(rp, rp + 0.45 * np.array([np.cos(t), np.sin(t), 0.0]),
                  buff=0, color=BLUE, stroke_width=2, max_tip_length_to_length_ratio=0.25)
            for t in np.linspace(0, 2 * np.pi, 6, endpoint=False)
        ])
        hint_arrows.set_opacity(0.55)
        self.play(LaggedStartMap(FadeIn, hint_arrows, lag_ratio=0.08), run_time=0.5)
        # Hold then exit
        self.wait(0.55)
        self.play(FadeOut(hint_arrows), run_time=0.3)

        # =================================================
        # BEAT A1.B2 | 2.00-4.00 s
        # =================================================
        # Compass-like dial spins and settles
        self.play(FadeIn(dial, run_time=0.3))
        self.play(Rotate(dial_tick, angle=2 * PI, about_point=dial.get_center()), run_time=0.5)
        # Add dial label quietly during hold
        self.play(FadeIn(dial_label), run_time=0.25)
        # Live readouts q=1.0, d=2.0
        self.play(FadeIn(VGroup(q_label, d_label, n_label, q_num, d_num, n_num), run_time=0.45))
        self.wait(0.7)
        self.play(FadeOut(dial), FadeOut(dial_label), run_time=0.3)

        # =================================================
        # BEAT A2.B1 | 4.00-6.50 s
        # =================================================
        # 8 starting seeds around +q and a separation arrow
        self.play(FadeIn(seeds, run_time=0.4))
        self.play(Create(sep_arrow), FadeIn(sep_label), run_time=0.5)
        self.wait(1.5)
        # Exit: keep seeds/arrow visible because the next beat references the same setup.
        # We only fade the equation/label after they no longer belong; keep seeds for A3.B1.
        # Nothing to fade out here; readable hold consumed the budget.
        # Reserve 0.3s exit budget but the next beat continues from this state.
        self.wait(0.1)

        # =================================================
        # BEAT A2.B2 | 6.50-9.00 s
        # =================================================
        # Full E-field equation fades in on left margin
        self.play(FadeIn(eq_short, run_time=0.4))
        # Live |E| readout (sample along horizontal axis at 5 points)
        self.play(FadeIn(VGroup(E_text, E_num), FadeIn(sample_dot), run_time=0.4))
        sample_xs = [-2.5, -1.5, 0.0, 1.5, 2.5]
        for sx in sample_xs:
            self.play(
                sample_tracker.animate.set_value(sx),
                run_time=0.18,
            )
            E_sample_tracker.set_value(axis_E(sx))
            self.wait(0.12)
        # Exit: clear the equation and sample dot, keep dipole + readouts for EVOLVE
        self.play(
            FadeOut(eq_short),
            FadeOut(sample_dot),
            FadeOut(sep_arrow),
            FadeOut(sep_label),
            run_time=0.3,
        )

        # =================================================
        # BEAT A3.B1 | 9.00-14.00 s
        # =================================================
        # Add τ readout now
        self.play(FadeIn(VGroup(tau_text, tau_num)), run_time=0.3)
        # For the first 4 streamlines, fade them in; the rest stagger in
        # We'll grow the half-subset progressively. To avoid per-frame rebuilds,
        # we create full streamlines but mask them by trimming with a partial set_points.
        # Simpler: animate each streamline growing via set_points_as_corners with a slice.
        for i, line in enumerate(half):
            pts = all_pts[i]
            # Start with one point, then expand to full via a custom updater pattern:
            # use an animation that interpolates a FloatTracker affecting line length.
            # We'll do it cleanly by Transform from a degenerate VMobject to the full one.
            start_vm = VMobject(stroke_color=BLUE, stroke_width=2.6)
            start_vm.set_points_as_corners(pts[:1])
            line.set_points_as_corners(pts[:1])
            self.play(
                Transform(start_vm, line, run_time=0.55),
                rate_func=linear,
            )
            line.become(start_vm)
            # Update τ to current streamline length fraction
            tau_tracker.set_value(tau_max * (i + 1) / 8.0)
            # Fade out the seed dot that this streamline started from (cosmetic)
            if i < len(seeds):
                self.remove(seeds[i])
        # Add the remaining 8 streamlines immediately (still semi-grown) for symmetry
        # We'll simply FadeIn them to keep render light.
        self.play(LaggedStartMap(FadeIn, streamlines[8:], lag_ratio=0.05), run_time=0.6)
        # Set τ readout to full
        tau_tracker.set_value(tau_max)
        self.wait(0.4)

        # =================================================
        # BEAT A3.B2 | 14.00-18.00 s
        # =================================================
        # Auxiliary plot fades in
        self.play(FadeIn(plot_group, run_time=0.45))
        # The |E| and +q curves are already drawn via axes.plot. Show them with Create.
        self.play(Create(curve_total), Create(curve_plusq), run_time=0.9)
        # Tick the live |E| readout across the axis as a small echo
        for sx in [-2.0, -1.0, 0.0, 1.0, 2.0]:
            self.play(sample_tracker.animate.set_value(sx), run_time=0.18)
            E_sample_tracker.set_value(axis_E(sx))
            self.wait(0.1)
        # Exit: leave the plot in place for the hero; clear the small sample
        self.wait(0.5)

        # =================================================
        # BEAT A4.B1 | 18.00-22.00 s
        # =================================================
        # All 16 streamlines should now be present (8 from A3.B1, 8 from the tail).
        # Compress near the negative pole visually: shift the right side's red glow
        # by tinting the last 8 streamlines red. We'll do a recolor Transform.
        red_recolor = []
        for i in range(8, 16):
            red_recolor.append(streamlines[i].animate.set_color(RED))
        self.play(*red_recolor, run_time=0.8)
        # Emphasize symmetry: scale the whole streamline set slightly to reveal onion shells
        self.play(streamlines.animate.scale(1.02).set_stroke(width=2.2), run_time=0.6)
        self.wait(1.5)

        # =================================================
        # BEAT A4.B2 | 22.00-26.00 s
        # =================================================
        # Hero composition: clear the plot and readouts to focus on the dipole portrait
        self.play(
            FadeOut(plot_group),
            FadeOut(VGroup(E_text, E_num, tau_text, tau_num)),
            run_time=0.5,
        )
        # Center the dipole composition and add hero annotation
        hero_group = VGroup(dipole, streamlines)
        # Scale-to-fit the hero within the safe frame
        hero_group.scale_to_fit_width(config.frame_width - 1.5)
        hero_group.move_to(0.3 * UP)
        self.play(
            FadeIn(hero_annotation, run_time=0.5),
        )
        # Soft godlight accent: a translucent yellow halo behind the dipole
        godlight = Circle(radius=2.6, color=YELLOW, fill_opacity=0.06, stroke_opacity=0.0)
        godlight.move_to(hero_group.get_center())
        self.play(FadeIn(godlight, run_time=0.6))
        # Hold the hero
        self.wait(2.0)

        # =================================================
        # BEAT A5.B1 | 26.00-29.00 s
        # =================================================
        # Recap: fade streamlines to faint dashes, drop the halo, show the equation
        self.play(
            FadeOut(godlight),
            streamlines.animate.set_stroke(opacity=0.35).set_stroke(width=1.4),
            run_time=0.4,
        )
        # Bring the recap equation back
        self.play(FadeIn(eq_main, run_time=0.4))
        # Bring back the corner readouts
        self.play(
            FadeIn(VGroup(E_text, E_num)),
            FadeIn(VGroup(tau_text, tau_num)),
            run_time=0.3,
        )
        # Tick |E| a few times for liveness
        for sx in [-2.0, -1.0, 0.0, 1.0, 2.0]:
            self.play(sample_tracker.animate.set_value(sx), run_time=0.12)
            E_sample_tracker.set_value(axis_E(sx))
        self.wait(0.4)

        # =================================================
        # BEAT A5.B2 | 29.00-30.00 s
        # =================================================
        # Idle loop: subtle micro-pulse of sphere radii ±2% and color shimmer on grid
        pulse = ValueTracker(0.0)
        # Add updaters for the two spheres and the grid stroke colors
        def pulse_pos():
            s = 1.0 + 0.02 * np.sin(2 * np.pi * 0.6 * pulse.get_value())
            sphere_pos.become(Circle(radius=radius * s, color=BLUE, fill_opacity=0.85, stroke_width=0).move_to(rp))
        def pulse_neg():
            s = 1.0 + 0.02 * np.sin(2 * np.pi * 0.6 * pulse.get_value() + np.pi)
            sphere_neg.become(Circle(radius=radius * s, color=RED, fill_opacity=0.85, stroke_width=0).move_to(rm))
        sphere_pos.add_updater(pulse_pos)
        sphere_neg.add_updater(pulse_neg)
        # Color shimmer: tint the grid's x_lines/bluish and y_lines reddish alternating
        shimmer_phase = ValueTracker(0.0)
        def shimmer(_):
            t = shimmer_phase.get_value()
            # blue-ish or red-ish tint by adjusting stroke_color
            blue_t = 0.5 + 0.5 * np.sin(2 * np.pi * 0.6 * t)
            new_color = interpolate_color(BLUE, RED, blue_t)
            grid.x_lines.set_stroke(color=new_color, width=1, opacity=0.25)
            grid.y_lines.set_stroke(color=interpolate_color(RED, BLUE, blue_t), width=1, opacity=0.25)
        grid.add_updater(shimmer)
        # Animate the phase tracker for the idle hold
        self.play(
            pulse.animate.set_value(1.0),
            shimmer_phase.animate.set_value(1.0),
            run_time=0.6,
        )
        self.wait(0.4)
        # Clean up updaters at the end of the scene
        sphere_pos.clear_updaters()
        sphere_neg.clear_updaters()
        grid.clear_updaters()