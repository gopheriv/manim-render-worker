from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # Palette
        BLUE_C = BLUE
        RED_C = RED
        YELLOW_C = YELLOW
        TEXT_C = WHITE
        DIM_C = GREY_B

        # ---- Geometry constants ----
        FRAME_W = config.frame_width
        FRAME_H = config.frame_height

        # World x-range for the carts in scene units
        SCENE_X0_BLUE = -3.2
        SCENE_X0_RED = 3.2
        SCENE_X_COLLIDE = 0.0
        SCENE_X_FINAL_BLUE = -1.6
        SCENE_X_FINAL_RED = 2.6

        def scene_x1(t):
            if t <= 1.0:
                return SCENE_X0_BLUE + t * (SCENE_X_COLLIDE - SCENE_X0_BLUE) / 1.0
            return SCENE_X_COLLIDE + (t - 1.0) * (SCENE_X_FINAL_BLUE - SCENE_X_COLLIDE) / (2.5 - 1.0)

        def scene_x2(t):
            if t <= 1.0:
                return SCENE_X_FINAL_RED
            return SCENE_X_COLLIDE + (t - 1.0) * (SCENE_X_FINAL_RED - SCENE_X_COLLIDE) / (2.5 - 1.0)

        # ---- Track (thin RECTANGLE running across lower third) ----
        track = Rectangle(
            width=FRAME_W - 0.6,
            height=0.18,
            stroke_color=GREY_C,
            fill_color=GREY_E,
            fill_opacity=0.45,
            stroke_width=2,
        ).move_to(np.array([0.0, -3.4, 0.0]))

        # Tick marks along the track for visual rhythm
        ticks = VGroup()
        for i in range(-6, 7):
            t_mark = Line(
                start=np.array([i * 0.6, -3.55, 0.0]),
                end=np.array([i * 0.6, -3.25, 0.0]),
                stroke_color=GREY_B,
                stroke_width=1.2,
                stroke_opacity=0.55,
            )
            ticks.add(t_mark)
        ticks.move_to(np.array([0.0, 0.0, 0.0]))

        # Track label: moved RIGHT side to avoid left-edge clipping
        track_label = Text("frictionless rail", font_size=20, color=GREY_B)
        track_label.next_to(track, RIGHT, buff=0.25)

        # ---- Carts ----
        cart_blue = RoundedRectangle(
            width=1.05, height=0.55, corner_radius=0.08,
            stroke_color=BLUE_E, fill_color=BLUE_C, fill_opacity=1.0, stroke_width=2,
        )
        cart_blue_label = Text("m1", font_size=22, color=WHITE).move_to(cart_blue.get_center())

        cart_red = RoundedRectangle(
            width=0.78, height=0.45, corner_radius=0.08,
            stroke_color=RED_E, fill_color=RED_C, fill_opacity=1.0, stroke_width=2,
        )
        cart_red_label = Text("m2", font_size=22, color=WHITE).move_to(cart_red.get_center())

        cart_blue_group = VGroup(cart_blue, cart_blue_label)
        cart_red_group = VGroup(cart_red, cart_red_label)

        # ---- Title ----
        title = Text("Elastic Collision on a Track", color=TEXT_C, font_size=30)
        title.to_edge(UP, buff=0.25)

        # ---- Position-vs-time plot: dominant background, fills upper two-thirds ----
        PLOT_CENTER = np.array([0.0, 1.4, 0.0])
        PLOT_W = 12.6
        PLOT_H = 5.2

        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[-0.5, 2.2, 1],
            x_length=PLOT_W,
            y_length=PLOT_H,
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 1.8,
                         "include_tip": False},
        ).move_to(PLOT_CENTER)

        x_axis_label = Text("time t (s)", font_size=22, color=GREY_A)
        x_axis_label.next_to(axes.x_axis, RIGHT, buff=0.15)
        y_axis_label = Text("position x (m)", font_size=22, color=GREY_A)
        y_axis_label.next_to(axes.y_axis, UP, buff=0.1)

        # Background panel for HUD legibility
        hud_bg = Rectangle(
            width=3.4, height=1.55,
            stroke_color=GREY_B, stroke_width=1,
            fill_color=BLACK, fill_opacity=0.78,
        ).to_corner(DL, buff=0.30)

        # ---- Value label group (HUD) — high-contrast on near-black panel ----
        def make_hud():
            m1_num = DecimalNumber(2.0, num_decimal_places=1, font_size=28, color=BLUE_A)
            v1_num = DecimalNumber(1.0, num_decimal_places=2, font_size=28, color=BLUE_A)
            m2_num = DecimalNumber(1.0, num_decimal_places=1, font_size=28, color=RED_A)
            v2_num = DecimalNumber(0.0, num_decimal_places=2, font_size=28, color=RED_A)

            m1_text = MathTex("m_1=", font_size=28, color=BLUE_A)
            v1_text = MathTex("v_1=", font_size=28, color=BLUE_A)
            m2_text = MathTex("m_2=", font_size=28, color=RED_A)
            v2_text = MathTex("v_2=", font_size=28, color=RED_A)

            row1 = VGroup(m1_text, m1_num).arrange(RIGHT, buff=0.10)
            row2 = VGroup(v1_text, v1_num).arrange(RIGHT, buff=0.10)
            row3 = VGroup(m2_text, m2_num).arrange(RIGHT, buff=0.10)
            row4 = VGroup(v2_text, v2_num).arrange(RIGHT, buff=0.10)

            grid = VGroup(row1, row2, row3, row4).arrange(
                DOWN, aligned_edge=LEFT, buff=0.16
            )
            grid.move_to(hud_bg.get_center())
            return VGroup(grid), m1_num, v1_num, m2_num, v2_num

        hud, m1_num, v1_num, m2_num, v2_num = make_hud()

        # ---- Physical trajectories ----
        T_MIN, T_MAX = 0.0, 3.0

        def x1_phys(t):
            if t <= 1.0:
                return 0.0 + 1.0 * t
            return 1.0 + (-1.0 / 3.0) * (t - 1.0)

        def x2_phys(t):
            if t <= 1.0:
                return 1.0
            return 1.0 + (4.0 / 3.0) * (t - 1.0)

        def P(t, x_phys):
            return axes.coords_to_point(t, x_phys)

        pre1 = axes.plot(
            lambda tt: x1_phys(tt) if tt <= 1.0 else x1_phys(1.0),
            x_range=[0.0, 1.0, 0.01],
            color=BLUE_C,
            stroke_width=6,
        )
        pre2 = axes.plot(
            lambda tt: x2_phys(tt),
            x_range=[0.0, 1.0, 0.01],
            color=RED_C,
            stroke_width=6,
        )

        post1 = axes.plot(
            lambda tt: x1_phys(tt) if tt > 1.0 else x1_phys(1.0),
            x_range=[1.0, 3.0, 0.01],
            color=BLUE_C,
            stroke_width=6,
        )
        post2 = axes.plot(
            lambda tt: x2_phys(tt) if tt > 1.0 else x2_phys(1.0),
            x_range=[1.0, 3.0, 0.01],
            color=RED_C,
            stroke_width=6,
        )

        t_c_label = MathTex("t_c = 1.0\\,\\text{s}", color=YELLOW_C, font_size=28)
        t_c_label.next_to(P(1.0, 1.0), UR, buff=0.15)
        collision_dot = Dot(P(1.0, 1.0), color=YELLOW_C, radius=0.09)
        collision_dot.set_stroke(YELLOW_C, width=2)

        # World-line trail markers (faint dotted history) to convey "bands"
        world_trail_blue = VGroup(*[
            Dot(P(tt, x1_phys(tt)), radius=0.045, color=BLUE_C, fill_opacity=0.55)
            for tt in np.arange(0.0, 1.05, 0.10)
        ])
        world_trail_red = VGroup(*[
            Dot(P(tt, x2_phys(tt)), radius=0.045, color=RED_C, fill_opacity=0.55)
            for tt in np.arange(0.0, 1.05, 0.10)
        ])

        # ---- Conservation labels: panel-style with frame for legibility ----
        cons1 = MathTex(
            "p_{\\text{tot}} = m_1 v_1 + m_2 v_2",
            font_size=28, color=WHITE,
        )
        cons2 = MathTex(
            "KE_{\\text{tot}} = \\tfrac{1}{2} m_1 v_1^2 + \\tfrac{1}{2} m_2 v_2^2",
            font_size=26, color=WHITE,
        )
        cons_panel = VGroup(cons1, cons2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        cons_panel.move_to(np.array([3.6, 2.0, 0.0]))
        cons_frame = SurroundingRectangle(
            cons_panel, color=GREY_B, stroke_width=1, buff=0.18,
            fill_color=BLACK, fill_opacity=0.72,
        )

        # ---- Flash ring (larger, brighter, double pulse for prominence) ----
        flash_outer = Annulus(
            inner_radius=0.10, outer_radius=0.55,
            color=YELLOW_C, stroke_width=12,
        ).move_to(np.array([SCENE_X_COLLIDE, -3.0, 0.0]))
        flash_inner = Annulus(
            inner_radius=0.05, outer_radius=0.32,
            color=YELLOW_C, stroke_width=10,
        ).move_to(np.array([SCENE_X_COLLIDE, -3.0, 0.0]))
        flash = VGroup(flash_outer, flash_inner)

        # ---- Velocity arrows (blue moves right pre, reverses left post) ----
        v_arrow_blue = always_redraw(
            lambda: Arrow(
                start=cart_blue.get_right(),
                end=cart_blue.get_right() + RIGHT * 1.0,
                color=BLUE_A, stroke_width=5, buff=0.05, max_tip_length_to_length_ratio=0.25,
            ).shift(UP * 0.55)
        )
        v_arrow_red_pre = always_redraw(
            lambda: Arrow(
                start=cart_red.get_left(),
                end=cart_red.get_left() + LEFT * 0.0,
                color=RED_A, stroke_width=5, buff=0.05, max_tip_length_to_length_ratio=0.25,
            ).shift(UP * 0.5)
        )
        v_arrow_red_post = always_redraw(
            lambda: Arrow(
                start=cart_red.get_left(),
                end=cart_red.get_left() + LEFT * -1.4,
                color=RED_A, stroke_width=5, buff=0.05, max_tip_length_to_length_ratio=0.25,
            ).shift(UP * 0.5)
        )

        # ============================================================
        # BEAT A1.B1 | 0.00-2.92 s   HOOK / ESTABLISH
        # ============================================================
        self.add(track, ticks)
        self.play(FadeIn(track_label, shift=LEFT * 0.2), run_time=0.4)

        # Place carts off-stage then slide them in
        cart_blue_group.move_to(np.array([SCENE_X0_BLUE - 1.5, -3.0, 0.0]))
        cart_red_group.move_to(np.array([SCENE_X0_RED, -3.0, 0.0]))
        self.add(cart_blue_group, cart_red_group)

        # Velocity arrow on the moving cart BEFORE the run so it's tied to motion
        self.add(v_arrow_blue)

        # Slide blue cart in from off-stage
        self.play(
            cart_blue_group.animate.move_to(np.array([SCENE_X0_BLUE, -3.0, 0.0])),
            run_time=1.2, rate_func=smooth,
        )
        # Blue cart continues drifting rightward (demonstrates v1 = +1 m/s)
        self.play(
            cart_blue_group.animate.move_to(
                np.array([SCENE_X_COLLIDE - 0.9, -3.0, 0.0])
            ),
            run_time=1.1, rate_func=smooth,
        )
        # Title written
        self.play(Write(title), run_time=0.6)

        # ============================================================
        # BEAT A1.B2 | 2.92-5.00 s   READOUTS
        # ============================================================
        self.play(
            FadeIn(hud_bg, shift=LEFT * 0.2),
            FadeIn(hud, shift=LEFT * 0.2),
            run_time=0.7,
        )
        # Animate v1_num reading to reinforce the visible motion
        self.play(v1_num.animate.set_value(1.0), run_time=0.4)
        self.wait(0.9)

        # ============================================================
        # BEAT A2.B1 | 5.00-8.00 s   WORLD-LINES (axes + pre segments)
        # ============================================================
        self.play(
            Create(axes, run_time=0.7),
            FadeIn(x_axis_label, shift=UP * 0.15),
            FadeIn(y_axis_label, shift=RIGHT * 0.15),
            run_time=0.8,
        )
        self.play(
            FadeIn(world_trail_blue, lag_ratio=0.05),
            FadeIn(world_trail_red, lag_ratio=0.05),
            run_time=0.6,
        )
        self.play(
            Create(pre1),
            Create(pre2),
            FadeIn(collision_dot, scale=0.5),
            run_time=1.4,
        )
        self.play(FadeIn(t_c_label, shift=UP * 0.2), run_time=0.4)
        self.wait(0.3)

        # ============================================================
        # BEAT A2.B2 | 8.00-11.00 s   CONSERVATION LAWS
        # ============================================================
        self.play(FadeIn(cons_frame, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(cons1, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(cons2, shift=RIGHT * 0.2), run_time=0.5)
        self.wait(1.0)

        # ============================================================
        # BEAT A3.B1 | 11.00-15.50 s   COLLISION
        # ============================================================
        t_clock = ValueTracker(0.0)

        def upd_blue(m):
            tt = t_clock.get_value()
            m.move_to(np.array([scene_x1(tt), -3.0, 0.0]))

        def upd_red(m):
            tt = t_clock.get_value()
            m.move_to(np.array([scene_x2(tt), -3.0, 0.0]))

        # Freeze the visible motion in HUD
        cart_blue_group.add_updater(upd_blue)
        cart_red_group.add_updater(upd_red)

        # Remove pre-collision blue velocity arrow (it was a static placeholder)
        self.remove(v_arrow_blue)
        # Add a "zero" arrow over red cart pre-collision
        self.add(v_arrow_red_pre)

        # Drive to t=0.99
        self.play(t_clock.animate.set_value(0.99), run_time=2.0, rate_func=linear)
        self.wait(0.2)

        # PROMINENT flash at collision (larger + double pulse)
        flash.move_to(np.array([SCENE_X_COLLIDE, -3.0, 0.0]))
        self.add(flash)
        # First pulse: scale up + fade
        self.play(
            t_clock.animate.set_value(1.02),
            flash[0].animate.set_opacity(0.0).scale(2.2),
            flash[1].animate.set_opacity(0.0).scale(1.8),
            run_time=0.35,
            rate_func=linear,
        )
        # Reset flash for second pulse to feel weight
        flash[0].set_opacity(1.0).scale(1 / 2.2)
        flash[1].set_opacity(1.0).scale(1 / 1.8)
        self.add(flash)
        self.play(
            t_clock.animate.set_value(1.05),
            flash[0].animate.set_opacity(0.0).scale(2.6),
            flash[1].animate.set_opacity(0.0).scale(2.0),
            run_time=0.35,
            rate_func=linear,
        )

        # Switch red arrow: from "stopped" indicator to "moving right" post-collision
        self.remove(v_arrow_red_pre)
        self.add(v_arrow_red_post)

        # Continue past collision
        self.play(t_clock.animate.set_value(2.5), run_time=1.5, rate_func=linear)

        # ============================================================
        # BEAT A3.B2 | 15.50-20.00 s   POST-COLLISION READOUTS
        # ============================================================
        self.play(
            v1_num.animate.set_value(-1.0 / 3.0),
            v2_num.animate.set_value(4.0 / 3.0),
            Flash(v1_num, color=BLUE_C, flash_radius=0.4, line_length=0.2, num_lines=10),
            Flash(v2_num, color=RED_C, flash_radius=0.4, line_length=0.2, num_lines=10),
            run_time=1.2,
        )
        self.wait(2.5)

        # ============================================================
        # BEAT A4.B1 | 20.00-23.50 s   POST-COLLISION WORLD-LINES
        # ============================================================
        self.play(
            Create(post1),
            Create(post2),
            run_time=1.4,
        )
        # Post-collision slope labels: place OUTSIDE the data line envelope
        # so they never overlap the world-line curve.
        slope1 = MathTex("v_1' = -\\tfrac{1}{3}\\,\\text{m/s}",
                         font_size=24, color=BLUE_A)
        slope1.next_to(axes.coords_to_point(2.4, x1_phys(2.4)), DL, buff=0.20)
        slope2 = MathTex("v_2' = +\\tfrac{4}{3}\\,\\text{m/s}",
                         font_size=24, color=RED_A)
        slope2.next_to(axes.coords_to_point(2.4, x2_phys(2.4)), UR, buff=0.20)
        self.play(FadeIn(slope1, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(slope2, shift=DOWN * 0.15), run_time=0.5)
        self.wait(0.5)

        # ============================================================
        # BEAT A4.B2 | 23.50-26.00 s   HERO ANNOTATION
        # ============================================================
        hero = MathTex("\\Delta p = 0,\\quad \\Delta KE = 0",
                       font_size=38, color=YELLOW_C)
        hero.move_to(np.array([3.6, -1.7, 0.0]))
        self.play(FadeIn(hero, shift=UP * 0.2), run_time=0.6)
        self.wait(1.8)

        # ============================================================
        # BEAT A5.B1 | 26.00-30.00 s   REVEAL & LIVING ENDING
        # ============================================================
        # Remove heavy updaters; show resolution with conservation
        # equations still present.
        cart_blue_group.remove_updater(upd_blue)
        cart_red_group.remove_updater(upd_red)

        # Remove velocity arrows at the curtain close
        self.remove(v_arrow_red_post)

        # Re-anchor carts at a clearly post-collision pose
        t_clock.set_value(2.95)
        cart_blue_group.move_to(np.array([scene_x1(2.95), -3.0, 0.0]))
        cart_red_group.move_to(np.array([scene_x2(2.95), -3.0, 0.0]))

        # Build KE equality in a non-yellow panel so yellow stays climactic
        self.play(
            FadeOut(title),
            FadeOut(track_label),
            run_time=0.5,
        )
        # The conservation equations panel stays put; the world-lines own the stage.
        ke_eq = MathTex(
            "KE_{\\text{after}} = KE_{\\text{before}} = "
            "\\tfrac{1}{2}(2)(1)^2 = 1.0\\,\\text{J}",
            font_size=26, color=WHITE,
        )
        ke_eq_panel = SurroundingRectangle(
            ke_eq, color=GREY_B, stroke_width=1, buff=0.18,
            fill_color=BLACK, fill_opacity=0.72,
        )
        ke_eq.move_to(np.array([0.0, -2.25, 0.0]))
        ke_eq_panel.move_to(ke_eq.get_center())
        self.play(
            FadeIn(ke_eq_panel, shift=UP * 0.2),
            FadeIn(ke_eq, shift=UP * 0.2),
            run_time=0.6,
        )

        # Living ending: carts continue to drift via a fresh ValueTracker
        # so sampled frames differ in the last beats.
        t_idle = ValueTracker(2.95)

        def upd_blue_idle(m):
            tt = t_idle.get_value()
            m.move_to(np.array([scene_x1(tt), -3.0, 0.0]))

        def upd_red_idle(m):
            tt = t_idle.get_value()
            m.move_to(np.array([scene_x2(tt), -3.0, 0.0]))

        cart_blue_group.add_updater(upd_blue_idle)
        cart_red_group.add_updater(upd_red_idle)

        for target in [3.0, 2.6, 3.1, 2.8]:
            self.play(t_idle.animate.set_value(target), run_time=0.45, rate_func=linear)