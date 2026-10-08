from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # Palette
        BLUE_C = BLUE
        RED_C = RED
        YELLOW_C = YELLOW
        TEXT_C = WHITE
        DIM = GREY_B

        # ---- Geometry constants ----
        FRAME_W = config.frame_width
        FRAME_H = config.frame_height

        # World x-range for the carts in scene units
        X_MIN, X_MAX = -4.2, 4.2
        SCENE_X0_BLUE = -3.2   # start position for m1
        SCENE_X0_RED = 3.2     # parking position for m2 (off-stage left first)
        SCENE_X_COLLIDE = 0.0  # collision x in scene units
        SCENE_X_FINAL_BLUE = -1.6
        SCENE_X_FINAL_RED = 2.6

        # Physical-to-scene scaling (so collision lands near centre bottom)
        # x1(t<t_c) = 0 + 1*t  -> x scene = -3 + t   (t in 0..1 => -3..-2)
        # x2(t<t_c) = 1
        # collision at t_c=1, position in scene ~ SCENE_X_COLLIDE
        # After: x1 rebounds to -1/3 m/s, x2 launches to 4/3 m/s

        def scene_x1(t):
            if t <= 1.0:
                return SCENE_X0_BLUE + t * (SCENE_X_COLLIDE - SCENE_X0_BLUE) / 1.0
            return SCENE_X_COLLIDE + (t - 1.0) * (SCENE_X_FINAL_BLUE - SCENE_X_COLLIDE) / (2.5 - 1.0)

        def scene_x2(t):
            if t <= 1.0:
                return SCENE_X_FINAL_RED + 0.0 * t  # parked
            return SCENE_X_COLLIDE + (t - 1.0) * (SCENE_X_FINAL_RED - SCENE_X_COLLIDE) / (2.5 - 1.0)

        # ---- Track (thin RECTANGLE running across lower third) ----
        track = Rectangle(
            width=FRAME_W - 1.0,
            height=0.18,
            stroke_color=GREY_C,
            fill_color=GREY_E,
            fill_opacity=0.35,
            stroke_width=2,
        ).move_to(np.array([0.0, -3.4, 0.0]))

        track_label = Text("frictionless rail", font_size=22, color=GREY_B)
        track_label.next_to(track, LEFT, buff=0.2)

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

        def place_blue(t):
            cart_blue_group.move_to(np.array([scene_x1(t), -3.0, 0.0]))

        def place_red(t):
            cart_red_group.move_to(np.array([scene_x2(t), -3.0, 0.0]))

        # ---- Title ----
        title = Text("Elastic Collision on a Track", color=TEXT_C, font_size=34)
        title.to_edge(UP, buff=0.35)

        # ---- Position-vs-time strip chart ----
        PLOT_CENTER = np.array([-1.4, 0.4, 0.0])
        PLOT_W = 7.6
        PLOT_H = 4.2

        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[-0.5, 2.2, 1],
            x_length=PLOT_W,
            y_length=PLOT_H,
            tips=False,
            axis_config={"stroke_color": GREY_B, "stroke_width": 1.5,
                         "include_tip": False},
        ).move_to(PLOT_CENTER)

        x_axis_label = Text("time t (s)", font_size=22, color=GREY_B)
        x_axis_label.next_to(axes.x_axis, RIGHT, buff=0.15)
        y_axis_label = Text("position x (m)", font_size=22, color=GREY_B)
        y_axis_label.next_to(axes.y_axis, UP, buff=0.1)

        # Convert physical (x_phys, t) to scene plot coords
        # physical: x in [0, 1.6], t in [0, 3]
        T_MIN, T_MAX = 0.0, 3.0
        X_MIN_P, X_MAX_P = 0.0, 1.6

        def x1_phys(t):
            if t <= 1.0:
                return 0.0 + 1.0 * t
            return 1.0 + (-1.0 / 3.0) * (t - 1.0)

        def x2_phys(t):
            if t <= 1.0:
                return 1.0
            return 1.0 + (4.0 / 3.0) * (t - 1.0)

        def to_plot(t, x_phys):
            # map t in [T_MIN,T_MAX] -> [0,1] along axes x
            tx = (t - T_MIN) / (T_MAX - T_MIN)
            yy = (x_phys - X_MIN_P) / (X_MAX_P - X_MIN_P)
            return axes.c2p(tx * PLOT_W / PLOT_W, yy)
            # axes.c2p expects data coords directly; use axes.coords_to_point
        # Simpler: use axes input_coords_to_plot
        # ManimCE Axes.c2p(x,y) uses x_axis_range directly. Map:
        # x_axis_range is [0,3] over width PLOT_W. Use:
        def P(t, x_phys):
            return axes.coords_to_point(t, x_phys)

        # Pre-build static pre-collision segments (always present after act 2)
        pre1 = axes.plot(
            lambda tt: x1_phys(tt) if tt <= 1.0 else x1_phys(1.0),
            x_range=[0.0, 1.0, 0.01],
            color=BLUE_C,
            stroke_width=4,
        )
        pre2 = axes.plot(
            lambda tt: x2_phys(tt),
            x_range=[0.0, 1.0, 0.01],
            color=RED_C,
            stroke_width=4,
        )

        # Post-collision segments (added in reveal)
        post1 = axes.plot(
            lambda tt: x1_phys(tt) if tt > 1.0 else x1_phys(1.0),
            x_range=[1.0, 3.0, 0.01],
            color=BLUE_C,
            stroke_width=4,
        )
        post2 = axes.plot(
            lambda tt: x2_phys(tt) if tt > 1.0 else x2_phys(1.0),
            x_range=[1.0, 3.0, 0.01],
            color=RED_C,
            stroke_width=4,
        )

        # Collision marker
        t_c_label = MathTex("t_c = 1.0\\,\\text{s}", color=YELLOW_C, font_size=30)
        collision_dot = Dot(P(1.0, 1.0), color=YELLOW_C, radius=0.07)

        # ---- Value label group (HUD) ----
        def make_hud():
            m1_num = DecimalNumber(2.0, num_decimal_places=1, font_size=30, color=BLUE_C)
            v1_num = DecimalNumber(1.0, num_decimal_places=2, font_size=30, color=BLUE_C)
            m2_num = DecimalNumber(1.0, num_decimal_places=1, font_size=30, color=RED_C)
            v2_num = DecimalNumber(0.0, num_decimal_places=2, font_size=30, color=RED_C)

            m1_text = MathTex("m_1=", "\\,", "\\text{kg}", font_size=30, color=BLUE_C)
            v1_text = MathTex("v_1=", "\\,", "\\text{m/s}", font_size=30, color=BLUE_C)
            m2_text = MathTex("m_2=", "\\,", "\\text{kg}", font_size=30, color=RED_C)
            v2_text = MathTex("v_2=", "\\,", "\\text{m/s}", font_size=30, color=RED_C)

            row1 = VGroup(m1_text, m1_num).arrange(RIGHT, buff=0.1)
            row2 = VGroup(v1_text, v1_num).arrange(RIGHT, buff=0.1)
            row3 = VGroup(m2_text, m2_num).arrange(RIGHT, buff=0.1)
            row4 = VGroup(v2_text, v2_num).arrange(RIGHT, buff=0.1)

            grid = VGroup(row1, row2, row3, row4).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            grid.to_corner(DR, buff=0.55)
            return grid, m1_num, v1_num, m2_num, v2_num

        hud, m1_num, v1_num, m2_num, v2_num = make_hud()

        # ---- Conservation label (act 2) ----
        cons1 = MathTex(
            "p_{\\text{tot}} = m_1 v_1 + m_2 v_2",
            font_size=30, color=WHITE,
        ).to_corner(UL, buff=0.6)
        cons2 = MathTex(
            "KE_{\\text{tot}} = \\tfrac{1}{2} m_1 v_1^2 + \\tfrac{1}{2} m_2 v_2^2",
            font_size=30, color=WHITE,
        ).next_to(cons1, DOWN, aligned_edge=LEFT, buff=0.22)

        # ---- Flash ring ----
        flash = Annulus(
            inner_radius=0.05, outer_radius=0.55,
            color=YELLOW_C, stroke_width=6,
        ).move_to(np.array([SCENE_X_COLLIDE, -3.0, 0.0]))

        # ============================================================
        # BEAT A1.B1 | 0.00-2.92 s
        # ============================================================
        # Stage: empty track enters, carts slide in from the wings.
        self.add(track)
        self.play(FadeIn(track_label, shift=RIGHT * 0.2), run_time=0.4)

        # Place carts off-stage then move into position
        cart_blue_group.move_to(np.array([SCENE_X0_BLUE - 1.5, -3.0, 0.0]))
        cart_red_group.move_to(np.array([SCENE_X0_RED, -3.0, 0.0]))
        self.add(cart_blue_group, cart_red_group)

        self.play(
            cart_blue_group.animate.move_to(np.array([SCENE_X0_BLUE, -3.0, 0.0])),
            run_time=1.2, rate_func=smooth,
        )
        # Quick shift toward collision point so viewer feels incoming
        self.play(
            cart_blue_group.animate.move_to(np.array([SCENE_X_COLLIDE - 0.9, -3.0, 0.0])),
            run_time=1.1, rate_func=smooth,
        )
        # Settle title (small hook)
        self.play(Write(title), run_time=0.6)
        # Hold briefly

        # ============================================================
        # BEAT A1.B2 | 2.92-5.00 s
        # ============================================================
        # HUD blooms: m1, v1, m2, v2 readouts
        # Build HUD off-screen first (we'll FadeIn)
        self.play(FadeIn(hud, shift=LEFT * 0.2), run_time=0.7)
        self.wait(1.0)
        # Hold remaining
        self.wait(0.4)

        # ============================================================
        # BEAT A2.B1 | 5.00-8.00 s
        # ============================================================
        # Faint world-line bands rise: pre-collision blue climbs, red flat.
        # Draw axes and pre segments.
        self.play(
            Create(axes, run_time=0.8),
            FadeIn(x_axis_label, shift=UP * 0.15),
            FadeIn(y_axis_label, shift=RIGHT * 0.15),
            run_time=0.9,
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
        # BEAT A2.B2 | 8.00-11.00 s
        # ============================================================
        # Conservation laws fade onto upper-left.
        self.play(
            FadeIn(cons1, shift=RIGHT * 0.2),
            run_time=0.7,
        )
        self.play(
            FadeIn(cons2, shift=RIGHT * 0.2),
            run_time=0.7,
        )
        # Readable hold
        self.wait(1.4)

        # ============================================================
        # BEAT A3.B1 | 11.00-15.50 s
        # ============================================================
        # Collision flash, carts bounce: blue reverses, red launches.
        # Bring carts together first (so they touch at SCENE_X_COLLIDE)
        # Drive by t_clock so positions stay consistent.
        t_clock = ValueTracker(0.0)

        def upd_blue(m):
            tt = t_clock.get_value()
            m.move_to(np.array([scene_x1(tt), -3.0, 0.0]))

        def upd_red(m):
            tt = t_clock.get_value()
            m.move_to(np.array([scene_x2(tt), -3.0, 0.0]))

        cart_blue_group.add_updater(upd_blue)
        cart_red_group.add_updater(upd_red)

        # Drive to t=0.99 (just before collision)
        self.play(t_clock.animate.set_value(0.99), run_time=2.0, rate_func=linear)
        # Hold for the narrative beat
        self.wait(0.3)

        # Flash at collision
        flash.move_to(np.array([SCENE_X_COLLIDE, -3.0, 0.0]))
        self.add(flash)
        # Step through collision instant: t goes from 0.99 to 1.05
        self.play(
            t_clock.animate.set_value(1.05),
            flash.animate.set_opacity(0.0).scale(1.6),
            run_time=0.5,
            rate_func=linear,
        )
        # Continue past to t=2.5
        self.play(t_clock.animate.set_value(2.5), run_time=1.6, rate_func=linear)

        # ============================================================
        # BEAT A3.B2 | 15.50-20.00 s
        # ============================================================
        # Rewire HUD numbers to post-collision values.
        # v1_prime = -1/3, v2_prime = +4/3
        # Animate v1 and v2 numbers; keep m1,m2 fixed.
        self.play(
            v1_num.animate.set_value(-1.0 / 3.0),
            v2_num.animate.set_value(4.0 / 3.0),
            Flash(v1_num, color=BLUE_C, flash_radius=0.35, line_length=0.2, num_lines=8),
            Flash(v2_num, color=RED_C, flash_radius=0.35, line_length=0.2, num_lines=8),
            run_time=1.2,
        )
        self.wait(2.5)

        # ============================================================
        # BEAT A4.B1 | 20.00-23.50 s
        # ============================================================
        # World-line bands extend past t_c; add post segments.
        self.play(
            Create(post1),
            Create(post2),
            run_time=1.4,
        )
        # Tiny slope labels
        slope1 = MathTex("v_1' = -\\tfrac{1}{3}\\,\\text{m/s}",
                         font_size=28, color=BLUE_C)
        slope1.next_to(post1, UP, buff=0.25).shift(LEFT * 0.2)
        slope2 = MathTex("v_2' = +\\tfrac{4}{3}\\,\\text{m/s}",
                         font_size=28, color=RED_C)
        slope2.next_to(post2, DOWN, buff=0.25).shift(LEFT * 0.2)
        self.play(FadeIn(slope1, shift=UP * 0.15), run_time=0.5)
        self.play(FadeIn(slope2, shift=DOWN * 0.15), run_time=0.5)
        self.wait(0.5)

        # ============================================================
        # BEAT A4.B2 | 23.50-26.00 s
        # ============================================================
        # Hero annotation: Δp=0, ΔKE=0
        hero = MathTex("\\Delta p = 0,\\quad \\Delta KE = 0",
                       font_size=40, color=YELLOW_C)
        hero.move_to(np.array([3.2, -1.6, 0.0]))
        self.play(FadeIn(hero, shift=UP * 0.2), run_time=0.6)
        # Hold (idle keeps carts moving via updater)
        self.wait(1.8)

        # ============================================================
        # BEAT A5.B1 | 26.00-30.00 s
        # ============================================================
        # Clear extraneous labels, keep plot, slopes, KE equality.
        # Fade out hud, cons labels, title, hero, flash remnants.
        self.play(
            FadeOut(hud),
            FadeOut(cons1),
            FadeOut(cons2),
            FadeOut(title),
            FadeOut(hero),
            FadeOut(track_label),
            run_time=0.7,
        )
        # KE equality remains
        ke_eq = MathTex(
            "KE_{\\text{after}} = KE_{\\text{before}} = "
            "\\tfrac{1}{2}(2)(1)^2 = 1.0\\,\\text{J}",
            font_size=32, color=YELLOW_C,
        ).move_to(np.array([0.0, -2.4, 0.0]))
        self.play(FadeIn(ke_eq, shift=UP * 0.2), run_time=0.6)

        # Idle loop: keep carts moving via updater (t_clock keeps advancing)
        # Drive t_clock slightly further then idle with updaters still on.
        self.play(t_clock.animate.set_value(2.95), run_time=0.6, rate_func=linear)

        # Live idle: a sampling updater that nudges the carts along.
        # Remove the heavy updaters and replace with a slow always_redraw
        # micro-shift using the ValueTracker.
        cart_blue_group.remove_updater(upd_blue)
        cart_red_group.remove_updater(upd_red)

        t_clock.set_value(2.95)
        t_idle = ValueTracker(2.95)

        def upd_blue_idle(m):
            tt = t_idle.get_value()
            m.move_to(np.array([scene_x1(tt), -3.0, 0.0]))

        def upd_red_idle(m):
            tt = t_idle.get_value()
            m.move_to(np.array([scene_x2(tt), -3.0, 0.0]))

        cart_blue_group.add_updater(upd_blue_idle)
        cart_red_group.add_updater(upd_red_idle)

        # Animate the tracker to advance, then bounce back so the carts
        # continue to move at sampled times (final three frames differ).
        for target in [3.4, 2.6, 3.1, 2.8]:
            self.play(t_idle.animate.set_value(target), run_time=0.4, rate_func=linear)

