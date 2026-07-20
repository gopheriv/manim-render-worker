from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Pendulum swings freely with perfect mathematical rhythm
        title = Text("Assume e = p/q for integers p, q", color=BLUE_E).scale(0.5).to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # Create pendulum
        pivot = Dot(ORIGIN, color=WHITE)
        string_length = 2.5
        bob = Circle(radius=0.2, color=GOLD_E, fill_opacity=1).shift(DOWN * string_length)
        string = Line(pivot.get_center(), bob.get_center(), color=WHITE, stroke_width=2)
        
        # Create digital displays
        damping_panel = Rectangle(height=0.8, width=2.5, color=BLUE_E, fill_opacity=0.2).to_corner(UL).shift(RIGHT*0.5+DOWN*0.5)
        damping_text = Text("damping = ", color=BLUE_E).scale(0.3)
        damping_val = DecimalNumber(0.15, num_decimal_places=2, color=BLUE_E).scale(0.3)
        damping_val.next_to(damping_text, RIGHT)
        damping_group = VGroup(damping_text, damping_val).move_to(damping_panel.get_center())
        
        mass_panel = Rectangle(height=0.8, width=2.5, color=BLUE_E, fill_opacity=0.2).next_to(damping_panel, DOWN, buff=0.2)
        mass_text = Text("mass = ", color=BLUE_E).scale(0.3)
        mass_val = DecimalNumber(1.0, num_decimal_places=1, color=BLUE_E).scale(0.3)
        mass_val.next_to(mass_text, RIGHT)
        mass_group = VGroup(mass_text, mass_val).move_to(mass_panel.get_center())
        
        stiffness_panel = Rectangle(height=0.8, width=2.5, color=BLUE_E, fill_opacity=0.2).next_to(mass_panel, DOWN, buff=0.2)
        stiffness_text = Text("stiffness = ", color=BLUE_E).scale(0.3)
        stiffness_val = DecimalNumber(1.0, num_decimal_places=1, color=BLUE_E).scale(0.3)
        stiffness_val.next_to(stiffness_text, RIGHT)
        stiffness_group = VGroup(stiffness_text, stiffness_val).move_to(stiffness_panel.get_center())

        # Show digital displays
        self.play(Create(damping_panel), Write(damping_group), run_time=0.8)
        self.play(Create(mass_panel), Write(mass_group), run_time=0.8)
        self.play(Create(stiffness_panel), Write(stiffness_group), run_time=0.8)

        # Create pendulum components
        self.play(Create(string), Create(bob), run_time=1.0)

        # Animate pendulum swing
        angle_tracker = ValueTracker(0)
        def update_pendulum(mob):
            angle = 0.3 * math.sin(angle_tracker.get_value())
            new_end = np.array([string_length * math.sin(angle), -string_length * math.cos(angle), 0])
            string.put_start_and_end_on(pivot.get_center(), new_end)
            bob.move_to(new_end)
        
        string.add_updater(update_pendulum)
        self.play(angle_tracker.animate.set_value(4 * PI), run_time=3.0, rate_func=linear)
        string.clear_updaters()

        # Materialize integer counters p and q
        p_counter = Integer(1, color=GOLD_E).scale(1.2).to_edge(LEFT).shift(UP)
        q_counter = Integer(1, color=GOLD_E).scale(1.2).to_edge(LEFT).shift(DOWN)
        p_label = Text("p =", color=GOLD_E).scale(0.6).next_to(p_counter, LEFT)
        q_label = Text("q =", color=GOLD_E).scale(0.6).next_to(q_counter, LEFT)
        
        self.play(Write(p_label), Create(p_counter), run_time=1.0)
        self.play(Write(q_label), Create(q_counter), run_time=1.0)
        self.wait(0.5)

        # EVOLVE — Pendulum motion becomes constrained
        title2 = Text("But the mathematics begins to resist this assumption...", color=BLUE_E).scale(0.4).to_edge(UP)
        self.play(Transform(title, title2), run_time=1.0)

        # Increase damping visually by changing the value
        new_damping_val = DecimalNumber(0.3, num_decimal_places=2, color=RED_C).scale(0.3)
        new_damping_val.move_to(damping_val.get_center())
        self.play(Transform(damping_val, new_damping_val), run_time=1.0)

        # Animate p and q cycling
        p_tracker = ValueTracker(1)
        q_tracker = ValueTracker(1)
        
        def update_p(mob):
            mob.set_value(int(p_tracker.get_value()))
        
        def update_q(mob):
            mob.set_value(int(q_tracker.get_value()))
            
        p_counter.add_updater(update_p)
        q_counter.add_updater(update_q)
        
        self.play(
            p_tracker.animate.set_value(10),
            q_tracker.animate.set_value(15),
            run_time=4.0,
            rate_func=there_and_back
        )
        
        # More dramatic pendulum motion with increased damping effect
        string.add_updater(update_pendulum)
        self.play(
            angle_tracker.animate.set_value(8 * PI),
            run_time=3.0,
            rate_func=linear
        )
        string.clear_updaters()
        
        p_counter.remove_updater(update_p)
        q_counter.remove_updater(update_q)

        # REVEAL — Pendulum violently rejects rational period
        title3 = Text("The contradiction destroys our rational framework completely.", color=RED_C).scale(0.4).to_edge(UP)
        self.play(Transform(title, title3), run_time=1.0)

        # Shatter integers p and q
        p_fragments = VGroup(*[
            Integer(1, color=RED_C).scale(0.3).shift(
                np.array([0.3*np.random.uniform(-1, 1), 0.3*np.random.uniform(-1, 1), 0])
            ) for _ in range(15)
        ]).move_to(p_counter.get_center())
        
        q_fragments = VGroup(*[
            Integer(1, color=RED_C).scale(0.3).shift(
                np.array([0.3*np.random.uniform(-1, 1), 0.3*np.random.uniform(-1, 1), 0])
            ) for _ in range(15)
        ]).move_to(q_counter.get_center())

        # Animate shattering
        self.play(
            FadeOut(p_counter), 
            FadeOut(q_counter),
            FadeIn(p_fragments),
            FadeIn(q_fragments),
            run_time=1.0
        )
        
        # Move fragments away
        self.play(
            LaggedStart(
                *[ApplyMethod(frag.shift, frag.get_center()*np.random.uniform(0.5, 2)) for frag in p_fragments],
                lag_ratio=0.05
            ),
            LaggedStart(
                *[ApplyMethod(frag.shift, frag.get_center()*np.random.uniform(0.5, 2)) for frag in q_fragments],
                lag_ratio=0.05
            ),
            run_time=1.5
        )

        # Show Euler's number e
        e_number = Text("e = 2.718281828459045...", color=GOLD_E).scale(0.8).move_to(ORIGIN)
        self.play(Write(e_number), run_time=2.0)

        # Cross out the original assumption
        cross_line = Line(title.get_left(), title.get_right(), color=RED_C, stroke_width=6)
        self.play(Create(cross_line), run_time=1.0)

        # IDLE LOOP — Subtle harmonic tremor with flickering numbers
        # Make p and q flicker faintly among debris
        p_flicker = Integer(1, color=GOLD).scale(0.2).move_to(p_fragments[0].get_center())
        q_flicker = Integer(1, color=GOLD).scale(0.2).move_to(q_fragments[0].get_center())
        
        def flicker_update(mob, dt):
            if np.random.random() < 0.05:  # 5% chance per frame to appear
                mob.set_opacity(0.7)
            else:
                mob.set_opacity(0.1)
        
        p_flicker.add_updater(lambda m, dt: flicker_update(m, dt))
        q_flicker.add_updater(lambda m, dt: flicker_update(m, dt))
        
        self.add(p_flicker, q_flicker)

        # Add subtle tremor to pendulum string
        tremor_tracker = ValueTracker(0)
        def update_tremor(mob):
            current_pos = mob.get_end()
            tremor_offset = 0.05 * math.sin(tremor_tracker.get_value()) * RIGHT
            new_end = current_pos + tremor_offset
            mob.put_start_and_end_on(mob.get_start(), new_end)
        
        string.add_updater(update_tremor)
        self.play(
            tremor_tracker.animate.set_value(20 * PI),
            run_time=5.0,
            rate_func=linear
        )
        string.clear_updaters()
        
        self.wait(2.0)