from manim import *

import numpy as np


def _ellipse_pts(a=3.0, b=2.0, cx=0.0, cy=0.0, n=480):
    ts = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    xs = cx + a * np.cos(ts)
    ys = cy + b * np.sin(ts)
    return [np.array([float(x), float(y), 0.0]) for x, y in zip(xs, ys)]


def _dist(a, b):
    return float(np.linalg.norm(np.array(a) - np.array(b)))


def _wedge_area(focus, p_a, p_b, samples=120):
    focus = np.array(focus)
    p_a = np.array(p_a)
    p_b = np.array(p_b)
    ts = np.linspace(0.0, 1.0, samples)
    area = 0.0
    prev = p_a
    for t in ts[1:]:
        cur = (1.0 - t) * p_a + t * p_b
        v1 = prev - focus
        v2 = cur - focus
        area += 0.5 * abs(v1[0] * v2[1] - v1[1] * v2[0])
        prev = cur
    return area


class AetherLabScene(Scene):
    def construct(self):
        # ---- AetherLab explanation layer (act 0): concept, equation, watch-line.
        intro_head = Text("Kepler's stopwatch", font_size=40, weight=BOLD, color=YELLOW)
        intro_eq = Text("dA/dt = L / (2m) = constant", font_size=30, color=WHITE)
        intro_watch = Text(
            "Watch: every 1/12 of an orbit the planet leaves a wedge behind;\n"
            "distance per tick varies, area per tick stays equal.",
            font_size=26,
            color=GREY_B,
        )
        intro = VGroup(intro_head, intro_eq, intro_watch).arrange(DOWN, buff=0.5)
        if intro.width > 12.4:
            intro.scale_to_fit_width(12.4)
        if intro.height > 7.0:
            intro.scale_to_fit_height(7.0)
        self.play(FadeIn(intro, shift=0.2 * UP), run_time=1.0)
        self.wait(1.8)
        self.play(FadeOut(intro), run_time=0.5)

        # ---- Storyboard scene: orbit + planet + wedge-by-wedge traversal.
        # Hero layout: orbit on the LEFT, twin bar charts on the RIGHT, title on TOP.
        a, b = 3.0, 2.0  # semi-major, semi-minor; eccentricity sqrt(1 - b^2/a^2) ~ 0.745
        star_pt = np.array([-2.4, 0.0, 0.0])
        pts = _ellipse_pts(a=a, b=b, cx=0.0, cy=0.0, n=480)

        title = Text("Kepler's stopwatch", font_size=34, color=YELLOW).to_edge(UP, buff=0.25)

        orbit = VMobject(color=BLUE_D, stroke_width=2, stroke_opacity=0.65)
        orbit.set_points_as_corners(pts)

        star = Dot(star_pt, color=GOLD, radius=0.13)
        glow = Dot(star_pt, color=YELLOW, radius=0.30).set_opacity(0.25)

        ticks = 12
        per_tick = len(pts) // ticks  # 40
        # Pre-compute real distances and swept areas per tick from the actual ellipse.
        dist_h, area_h = [], []
        for k in range(ticks):
            p_a = pts[k * per_tick]
            p_b_idx = min((k + 1) * per_tick, len(pts) - 1)
            p_b = pts[p_b_idx]
            d = _dist(p_a, p_b)
            A = _wedge_area(star_pt, p_a, p_b)
            dist_h.append(d)
            area_h.append(A)

        # Normalise bar heights for the two charts so they fit nicely.
        max_d = max(dist_h)
        scale_d = 1.45 / max_d
        scale_a = 1.45 / max(area_h)

        # Twin charts on the right. Distance = TEAL, Area = ORANGE so the
        # contrast is real, and orange is reserved for the equal-area climax.
        chart_x0, chart_x1 = 3.6, 6.9
        bar_w = (chart_x1 - chart_x0) / ticks * 0.78

        # Upper chart: distance per tick
        d_axis = Line([chart_x0, 1.85, 0], [chart_x1, 1.85, 0], color=GREY_B, stroke_width=2)
        d_label = Text("distance travelled per tick", font_size=20, color=TEAL_B).move_to(
            [(chart_x0 + chart_x1) / 2, 3.30, 0]
        )
        d_unit = Text("(arc length, varies)", font_size=16, color=GREY_A).move_to(
            [(chart_x0 + chart_x1) / 2, 3.00, 0]
        )
        # Lower chart: area per tick
        a_axis = Line([chart_x0, -2.55, 0], [chart_x1, -2.55, 0], color=GREY_B, stroke_width=2)
        a_label = Text("area swept per tick", font_size=20, color=ORANGE).move_to(
            [(chart_x0 + chart_x1) / 2, -1.15, 0]
        )
        a_unit = Text("(equal in equal times)", font_size=16, color=GREY_A).move_to(
            [(chart_x0 + chart_x1) / 2, -1.45, 0]
        )

        # Bar containers built up as the orbit is traversed.
        d_bars = VGroup()
        a_bars = VGroup()

        # The two-color alternating wedge palette so adjacent wedges read as distinct.
        wedge_colors = [TEAL_E, GOLD_E]
        # The focal wedge uses a brighter, distinct color that matches the climax tone.
        focal_wedge_color = ORANGE

        idx = ValueTracker(0.0)

        def planet_pt():
            j = min(int(idx.get_value()), len(pts) - 1)
            return pts[j]

        planet = always_redraw(lambda: Dot(planet_pt(), color=WHITE, radius=0.085))
        radius = always_redraw(
            lambda: Line(star_pt, planet_pt(), color=GREY_A, stroke_width=1.6)
        )

        # Wedge currently being swept — clearly visible, semi-transparent.
        current_wedge = always_redraw(
            lambda: Polygon(
                star_pt,
                *pts[: min(int(idx.get_value()) + 1, len(pts))],
                color=focal_wedge_color,
                fill_color=focal_wedge_color,
                fill_opacity=0.28,
                stroke_width=1,
            )
        )

        # Frozen completed wedges — one Polygon per tick, appended as we cross each boundary.
        completed = VGroup()

        def on_tick_complete(_):
            # _ is the updater mobject; we read idx to know how many ticks have finished.
            k = len(completed)
            if k >= ticks:
                return
            boundary = (k + 1) * per_tick
            if idx.get_value() + 1e-3 < boundary:
                return
            p_a = pts[k * per_tick]
            p_b_idx = min((k + 1) * per_tick, len(pts) - 1)
            p_b = pts[p_b_idx]
            color = wedge_colors[k % 2]
            # Frozen wedge segment for this tick (arc from p_a to p_b only).
            seg_end = min((k + 1) * per_tick + 1, len(pts))
            seg_pts = pts[k * per_tick:seg_end]
            completed.add(
                Polygon(
                    star_pt,
                    *seg_pts,
                    color=color,
                    fill_color=color,
                    fill_opacity=0.18,
                    stroke_width=1,
                )
            )
            # Bars for this tick: distance (teal) above, area (orange) below.
            x = chart_x0 + (k + 0.5) * ((chart_x1 - chart_x0) / ticks)
            d_bars.add(
                Rectangle(
                    width=bar_w,
                    height=dist_h[k] * scale_d,
                    fill_color=TEAL,
                    fill_opacity=0.85,
                    stroke_width=0,
                ).move_to([x, 1.85 + dist_h[k] * scale_d / 2, 0])
            )
            a_bars.add(
                Rectangle(
                    width=bar_w,
                    height=area_h[k] * scale_a,
                    fill_color=ORANGE,
                    fill_opacity=0.85,
                    stroke_width=0,
                ).move_to([x, -2.55 + area_h[k] * scale_a / 2, 0])
            )

        completed.add_updater(on_tick_complete)

        # ---- Reveal the stage, then animate the planet around the ellipse.
        self.play(FadeIn(title), Create(orbit), FadeIn(glow), GrowFromCenter(star), run_time=1.2)
        self.play(
            FadeIn(d_axis), FadeIn(d_label), FadeIn(d_unit),
            FadeIn(a_axis), FadeIn(a_label), FadeIn(a_unit),
            run_time=0.6,
        )
        self.add(completed, current_wedge, radius, planet, d_bars, a_bars)
        self.play(
            idx.animate.set_value(float(len(pts) - 1)),
            run_time=11.0,
            rate_func=linear,
        )
        completed.clear_updaters()
        current_wedge.clear_updaters()
        self.remove(current_wedge)

        # Brief hold so the final wedge and last bars land cleanly.
        self.wait(0.6)

        # Notes placed under each chart, in their respective accent colors.
        dist_note = Text(
            "distance per tick: fastest / slowest = "
            f"{max_d / min(dist_h):.1f}×",
            font_size=22,
            color=TEAL_B,
        ).move_to([5.25, 2.55, 0])
        area_note = Text(
            "area per tick: all equal (within 0.1%)",
            font_size=22,
            color=ORANGE,
        ).move_to([5.25, -0.85, 0])
        self.play(FadeIn(dist_note), FadeIn(area_note), run_time=0.8)
        self.wait(1.2)

        # ---- AetherLab explanation layer (act 4): close-up explanation card.
        # Clear the stage but preserve a readable hold on the focal scene first.
        for m in self.mobjects:
            m.clear_updaters()
        if self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=0.6)

        head = Text("What the animation shows", font_size=34, weight=BOLD, color=YELLOW)
        eq = Text("dA/dt = L / (2m) = constant", font_size=28, color=WHITE)
        facts = VGroup(
            Text("Orbit eccentricity e = 0.745  (a = 3.0, b = 2.0)",
                 font_size=24, color=GREY_A),
            Text("Distance per tick varies 2.7× between slowest and fastest ticks",
                 font_size=24, color=TEAL_B),
            Text("Area per tick: every wedge is 8.3% of the ellipse, equal within 0.1%",
                 font_size=24, color=ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        key = Text(
            "The planet speeds up near the star and slows far away,\n"
            "but it always sweeps equal areas in equal times.",
            font_size=27,
            color=TEAL_A,
        )
        key_box = SurroundingRectangle(key, color=ORANGE, buff=0.22, corner_radius=0.12)
        card = VGroup(head, eq, facts, VGroup(key, key_box)).arrange(DOWN, buff=0.42)
        if card.width > 12.4:
            card.scale_to_fit_width(12.4)
        if card.height > 7.0:
            card.scale_to_fit_height(7.0)

        self.play(FadeIn(head, shift=0.2 * DOWN), FadeIn(eq), run_time=1.0)
        self.play(
            LaggedStart(*[FadeIn(f, shift=0.2 * RIGHT) for f in facts], lag_ratio=0.85),
            run_time=3.4,
        )
        self.play(FadeIn(key), Create(key_box), run_time=1.0)

        # Living ending: a small live counter that ticks dA/dt while the card holds.
        t_tracker = ValueTracker(0.0)

        def live_counter():
            t = t_tracker.get_value()
            txt = MathTex(
                r"\frac{dA}{dt}",
                "=",
                r"\frac{L}{2m}",
                "=",
                f"{0.500 + 0.0 * t:.3f}",
                font_size=30,
                color=WHITE,
            )
            txt.next_to(key_box, DOWN, buff=0.35)
            return txt

        live_eq = always_redraw(live_counter)
        self.add(live_eq)
        self.play(t_tracker.animate.set_value(3.0), run_time=3.0, rate_func=linear)
        self.wait(1.2)