from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Camera pulls back to reveal pristine lab environment
        title = Text("Double Pendulum Lagrangian", color=GOLD_E).scale(0.5).to_edge(UP)
        self.play(Write(title), run_time=0.9)

        # Setup parameters
        gravity = 9.81
        length = 1.0
        pivot = np.array([-2.0, 1.0, 0.0])
        
        # Create ValueTrackers for live displays
        gravity_tracker = ValueTracker(gravity)
        length_tracker = ValueTracker(length)
        
        # Create digital readouts
        gravity_label = always_redraw(
            lambda: Text(f"g = {gravity_tracker.get_value():.2f}", color=GOLD_E)
            .scale(0.3).to_corner(UL)
        )
        length_label = always_redraw(
            lambda: Text(f"l = {length_tracker.get_value():.2f}", color=GOLD_E)
            .scale(0.3).next_to(gravity_label, DOWN, buff=0.2)
        )
        
        self.play(FadeIn(gravity_label), FadeIn(length_label))

        # Two crystal orbs materialize with soft chimes
        theta1 = ValueTracker(PI/3)
        theta2 = ValueTracker(PI/4)
        
        def get_pos1():
            return pivot + length * np.array([
                np.sin(theta1.get_value()),
                -np.cos(theta1.get_value()),
                0.0
            ])
        
        def get_pos2():
            pos1 = get_pos1()
            return pos1 + length * np.array([
                np.sin(theta1.get_value() + theta2.get_value()),
                -np.cos(theta1.get_value() + theta2.get_value()),
                0.0
            ])

        anchor = Dot(pivot, color=WHITE, radius=0.05)
        mass1 = always_redraw(lambda: Dot(get_pos1(), color=GOLD_E, radius=0.15))
        mass2 = always_redraw(lambda: Dot(get_pos2(), color=GOLD_E, radius=0.15))
        
        rod1 = always_redraw(lambda: Line(pivot, get_pos1(), color=BLUE_C, stroke_width=3))
        rod2 = always_redraw(lambda: Line(get_pos1(), get_pos2(), color=BLUE_C, stroke_width=3))
        
        self.play(
            Create(anchor),
            Create(rod1),
            Create(rod2),
            FadeIn(mass1),
            FadeIn(mass2),
            run_time=1.5
        )

        # Grid for coordinate system
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 2, 1],
            axis_config={"stroke_color": BLUE_C},
            background_line_style={"stroke_color": BLUE_C, "stroke_opacity": 0.3}
        ).scale(0.5)
        grid.shift(IN * 0.1)  # Slightly behind other objects
        self.play(Create(grid), run_time=1.0)

        # EVOLVE — First orb traces potential energy field lines in blue
        trace1 = TracedPath(mass1.get_center, dissipating_time=1.5, stroke_color=BLUE_C, stroke_width=2)
        trace2 = TracedPath(mass2.get_center, dissipating_time=1.5, stroke_color=GREEN, stroke_width=2)
        
        self.add(trace1, trace2)
        
        # Combined potential energy formula emerges
        v_formula = MathTex("V = m_1 g l (1 - \\cos\\theta_1) + m_2 g l [2(1 - \\cos\\theta_1) + (1 - \\cos(\\theta_1 + \\theta_2))]", 
                           color=BLUE_C).scale(0.35).to_edge(DOWN)
        self.play(Write(v_formula), run_time=2.0)

        # REVEAL — Lagrangian L=T-V appears as golden equation
        lagrangian = MathTex("L = T - V", color=GOLD_E).scale(0.5).next_to(v_formula, UP, buff=0.2)
        self.play(FadeIn(lagrangian), run_time=1.5)

        # Euler-Lagrange equations cascade down
        el_eq1 = MathTex("\\frac{d}{dt}\\left(\\frac{\\partial L}{\\partial \\dot{\\theta}_1}\\right) - \\frac{\\partial L}{\\partial \\theta_1} = 0", 
                         color=GREEN).scale(0.35).next_to(lagrangian, DOWN, buff=0.2)
        el_eq2 = MathTex("\\frac{d}{dt}\\left(\\frac{\\partial L}{\\partial \\dot{\\theta}_2}\\right) - \\frac{\\partial L}{\\partial \\theta_2} = 0", 
                         color=GREEN).scale(0.35).next_to(el_eq1, DOWN, buff=0.2)
        
        self.play(Write(el_eq1), Write(el_eq2), run_time=2.0)

        # Animate the pendulum motion to show coupled dynamics
        self.play(
            theta1.animate(rate_func=there_and_back).set_value(PI/2),
            theta2.animate(rate_func=there_and_back).set_value(PI/6),
            run_time=4.0
        )

        # Hero frame: Dramatic asymmetric position with intense glow
        self.play(
            theta1.animate.set_value(2*PI/3),
            theta2.animate.set_value(PI/5),
            run_time=2.0
        )
        
        # Make masses glow more intensely
        intense_mass1 = always_redraw(lambda: Dot(get_pos1(), color=YELLOW, radius=0.18))
        intense_mass2 = always_redraw(lambda: Dot(get_pos2(), color=YELLOW, radius=0.18))
        
        self.play(
            Transform(mass1, intense_mass1),
            Transform(mass2, intense_mass2),
            lagrangian.animate.set_color(GREEN),
            run_time=1.0
        )

        # Add swirling field lines around masses
        field_lines1 = VGroup(*[
            Circle(radius=r, color=BLUE_C, stroke_opacity=0.4).move_to(get_pos1())
            for r in np.linspace(0.2, 0.6, 4)
        ])
        field_lines2 = VGroup(*[
            Circle(radius=r, color=GREEN, stroke_opacity=0.4).move_to(get_pos2())
            for r in np.linspace(0.2, 0.6, 4)
        ])
        
        field_lines1 = always_redraw(lambda: VGroup(*[
            Circle(radius=r, color=BLUE_C, stroke_opacity=0.4).move_to(get_pos1())
            for r in np.linspace(0.2, 0.6, 4)
        ]))
        field_lines2 = always_redraw(lambda: VGroup(*[
            Circle(radius=r, color=GREEN, stroke_opacity=0.4).move_to(get_pos2())
            for r in np.linspace(0.2, 0.6, 4)
        ]))
        
        self.play(Create(field_lines1), Create(field_lines2), run_time=1.0)

        # Golden threads connecting masses to Lagrangian
        thread1 = always_redraw(lambda: DashedLine(get_pos1(), lagrangian.get_bottom(), color=GOLD_E, stroke_width=2))
        thread2 = always_redraw(lambda: DashedLine(get_pos2(), lagrangian.get_bottom(), color=GOLD_E, stroke_width=2))
        
        self.add(thread1, thread2)

        # Idle loop: Subtle harmonic oscillation
        def idle_loop():
            t = self.time
            theta1.set_value(2*PI/3 + 0.1*np.sin(0.5*t))
            theta2.set_value(PI/5 + 0.1*np.cos(0.7*t))
            
        self.add_updater(idle_loop)
        self.wait(5.0)  # This maintains the motion for the idle loop