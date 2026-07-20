from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # Define parameters
        gravity = 9.81
        length1 = 1.0
        length2 = 1.0
        mass1 = 1.0
        mass2 = 1.0
        
        # Pivot point
        pivot = np.array([0, 2, 0])
        
        # Initial angles
        theta1_0 = PI / 3
        theta2_0 = PI / 4
        
        # Time tracker
        t = ValueTracker(0.0)
        
        # Position functions for double pendulum (simplified harmonic approximation for visualization)
        def get_theta1(t_val):
            return theta1_0 * np.cos(1.2 * t_val)
        
        def get_theta2(t_val):
            return theta2_0 * np.cos(2.0 * t_val)
        
        def get_pos1():
            theta1 = get_theta1(t.get_value())
            return pivot + length1 * np.array([np.sin(theta1), -np.cos(theta1), 0])
        
        def get_pos2():
            theta1 = get_theta1(t.get_value())
            theta2 = get_theta2(t.get_value())
            pos1 = get_pos1()
            return pos1 + length2 * np.array([np.sin(theta2), -np.cos(theta2), 0])
        
        # Velocity functions (derivatives)
        def get_vel1():
            theta1 = get_theta1(t.get_value())
            dtheta1_dt = -theta1_0 * 1.2 * np.sin(1.2 * t.get_value())
            return length1 * dtheta1_dt * np.array([np.cos(theta1), np.sin(theta1), 0])
        
        def get_vel2():
            theta1 = get_theta1(t.get_value())
            theta2 = get_theta2(t.get_value())
            dtheta1_dt = -theta1_0 * 1.2 * np.sin(1.2 * t.get_value())
            dtheta2_dt = -theta2_0 * 2.0 * np.sin(2.0 * t.get_value())
            
            # Velocity of second mass
            vx = length1 * dtheta1_dt * np.cos(theta1) + length2 * (dtheta1_dt + dtheta2_dt) * np.cos(theta2)
            vy = length1 * dtheta1_dt * np.sin(theta1) + length2 * (dtheta1_dt + dtheta2_dt) * np.sin(theta2)
            return np.array([vx, vy, 0])
        
        # Create pendulum objects
        anchor = Dot(pivot, color=BLUE_E, radius=0.1)
        rod1 = always_redraw(lambda: Line(pivot, get_pos1(), color=BLUE_E, stroke_width=3))
        rod2 = always_redraw(lambda: Line(get_pos1(), get_pos2(), color=BLUE_E, stroke_width=3))
        bob1 = always_redraw(lambda: Dot(get_pos1(), color=GOLD_E, radius=0.15))
        bob2 = always_redraw(lambda: Dot(get_pos2(), color=GOLD_E, radius=0.15))
        
        # ACT 1: ESTABLISH
        self.play(
            Create(anchor),
            Create(rod1),
            Create(rod2),
            Create(bob1),
            Create(bob2),
            run_time=2
        )
        
        # Position labels
        pos_label1 = always_redraw(lambda: MathTex("(x_1, y_1)", color=BLUE_E)
                                  .next_to(get_pos1(), DOWN, buff=0.2))
        pos_label2 = always_redraw(lambda: MathTex("(x_2, y_2)", color=BLUE_E)
                                  .next_to(get_pos2(), DOWN, buff=0.2))
        
        self.play(
            FadeIn(pos_label1),
            FadeIn(pos_label2),
            run_time=1.5
        )
        
        # Velocity vectors
        vel_arrow1 = always_redraw(lambda: Arrow(
            get_pos1(),
            get_pos1() + 0.5 * get_vel1() / max(np.linalg.norm(get_vel1()), 0.1),
            color=RED_D, buff=0, stroke_width=3, max_stroke_width_to_length_ratio=5
        ))
        vel_arrow2 = always_redraw(lambda: Arrow(
            get_pos2(),
            get_pos2() + 0.5 * get_vel2() / max(np.linalg.norm(get_vel2()), 0.1),
            color=RED_D, buff=0, stroke_width=3, max_stroke_width_to_length_ratio=5
        ))
        
        self.play(
            Create(vel_arrow1),
            Create(vel_arrow2),
            run_time=1.5
        )
        
        # Derivative labels for first mass
        deriv_label1 = always_redraw(lambda: VGroup(
            MathTex("\\frac{dx_1}{dt}", color=BLUE_E).scale(0.5),
            MathTex("\\frac{dy_1}{dt}", color=BLUE_E).scale(0.5)
        ).arrange(DOWN, buff=0.2).next_to(get_pos1(), UP, buff=0.5))
        
        self.play(
            FadeIn(deriv_label1),
            run_time=1
        )
        
        # Narration for Act 1
        narration1 = Text("Two masses begin their gravitational dance...", color=BLUE_E).scale(0.4).to_edge(UP)
        self.play(Write(narration1), run_time=0.5)
        
        # Animate initial swinging
        self.play(t.animate.set_value(2.0), run_time=6, rate_func=linear)
        
        # ACT 2: EVOLVE
        # Remove narration 1 and add narration 2
        self.play(FadeOut(narration1))
        narration2 = Text("Velocities square and energies emerge...", color=BLUE_E).scale(0.4).to_edge(UP)
        self.play(Write(narration2), run_time=0.5)
        
        # Add derivative labels for second mass
        deriv_label2 = always_redraw(lambda: VGroup(
            MathTex("\\frac{dx_2}{dt}", color=BLUE_E).scale(0.5),
            MathTex("\\frac{dy_2}{dt}", color=BLUE_E).scale(0.5)
        ).arrange(DOWN, buff=0.2).next_to(get_pos2(), UP, buff=0.5))
        
        self.play(
            FadeIn(deriv_label2),
            run_time=1
        )
        
        # Squared velocity calculations
        v1_squared = always_redraw(lambda: MathTex("v_1^2 =", color=GOLD_E).scale(0.4)
                                  .next_to(get_pos1(), LEFT, buff=0.8))
        v2_squared = always_redraw(lambda: MathTex("v_2^2 =", color=GOLD_E).scale(0.4)
                                  .next_to(get_pos2(), RIGHT, buff=0.8))
        
        # Values for squared velocities
        v1_sq_val = always_redraw(lambda: DecimalNumber(
            np.dot(get_vel1(), get_vel1()),
            num_decimal_places=2,
            color=GOLD_E
        ).scale(0.4).next_to(v1_squared, RIGHT, buff=0.2))
        
        v2_sq_val = always_redraw(lambda: DecimalNumber(
            np.dot(get_vel2(), get_vel2()),
            num_decimal_places=2,
            color=GOLD_E
        ).scale(0.4).next_to(v2_squared, RIGHT, buff=0.2))
        
        self.play(
            FadeIn(v1_squared),
            FadeIn(v2_squared),
            FadeIn(v1_sq_val),
            FadeIn(v2_sq_val),
            run_time=1.5
        )
        
        # Kinetic energy terms
        ke1_term = always_redraw(lambda: MathTex("\\frac{1}{2}m_1v_1^2", color=GOLD_E).scale(0.4)
                                .next_to(get_pos1(), UL, buff=0.5))
        ke2_term = always_redraw(lambda: MathTex("\\frac{1}{2}m_2v_2^2", color=GOLD_E).scale(0.4)
                                .next_to(get_pos2(), UR, buff=0.5))
        
        # Animate the kinetic energy terms appearing with pulsing effect
        self.play(
            FadeIn(ke1_term),
            FadeIn(ke2_term),
            run_time=1.5
        )
        
        # Continue the motion for Act 2
        self.play(t.animate.set_value(6.0), run_time=8, rate_func=linear)
        
        # ACT 3: REVEAL
        # Remove narration 2 and add narration 3
        self.play(FadeOut(narration2))
        narration3 = Text("Total kinetic energy revealed.", color=BLUE_E).scale(0.4).to_edge(UP)
        self.play(Write(narration3), run_time=0.5)
        
        # Final kinetic energy equation
        total_ke = MathTex("T = \\frac{1}{2}m_1v_1^2 + \\frac{1}{2}m_2v_2^2", color=GOLD_E).scale(0.6).to_edge(UP, buff=1.0)
        
        # Total energy value
        total_energy = always_redraw(lambda: DecimalNumber(
            0.5 * mass1 * np.dot(get_vel1(), get_vel1()) + 0.5 * mass2 * np.dot(get_vel2(), get_vel2()),
            num_decimal_places=2,
            color=GOLD_E
        ).scale(0.5).next_to(total_ke, DOWN, buff=0.3))
        
        self.play(
            Write(total_ke),
            FadeIn(total_energy),
            run_time=2
        )
        
        # Highlight the pendulum system with a glowing effect
        self.play(
            bob1.animate.set_color(RED_D),
            bob2.animate.set_color(RED_D),
            run_time=0.5
        )
        self.play(
            bob1.animate.set_color(GOLD_E),
            bob2.animate.set_color(GOLD_E),
            run_time=0.5
        )
        
        # Continue motion for Act 3
        self.play(t.animate.set_value(10.0), run_time=7, rate_func=linear)
        
        # IDLE LOOP - continue the motion indefinitely
        self.play(t.animate.set_value(20.0), run_time=10, rate_func=linear)