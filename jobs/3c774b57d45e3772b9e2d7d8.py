from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Single pendulum with digital readout
        title = Text("Coupled Chaos: Double Pendulum", color=BLUE).scale(0.5).to_edge(UP)
        self.play(Write(title), run_time=0.9)

        # Digital readout panel
        gravity_label = Text("gravity:", color=GOLD).scale(0.3)
        gravity_value = DecimalNumber(9.81, num_decimal_places=2, color=GOLD).scale(0.3)
        gravity_group = VGroup(gravity_label, gravity_value).arrange(RIGHT, buff=0.2)
        
        length_label = Text("length:", color=GOLD).scale(0.3)
        length_value = DecimalNumber(1.0, num_decimal_places=2, color=GOLD).scale(0.3)
        length_group = VGroup(length_label, length_value).arrange(RIGHT, buff=0.2)
        
        readout_panel = VGroup(gravity_group, length_group).arrange(DOWN, buff=0.3).to_corner(UL).shift(DOWN*0.5)
        self.play(FadeIn(readout_panel), run_time=0.8)

        # Single pendulum setup
        g, length = 9.81, 1.0
        omega = math.sqrt(g / length)
        theta0 = 0.5
        pivot = np.array([-2.0, 1.0, 0.0])
        rod_len = 1.5
        t = ValueTracker(0.0)

        def theta_single(time):
            return theta0 * math.cos(omega * time)

        def bob_pos_single():
            th = theta_single(t.get_value())
            return pivot + rod_len * np.array([math.sin(th), -math.cos(th), 0.0])

        anchor = Dot(pivot, color=BLUE, radius=0.05)
        rod = always_redraw(lambda: Line(pivot, bob_pos_single(), color=BLUE, stroke_width=3))
        bob = always_redraw(lambda: Dot(bob_pos_single(), color=GOLD, radius=0.12))
        
        self.play(Create(rod), Create(bob), Create(anchor), run_time=0.8)
        self.play(t.animate.set_value(6.0), run_time=5.0, rate_func=linear)
        
        # EVOLVE — Add second pendulum and show chaos
        # Reset tracker
        t.set_value(0.0)
        
        # Parameters for double pendulum
        m1, m2 = 1.0, 1.0
        l1, l2 = 1.0, 1.0
        
        # Initial conditions for chaotic motion
        theta1_0, theta2_0 = 2.0, 1.0
        omega1_0, omega2_0 = 0.0, 0.0
        
        # State variables
        state = np.array([theta1_0, omega1_0, theta2_0, omega2_0])
        
        def derivs(t, state):
            theta1, z1, theta2, z2 = state
            c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)
            
            theta1_dot = z1
            theta2_dot = z2
            
            z1_dot = (m2*g*np.sin(theta2)*c - m2*s*(l1*z1**2*c + l2*z2**2) -
                     (m1+m2)*g*np.sin(theta1)) / l1 / (m1 + m2*s**2)
            z2_dot = ((m1+m2)*(l1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) +
                     m2*l2*z2**2*s*c) / l2 / (m1 + m2*s**2)
            
            return np.array([theta1_dot, z1_dot, theta2_dot, z2_dot])
        
        def get_positions_double(t_val):
            dt = 0.01
            current_state = state.copy()
            for i in range(int(t_val/dt)):
                k1 = dt * derivs(i*dt, current_state)
                k2 = dt * derivs(i*dt + dt/2, current_state + k1/2)
                k3 = dt * derivs(i*dt + dt/2, current_state + k2/2)
                k4 = dt * derivs(i*dt + dt, current_state + k3)
                current_state += (k1 + 2*k2 + 2*k3 + k4)/6
            theta1, theta2 = current_state[0], current_state[2]
            
            x1 = l1 * np.sin(theta1)
            y1 = -l1 * np.cos(theta1)
            x2 = x1 + l2 * np.sin(theta2)
            y2 = y1 - l2 * np.cos(theta2)
            
            pos1 = pivot + np.array([x1, y1, 0])
            pos2 = pivot + np.array([x2, y2, 0])
            return pos1, pos2
        
        # Remove single pendulum
        self.play(FadeOut(rod), FadeOut(bob), run_time=0.5)
        
        # Create double pendulum
        def get_pos1():
            pos1, pos2 = get_positions_double(t.get_value())
            return pos1
        
        def get_pos2():
            pos1, pos2 = get_positions_double(t.get_value())
            return pos2
        
        # Rods and bobs for double pendulum
        rod1 = always_redraw(lambda: Line(pivot, get_pos1(), color=BLUE, stroke_width=3))
        rod2 = always_redraw(lambda: Line(get_pos1(), get_pos2(), color=BLUE, stroke_width=3))
        bob1 = always_redraw(lambda: Dot(get_pos1(), color=GOLD, radius=0.1))
        bob2 = always_redraw(lambda: Dot(get_pos2(), color=GOLD, radius=0.1))
        
        # Trails for chaotic motion
        trail1 = VMobject(color=GOLD, stroke_width=2)
        trail1.start_new_path(get_pos1())
        trail2 = VMobject(color=RED, stroke_width=2)
        trail2.start_new_path(get_pos2())
        
        def update_trail1(trail):
            trail.add_line_to(get_pos1())
        
        def update_trail2(trail):
            trail.add_line_to(get_pos2())
        
        trail1.add_updater(update_trail1)
        trail2.add_updater(update_trail2)
        
        self.play(Create(rod1), Create(rod2), Create(bob1), Create(bob2), 
                  Create(trail1), Create(trail2), run_time=1.0)
        
        self.play(t.animate.set_value(8.0), run_time=7.0, rate_func=linear)
        
        # REVEAL — Split screen and equations
        self.play(FadeOut(trail1), FadeOut(trail2), run_time=0.5)
        
        # Create split screen effect
        left_rect = Rectangle(height=6, width=4, color=BLUE, fill_opacity=0.1).to_edge(LEFT, buff=0.1)
        right_rect = Rectangle(height=6, width=4, color=BLUE, fill_opacity=0.1).to_edge(RIGHT, buff=0.1)
        
        self.play(Create(left_rect), Create(right_rect), run_time=0.8)
        
        # Equations for double pendulum
        eq1 = MathTex(r"\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{\theta}_1}\right) - \frac{\partial L}{\partial \theta_1} = 0", color=GOLD).scale(0.4)
        eq2 = MathTex(r"\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{\theta}_2}\right) - \frac{\partial L}{\partial \theta_2} = 0", color=GOLD).scale(0.4)
        
        eq1.next_to(left_rect.get_center(), DOWN, buff=0.5)
        eq2.next_to(right_rect.get_center(), DOWN, buff=0.5)
        
        # Coupling lines
        coupling_line = Line(get_pos1(), get_pos2(), color=RED, stroke_width=4)
        
        self.play(Write(eq1), Write(eq2), Create(coupling_line), run_time=1.0)
        
        # Final hero frame: freeze pendulums at extreme positions
        t.set_value(8.5)  # Freeze at chaotic position
        self.wait(0.5)
        
        # IDLE LOOP: Slow breathing of equations while trails fade
        def breathe_eq(mob):
            mob.scale(1 + 0.02 * np.sin(0.5 * t.get_value()))
        
        eq1.add_updater(breathe_eq)
        eq2.add_updater(lambda m: m.scale(1 + 0.02 * np.sin(0.5 * t.get_value() + 0.5)))
        
        self.play(t.animate.set_value(15.0), run_time=5.0, rate_func=linear)