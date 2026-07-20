from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # Define colors from palette
        primary_color = BLUE_E
        secondary_color = ORANGE
        accent_color = GOLD_E
        
        # Set up the double pendulum parameters
        gravity = 9.81
        length1 = 1.0
        length2 = 1.0
        mass1 = 1.0
        mass2 = 1.0
        
        # Initial angles
        theta1_0 = PI / 3
        theta2_0 = PI / 4
        
        # Pivot point
        pivot = np.array([0, 2, 0])
        
        # Value trackers for angles
        t = ValueTracker(0.0)
        theta1_tracker = ValueTracker(theta1_0)
        theta2_tracker = ValueTracker(theta2_0)
        
        # Function to get positions of the two masses
        def get_positions():
            theta1 = theta1_tracker.get_value()
            theta2 = theta2_tracker.get_value()
            
            # Position of first mass
            x1 = pivot[0] + length1 * np.sin(theta1)
            y1 = pivot[1] - length1 * np.cos(theta1)
            pos1 = np.array([x1, y1, 0])
            
            # Position of second mass
            x2 = x1 + length2 * np.sin(theta2)
            y2 = y1 - length2 * np.cos(theta2)
            pos2 = np.array([x2, y2, 0])
            
            return pos1, pos2
        
        # Create the pendulum parts
        anchor = Dot(pivot, color=accent_color, radius=0.1)
        
        rod1 = always_redraw(lambda: Line(
            pivot, 
            get_positions()[0], 
            color=primary_color, 
            stroke_width=6
        ))
        
        rod2 = always_redraw(lambda: Line(
            get_positions()[0], 
            get_positions()[1], 
            color=primary_color, 
            stroke_width=6
        ))
        
        mass1_dot = always_redraw(lambda: Dot(
            get_positions()[0], 
            color=secondary_color, 
            radius=0.2
        ))
        
        mass2_dot = always_redraw(lambda: Dot(
            get_positions()[1], 
            color=secondary_color, 
            radius=0.25
        ))
        
        # Grid for reference
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_opacity": 0.2,
                "stroke_width": 1
            }
        )
        
        # ESTABLISH: Reveal the structure
        title = Text("Double Pendulum", color=WHITE).scale(0.6).to_edge(UP)
        self.play(Create(grid), run_time=1)
        self.play(Write(title), run_time=0.8)
        self.play(
            Create(anchor),
            Create(rod1),
            Create(rod2),
            Create(mass1_dot),
            Create(mass2_dot),
            run_time=1.5
        )
        
        # Animate initial slow rotation
        self.play(
            theta1_tracker.animate.set_value(theta1_0 + 0.3),
            theta2_tracker.animate.set_value(theta2_0 + 0.2),
            run_time=3
        )
        
        # EVOLVE: Accelerate into chaotic motion
        # Create velocity vectors
        vel_arrow1 = always_redraw(lambda: Arrow(
            get_positions()[0],
            get_positions()[0] + np.array([0.5 * np.cos(theta1_tracker.get_value()), 0.5 * np.sin(theta1_tracker.get_value()), 0]),
            color=GREEN,
            buff=0,
            max_tip_length_to_length_ratio=0.3
        ))
        
        vel_arrow2 = always_redraw(lambda: Arrow(
            get_positions()[1],
            get_positions()[1] + np.array([0.5 * np.cos(theta2_tracker.get_value()), 0.5 * np.sin(theta2_tracker.get_value()), 0]),
            color=GREEN,
            buff=0,
            max_tip_length_to_length_ratio=0.3
        ))
        
        # Length callouts
        length_label1 = always_redraw(lambda: Text(f"L₁ = {length1:.1f}", color=YELLOW).scale(0.3).next_to(rod1.get_center(), LEFT))
        length_label2 = always_redraw(lambda: Text(f"L₂ = {length2:.1f}", color=YELLOW).scale(0.3).next_to(rod2.get_center(), RIGHT))
        
        # Angular velocity displays
        omega1_text = always_redraw(lambda: DecimalNumber(
            np.sin(t.get_value()),
            color=WHITE,
            num_decimal_places=2
        ).scale(0.4).to_edge(UL).shift(DOWN))
        omega1_label = Text("ω₁ =", color=WHITE).scale(0.4).next_to(omega1_text, LEFT)
        
        omega2_text = always_redraw(lambda: DecimalNumber(
            np.cos(t.get_value()),
            color=WHITE,
            num_decimal_places=2
        ).scale(0.4).to_edge(UL).shift(2*DOWN))
        omega2_label = Text("ω₂ =", color=WHITE).scale(0.4).next_to(omega2_text, LEFT)
        
        # Add velocity vectors and labels
        self.play(
            Create(vel_arrow1),
            Create(vel_arrow2),
            Write(length_label1),
            Write(length_label2),
            Write(omega1_label),
            Write(omega2_label),
            run_time=1
        )
        self.add(omega1_text, omega2_text)
        
        # Simulate chaotic motion
        self.play(
            t.animate.set_value(8.0),
            theta1_tracker.animate.set_value(theta1_0 + 3*np.sin(0.8)),
            theta2_tracker.animate.set_value(theta2_0 + 2*np.cos(1.2)),
            run_time=7,
            rate_func=linear
        )
        
        # REVEAL: Freeze at peak chaos and show kinetic energy formula
        # Calculate positions and velocities at this moment
        pos1, pos2 = get_positions()
        
        # Show kinetic energy formula
        ke_formula = MathTex(
            "T = \\frac{1}{2}m_1v_1^2 + \\frac{1}{2}m_2v_2^2",
            color=WHITE
        ).scale(0.8).to_edge(UP).shift(DOWN*0.5)
        ke_formula_background = BackgroundRectangle(ke_formula, color=BLACK, fill_opacity=0.7, buff=0.1)
        
        # Highlight velocity components
        v_components = VGroup(
            MathTex("\\frac{dx_1}{dt}, \\frac{dy_1}{dt}", color=accent_color),
            MathTex("\\frac{dx_2}{dt}, \\frac{dy_2}{dt}", color=accent_color)
        ).arrange(DOWN, buff=0.5).to_corner(UR)
        
        self.play(
            FadeOut(vel_arrow1),
            FadeOut(vel_arrow2),
            FadeOut(length_label1),
            FadeOut(length_label2),
            FadeOut(omega1_label),
            FadeOut(omega2_label),
            FadeOut(omega1_text),
            FadeOut(omega2_text),
            run_time=0.5
        )
        
        self.play(
            FadeIn(ke_formula_background),
            Write(ke_formula),
            run_time=1
        )
        
        self.play(Write(v_components), run_time=1)
        
        # Add enhanced velocity vectors at freeze point
        enhanced_vel1 = Arrow(
            pos1,
            pos1 + np.array([0.8, 0.3, 0]),
            color=accent_color,
            buff=0,
            max_tip_length_to_length_ratio=0.3,
            stroke_width=5
        )
        
        enhanced_vel2 = Arrow(
            pos2,
            pos2 + np.array([-0.6, 0.5, 0]),
            color=accent_color,
            buff=0,
            max_tip_length_to_length_ratio=0.3,
            stroke_width=5
        )
        
        self.play(
            Create(enhanced_vel1),
            Create(enhanced_vel2),
            run_time=1
        )
        
        # IDLE LOOP: Subtle pulsing of velocity vectors and energy value
        def pulse_arrow(arrow, dt):
            scale_factor = 1 + 0.05 * np.sin(2 * t.get_value())
            arrow.scale(scale_factor, about_point=arrow.get_start())
            arrow.scale(1/scale_factor, about_point=arrow.get_start())
        
        enhanced_vel1.add_updater(pulse_arrow)
        enhanced_vel2.add_updater(pulse_arrow)
        
        # Also make the KE formula gently oscillate
        def oscillate_ke(formula, dt):
            formula.shift(0.01 * np.sin(3 * t.get_value()) * UP)
        
        ke_formula.add_updater(oscillate_ke)
        
        # Continue the animation for the idle loop
        self.play(t.animate.set_value(t.get_value() + 4), run_time=4, rate_func=linear)