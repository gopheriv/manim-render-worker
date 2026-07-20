from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Golden pendulum begins steady swing at natural frequency
        title = Text("Is e Rational? Pendulum Reveals the Truth", color=GOLD_E).scale(0.5).to_edge(UP)
        subtitle = Text("e = p/q?", color=BLUE_E).scale(0.4)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.6)

        # Create pendulum setup
        pivot = np.array([0, 2, 0])
        length = 2.0
        angle_tracker = ValueTracker(0)
        
        def get_pendulum():
            theta = angle_tracker.get_value()
            bob_pos = pivot + length * np.array([np.sin(theta), -np.cos(theta), 0])
            string = Line(pivot, bob_pos, color=GOLD_E, stroke_width=3)
            bob = Circle(radius=0.15, fill_color=GOLD_E, fill_opacity=1, stroke_color=GOLD_E).move_to(bob_pos)
            return VGroup(string, bob)
        
        pendulum = always_redraw(get_pendulum)
        self.play(Create(pendulum), run_time=1.0)

        # Digital display showing initial values
        mass_val = ValueTracker(1.0)
        damping_val = ValueTracker(0.15)
        stiffness_val = ValueTracker(1.0)
        
        mass_label = VGroup(
            Text("mass (p): ", color=WHITE),
            DecimalNumber(mass_val.get_value(), num_decimal_places=2, color=WHITE)
        ).arrange(RIGHT).scale(0.4).to_corner(UL)
        
        damping_label = VGroup(
            Text("damping (q): ", color=WHITE),
            DecimalNumber(damping_val.get_value(), num_decimal_places=2, color=WHITE)
        ).arrange(RIGHT).scale(0.4).next_to(mass_label, DOWN, buff=0.3)
        
        target_label = Text("Target: e ≈ 2.71828...", color=BLUE_E).scale(0.35).next_to(damping_label, DOWN, buff=0.3)
        
        mass_num = mass_label[1]
        damping_num = damping_label[1]
        
        mass_num.add_updater(lambda d: d.set_value(mass_val.get_value()))
        damping_num.add_updater(lambda d: d.set_value(damping_val.get_value()))
        
        self.play(
            FadeIn(mass_label),
            FadeIn(damping_label),
            FadeIn(target_label)
        )

        # Pendulum trace drawing
        trace_true = TracedPath(lambda: pendulum[1].get_center(), dissipating_time=5, stroke_color=GOLD_E, stroke_width=2)
        self.add(trace_true)
        
        # Animate pendulum swing
        self.play(angle_tracker.animate.set_value(-0.8), run_time=2.0, rate_func=smooth)
        self.play(angle_tracker.animate.set_value(0.8), run_time=2.0, rate_func=smooth)
        self.play(angle_tracker.animate.set_value(-0.4), run_time=1.5, rate_func=smooth)
        
        # EVOLVE — Rational approximation tries to lock onto pendulum frequency
        contradiction_text = Text("Rational Approximation Attempt", color=RED_E).scale(0.35).to_edge(DOWN)
        self.play(Write(contradiction_text), run_time=1.0)
        
        # Show error function growing
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[-1, 1, 0.5],
            axis_config={"color": BLUE_E, "stroke_opacity": 0.3}
        ).scale(0.4).to_corner(DR)
        
        error_graph = always_redraw(lambda: axes.plot(
            lambda x: 0.5 * np.sin(2*x) * np.exp(0.2*x), 
            color=RED_E, 
            stroke_width=2
        ))
        
        error_label = Text("Error Growth", color=RED_E).scale(0.25).next_to(axes, UP, buff=0.2)
        
        self.play(
            Create(axes),
            Create(error_graph),
            Write(error_label)
        )
        
        # Continue pendulum motion while showing drift
        self.play(
            angle_tracker.animate.set_value(0.6),
            run_time=3.0,
            rate_func=linear
        )
        
        # REVEAL — Contradiction emerges
        contradiction_flash = Text("CONTRADICTION!", color=RED_E).scale(0.8).move_to(ORIGIN)
        contradiction_flash.shift(IN)
        self.play(
            FadeOut(contradiction_text),
            Create(contradiction_flash),
            run_time=0.5
        )
        
        # Show waveform transformation
        waveform_axes = Axes(
            x_range=[0, 4*np.pi, np.pi],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE_E, "stroke_opacity": 0.3}
        ).scale(0.5).center()
        
        true_wave = waveform_axes.plot(lambda x: np.sin(x), color=GOLD_E, stroke_width=4)
        rational_wave = waveform_axes.plot(lambda x: 0.8*np.sin(1.1*x), color=RED_E, stroke_width=2, stroke_dash_pattern="-.--")
        
        self.play(
            FadeOut(contradiction_flash),
            Create(waveform_axes),
            Create(true_wave),
            Create(rational_wave),
            run_time=2.0
        )
        
        # Labels for waves
        true_label = Text("True e Wave", color=GOLD_E).scale(0.3).next_to(true_wave, UP, buff=0.5)
        rational_label = Text("Rational p/q Wave", color=RED_E).scale(0.3).next_to(rational_wave, DOWN, buff=0.5)
        
        self.play(
            Write(true_label),
            Write(rational_label)
        )
        
        # Final animation showing divergence
        self.play(
            angle_tracker.animate.set_value(-0.7),
            run_time=3.0,
            rate_func=linear
        )
        
        # IDLE LOOP — Golden pendulum continues eternal swing
        self.remove(trace_true)  # Remove old trace
        trace_true = TracedPath(lambda: pendulum[1].get_center(), dissipating_time=8, stroke_color=GOLD_E, stroke_width=2)
        self.add(trace_true)
        
        # Fade out rational wave to emphasize gap
        self.play(
            rational_wave.animate.set_stroke(opacity=0.2),
            run_time=2.0
        )
        
        # Continue pendulum motion indefinitely
        self.play(
            angle_tracker.animate.set_value(0.7),
            run_time=6.0,
            rate_func=linear
        )