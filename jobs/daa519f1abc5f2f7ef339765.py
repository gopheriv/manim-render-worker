from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Large central gear 'q!' with arms labeled 'p' and 'q'
        title = Text("Proof: e is Irrational", color=BLUE_E).scale(0.6).to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # Central gear representing q!
        q_factorial_gear = Circle(radius=1.2, color=GOLD_E, fill_opacity=0.3).set_stroke(width=5)
        q_label = Text("q!", color=GOLD_E).scale(1.2)
        q_factorial_gear_group = VGroup(q_factorial_gear, q_label).move_to(ORIGIN)

        # Arms extending from the gear
        p_arm = Line(LEFT * 4, LEFT * 1.2, color=BLUE_E, stroke_width=8)
        q_arm = Line(RIGHT * 1.2, RIGHT * 4, color=BLUE_E, stroke_width=8)
        
        # Labels for arms
        p_label = Text("p", color=BLUE_E).scale(0.8).next_to(p_arm.get_end(), LEFT, buff=0.3)
        q_label_arm = Text("q", color=BLUE_E).scale(0.8).next_to(q_arm.get_end(), RIGHT, buff=0.3)

        # Floating numbers above arms
        mass_tracker = ValueTracker(1.0)
        p_value = always_redraw(lambda: DecimalNumber(mass_tracker.get_value() * 100, num_decimal_places=0, color=BLUE_E)
                                .scale(0.5).next_to(p_arm.get_start(), UP, buff=0.3))
        
        stiffness_tracker = ValueTracker(1.0)
        q_value = always_redraw(lambda: DecimalNumber(stiffness_tracker.get_value() * 10, num_decimal_places=0, color=BLUE_E)
                                .scale(0.5).next_to(q_arm.get_start(), UP, buff=0.3))

        # Equation plaque
        eq_plaque = Rectangle(height=0.8, width=2.5, color=GREY_A, fill_opacity=0.7).to_edge(UP, buff=1.2)
        eq_text = Text("e = p/q", color=WHITE).scale(0.5).move_to(eq_plaque.get_center())

        self.play(
            Create(q_factorial_gear),
            Write(q_label),
            Create(p_arm),
            Create(q_arm),
            Write(p_label),
            Write(q_label_arm),
            run_time=2.0
        )
        
        self.play(
            FadeIn(p_value),
            FadeIn(q_value),
            Create(eq_plaque),
            Write(eq_text),
            run_time=2.0
        )

        # Rotate the central gear slowly
        self.play(
            Rotate(q_factorial_gear_group, angle=PI/2, run_time=3.0),
            rate_func=linear
        )

        # EVOLVE — Accelerate mechanism and separate series
        self.play(
            Rotate(q_factorial_gear_group, angle=PI, run_time=2.0),
            rate_func=linear
        )

        # Show multiplication by q!
        mult_text = Text("× q!", color=GOLD_E).scale(0.7).next_to(eq_plaque, DOWN, buff=0.2)
        self.play(Write(mult_text), run_time=1.5)

        # Separate into finite and infinite parts
        finite_box = Rectangle(height=1.5, width=3, color=GOLD_E, fill_opacity=0.2).shift(LEFT * 3)
        infinite_box = Rectangle(height=1.5, width=3, color=RED_E, fill_opacity=0.2).shift(RIGHT * 3)
        
        finite_label = Text("Finite Sum", color=GOLD_E).scale(0.4).move_to(finite_box.get_top()).shift(DOWN*0.3)
        infinite_label = Text("Infinite Tail", color=RED_E).scale(0.4).move_to(infinite_box.get_top()).shift(DOWN*0.3)

        self.play(
            Create(finite_box),
            Create(infinite_box),
            Write(finite_label),
            Write(infinite_label),
            run_time=2.0
        )

        # Show gears meshing with increasing complexity
        small_gears = VGroup()
        for i in range(5):
            angle = i * PI / 2.5
            x_pos = 2 * np.cos(angle)
            y_pos = 2 * np.sin(angle)
            small_gear = Circle(radius=0.3, color=GOLD_E, fill_opacity=0.5).move_to([x_pos, y_pos, 0])
            small_gears.add(small_gear)
        
        self.play(
            LaggedStart(*[Create(gear) for gear in small_gears]),
            Rotate(q_factorial_gear_group, angle=PI, run_time=3.0),
            rate_func=linear
        )

        # REVEAL — Finite resolves to integer, infinite shows remainder
        # Integer result in gold
        integer_result = Text("Integer", color=GOLD_E).scale(0.8).move_to(finite_box.get_center())
        integer_highlight = SurroundingRectangle(integer_result, color=GOLD_E, buff=0.2)
        
        self.play(
            Write(integer_result),
            Create(integer_highlight),
            run_time=1.5
        )

        # Remainder in red
        remainder_result = Text("Non-Integer\nRemainder", color=RED_E).scale(0.6).move_to(infinite_box.get_center())
        remainder_highlight = SurroundingRectangle(remainder_result, color=RED_E, buff=0.2)
        
        self.play(
            Write(remainder_result),
            Create(remainder_highlight),
            run_time=1.5
        )

        # Jam the mechanism and destroy plaque
        self.play(
            Rotate(q_factorial_gear_group, angle=PI/4, run_time=1.0),
            ApplyMethod(q_factorial_gear_group.shift, UP * 0.2),
            run_time=0.5
        )
        
        # Break the equation plaque
        broken_pieces = VGroup(*[eq_plaque.copy().shift(np.random.uniform(-0.2, 0.2)*RIGHT + 
                                                       np.random.uniform(-0.2, 0.2)*UP).rotate(np.random.uniform(-0.2, 0.2))
                                for _ in range(4)])
        
        self.play(
            FadeOut(eq_text),
            LaggedStart(*[Transform(eq_plaque, piece) for piece in broken_pieces]),
            run_time=1.0
        )

        # IDLE LOOP — Sparks and pulsing
        spark_tracker = ValueTracker(0)
        def create_spark():
            angle = spark_tracker.get_value()
            pos = np.array([1.2*np.cos(angle), 1.2*np.sin(angle), 0])
            return Dot(pos, color=YELLOW, radius=0.05).add_updater(
                lambda d: d.shift((np.random.random()-0.5)*0.02*RIGHT + (np.random.random()-0.5)*0.02*UP)
            )
        
        spark = always_redraw(create_spark)
        
        # Pulsing effects
        integer_pulse = ValueTracker(0)
        remainder_pulse = ValueTracker(PI)
        
        integer_result.add_updater(lambda m: m.set_opacity(0.7 + 0.3*np.sin(integer_pulse.get_value())))
        remainder_result.add_updater(lambda m: m.set_opacity(0.7 + 0.3*np.sin(remainder_pulse.get_value())))
        
        self.add(spark)
        
        # Continue the motion for the idle loop
        for _ in range(30):  # About 2 seconds at 15 fps
            self.play(
                spark_tracker.animate.increment_value(0.5),
                integer_pulse.animate.increment_value(0.3),
                remainder_pulse.animate.increment_value(0.3),
                run_time=0.1
            )