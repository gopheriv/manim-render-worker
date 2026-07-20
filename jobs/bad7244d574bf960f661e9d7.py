from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Pendulum with golden arc traces and digital displays
        title = Text("Euler's Number: An Infinite Oscillation", color=GOLD).scale(0.5).to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # Create pendulum
        pivot = Dot(ORIGIN, color=GOLD, radius=0.1)
        length = 2.0
        angle_tracker = ValueTracker(PI / 4)
        
        def get_pendulum_bob():
            bob_pos = [length * np.sin(angle_tracker.get_value()), 
                      -length * np.cos(angle_tracker.get_value()), 0]
            return Dot(bob_pos, color=GOLD, radius=0.2)
        
        def get_string():
            bob_pos = [length * np.sin(angle_tracker.get_value()), 
                      -length * np.cos(angle_tracker.get_value()), 0]
            return Line(ORIGIN, bob_pos, color=GOLD, stroke_width=3)
        
        bob = always_redraw(get_pendulum_bob)
        string = always_redraw(get_string)
        
        self.play(Create(pivot), run_time=0.5)
        self.play(Create(string), Create(bob), run_time=0.5)
        
        # Digital displays
        damping_val = ValueTracker(0.15)
        mass_val = ValueTracker(1.0)
        stiffness_val = ValueTracker(1.0)
        
        damping_label = VGroup(
            Text("damping=", color=GOLD).scale(0.3),
            DecimalNumber(damping_val.get_value(), num_decimal_places=2, color=GOLD).scale(0.3)
        ).arrange(RIGHT, buff=0.1).to_corner(UL)
        
        mass_label = VGroup(
            Text("mass=", color=GOLD).scale(0.3),
            DecimalNumber(mass_val.get_value(), num_decimal_places=1, color=GOLD).scale(0.3)
        ).arrange(RIGHT, buff=0.1).next_to(damping_label, DOWN, buff=0.2)
        
        stiffness_label = VGroup(
            Text("stiffness=", color=GOLD).scale(0.3),
            DecimalNumber(stiffness_val.get_value(), num_decimal_places=1, color=GOLD).scale(0.3)
        ).arrange(RIGHT, buff=0.1).next_to(mass_label, DOWN, buff=0.2)
        
        self.play(
            Write(damping_label),
            Write(mass_label),
            Write(stiffness_label),
            run_time=1.0
        )
        
        # Arc trace
        arc_trace = TracedPath(bob.get_center, dissipate=True, stroke_color=GOLD_A, stroke_width=2)
        self.add(arc_trace)
        
        # Series formula scrolling up
        series_terms = [
            "e = 1/0! + 1/1! + 1/2! + 1/3! + ...",
            "e = 1 + 1 + 1/2 + 1/6 + ...",
            "e = 2 + 0.5 + 0.166... + ...",
            "e = 2.70833...",
            "e ≈ 2.718281828..."
        ]
        
        series_group = VGroup()
        for i, term in enumerate(series_terms):
            text = Text(term, color=GOLD).scale(0.4).shift(DOWN * (i * 0.8))
            series_group.add(text)
        
        series_group.arrange(DOWN, buff=0.5).to_edge(DOWN)
        
        # Animate pendulum swing and series appearance
        self.play(
            angle_tracker.animate.set_value(-PI/4),
            run_time=1.5, rate_func=smooth
        )
        
        self.play(
            LaggedStart(*[Write(text) for text in series_group]),
            run_time=3.0
        )
        
        self.play(
            angle_tracker.animate.set_value(PI/5),
            run_time=1.0, rate_func=smooth
        )
        
        # EVOLVE — More chaotic motion and additional series
        self.play(
            angle_tracker.animate.set_value(-PI/5),
            run_time=1.0, rate_func=there_and_back
        )
        
        # Additional series lines
        additional_series = VGroup(
            Text("e = Σ (1/n!) for n=0 to ∞", color=TEAL).scale(0.35),
            Text("Partial sums: S₀=1, S₁=2, S₂=2.5, S₃≈2.667...", color=GOLD).scale(0.3),
            Text("Convergence: lim(n→∞) Sₙ = e", color=TEAL).scale(0.3)
        ).arrange(DOWN, buff=0.3).next_to(series_group, UP, buff=0.5)
        
        self.play(
            FadeIn(additional_series),
            run_time=2.0
        )
        
        # Pulse the numbers
        self.play(
            damping_label[1].animate.set_color(TEAL),
            mass_label[1].animate.set_color(TEAL),
            stiffness_label[1].animate.set_color(TEAL),
            run_time=0.5
        )
        self.wait(0.3)
        self.play(
            damping_label[1].animate.set_color(GOLD),
            mass_label[1].animate.set_color(GOLD),
            stiffness_label[1].animate.set_color(GOLD),
            run_time=0.5
        )
        
        # Continue pendulum motion
        self.play(
            angle_tracker.animate.set_value(PI/6),
            run_time=1.5, rate_func=smooth
        )
        self.play(
            angle_tracker.animate.set_value(-PI/6),
            run_time=1.5, rate_func=smooth
        )
        
        # REVEAL — Final frame with infinite series
        final_series = MathTex(
            "e = \\sum_{n=0}^{\\infty} \\frac{1}{n!}",
            color=GOLD
        ).scale(1.2).move_to(ORIGIN).shift(UP*1.5)
        
        infinity_dots = VGroup(
            *[Dot(ORIGIN + np.array([i*0.5, 0, 0]), color=GOLD) for i in range(-5, 6)]
        ).arrange(RIGHT, buff=0.3).next_to(final_series, DOWN, buff=0.8)
        
        # Make pendulum continue oscillating
        self.play(
            FadeOut(series_group),
            FadeOut(additional_series),
            Create(final_series),
            Create(infinity_dots),
            run_time=2.0
        )
        
        # Highlight the parameters
        self.play(
            damping_label.animate.set_color(TEAL),
            mass_label.animate.set_color(TEAL),
            stiffness_label.animate.set_color(TEAL),
            run_time=1.0
        )
        
        # Continue pendulum motion for idle loop
        self.play(
            angle_tracker.animate.set_value(PI/8),
            run_time=2.0, rate_func=smooth
        )
        
        # Idle loop: tiny micro-oscillations and scrolling digits
        def idle_loop():
            self.play(
                angle_tracker.animate.increment_value(0.05),
                run_time=0.5, rate_func=smooth
            )
            self.play(
                angle_tracker.animate.increment_value(-0.05),
                run_time=0.5, rate_func=smooth
            )
        
        # Perform several iterations of idle loop
        for _ in range(3):
            idle_loop()
        
        # Keep the series scrolling slowly
        series_mover = always_redraw(lambda: series_group.shift(UP * 0.05 * (self.time % 2)))
        self.add(series_mover)
        
        self.wait(2.0)