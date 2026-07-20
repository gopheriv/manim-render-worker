from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # Initialize variables
        damping = 0.15
        mass = 1.0
        stiffness = 1.0
        
        # Create ValueTrackers for dynamic display
        damping_tracker = ValueTracker(damping)
        
        # ESTABLISH - Spring begins gentle oscillation with mass 1.0 weight bob
        title = Text("Proof that e is irrational", color=BLUE).scale(0.6).to_edge(UP)
        self.play(Write(title), run_time=1.0)
        
        # Create spring and mass
        spring_origin = UP * 2
        mass_obj = Circle(radius=0.3, color=GOLD, fill_opacity=1).shift(spring_origin + DOWN * 1.5)
        spring_line = always_redraw(lambda: Line(
            start=spring_origin,
            end=mass_obj.get_top(),
            color=BLUE,
            stroke_width=3
        ))
        
        self.play(Create(spring_line), Create(mass_obj), run_time=1.0)
        
        # Mathematical terms appearing below like building blocks
        terms_group = VGroup()
        for i in range(5):
            term = Rectangle(width=1.2, height=0.6, color=GOLD, fill_opacity=0.3)
            term.shift((i - 2) * RIGHT * 1.3)
            terms_group.add(term)
        
        terms_group.arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=1.0)
        self.play(LaggedStart(*[Create(term) for term in terms_group], lag_ratio=0.3), run_time=2.0)
        
        # First q+1 terms materialize as golden blocks forming a solid foundation
        q_plus_1_label = MathTex("q+1", color=GOLD).scale(0.8).next_to(terms_group, UP, buff=0.2)
        self.play(Write(q_plus_1_label), run_time=1.0)
        
        # Add checkmarks to verify terms
        checks = VGroup()
        for term in terms_group:
            check = MathTex("\\checkmark", color=GREEN).scale(0.6).move_to(term)
            checks.add(check)
        
        self.play(LaggedStart(*[Write(check) for check in checks], lag_ratio=0.2), run_time=1.5)
        
        # Damping factor 0.15 pulses on screen
        damping_text = always_redraw(lambda: 
            Text(f"Damping: {damping_tracker.get_value():.2f}", color=BLUE).scale(0.4).to_corner(UR)
        )
        self.play(FadeIn(damping_text), run_time=0.5)
        
        # Animate spring oscillation
        def oscillate(mob, dt):
            current_y = mob.get_center()[1]
            target_y = spring_origin[1] - 1.5 + 0.3 * np.sin(2 * np.pi * 0.8 * self.time)
            mob.shift((target_y - current_y) * UP)
        
        mass_obj.add_updater(oscillate)
        self.wait(2.0)
        mass_obj.remove_updater(oscillate)
        
        # Integer N label emerges glowing gold above the foundation blocks
        N_label = MathTex("N", color=GOLD).scale(1.2).next_to(q_plus_1_label, UP, buff=0.3)
        self.play(Write(N_label), run_time=1.0)
        
        # EVOLVE - Spring oscillates faster as 'n ≤ q' condition activates
        n_leq_q = MathTex("n \\leq q", color=BLUE).scale(0.8).next_to(N_label, LEFT, buff=0.5)
        self.play(Write(n_leq_q), run_time=1.0)
        
        # Highlight relevant terms
        self.play(
            *[term.animate.set_fill(opacity=0.7) for term in terms_group[:3]],
            run_time=1.0
        )
        
        # Each term transforms into integer representation
        integer_terms = VGroup()
        for i in range(3):
            int_term = MathTex(str(i+1), color=GOLD).scale(0.8).move_to(terms_group[i])
            integer_terms.add(int_term)
        
        self.play(TransformMatchingShapes(terms_group[:3], integer_terms), run_time=1.5)
        
        # Arithmetic verification symbols
        verif_symbols = VGroup()
        for term in integer_terms:
            symbol = MathTex("\\in \\mathbb{Z}", color=GREEN).scale(0.5).next_to(term, UP, buff=0.1)
            verif_symbols.add(symbol)
        
        self.play(LaggedStart(*[Write(sym) for sym in verif_symbols], lag_ratio=0.2), run_time=1.0)
        
        # Terms sync their pulsing rhythm with spring oscillations
        def pulse(mob, dt):
            scale_factor = 1 + 0.05 * np.sin(2 * np.pi * 1.2 * self.time)
            mob.scale_to_fit_width(scale_factor * mob.width)
        
        for term in integer_terms:
            term.add_updater(pulse)
        
        # Stiffness adjustment demonstration
        stiffness_text = Text("Stiffness: 1.0", color=BLUE).scale(0.4).next_to(damping_text, DOWN, buff=0.2)
        self.play(FadeIn(stiffness_text), run_time=0.5)
        
        # Faster oscillation
        def fast_oscillate(mob, dt):
            current_y = mob.get_center()[1]
            target_y = spring_origin[1] - 1.5 + 0.2 * np.sin(2 * np.pi * 1.5 * self.time)
            mob.shift((target_y - current_y) * UP)
        
        mass_obj.add_updater(fast_oscillate)
        self.wait(3.0)
        mass_obj.remove_updater(fast_oscillate)
        
        # Remove pulsing updaters
        for term in integer_terms:
            term.remove_updater(pulse)
        
        # REVEAL - All verified integers converge into single glowing N block
        # Group all integer terms and move them toward N
        all_integers = VGroup(*integer_terms, *verif_symbols)
        
        self.play(
            all_integers.animate.arrange(DOWN, buff=0.1).move_to(ORIGIN + DOWN*0.5),
            run_time=2.0
        )
        
        # Spring settles to rest
        mass_obj.clear_updaters()
        self.play(mass_obj.animate.shift(UP*0.1), run_time=1.0)
        
        # Convergence to single N block
        final_N = MathTex("N", color=GOLD).scale(1.8).move_to(ORIGIN)
        self.play(Transform(all_integers, final_N), run_time=1.5)
        
        # Contradiction becomes apparent
        contradiction = Text("Contradiction!", color=RED).scale(0.6).to_edge(DOWN)
        self.play(Write(contradiction), run_time=1.0)
        
        # Final proof structure crystallizes
        proof_structure = SurroundingRectangle(final_N, color=GOLD, buff=0.2)
        self.play(Create(proof_structure), run_time=1.0)
        
        # Hero frame: Spring still, foundation glowing, N floating, damping pulsing
        self.wait(1.0)
        
        # IDLE LOOP - Subtle harmonic tremor in the spring with gentle pulsing of integer blocks
        def subtle_oscillate(mob, dt):
            current_y = mob.get_center()[1]
            target_y = spring_origin[1] - 1.4 + 0.05 * np.sin(2 * np.pi * 0.3 * self.time)
            mob.shift((target_y - current_y) * UP)
        
        def subtle_pulse(mob, dt):
            scale_factor = 1 + 0.02 * np.sin(2 * np.pi * 0.4 * self.time)
            mob.scale(scale_factor)
        
        mass_obj.add_updater(subtle_oscillate)
        final_N.add_updater(subtle_pulse)
        
        # Continue pulsing damping text
        def pulse_damping_text(mob, dt):
            alpha = 0.5 + 0.3 * np.sin(2 * np.pi * 0.6 * self.time)
            mob.set_opacity(alpha)
        
        damping_text.add_updater(pulse_damping_text)
        
        self.wait(5.0)  # This ensures the idle loop runs with visible changes