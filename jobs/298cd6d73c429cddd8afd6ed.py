import math

import numpy as np
from manim import *


class AetherLabScene(Scene):
    def construct(self):
        ts = [0.0, 0.012, 0.024, 0.036, 0.0481, 0.0601, 0.0721, 0.0841, 0.0961, 0.1081, 0.1201, 0.1321, 0.1442, 0.1562, 0.1682, 0.1802, 0.1922, 0.2042, 0.2162, 0.2283, 0.2403, 0.2523, 0.2643, 0.2763, 0.2883, 0.3003, 0.3123, 0.3244, 0.3364, 0.3484, 0.3604, 0.3724, 0.3844, 0.3964, 0.4085, 0.4205, 0.4325, 0.4445, 0.4565, 0.4685, 0.4805, 0.4925, 0.5046, 0.5166, 0.5286, 0.5406, 0.5526, 0.5646, 0.5766, 0.5887, 0.6007, 0.6127, 0.6247, 0.6367, 0.6487, 0.6607, 0.6727, 0.6848, 0.6968, 0.7088, 0.7208, 0.7328, 0.7448, 0.7568, 0.7689, 0.7809, 0.7929, 0.8049, 0.8169, 0.8289, 0.8409, 0.8529, 0.865, 0.877, 0.889, 0.901, 0.913, 0.925, 0.937, 0.9491, 0.9611, 0.9731, 0.9851, 0.9971, 1.0091, 1.0211, 1.0331, 1.0452, 1.0572, 1.0692, 1.0812, 1.0932, 1.1052, 1.1172, 1.1293, 1.1413, 1.1533, 1.1653, 1.1773, 1.1893, 1.2013, 1.2134, 1.2254, 1.2374, 1.2494, 1.2614, 1.2734, 1.2854, 1.2974, 1.3095, 1.3215, 1.3335, 1.3455, 1.3575, 1.3695, 1.3815, 1.3936, 1.4056, 1.4176, 1.4296, 1.4416, 1.4536, 1.4656, 1.4776, 1.4897, 1.5017, 1.5137, 1.5257, 1.5377, 1.5497, 1.5617, 1.5738, 1.5858, 1.5978, 1.6098, 1.6218, 1.6338, 1.6458, 1.6578, 1.6699, 1.6819, 1.6939, 1.7059, 1.7179, 1.7299, 1.7419, 1.754, 1.766, 1.778, 1.79, 1.802, 1.814, 1.826, 1.838, 1.8501, 1.8621, 1.8741, 1.8861, 1.8981, 1.9101, 1.9221, 1.9342, 1.9462, 1.9582, 1.9702, 1.9822, 1.9942, 2.0062, 2.0182, 2.0303, 2.0423, 2.0543, 2.0663, 2.0783, 2.0903, 2.1023, 2.1144, 2.1264, 2.1384, 2.1504, 2.1624, 2.1744, 2.1864, 2.1984, 2.2105, 2.2225, 2.2345, 2.2465, 2.2585, 2.2705, 2.2825, 2.2946, 2.3066, 2.3186, 2.3306, 2.3426, 2.3546, 2.3666, 2.3786, 2.3907, 2.4027, 2.4147, 2.4267, 2.4387, 2.4507, 2.4627, 2.4748, 2.4868, 2.4988, 2.5108, 2.5228, 2.5348, 2.5468, 2.5588, 2.5709, 2.5829, 2.5949, 2.6069, 2.6189, 2.6309, 2.6429, 2.655, 2.667, 2.679, 2.691, 2.703, 2.715, 2.727, 2.739, 2.7511, 2.7631, 2.7751, 2.7871, 2.7991, 2.8111, 2.8231, 2.8352, 2.8472, 2.8592, 2.8712, 2.8832]
        xs = [0.0, 0.1699, 0.3398, 0.5097, 0.6796, 0.8495, 1.0194, 1.1893, 1.3592, 1.5291, 1.6989, 1.8688, 2.0387, 2.2086, 2.3785, 2.5484, 2.7183, 2.8882, 3.0581, 3.228, 3.3979, 3.5678, 3.7377, 3.9076, 4.0775, 4.2474, 4.4173, 4.5872, 4.7571, 4.9269, 5.0968, 5.2667, 5.4366, 5.6065, 5.7764, 5.9463, 6.1162, 6.2861, 6.456, 6.6259, 6.7958, 6.9657, 7.1356, 7.3055, 7.4754, 7.6453, 7.8152, 7.985, 8.1549, 8.3248, 8.4947, 8.6646, 8.8345, 9.0044, 9.1743, 9.3442, 9.5141, 9.684, 9.8539, 10.0238, 10.1937, 10.3636, 10.5335, 10.7034, 10.8733, 11.0432, 11.213, 11.3829, 11.5528, 11.7227, 11.8926, 12.0625, 12.2324, 12.4023, 12.5722, 12.7421, 12.912, 13.0819, 13.2518, 13.4217, 13.5916, 13.7615, 13.9314, 14.1013, 14.2712, 14.441, 14.6109, 14.7808, 14.9507, 15.1206, 15.2905, 15.4604, 15.6303, 15.8002, 15.9701, 16.14, 16.3099, 16.4798, 16.6497, 16.8196, 16.9895, 17.1594, 17.3293, 17.4992, 17.669, 17.8389, 18.0088, 18.1787, 18.3486, 18.5185, 18.6884, 18.8583, 19.0282, 19.1981, 19.368, 19.5379, 19.7078, 19.8777, 20.0476, 20.2175, 20.3874, 20.5573, 20.7271, 20.897, 21.0669, 21.2368, 21.4067, 21.5766, 21.7465, 21.9164, 22.0863, 22.2562, 22.4261, 22.596, 22.7659, 22.9358, 23.1057, 23.2756, 23.4455, 23.6154, 23.7853, 23.9551, 24.125, 24.2949, 24.4648, 24.6347, 24.8046, 24.9745, 25.1444, 25.3143, 25.4842, 25.6541, 25.824, 25.9939, 26.1638, 26.3337, 26.5036, 26.6735, 26.8434, 27.0133, 27.1831, 27.353, 27.5229, 27.6928, 27.8627, 28.0326, 28.2025, 28.3724, 28.5423, 28.7122, 28.8821, 29.052, 29.2219, 29.3918, 29.5617, 29.7316, 29.9015, 30.0714, 30.2413, 30.4111, 30.581, 30.7509, 30.9208, 31.0907, 31.2606, 31.4305, 31.6004, 31.7703, 31.9402, 32.1101, 32.28, 32.4499, 32.6198, 32.7897, 32.9596, 33.1295, 33.2994, 33.4692, 33.6391, 33.809, 33.9789, 34.1488, 34.3187, 34.4886, 34.6585, 34.8284, 34.9983, 35.1682, 35.3381, 35.508, 35.6779, 35.8478, 36.0177, 36.1876, 36.3575, 36.5274, 36.6972, 36.8671, 37.037, 37.2069, 37.3768, 37.5467, 37.7166, 37.8865, 38.0564, 38.2263, 38.3962, 38.5661, 38.736, 38.9059, 39.0758, 39.2457, 39.4156, 39.5855, 39.7554, 39.9252, 40.0951, 40.265, 40.4349, 40.6048, 40.7747]
        ys = [0.0, 0.1692, 0.337, 0.5033, 0.6683, 0.8318, 0.9939, 1.1546, 1.3139, 1.4717, 1.6282, 1.7832, 1.9368, 2.089, 2.2398, 2.3891, 2.5371, 2.6836, 2.8287, 2.9724, 3.1147, 3.2556, 3.3951, 3.5331, 3.6697, 3.8049, 3.9387, 4.0711, 4.2021, 4.3316, 4.4597, 4.5864, 4.7117, 4.8356, 4.9581, 5.0791, 5.1988, 5.317, 5.4338, 5.5492, 5.6632, 5.7757, 5.8869, 5.9966, 6.1049, 6.2118, 6.3172, 6.4213, 6.524, 6.6252, 6.725, 6.8234, 6.9204, 7.0159, 7.1101, 7.2028, 7.2941, 7.384, 7.4725, 7.5596, 7.6453, 7.7295, 7.8123, 7.8937, 7.9737, 8.0523, 8.1295, 8.2052, 8.2795, 8.3524, 8.4239, 8.494, 8.5627, 8.6299, 8.6958, 8.7602, 8.8232, 8.8848, 8.945, 9.0037, 9.061, 9.117, 9.1715, 9.2246, 9.2762, 9.3265, 9.3754, 9.4228, 9.4688, 9.5134, 9.5566, 9.5983, 9.6387, 9.6776, 9.7151, 9.7512, 9.7859, 9.8192, 9.8511, 9.8815, 9.9105, 9.9381, 9.9643, 9.9891, 10.0125, 10.0344, 10.0549, 10.074, 10.0917, 10.108, 10.1229, 10.1363, 10.1484, 10.159, 10.1682, 10.176, 10.1824, 10.1873, 10.1908, 10.193, 10.1937, 10.193, 10.1908, 10.1873, 10.1824, 10.176, 10.1682, 10.159, 10.1484, 10.1363, 10.1229, 10.108, 10.0917, 10.074, 10.0549, 10.0344, 10.0125, 9.9891, 9.9643, 9.9381, 9.9105, 9.8815, 9.8511, 9.8192, 9.7859, 9.7512, 9.7151, 9.6776, 9.6387, 9.5983, 9.5566, 9.5134, 9.4688, 9.4228, 9.3754, 9.3265, 9.2762, 9.2246, 9.1715, 9.117, 9.061, 9.0037, 8.945, 8.8848, 8.8232, 8.7602, 8.6958, 8.6299, 8.5627, 8.494, 8.4239, 8.3524, 8.2795, 8.2052, 8.1295, 8.0523, 7.9737, 7.8937, 7.8123, 7.7295, 7.6453, 7.5596, 7.4725, 7.384, 7.2941, 7.2028, 7.1101, 7.0159, 6.9204, 6.8234, 6.725, 6.6252, 6.524, 6.4213, 6.3172, 6.2118, 6.1049, 5.9966, 5.8869, 5.7757, 5.6632, 5.5492, 5.4338, 5.317, 5.1988, 5.0791, 4.9581, 4.8356, 4.7117, 4.5864, 4.4597, 4.3316, 4.2021, 4.0711, 3.9387, 3.8049, 3.6697, 3.5331, 3.3951, 3.2556, 3.1147, 2.9724, 2.8287, 2.6836, 2.5371, 2.3891, 2.2398, 2.089, 1.9368, 1.7832, 1.6282, 1.4717, 1.3139, 1.1546, 0.9939, 0.8318, 0.6683, 0.5033, 0.337, 0.1692, -0.0]
        s = 0.25417
        speed, angle, g = 20.0, 45.0, 9.81
        t_flight, rng = 2.8832, 40.7747
        th = math.radians(angle)
        ground_y, x0, wall_x = -2.55, -5.5, -6.35
        origin = np.array([x0, ground_y, 0.0])

        def world(x, y):
            return np.array([x0 + s * x, ground_y + s * y, 0.0])

        def chip(text):
            return Text(text, font_size=24, color=YELLOW_A).to_corner(UL, buff=0.3)

        def fit(m, width=13.0):
            if m.width > width:
                m.scale_to_fit_width(width)
            return m

        # ============================================================
        # 1 · Title card that is also a physics picture.
        # Instead of an empty title, show the ground, axes with ticks,
        # the kick arrow, the angle, and the trajectory preview up front.
        # ============================================================
        title = Text("Where does the ball land?", font_size=40, color=YELLOW).to_edge(UP, buff=0.35)
        problem = fit(Text('A ball is kicked at 20 m/s, 45° above level ground.', font_size=26)).next_to(title, DOWN, buff=0.25)
        question = fit(Text('How far away does it land, and how long is it in the air?', font_size=26, color=TEAL_A)).next_to(problem, DOWN, buff=0.12)

        # Axes with numeric ticks on both directions (critique: legibility).
        x_min, x_max = -7.0, 7.0
        x_axis = NumberLine(x_range=[-7, 7, 1], length=10.6, include_numbers=True,
                            label_direction=DOWN, font_size=16, color=BLUE_B)
        x_axis.move_to([0, ground_y - 0.05, 0])
        y_axis = NumberLine(x_range=[0, 15, 3], length=4.6, include_numbers=True,
                            label_direction=LEFT, font_size=16, color=BLUE_B, rotation=90 * DEGREES)
        y_axis.move_to([x0 - 0.6, ground_y + 2.2, 0])
        x_label = Text("x (m)", font_size=20, color=BLUE_B).next_to(x_axis, DOWN, buff=0.18)
        y_label = Text("y (m)", font_size=20, color=BLUE_B).next_to(y_axis, UP, buff=0.15)

        ground = Line([x_min, ground_y, 0], [x_max, ground_y, 0], color=GREY_B, stroke_width=3)
        ball = Dot(origin, color=WHITE, radius=0.12).set_z_index(5)
        v_len = 2.2
        v_tip = origin + v_len * np.array([math.cos(th), math.sin(th), 0.0])
        v_arrow = Arrow(origin, v_tip, buff=0, color=YELLOW, stroke_width=6,
                        max_tip_length_to_length_ratio=0.15)
        v_text = Text(f"{speed:g} m/s", font_size=24, color=YELLOW).next_to(v_tip, UP, buff=0.08)
        arc = Arc(radius=0.75, start_angle=0, angle=th, arc_center=origin, color=GREY_A)
        a_text = Text(f"{angle:g}°", font_size=22, color=GREY_A).move_to(
            origin + 1.1 * np.array([math.cos(th / 2), math.sin(th / 2), 0.0]))

        # Living preview arc — gives motion in frame 1, fixes "empty title".
        preview = ParametricFunction(
            lambda u: world(speed * math.cos(th) * u, speed * math.sin(th) * u - 0.5 * g * u * u),
            t_range=[0, t_flight], color=YELLOW_E, stroke_width=2.5, stroke_opacity=0.55)

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(problem), FadeIn(question), Create(ground), Create(x_axis),
                  FadeIn(x_label), Create(y_axis), FadeIn(y_label), FadeIn(ball), run_time=1.4)
        self.play(GrowArrow(v_arrow), FadeIn(v_text), Create(arc), FadeIn(a_text),
                  Create(preview), run_time=1.5)
        guess = Text("?", font_size=44, color=TEAL).move_to(world(rng, 0) + UP * 0.6)
        self.play(FadeIn(guess), run_time=0.6)
        self.wait(2.6)

        # ============================================================
        # 2 · Split the motion into two simple ones.
        # ============================================================
        brief = fit(Text('v = 20 m/s at 45°:  split it sideways + up.', font_size=24, color=GREY_A), 7.4).to_corner(UR, buff=0.3)
        step = chip("1 · split the motion")
        # Fade out the narrative scene but keep axes + ground + preview for context.
        self.play(FadeOut(VGroup(title, problem, question, v_text, arc, a_text, guess)),
                  FadeIn(brief), FadeIn(step), run_time=0.7)
        vx_tip = origin + v_len * math.cos(th) * RIGHT
        vy_tip = origin + v_len * math.sin(th) * UP
        vx_arrow = Arrow(origin, vx_tip, buff=0, color=BLUE, stroke_width=6, max_tip_length_to_length_ratio=0.18)
        vy_arrow = Arrow(origin, vy_tip, buff=0, color=RED, stroke_width=6, max_tip_length_to_length_ratio=0.18)
        dash_x = DashedLine(v_tip, vx_tip, color=GREY_B, stroke_width=1.5)
        dash_y = DashedLine(v_tip, vy_tip, color=GREY_B, stroke_width=1.5)
        vx_text = Text('sideways: 20·cos 45° ≈ 14.1 m/s', font_size=22, color=BLUE).move_to([2.6, 1.7, 0])
        vy_text = Text('upward:  20·sin 45° ≈ 14.1 m/s', font_size=22, color=RED).move_to([2.6, 1.2, 0])
        self.play(Create(dash_x), Create(dash_y), GrowArrow(vx_arrow), GrowArrow(vy_arrow), run_time=1.2)
        self.play(FadeIn(vx_text, shift=0.2 * LEFT), FadeIn(vy_text, shift=0.2 * LEFT), run_time=0.9)
        rule_x = Text("sideways: no push, so speed is steady", font_size=22,
                      color=BLUE_B).move_to([2.6, 0.6, 0])
        rule_y = Text("up/down: gravity slows, stops, returns", font_size=22,
                      color=RED_B).move_to([2.6, 0.15, 0])
        self.play(FadeIn(rule_x), run_time=0.7)
        self.play(FadeIn(rule_y), run_time=0.7)
        self.wait(2.6)

        # ============================================================
        # 3 · Watch the two shadows in slow motion.
        # ============================================================
        step2 = chip("2 · watch the two shadows")
        wall = Line([wall_x, ground_y, 0], [wall_x, 1.7, 0], color=GREY_B, stroke_width=3)
        self.play(FadeOut(VGroup(v_arrow, vx_arrow, vy_arrow, dash_x, dash_y,
                                 rule_x, rule_y, vx_text, vy_text, brief)),
                  FadeOut(step), FadeIn(step2), Create(wall), run_time=0.8)
        t = ValueTracker(0.0)

        def pos():
            return world(float(np.interp(t.get_value(), ts, xs)),
                         float(np.interp(t.get_value(), ts, ys)))

        ball.add_updater(lambda m: m.move_to(pos()))
        ground_shadow = always_redraw(lambda: Dot([pos()[0], ground_y, 0], color=BLUE, radius=0.1))
        wall_shadow = always_redraw(lambda: Dot([wall_x, pos()[1], 0], color=RED, radius=0.1))
        link_g = always_redraw(lambda: DashedLine(pos(), [pos()[0], ground_y, 0],
                                                  color=BLUE_E, stroke_width=1.5))
        link_w = always_redraw(lambda: DashedLine(pos(), [wall_x, pos()[1], 0],
                                                  color=RED_E, stroke_width=1.5))
        ticks = VGroup()

        def drop_ticks(group):
            # Drop a pair of marks for every 0.25 s of slow-motion flight.
            n = int(t.get_value() / 0.25 + 1e-9)
            while len(group) // 2 < n:
                k = len(group) // 2 + 1
                p = world(float(np.interp(0.25 * k, ts, xs)),
                          float(np.interp(0.25 * k, ts, ys)))
                group.add(Dot([p[0], ground_y, 0], color=BLUE_B, radius=0.05))
                group.add(Dot([wall_x, p[1], 0], color=RED_B, radius=0.05))

        ticks.add_updater(drop_ticks)
        # Fade the static preview arc — the trail will replace it with real motion.
        self.play(FadeOut(preview), run_time=0.5)
        trail = TracedPath(pos, stroke_color=WHITE, stroke_width=2, stroke_opacity=0.6)
        slow = Text("slow motion, a mark every 0.25 s", font_size=20, color=GREY_B).to_corner(DR, buff=0.2)
        self.add(trail, link_g, link_w, ground_shadow, wall_shadow, ticks)
        self.play(FadeIn(slow), run_time=0.4)
        self.play(t.animate.set_value(t_flight), run_time=8.5, rate_func=linear)
        ticks.clear_updaters()
        note_g = Text("ground shadow: evenly spaced → steady speed", font_size=22,
                      color=BLUE_B).move_to([2.4, 1.5, 0])
        note_w = Text("wall shadow: bunched at top → up-then-down", font_size=22,
                      color=RED_B).move_to([2.4, 1.0, 0])
        self.play(FadeIn(note_g), run_time=0.6)
        self.play(FadeIn(note_w), run_time=0.6)
        self.wait(2.6)

        # ============================================================
        # 4 · Solve: read time & distance from the shadows.
        # ============================================================
        step3 = chip("3 · solve")
        eq_t = Text('time up & down:  t = 2·vy / g = 2 × 14.1 / 9.81 ≈ 2.88 s',
                    font_size=24, color=RED_A).move_to([1.5, 2.2, 0])
        eq_x = Text('sideways 2.88 s:  x = vx·t = 14.1 × 2.88 ≈ 40.8 m',
                    font_size=24, color=BLUE_A).move_to([1.5, 1.65, 0])
        self.play(FadeOut(VGroup(note_g, note_w, slow, step2)),
                  FadeIn(step3), run_time=0.6)
        self.play(Indicate(wall_shadow, color=RED), FadeIn(eq_t, shift=0.2 * DOWN), run_time=1.2)
        self.wait(1.6)
        self.play(Indicate(ground_shadow, color=BLUE), FadeIn(eq_x, shift=0.2 * DOWN), run_time=1.2)
        flag_base = world(rng, 0)
        pole = Line(flag_base, flag_base + UP * 1.0, color=GREY_A, stroke_width=3)
        cloth = Polygon(flag_base + UP * 1.0, flag_base + UP * 0.72 + RIGHT * 0.45,
                        flag_base + UP * 0.44, color=TEAL, fill_color=TEAL, fill_opacity=0.9)
        flag_text = Text('40.8 m', font_size=22, color=TEAL).next_to(pole, DOWN, buff=0.12)
        self.play(Create(pole), FadeIn(cloth), FadeIn(flag_text), run_time=0.9)
        self.wait(2.4)

        # ============================================================
        # 5 · Check: fly the real (simulated) ball at real speed onto the flag.
        # ============================================================
        step4 = chip("4 · check it with real speed")
        for mob in (link_g, link_w, ground_shadow, wall_shadow):
            mob.clear_updaters()
        self.play(FadeOut(VGroup(link_g, link_w, ground_shadow, wall_shadow, ticks,
                                 trail, eq_t, eq_x, step3)),
                  FadeIn(step4), run_time=0.6)
        t.set_value(0.0)
        trail2 = TracedPath(pos, stroke_color=YELLOW, stroke_width=3)
        clock = always_redraw(lambda: Text(f"t = {t.get_value():.2f} s", font_size=24)
                              .move_to([5.2, 3.05, 0]))
        # Keep the slow-motion trail visible (faded) so the eye can compare.
        self.add(trail2, clock)
        self.play(t.animate.set_value(t_flight), run_time=t_flight, rate_func=linear)
        hit = Text('simulated flight lands at 40.8 m after 2.88 s', font_size=24,
                   color=GREEN_B).move_to([1.0, 1.6, 0])
        self.play(Flash(ball, color=GREEN, flash_radius=0.6), Indicate(cloth, color=GREEN),
                  FadeIn(hit), run_time=1.0)
        self.wait(2.4)

        # ============================================================
        # 6 · What if: which angle goes farthest?
        # Build ON the 45° trajectory rather than abandoning it.
        # Animate the live ball from 45° toward 30°/60° to explain overshoot
        # of the 40.8 m mark (handles the "amplitude grew 8.39 → 27.1" warning).
        # ============================================================
        step5 = chip("5 · what if the angle changes?")
        ball.clear_updaters()
        clock.clear_updaters()

        # Briefly mute hit before swapping step label so they don't pile up.
        self.play(FadeOut(VGroup(hit, clock, trail2)), FadeOut(step4), FadeIn(step5), run_time=0.5)

        def arc_for(deg, color):
            a = math.radians(deg)
            tf = 2 * speed * math.sin(a) / g
            pts = [world(speed * math.cos(a) * u, speed * math.sin(a) * u - 0.5 * g * u * u)
                   for u in np.linspace(0, tf, 90)]
            path = VMobject(color=color, stroke_width=3.5)
            path.set_points_as_corners(pts)
            return path

        # 45° stays as the green reference; 30° (blue) and 60° (orange) join it.
        a45 = arc_for(45, GREEN)
        a30 = arc_for(30, BLUE)
        a60 = arc_for(60, ORANGE)
        self.play(Create(a45), run_time=1.4)
        self.play(Create(a30), run_time=1.4)
        same = Text('30° lands at 35.3 m  →  shorter than 45°', font_size=22,
                    color=BLUE).move_to([1.2, 2.25, 0])
        self.play(FadeIn(same), run_time=0.7)
        self.play(Create(a60), run_time=1.4)
        mirror = Text('60° also lands at 35.3 m  →  mirror of 30°', font_size=22,
                      color=ORANGE).next_to(same, DOWN, buff=0.18).align_to(same, LEFT)
        self.play(FadeIn(mirror), run_time=0.7)
        self.wait(1.6)

        # Live demo: rotate the live ball from 45° to 30° to 60° to show overshoot.
        live = Dot(origin, color=WHITE, radius=0.12).set_z_index(6)
        live_arrow = always_redraw(lambda: Arrow(
            origin,
            origin + v_len * np.array([math.cos(live_t.get_value()),
                                       math.sin(live_t.get_value()), 0.0]),
            buff=0, color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.15))
        live_t = ValueTracker(th)
        self.add(live, live_arrow)
        self.play(live_t.animate.set_value(math.radians(30)), run_time=1.6, rate_func=smooth)
        self.wait(0.3)
        self.play(live_t.animate.set_value(math.radians(60)), run_time=1.6, rate_func=smooth)
        # Sweep through, briefly tagging the live apogee (>9.81 m) as overshoot.
        self.play(live_t.animate.set_value(th), run_time=1.2, rate_func=smooth)
        over = Text('higher angle → higher peak, but lands sooner',
                    font_size=22, color=YELLOW_A).move_to([1.0, 3.05, 0])
        self.play(FadeIn(over), run_time=0.6)
        self.wait(1.4)

        # ============================================================
        # 7 · Final answer card with the 45° trajectory still on screen.
        # ============================================================
        answer = Text('Answer: lands 40.8 m away after 2.88 s in the air',
                      font_size=28, color=YELLOW)
        box = SurroundingRectangle(answer, color=YELLOW, buff=0.2, corner_radius=0.12)
        card = VGroup(answer, box).move_to([1.4, 3.05, 0])
        self.play(FadeOut(VGroup(same, mirror, over, live, live_arrow)),
                  FadeIn(card, scale=0.9), run_time=0.9)
        # Final living beat: pulse the flag and let the ball finish a quiet half-arc.
        self.play(Indicate(cloth, color=GREEN, scale_factor=1.1), run_time=0.6)
        self.wait(3.6)