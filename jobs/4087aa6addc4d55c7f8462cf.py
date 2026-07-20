from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Camera starts close on a single pendulum oscillating in perfect regular rhythm
        title = Text("Double Pendulum Dynamics", color=BLUE_E).scale(0.5).to_edge(UP)
        self.play(Write(title), run_time=0.9)

        # Physics parameters
        g = 9.81
        l1, l2 = 1.0, 0.8
        m1, m2 = 1.0, 1.0
        
        # Pivot point
        pivot = np.array([0, 2, 0])
        
        # ValueTrackers for angles
        theta1_tracker = ValueTracker(PI/4)
        theta2_tracker = ValueTracker(PI/6)
        
        # Digital readout panel
        panel = Rectangle(height=2, width=4, color=BLUE_E, fill_opacity=0.2, stroke_width=2)
        panel.to_corner(UR).shift(IN)
        panel_title = Text("Physics Parameters", color=BLUE_E).scale(0.3).next_to(panel.get_top(), DOWN, buff=0.1)
        
        # Parameter displays
        g_label = VGroup(
            Text("g =", color=GOLD_E),
            DecimalNumber(g, num_decimal_places=2, color=GOLD_E)
        ).arrange(RIGHT, buff=0.2).scale(0.3)
        
        l1_label = VGroup(
            Text("l1 =", color=GOLD_E),
            DecimalNumber(l1, num_decimal_places=2, color=GOLD_E)
        ).arrange(RIGHT, buff=0.2).scale(0.3)
        
        l2_label = VGroup(
            Text("l2 =", color=GOLD_E),
            DecimalNumber(l2, num_decimal_places=2, color=GOLD_E)
        ).arrange(RIGHT, buff=0.2).scale(0.3)
        
        param_group = VGroup(g_label, l1_label, l2_label).arrange(DOWN, buff=0.2).move_to(panel.get_center())
        
        self.play(Create(panel), Write(panel_title), *[Write(param) for param in param_group], run_time=1.5)
        
        # Single pendulum initially
        def get_bob1_pos():
            theta = theta1_tracker.get_value()
            return pivot + l1 * np.array([np.sin(theta), -np.cos(theta), 0])
        
        anchor = Dot(pivot, color=BLUE_E, radius=0.08)
        rod1 = always_redraw(lambda: Line(pivot, get_bob1_pos(), color=BLUE_E, stroke_width=4))
        bob1 = always_redraw(lambda: Dot(get_bob1_pos(), color=GOLD_E, radius=0.15))
        
        self.play(Create(rod1), Create(bob1), Create(anchor), run_time=1)
        
        # Animate single pendulum motion briefly
        self.play(theta1_tracker.animate.set_value(PI/6), run_time=1.5, rate_func=there_and_back)
        self.play(theta1_tracker.animate.set_value(-PI/4), run_time=1.5, rate_func=there_and_back)
        
        # Pull back to reveal second pendulum
        self.play(theta2_tracker.animate.set_value(PI/3), run_time=1)
        
        def get_bob2_pos():
            theta1 = theta1_tracker.get_value()
            theta2 = theta2_tracker.get_value()
            pos1 = get_bob1_pos()
            return pos1 + l2 * np.array([np.sin(theta2), -np.cos(theta2), 0])
        
        rod2 = always_redraw(lambda: Line(get_bob1_pos(), get_bob2_pos(), color=BLUE_E, stroke_width=4))
        bob2 = always_redraw(lambda: Dot(get_bob2_pos(), color=GOLD_E, radius=0.15))
        
        self.play(Create(rod2), Create(bob2), run_time=1)
        
        # Both pendulums motionless initially
        self.wait(0.5)
        
        # EVOLVE — First pendulum begins swinging while second remains still
        t = ValueTracker(0)
        
        def double_pendulum_system(t_val):
            # Simplified double pendulum simulation using small angle approximations
            # More accurate simulation would require solving coupled differential equations
            theta1 = PI/4 * np.cos(2 * t_val) * np.exp(-0.01 * t_val)
            theta2 = PI/6 * np.cos(3 * t_val + PI/3) * np.exp(-0.01 * t_val)
            return theta1, theta2
        
        def update_pendulum(mob):
            theta1, theta2 = double_pendulum_system(t.get_value())
            theta1_tracker.set_value(theta1)
            theta2_tracker.set_value(theta2)
        
        self.add_updater(update_pendulum)
        
        # Animate evolution of chaotic motion
        self.play(t.animate.set_value(8), run_time=8, rate_func=linear)
        self.remove_updater(update_pendulum)
        
        # Trajectory traces
        trace1 = TracedPath(bob1.get_center, dissipate=True, stroke_color=GOLD_E, stroke_width=2)
        trace2 = TracedPath(bob2.get_center, dissipate=True, stroke_color=RED_D, stroke_width=2)
        self.add(trace1, trace2)
        
        # REVEAL — Mathematical notation appears above apparatus
        euler_lagrange_text = Text("Euler-Lagrange Equations", color=GOLD_E).scale(0.4).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(euler_lagrange_text), run_time=1)
        
        # Lagrangian equations
        eq1 = MathTex(
            "\\frac{d}{dt}\\left(\\frac{\\partial L}{\\partial \\dot{\\theta}_1}\\right) - \\frac{\\partial L}{\\partial \\theta_1} = 0",
            color=GOLD_E
        ).scale(0.5).next_to(euler_lagrange_text, DOWN, buff=0.3)
        
        eq2 = MathTex(
            "\\frac{d}{dt}\\left(\\frac{\\partial L}{\\partial \\dot{\\theta}_2}\\right) - \\frac{\\partial L}{\\partial \\theta_2} = 0",
            color=GOLD_E
        ).scale(0.5).next_to(eq1, DOWN, buff=0.3)
        
        self.play(Write(eq1), run_time=1.5)
        self.play(Write(eq2), run_time=1.5)
        
        # Continue motion during reveal
        def update_pendulum_reveal(mob):
            theta1, theta2 = double_pendulum_system(t.get_value())
            theta1_tracker.set_value(theta1)
            theta2_tracker.set_value(theta2)
        
        t.set_value(8)
        self.add_updater(update_pendulum_reveal)
        self.play(t.animate.set_value(15), run_time=7, rate_func=linear)
        self.remove_updater(update_pendulum_reveal)
        
        # IDLE LOOP setup - subtle pendulum sway with gently pulsing equation text
        # Keep the pendulum moving with a slow oscillation
        def idle_update(mob):
            current_t = t.get_value()
            theta1 = PI/6 * np.cos(0.5 * current_t)
            theta2 = PI/8 * np.cos(0.7 * current_t + PI/4)
            theta1_tracker.set_value(theta1)
            theta2_tracker.set_value(theta2)
        
        t.set_value(0)
        self.add_updater(idle_update)
        
        # Make equations pulse gently
        def pulse_equations():
            scale_factor = 0.5 + 0.05 * np.sin(t.get_value())
            eq1.scale_to_fit_width(scale_factor * 3)
            eq2.scale_to_fit_width(scale_factor * 3)
        
        pulse_updater = always_redraw(pulse_equations)
        self.add(pulse_updater)
        
        # Update parameters on digital panel
        def update_params():
            current_g = 9.81 + 0.1 * np.sin(0.3 * t.get_value())
            current_l1 = 1.0 + 0.05 * np.sin(0.4 * t.get_value())
            current_l2 = 0.8 + 0.05 * np.cos(0.3 * t.get_value())
            
            g_label[1].set_value(current_g)
            l1_label[1].set_value(current_l1)
            l2_label[1].set_value(current_l2)
        
        param_updater = always_redraw(update_params)
        self.add(param_updater)
        
        # Run idle loop
        self.play(t.animate.set_value(20), run_time=10, rate_func=linear)
        self.remove_updater(idle_update)