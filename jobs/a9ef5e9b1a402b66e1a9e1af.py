from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
            # Background
            bg = Rectangle(width=config.frame_width, height=config.frame_height)
            bg.set_fill("#E5E7EB", opacity=1).set_stroke(opacity=0)
            self.add(bg)

            # Horizontal ground line
            ground = Line(LEFT * 6.5, RIGHT * 6.5, color=GRAY_D)
            ground.shift(DOWN * 2.4)
            self.add(ground)

            # BEAT A1.B1 | 0.00-4.00 s
            # Truck enters from left with v0 label
            truck_body = RoundedRectangle(width=2.0, height=0.9, corner_radius=0.15,
                                          color=BLUE, fill_opacity=1, stroke_width=2)
            truck_cab = RoundedRectangle(width=0.7, height=0.7, corner_radius=0.1,
                                         color=BLUE_E, fill_opacity=1, stroke_width=2)
            truck_cab.move_to(truck_body.get_right() + LEFT * 0.35 + UP * 0.35)
            wheel1 = Circle(radius=0.18, color=BLACK, fill_opacity=1, stroke_width=2)
            wheel2 = Circle(radius=0.18, color=BLACK, fill_opacity=1, stroke_width=2)
            wheel1.move_to(truck_body.get_left() + DOWN * 0.45 + RIGHT * 0.2)
            wheel2.move_to(truck_body.get_right() + DOWN * 0.45 + LEFT * 0.4)
            hub1 = Dot(wheel1.get_center(), color=WHITE, radius=0.05)
            hub2 = Dot(wheel2.get_center(), color=WHITE, radius=0.05)
            truck = VGroup(truck_body, truck_cab, wheel1, wheel2, hub1, hub2)
            truck.move_to(LEFT * 5.5 + UP * 1.0)

            v0_label = MathTex("v_0", color=RED).scale(0.7)
            v0_label.next_to(truck, UP, buff=0.15)
            v0_value = Text("5 м/с", color=RED).scale(0.32)
            v0_value.next_to(v0_label, RIGHT, buff=0.15)

            self.play(FadeIn(truck, shift=RIGHT * 0.3), run_time=0.8)
            self.play(Write(v0_label), FadeIn(v0_value, shift=UP * 0.2), run_time=0.8)
            self.wait(2.1)

            # BEAT A2.B1 | 4.00-9.00 s
            # Acceleration label appears, speedometer scale fades in
            a_label = MathTex("a = 2\\,\\text{м/с}^{2}", color=YELLOW).scale(0.55)
            a_label.next_to(truck, UP, buff=0.15)

            # Vertical speedometer scale on the right
            scale_base = RIGHT * 5.0 + DOWN * 0.3
            scale_axis = Line(scale_base + DOWN * 1.8, scale_base + UP * 2.0,
                              color=GRAY_B, stroke_width=3)
            ticks = VGroup()
            tick_labels = VGroup()
            speeds = [5, 7, 9, 11]
            for i, v in enumerate(speeds):
                y = scale_base[1] + DOWN * 1.5 + UP * 1.0 * i
                tick = Line(scale_base + RIGHT * 0.15 + np.array([0, y - scale_base[1], 0]),
                            scale_base + RIGHT * 0.35 + np.array([0, y - scale_base[1], 0]),
                            color=YELLOW, stroke_width=3)
                lbl = Text(f"{v}", color=YELLOW).scale(0.32)
                lbl.next_to(tick, RIGHT, buff=0.1)
                ticks.add(tick)
                tick_labels.add(lbl)
            scale_title = Text("v, м/с", color=YELLOW).scale(0.3)
            scale_title.next_to(scale_axis, UP, buff=0.1)

            self.play(FadeOut(v0_value), Transform(v0_label, a_label), run_time=0.8)
            self.play(Create(scale_axis), FadeIn(ticks), FadeIn(tick_labels),
                      FadeIn(scale_title), run_time=1.0)
            self.wait(3.0)

            # BEAT A3.B1 | 9.00-17.00 s
            # Stopwatch and truck jumps at each second
            stopwatch_group = VGroup()
            sw_center = Circle(radius=0.35, color=WHITE, fill_opacity=0.15, stroke_width=2)
            sw_hand = Line(ORIGIN, UP * 0.25, color=WHITE, stroke_width=2)
            sw = VGroup(sw_center, sw_hand).move_to(DOWN * 2.0 + LEFT * 4.5)
            sw_label = Text("t", color=WHITE).scale(0.32).next_to(sw, DOWN, buff=0.1)
            stopwatch_group.add(sw, sw_label)
            self.add(stopwatch_group)

            t_tracker = ValueTracker(0)
            t_readout = always_redraw(
                lambda: DecimalNumber(t_tracker.get_value(), num_decimal_places=0,
                                      color=WHITE).scale(0.5).next_to(sw, UP, buff=0.15)
            )
            self.play(FadeIn(t_readout), run_time=0.4)

            # Position the truck by t so it moves right with accelerating jumps
            truck.add_updater(lambda m: m.move_to(LEFT * 1.5 + RIGHT * 0.6 * t_tracker.get_value()
                                                  + UP * 1.0))
            self.add(truck)

            # Highlight ticks 5, 7, 9 in red as t advances
            highlight = VGroup()
            for i in range(3):
                dot = Dot(ticks[i].get_right(), color=RED, radius=0.06)
                highlight.add(dot)
            self.add(highlight)

            # Animate t from 0 to 3 in three jumps
            self.play(t_tracker.animate.set_value(1), run_time=1.2, rate_func=linear)
            self.play(t_tracker.animate.set_value(2), run_time=1.2, rate_func=linear)
            self.play(t_tracker.animate.set_value(3), run_time=1.2, rate_func=linear)
            self.wait(3.6)

            truck.clear_updaters()

            # BEAT A4.B1 | 17.00-25.00 s
            # Equation reveals with live values
            formula = MathTex("v", "=", "v_0", "+", "a t", color=WHITE).scale(0.9)
            formula.set_color_by_tex("v", RED)
            formula.set_color_by_tex("v_0", RED)
            formula.set_color_by_tex("a t", YELLOW)
            formula.move_to(UP * 0.8)

            # Live values
            v0_num = DecimalNumber(5, num_decimal_places=0, color=RED).scale(0.45)
            a_num = DecimalNumber(2, num_decimal_places=0, color=YELLOW).scale(0.45)
            t_num = DecimalNumber(3, num_decimal_places=0, color=WHITE).scale(0.45)
            v_num = DecimalNumber(11, num_decimal_places=0, color=RED).scale(0.55)

            values = VGroup(v0_num, a_num, t_num, v_num).arrange(RIGHT, buff=0.3)
            values.next_to(formula, DOWN, buff=0.4)

            # Clear previous beat content
            self.play(FadeOut(VGroup(t_readout, stopwatch_group, highlight, scale_title,
                                      scale_axis, ticks[3], tick_labels[3])),
                      run_time=0.5)

            self.play(Write(formula), run_time=1.2)
            self.play(FadeIn(values, shift=UP * 0.2), run_time=0.8)

            # Position truck under the formula
            self.play(truck.animate.move_to(LEFT * 2.0 + DOWN * 1.3), run_time=1.0)

            # Highlight the 11 m/s tick
            dot11 = Dot(ticks[3].get_right(), color=RED, radius=0.08)
            self.play(FadeIn(dot11), run_time=0.5)
            self.wait(3.8)

            # BEAT A5.B1 | 25.00-30.00 s
            # Recap: clean frame, only formula + truck + summary
            summary = Text("v₀=5, a=2, t=3 ⇒ v=11 м/с", color=WHITE).scale(0.38)
            summary.next_to(truck, DOWN, buff=0.3)

            self.play(FadeOut(VGroup(values, ticks[0], ticks[1], ticks[2],
                                      tick_labels[0], tick_labels[1], tick_labels[2],
                                      dot11, a_label, v0_label)),
                      run_time=0.6)

            # Idle loop: wheel wobble + summary blink
            wheel1.add_updater(lambda m: m.rotate(0.02))
            wheel2.add_updater(lambda m: m.rotate(0.02))

            blink_tracker = ValueTracker(0)
            summary.add_updater(
                lambda m: m.set_fill(opacity=0.6 + 0.4 * abs(np.sin(2 * PI * blink_tracker.get_value())))
            )

            self.play(FadeIn(summary, shift=UP * 0.2), run_time=0.6)
            self.play(blink_tracker.animate.set_value(2.5), run_time=3.4, rate_func=linear)
            self.wait(0.6)