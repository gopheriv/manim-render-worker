from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH - Single pendulum swinging in perfect sine wave rhythm
        title = Text("Double Pendulum Chaos", color=BLUE_E).scale(0.5).to_edge(UP)
        self.play(Write(title), run_time=0.9)

        # Physics parameters
        gravity = 9.81
        length = 1.0
        g_tracker = ValueTracker(gravity)
        l_tracker = ValueTracker(length)

        g_label = always_redraw(lambda: Text(f"g={g_tracker.get_value():.2f}", color=GOLD_E).scale(0.3).to_corner(UL))
        l_label = always_redraw(lambda: Text(f"L={l_tracker.get_value():.2f}", color=GOLD_E).scale(0.3).next_to(g_label, DOWN))

        self.play(FadeIn(g_label), FadeIn(l_label), run_time=0.8)

        # Single pendulum setup
        pivot = np.array([-2.0, 1.0, 0.0])
        pivot_dot = Dot(pivot, color=BLUE_E, radius=0.08)
        
        # Single pendulum variables
        theta1 = ValueTracker(np.pi/4)
        omega1 = ValueTracker(0.0)
        dt = 0.01
        
        def get_bob_pos():
            angle = theta1.get_value()
            return pivot + length * np.array([np.sin(angle), -np.cos(angle), 0.0])
        
        rod1 = always_redraw(lambda: Line(pivot, get_bob_pos(), color=BLUE_E, stroke_width=3))
        bob1 = always_redraw(lambda: Dot(get_bob_pos(), color=GOLD_E, radius=0.12))
        
        self.play(Create(rod1), Create(bob1), Create(pivot_dot), run_time=0.8)
        
        # Trace for single pendulum
        trace_path = VMobject(color=BLUE_E)
        trace_path.set_points_as_corners([get_bob_pos(), get_bob_pos()])
        
        def update_trace(mob):
            mob.add_points_as_corners([get_bob_pos()])
        
        trace_path.add_updater(update_trace)
        self.add(trace_path)
        
        # Animate single pendulum for establish phase
        for _ in range(120):  # About 4 seconds at 30 fps
            alpha = self.renderer.time
            new_theta = np.pi/4 * np.cos(np.sqrt(gravity/length) * alpha)
            theta1.set_value(new_theta)
            self.wait(dt)
        
        # EVOLVE - Second pendulum attaches creating double system
        # Add second pendulum
        def get_second_bob_pos():
            angle1 = theta1.get_value()
            angle2 = theta2.get_value()
            first_bob = pivot + length * np.array([np.sin(angle1), -np.cos(angle1), 0.0])
            return first_bob + length * np.array([np.sin(angle2), -np.cos(angle2), 0.0])
        
        # Initialize second pendulum variables
        theta2 = ValueTracker(np.pi/6)
        omega2 = ValueTracker(0.0)
        
        rod2 = always_redraw(lambda: Line(get_bob_pos(), get_second_bob_pos(), color=BLUE_E, stroke_width=3))
        bob2 = always_redraw(lambda: Dot(get_second_bob_pos(), color=GOLD_E, radius=0.12))
        
        # New trace for second bob
        trace_path2 = VMobject(color=RED_D)
        trace_path2.set_points_as_corners([get_second_bob_pos(), get_second_bob_pos()])
        
        def update_trace2(mob):
            mob.add_points_as_corners([get_second_bob_pos()])
        
        trace_path2.add_updater(update_trace2)
        
        # Add second pendulum components
        self.play(Create(rod2), Create(bob2), run_time=0.8)
        self.add(trace_path2)
        
        # Simulate double pendulum physics using numerical integration
        def double_pendulum_derivatives(theta1_val, omega1_val, theta2_val, omega2_val):
            # Parameters
            g = gravity
            L1 = L2 = length
            m1 = m2 = 1.0
            
            cos_diff = np.cos(theta1_val - theta2_val)
            sin_diff = np.sin(theta1_val - theta2_val)
            
            denominator = m1 + m2 * sin_diff**2
            
            # Angular accelerations
            alpha1 = (-g * (2*m1 + m2) * np.sin(theta1_val) 
                     - m2 * g * np.sin(theta1_val - 2*theta2_val) 
                     - 2 * np.sin_diff * m2 * (omega2_val**2 * L2 + omega1_val**2 * L1 * cos_diff)) / (L1 * denominator)
            
            alpha2 = (2 * sin_diff * (omega1_val**2 * L1 * (m1 + m2) 
                     + g * (m1 + m2) * np.cos(theta1_val) 
                     + omega2_val**2 * L2 * m2 * cos_diff)) / (L2 * denominator)
            
            return omega1_val, alpha1, omega2_val, alpha2
        
        # Animate double pendulum for evolve phase
        for _ in range(160):  # About 5.3 seconds at 30 fps
            domega1, dalpha1, domega2, dalpha2 = double_pendulum_derivatives(
                theta1.get_value(), omega1.get_value(), 
                theta2.get_value(), omega2.get_value()
            )
            
            theta1.increment_value(domega1 * dt)
            omega1.increment_value(dalpha1 * dt)
            theta2.increment_value(domega2 * dt)
            omega2.increment_value(dalpha2 * dt)
            
            # Make g and L labels pulse during chaotic motion
            if _ % 15 == 0:  # Pulse every 15 frames
                self.play(
                    g_label.animate.set_color(RED_D),
                    l_label.animate.set_color(RED_D),
                    run_time=0.1
                )
                self.play(
                    g_label.animate.set_color(GOLD_E),
                    l_label.animate.set_color(GOLD_E),
                    run_time=0.1
                )
            
            self.wait(dt)
        
        # REVEAL - Euler-Lagrange equations materialize above chaotic motion
        eq_text = MathTex(
            r"\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}_i}\right) - \frac{\partial L}{\partial q_i} = 0",
            color=RED_D
        ).scale(0.6).to_edge(UP).shift(DOWN*0.5)
        
        self.play(Write(eq_text), run_time=2.0)
        
        # Continue chaotic motion while showing equations
        for _ in range(105):  # About 3.5 seconds at 30 fps
            domega1, dalpha1, domega2, dalpha2 = double_pendulum_derivatives(
                theta1.get_value(), omega1.get_value(), 
                theta2.get_value(), omega2.get_value()
            )
            
            theta1.increment_value(domega1 * dt)
            omega1.increment_value(dalpha1 * dt)
            theta2.increment_value(domega2 * dt)
            omega2.increment_value(dalpha2 * dt)
            
            self.wait(dt)
        
        # IDLE LOOP - Chaotic attractor continues with gentle pulsing equations
        # Make equation pulse gently
        def pulse_equation(mob):
            scale_factor = 0.6 + 0.02 * np.sin(self.renderer.time * 2)
            mob.scale(scale_factor / mob.width * 0.6)
        
        eq_text.add_updater(pulse_equation)
        
        # Continue simulation indefinitely
        for _ in range(100):  # This creates the idle loop effect
            domega1, dalpha1, domega2, dalpha2 = double_pendulum_derivatives(
                theta1.get_value(), omega1.get_value(), 
                theta2.get_value(), omega2.get_value()
            )
            
            theta1.increment_value(domega1 * dt)
            omega1.increment_value(dalpha1 * dt)
            theta2.increment_value(domega2 * dt)
            omega2.increment_value(dalpha2 * dt)
            
            self.wait(dt)