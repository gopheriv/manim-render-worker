from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # Set up the scene with the specified palette
        self.camera.background_color = WHITE
        
        # Define parameters
        gravity = 9.81
        length = 1.0
        m1, m2 = 1.0, 1.0  # Masses
        l1, l2 = 1.0, 1.0  # Lengths
        
        # Create ValueTrackers for angles
        theta1_tracker = ValueTracker(PI/4)
        theta2_tracker = ValueTracker(PI/6)
        
        # Pivot point
        pivot = np.array([0, 2, 0])
        
        # Position functions for the bobs
        def get_bob1_position():
            angle = theta1_tracker.get_value()
            return pivot + l1 * np.array([np.sin(angle), -np.cos(angle), 0])
        
        def get_bob2_position():
            angle1 = theta1_tracker.get_value()
            angle2 = theta2_tracker.get_value()
            pos1 = get_bob1_position()
            return pos1 + l2 * np.array([np.sin(angle2), -np.cos(angle2), 0])
        
        # Create pendulum components
        anchor = Dot(pivot, color=BLUE_E, radius=0.1)
        
        rod1 = always_redraw(lambda: Line(pivot, get_bob1_position(), 
                                         color=GOLD_E, stroke_width=4))
        rod2 = always_redraw(lambda: Line(get_bob1_position(), get_bob2_position(), 
                                         color=GOLD_E, stroke_width=4))
        
        bob1 = always_redraw(lambda: Dot(get_bob1_position(), 
                                        color=BLUE_E, radius=0.15))
        bob2 = always_redraw(lambda: Dot(get_bob2_position(), 
                                        color=BLUE_E, radius=0.15))
        
        # Velocity vectors (initially zero)
        vel1_arrow = always_redraw(lambda: Arrow(
            get_bob1_position(),
            get_bob1_position() + np.array([0, 0, 0]),
            color=BLUE_E, buff=0, max_tip_length_to_length_ratio=0.2
        ))
        
        vel2_arrow = always_redraw(lambda: Arrow(
            get_bob2_position(),
            get_bob2_position() + np.array([0, 0, 0]),
            color=BLUE_E, buff=0, max_tip_length_to_length_ratio=0.2
        ))
        
        # ESTABLISH ACT (6 seconds)
        title = Text("Double Pendulum System", color=BLUE_E).scale(0.6).to_edge(UP)
        self.play(Write(title))
        
        # Show the first pendulum
        self.play(Create(anchor), Create(rod1), Create(bob1), run_time=1.5)
        
        # Add the second pendulum
        self.play(Create(rod2), Create(bob2), run_time=1.5)
        
        # Show velocity vectors
        self.play(GrowArrow(vel1_arrow), GrowArrow(vel2_arrow), run_time=1.5)
        
        # Add labels for the bobs
        label1 = Text("Mass 1", color=BLUE_E).scale(0.4).next_to(bob1, DOWN)
        label2 = Text("Mass 2", color=BLUE_E).scale(0.4).next_to(bob2, DOWN)
        label1.add_updater(lambda x: x.next_to(bob1, DOWN))
        label2.add_updater(lambda x: x.next_to(bob2, DOWN))
        
        self.play(FadeIn(label1), FadeIn(label2))
        
        # EVOLVE ACT (8 seconds)
        # Mathematical expressions for derivatives
        deriv1_text = MathTex("\\frac{dx_1}{dt}, \\frac{dy_1}{dt}", color=BLUE_E).scale(0.5)
        deriv2_text = MathTex("\\frac{dx_2}{dt}, \\frac{dy_2}{dt}", color=BLUE_E).scale(0.5)
        deriv1_text.next_to(bob1, UR, buff=0.5)
        deriv2_text.next_to(bob2, UR, buff=0.5)
        
        # Position the derivative texts
        self.play(Write(deriv1_text), Write(deriv2_text))
        
        # Add more mathematical expressions
        v_squared1 = MathTex("v_1^2 = \\left(\\frac{dx_1}{dt}\\right)^2 + \\left(\\frac{dy_1}{dt}\\right)^2", 
                             color=BLUE_E).scale(0.4)
        v_squared2 = MathTex("v_2^2 = \\left(\\frac{dx_2}{dt}\\right)^2 + \\left(\\frac{dy_2}{dt}\\right)^2", 
                             color=BLUE_E).scale(0.4)
        v_squared1.next_to(deriv1_text, UP, buff=0.3)
        v_squared2.next_to(deriv2_text, UP, buff=0.3)
        
        self.play(Write(v_squared1), Write(v_squared2))
        
        # Energy terms
        energy1 = MathTex("\\frac{1}{2}m_1v_1^2", color=BLUE_E).scale(0.4)
        energy2 = MathTex("\\frac{1}{2}m_2v_2^2", color=BLUE_E).scale(0.4)
        energy1.next_to(v_squared1, UP, buff=0.3)
        energy2.next_to(v_squared2, UP, buff=0.3)
        
        self.play(Write(energy1), Write(energy2))
        
        # Animate the pendulums swinging
        self.play(
            theta1_tracker.animate.set_value(PI/3),
            theta2_tracker.animate.set_value(PI/4),
            run_time=3,
            rate_func=there_and_back
        )
        
        self.play(
            theta1_tracker.animate.set_value(-PI/4),
            theta2_tracker.animate.set_value(-PI/6),
            run_time=3,
            rate_func=there_and_back
        )
        
        # REVEAL ACT (6 seconds)
        # Total kinetic energy equation
        total_energy = MathTex("T = \\frac{1}{2}m_1v_1^2 + \\frac{1}{2}m_2v_2^2", 
                               color=GOLD_E).scale(0.6)
        total_energy.move_to(np.array([0, -2, 0]))
        
        # Highlight the total energy
        self.play(Write(total_energy), run_time=2)
        
        # Make the pendulums reach synchronized motion
        self.play(
            theta1_tracker.animate.set_value(PI/5),
            theta2_tracker.animate.set_value(PI/3),
            run_time=2
        )
        
        # Pulse effect for energy value
        self.play(
            total_energy.animate.set_color(TEAL_A),
            run_time=0.5
        )
        self.play(
            total_energy.animate.set_color(GOLD_E),
            run_time=0.5
        )
        
        # Stabilize the system
        self.play(
            theta1_tracker.animate.set_value(PI/6),
            theta2_tracker.animate.set_value(PI/4),
            run_time=1
        )
        
        # IDLE LOOP setup
        # Continue the gentle oscillation
        def update_velocities(mob):
            # Calculate approximate velocities based on angular changes
            dt = 0.01
            theta1 = theta1_tracker.get_value()
            theta2 = theta2_tracker.get_value()
            
            # Approximate velocity directions based on current angles
            vel1_dir = np.array([np.cos(theta1), np.sin(theta1), 0]) * 0.3
            vel2_dir = np.array([np.cos(theta2), np.sin(theta2), 0]) * 0.3
            
            mob.become(Arrow(
                get_bob1_position(),
                get_bob1_position() + vel1_dir,
                color=BLUE_E, buff=0, max_tip_length_to_length_ratio=0.2
            ))
        
        def update_vel2(mob):
            dt = 0.01
            theta1 = theta1_tracker.get_value()
            theta2 = theta2_tracker.get_value()
            
            # Approximate velocity directions based on current angles
            vel2_dir = np.array([np.cos(theta2), np.sin(theta2), 0]) * 0.3
            
            mob.become(Arrow(
                get_bob2_position(),
                get_bob2_position() + vel2_dir,
                color=BLUE_E, buff=0, max_tip_length_to_length_ratio=0.2
            ))
        
        vel1_arrow.add_updater(update_velocities)
        vel2_arrow.add_updater(update_vel2)
        
        # Continue the oscillation for the idle loop
        self.play(
            theta1_tracker.animate.set_value(PI/4),
            theta2_tracker.animate.set_value(PI/5),
            run_time=3,
            rate_func=linear
        )
        
        # Keep the system moving gently
        self.wait(2)


# The scene will continue with the idle loop where pendulums maintain gentle oscillation
# while energy value pulses subtly, velocity vectors shimmer and fade in sync with
# the mathematical terms above.