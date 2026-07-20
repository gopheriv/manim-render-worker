from manim import *
import numpy as np


class AetherLabScene(MovingCameraScene):
    def construct(self):
        # Set up the background
        self.camera.background_color = DARK_BLUE
        
        # Create starfield background
        stars = VGroup()
        for _ in range(100):
            x = np.random.uniform(-config.frame_width/2, config.frame_width/2)
            y = np.random.uniform(-config.frame_height/2, config.frame_height/2)
            star = Dot(point=[x, y, 0], color=WHITE, radius=0.02)
            stars.add(star)
        self.add(stars)

        # Define parameters
        gravity = 9.81
        length = 1.0
        m1 = 1.0
        m2 = 1.0
        
        # Pivot points
        pivot1 = np.array([-1.5, 1.0, 0])
        pivot2 = lambda: pivot1 + length * np.array([np.sin(self.theta1.get_value()), -np.cos(self.theta1.get_value()), 0])
        
        # Angles
        self.theta1 = ValueTracker(0)
        self.theta2 = ValueTracker(0)
        
        # Create pendulum arms
        arm1 = always_redraw(lambda: Line(pivot1, pivot2(), color=GOLD, stroke_width=5))
        arm2 = always_redraw(lambda: Line(pivot2(), 
                                         pivot2() + length * np.array([
                                             np.sin(self.theta1.get_value() + self.theta2.get_value()),
                                             -np.cos(self.theta1.get_value() + self.theta2.get_value()), 0]),
                                         color=GOLD, stroke_width=5))

        # Create masses
        mass1 = always_redraw(lambda: Dot(pivot2(), color=BLACK, radius=0.15, stroke_color=GOLD, stroke_width=2))
        mass2 = always_redraw(lambda: Dot(
            pivot2() + length * np.array([
                np.sin(self.theta1.get_value() + self.theta2.get_value()),
                -np.cos(self.theta1.get_value() + self.theta2.get_value()), 0]),
            color=BLACK, radius=0.15, stroke_color=GOLD, stroke_width=2))

        # Gravitational field lines
        field_lines = VGroup()
        for i in range(-5, 6):
            for j in range(3, 8):
                start = np.array([i*0.6, j*0.5, 0])
                end = np.array([i*0.6, j*0.5 - 0.3, 0])
                line = Arrow(start, end, color=BLUE, stroke_width=1, buff=0, max_tip_length_to_length_ratio=0.2)
                field_lines.add(line)

        # ACT 1: ESTABLISH
        title = Text("Double Pendulum System", color=GOLD).scale(0.6).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        
        # Show pendulum arms in rest position
        self.play(Create(arm1), Create(arm2), run_time=1.5)
        self.play(FadeIn(mass1), FadeIn(mass2), run_time=1.0)
        
        # Show gravitational field lines
        self.play(Create(field_lines), run_time=1.5)
        
        # Add mass labels
        m1_label = Text("m₁", color=GOLD).scale(0.4).next_to(mass1, RIGHT, buff=0.1)
        m2_label = Text("m₂", color=GOLD).scale(0.4).next_to(mass2, RIGHT, buff=0.1)
        self.play(Write(m1_label), Write(m2_label), run_time=1.0)
        
        # Add length labels
        l1_label = Text("ℓ = 1.0", color=GOLD).scale(0.3).next_to(arm1, LEFT, buff=0.1)
        l2_label = Text("ℓ = 1.0", color=GOLD).scale(0.3).next_to(arm2, LEFT, buff=0.1)
        self.play(Write(l1_label), Write(l2_label), run_time=1.0)
        
        # Wait to complete act 1
        self.wait(0.5)

        # ACT 2: EVOLVE
        # Slightly perturb the system
        self.play(
            self.theta1.animate.set_value(0.3),
            self.theta2.animate.set_value(0.2),
            run_time=2.0
        )
        
        # Show angles
        angle1_arc = always_redraw(lambda: Arc(radius=0.5, start_angle=-PI/2, angle=self.theta1.get_value(), color=YELLOW).move_arc_center_to(pivot1))
        angle2_arc = always_redraw(lambda: Arc(radius=0.4, start_angle=-PI/2 + self.theta1.get_value(), angle=self.theta2.get_value(), color=YELLOW).move_arc_center_to(pivot2()))
        
        theta1_label = always_redraw(lambda: Text("θ₁", color=YELLOW).scale(0.3).next_to(angle1_arc, UR, buff=0.1))
        theta2_label = always_redraw(lambda: Text("θ₂", color=YELLOW).scale(0.3).next_to(angle2_arc, UR, buff=0.1))
        
        self.play(Create(angle1_arc), Create(angle2_arc), Write(theta1_label), Write(theta2_label), run_time=1.0)
        
        # Show potential energy formula
        pe_formula = MathTex("V = mgh", color=GOLD).scale(0.5).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(pe_formula), run_time=1.0)
        
        # Show height calculations
        h1_text = MathTex("h_1 =", color=GOLD).scale(0.4).next_to(pe_formula, DOWN, buff=0.3)
        h2_text = MathTex("h_2 =", color=GOLD).scale(0.4).next_to(h1_text, DOWN, buff=0.3)
        self.play(Write(h1_text), Write(h2_text), run_time=1.0)
        
        # Show gravity value tracker
        gravity_tracker = ValueTracker(gravity)
        gravity_decimal = always_redraw(lambda: DecimalNumber(gravity_tracker.get_value(), num_decimal_places=2, color=YELLOW).scale(0.4).next_to(h2_text, DOWN, buff=0.3))
        gravity_label = Text("g =", color=YELLOW).scale(0.4).next_to(gravity_decimal, LEFT, buff=0.1)
        gravity_group = VGroup(gravity_decimal, gravity_label).next_to(h2_text, DOWN, buff=0.3)
        self.play(FadeIn(gravity_group), run_time=1.0)
        
        # Animate slight movement to show evolution
        self.play(
            self.theta1.animate.set_value(0.5),
            self.theta2.animate.set_value(-0.3),
            run_time=2.0
        )

        # ACT 3: REVEAL
        # Total potential energy expression
        full_pe = MathTex(
            "V = m_1g(\\ell_1(1-\\cos \\theta_1)) + m_2g(\\ell_1(1-\\cos \\theta_1) + \\ell_2(1-\\cos \\theta_2))",
            color=GOLD
        ).scale(0.4).to_edge(UP).shift(DOWN)
        
        # Move camera to focus on the formula
        self.play(self.camera.frame.animate.move_to(full_pe.get_center()).scale(1.2), run_time=1.5)
        self.play(Write(full_pe), run_time=2.0)
        
        # Kinetic energy component
        ke_component = MathTex("T =", color=GOLD).scale(0.5).to_edge(LEFT).shift(UP*0.5)
        self.play(Write(ke_component), run_time=1.0)
        
        # Complete Lagrangian
        lagrangian = MathTex("L = T - V", color=YELLOW).scale(0.6).move_to(ORIGIN)
        self.play(Write(lagrangian), run_time=1.5)
        
        # Highlight coupled terms
        coupled_terms = MathTex("m_2g\\ell_1(1-\\cos \\theta_1)", color=ORANGE).scale(0.4).next_to(lagrangian, DOWN, buff=0.5)
        self.play(Indicate(coupled_terms, scale_factor=1.2, color=ORANGE), run_time=1.0)
        self.play(FadeIn(coupled_terms), run_time=1.0)
        
        # Continue the chaotic motion for idle loop
        def chaotic_motion(dt):
            # Simple chaotic-like motion for demonstration
            dtheta1 = 0.02 * np.sin(self.theta2.get_value() * 3)
            dtheta2 = 0.03 * np.cos(self.theta1.get_value() * 2)
            self.theta1.increment_value(dtheta1)
            self.theta2.increment_value(dtheta2)
        
        # Add updater for chaotic motion
        self.add_updater(chaotic_motion)
        
        # Rotate Lagrangian gently for optimal viewing
        def rotate_lagrangian(mob, dt):
            mob.rotate(0.1 * dt)
        
        lagrangian.add_updater(rotate_lagrangian)
        
        # Pulse field lines occasionally
        def pulse_field_lines(dt):
            if int(self.time) % 3 == 0:  # Every 3 seconds
                for line in field_lines:
                    line.set_opacity(0.7)
            else:
                for line in field_lines:
                    line.set_opacity(0.3)
        
        field_lines.add_updater(lambda m, dt: pulse_field_lines(dt))
        
        # Let the system continue moving chaotically
        self.wait(5.0)
        
        # Clean up updaters
        self.remove_updater(chaotic_motion)
        lagrangian.clear_updaters()
        field_lines.clear_updaters()