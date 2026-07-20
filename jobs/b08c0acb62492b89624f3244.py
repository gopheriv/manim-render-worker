from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # Set up the scene with dark background
        self.camera.background_color = BLACK
        
        # Define parameters
        g = 9.81
        L1 = 1.5
        L2 = 1.2
        pivot = np.array([-2.0, 1.0, 0.0])
        
        # Create ValueTrackers for angles
        theta1_tracker = ValueTracker(0.2)
        theta2_tracker = ValueTracker(0.1)
        
        # Create the double pendulum components
        def get_m1_position():
            theta1 = theta1_tracker.get_value()
            return pivot + L1 * np.array([np.sin(theta1), -np.cos(theta1), 0.0])
        
        def get_m2_position():
            theta1 = theta1_tracker.get_value()
            theta2 = theta2_tracker.get_value()
            m1_pos = get_m1_position()
            return m1_pos + L2 * np.array([np.sin(theta2), -np.cos(theta2), 0.0])
        
        # Create pendulum components
        anchor = Dot(pivot, color=BLUE_E, radius=0.08)
        rod1 = always_redraw(lambda: Line(pivot, get_m1_position(), color=BLUE_E, stroke_width=4))
        rod2 = always_redraw(lambda: Line(get_m1_position(), get_m2_position(), color=BLUE_E, stroke_width=4))
        m1 = always_redraw(lambda: Dot(get_m1_position(), color=GOLD_E, radius=0.15))
        m2 = always_redraw(lambda: Dot(get_m2_position(), color=GOLD_E, radius=0.15))
        m1_label = always_redraw(lambda: MathTex("m_1", color=GOLD_E).scale(0.4).next_to(m1.get_center(), DOWN, buff=0.1))
        m2_label = always_redraw(lambda: MathTex("m_2", color=GOLD_E).scale(0.4).next_to(m2.get_center(), DOWN, buff=0.1))
        
        # Create angle arcs
        angle_arc1 = always_redraw(lambda: Arc(radius=0.5, start_angle=-PI/2, angle=theta1_tracker.get_value(), color=BLUE_E))
        angle_arc1.add_updater(lambda a: a.move_arc_center_to(pivot))
        
        angle_arc2 = always_redraw(lambda: Arc(radius=0.4, start_angle=-PI/2, angle=theta2_tracker.get_value(), color=BLUE_E))
        angle_arc2.add_updater(lambda a: a.move_arc_center_to(get_m1_position()))
        
        theta1_label = always_redraw(lambda: MathTex("\\theta_1", color=BLUE_E).scale(0.3).next_to(angle_arc1, LEFT, buff=0.1))
        theta2_label = always_redraw(lambda: MathTex("\\theta_2", color=BLUE_E).scale(0.3).next_to(angle_arc2, LEFT, buff=0.1))
        
        # Create angle readouts
        theta1_decimal = always_redraw(lambda: DecimalNumber(num_decimal_places=2, color=BLUE_E)
                                      .set_value(theta1_tracker.get_value()).scale(0.4))
        theta1_text = Text("θ1 =", color=BLUE_E).scale(0.4)
        theta1_group = VGroup(theta1_text, theta1_decimal).arrange(RIGHT, buff=0.2).to_corner(UL)
        
        theta2_decimal = always_redraw(lambda: DecimalNumber(num_decimal_places=2, color=BLUE_E)
                                      .set_value(theta2_tracker.get_value()).scale(0.4))
        theta2_text = Text("θ2 =", color=BLUE_E).scale(0.4)
        theta2_group = VGroup(theta2_text, theta2_decimal).arrange(RIGHT, buff=0.2).next_to(theta1_group, DOWN, buff=0.3)
        
        # ACT 1: ESTABLISH
        title = Text("Double Pendulum System", color=BLUE_E).scale(0.5).to_edge(UP)
        self.play(Write(title))
        self.play(Create(anchor), Create(rod1), Create(rod2), 
                  FadeIn(m1), FadeIn(m2), FadeIn(m1_label), FadeIn(m2_label),
                  run_time=2)
        self.play(FadeIn(angle_arc1), FadeIn(angle_arc2), 
                  FadeIn(theta1_label), FadeIn(theta2_label),
                  FadeIn(theta1_group), FadeIn(theta2_group), run_time=2)
        
        # EVOLVE: Start the motion
        self.play(
            theta1_tracker.animate.set_value(0.8), 
            theta2_tracker.animate.set_value(0.5),
            run_time=3
        )
        self.play(
            theta1_tracker.animate.set_value(-0.6), 
            theta2_tracker.animate.set_value(-0.4),
            run_time=3
        )
        
        # REVEAL: Coordinate system and vectors
        # Create coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY_A, "stroke_width": 1},
        ).scale(0.4).shift(pivot*0.4)
        
        # Position vectors
        r1_vector = always_redraw(lambda: Arrow(pivot, get_m1_position(), color=GOLD_E, buff=0, stroke_width=3, max_stroke_width_to_length_ratio=4))
        r2_vector = always_redraw(lambda: Arrow(pivot, get_m2_position(), color=GOLD_E, buff=0, stroke_width=3, max_stroke_width_to_length_ratio=4))
        
        r1_label = always_redraw(lambda: MathTex("\\vec{r}_1", color=GOLD_E).scale(0.35).next_to(r1_vector.get_center(), UP, buff=0.1))
        r2_label = always_redraw(lambda: MathTex("\\vec{r}_2", color=GOLD_E).scale(0.35).next_to(r2_vector.get_center(), UP, buff=0.1))
        
        # Add coordinate system and vectors
        self.play(Create(axes), run_time=1)
        self.play(GrowArrow(r1_vector), GrowArrow(r2_vector), 
                  FadeIn(r1_label), FadeIn(r2_label), run_time=2)
        
        # Highlight the hero moment with accent color
        hero_equation = Tex("\\text{Lagrangian: } \\mathcal{L} = T - V", color=RED_D).scale(0.4).to_edge(DOWN)
        self.play(Write(hero_equation), run_time=2)
        
        # Continue motion for remaining time
        self.play(
            theta1_tracker.animate.set_value(0.5), 
            theta2_tracker.animate.set_value(-0.3),
            run_time=4
        )
        
        # IDLE LOOP: Subtle harmonic wobble
        def idle_wobble(dt):
            t = self.time
            theta1_tracker.set_value(0.5 + 0.1 * np.sin(0.8 * t))
            theta2_tracker.set_value(-0.3 + 0.1 * np.cos(1.2 * t))
        
        self.add_updater(idle_wobble)
        self.wait(3)  # This creates the idle loop effect