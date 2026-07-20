from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Pendulum swings with clean periodic motion, showing parameters
        title = Text("The Irrationality of e", color=BLUE_E).scale(0.6).to_edge(UP)
        subtitle = Text("A pendulum reveals infinite complexity", color=GOLD_E).scale(0.4)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(Write(title), Write(subtitle), run_time=1.5)

        # Create pendulum setup
        pivot = Dot(ORIGIN, color=WHITE)
        rod_length = 2.0
        bob_radius = 0.2
        pendulum_bob = Circle(radius=bob_radius, fill_color=BLUE_E, fill_opacity=0.8, stroke_color=WHITE)
        pendulum_bob.move_to(rod_length * DOWN)
        
        rod = Line(ORIGIN, pendulum_bob.get_center(), color=WHITE, stroke_width=2)
        
        # Group pendulum components
        pendulum = VGroup(pivot, rod, pendulum_bob)
        pendulum.shift(UP*0.5)
        
        self.play(Create(pendulum), run_time=1.0)
        
        # Digital displays for parameters
        param_box = Rectangle(height=1.5, width=3.5, color=WHITE, stroke_width=2)
        param_box.to_corner(UL, buff=0.5)
        
        mass_label = Text(f"mass = {1.0}", color=GOLD_E).scale(0.35)
        stiffness_label = Text(f"stiffness = {1.0}", color=GOLD_E).scale(0.35)
        damping_label = Text(f"damping = {0.15}", color=GOLD_E).scale(0.35)
        
        params_vgroup = VGroup(mass_label, stiffness_label, damping_label)
        params_vgroup.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        params_vgroup.move_to(param_box.get_center())
        
        param_group = VGroup(param_box, params_vgroup)
        self.play(Create(param_group), run_time=1.0)
        
        # Show decimal expansion of e and rational approximations
        e_expansion = Text("e = 2.718281828...", color=BLUE_E).scale(0.4)
        e_expansion.to_corner(UR, buff=0.5)
        
        rational_approxs = VGroup(
            Text("Rational approximations:", color=GOLD_E).scale(0.35),
            Text("3/1 = 3.0", color=GOLD_E).scale(0.3),
            Text("22/7 ≈ 3.14", color=GOLD_E).scale(0.3),
            Text("19/7 ≈ 2.71", color=GOLD_E).scale(0.3)
        )
        rational_approxs.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        rational_approxs.next_to(e_expansion, DOWN, aligned_edge=RIGHT, buff=0.5)
        
        self.play(Write(e_expansion), run_time=1.0)
        self.play(Write(rational_approxs), run_time=2.0)
        
        # Animate pendulum swing
        t = ValueTracker(0)
        def update_pendulum(pend):
            angle = 0.3 * math.sin(t.get_value() * 2)
            new_end = rod_length * (math.sin(angle) * RIGHT + math.cos(angle) * DOWN)
            pend[1].put_start_and_end_on(ORIGIN, new_end)
            pend[2].move_to(new_end)
        
        pendulum.add_updater(update_pendulum)
        self.play(t.animate.set_value(6.0), run_time=3.0, rate_func=linear)
        pendulum.remove_updater(update_pendulum)
        
        # EVOLVE — Pendulum motion complexifies, more approximations appear
        self.wait(0.5)
        
        # More complex rational approximations
        more_approxs = VGroup(
            Text("More precise approximations:", color=GOLD_E).scale(0.35),
            Text("87/32 ≈ 2.71875", color=GOLD_E).scale(0.3),
            Text("106/39 ≈ 2.71794", color=GOLD_E).scale(0.3),
            Text("497/184 ≈ 2.70108", color=GOLD_E).scale(0.3)
        )
        more_approxs.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        more_approxs.next_to(rational_approxs, DOWN, aligned_edge=LEFT, buff=0.3)
        
        self.play(Write(more_approxs), run_time=2.0)
        
        # Continue pendulum motion with more complex behavior
        pendulum.add_updater(update_pendulum)
        self.play(t.animate.set_value(12.0), run_time=5.0, rate_func=linear)
        pendulum.remove_updater(update_pendulum)
        
        # REVEAL — Exponential decay curve and proof setup
        self.wait(0.5)
        
        # Draw exponential decay curve
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.2, 0.5],
            axis_config={"color": BLUE_E, "stroke_width": 1},
            tips=False
        ).scale(0.8).shift(LEFT*2)
        
        decay_curve = axes.plot(lambda x: math.exp(-0.15*x), color=GOLD_E, stroke_width=3)
        
        self.play(Create(axes), run_time=1.0)
        self.play(Create(decay_curve), run_time=2.0)
        
        # Proof setup - positioned clearly below the pendulum
        proof_title = Text("Proof by Contradiction", color=RED_C).scale(0.5)
        proof_title.to_edge(UP)
        
        assumption = MathTex("\\text{Assume } e = \\frac{p}{q} \\text{ where } p, q \\in \\mathbb{Z}", color=RED_C).scale(0.6)
        assumption.next_to(proof_title, DOWN, buff=0.5)
        
        contradiction = MathTex("\\Rightarrow \\text{Impossible integer result}", color=RED_C).scale(0.6)
        contradiction.next_to(assumption, DOWN, buff=0.5)
        
        # Transform title and add proof elements in clear positions
        self.play(FadeOut(title), FadeOut(subtitle), Write(proof_title))
        self.play(Write(assumption), run_time=1.5)
        self.play(Write(contradiction), run_time=1.5)
        
        # Infinite series representation - positioned at bottom center
        series = MathTex("e = \\sum_{n=0}^{\\infty} \\frac{1}{n!} = 1 + 1 + \\frac{1}{2} + \\frac{1}{6} + \\frac{1}{24} + \\cdots", color=GOLD_E).scale(0.5)
        series.to_edge(DOWN)
        
        self.play(Write(series), run_time=2.0)
        
        # Final crystallized state - pendulum continues oscillating, but equations stay fixed
        pendulum.add_updater(update_pendulum)
        
        # Keep all elements stationary in final frame
        self.play(
            t.animate.set_value(18.0),
            run_time=6.0,
            rate_func=linear
        )
        
        # Clean up updaters
        pendulum.remove_updater(update_pendulum)