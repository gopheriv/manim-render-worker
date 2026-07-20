from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Red dominoes cascade up to position q! with golden number displays
        title = Text("Proof: e is Irrational", color=WHITE).scale(0.6).to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # Create dominoes
        red_dominoes = VGroup()
        blue_dominoes = VGroup()
        
        num_red = 6  # q! = 6 for demonstration
        for i in range(num_red):
            domino = Rectangle(height=0.8, width=0.4, fill_color=RED, fill_opacity=0.8, stroke_color=RED_A)
            domino.move_to(LEFT*4 + RIGHT*i*0.6)
            red_dominoes.add(domino)
        
        for i in range(6):
            domino = Rectangle(height=0.8, width=0.4, fill_color=BLUE_E, fill_opacity=0.8, stroke_color=BLUE_A)
            domino.move_to(LEFT*4 + RIGHT*(num_red*0.6 + i*0.6))
            blue_dominoes.add(domino)
        
        # Add more blue dominoes to show infinity
        for i in range(6, 12):
            domino = Rectangle(height=0.8, width=0.4, fill_color=BLUE_E, fill_opacity=0.6, stroke_color=BLUE_A)
            domino.move_to(LEFT*4 + RIGHT*(num_red*0.6 + i*0.6))
            blue_dominoes.add(domino)
        
        # Position them
        red_dominoes.arrange(RIGHT, buff=0.2).shift(LEFT*2)
        blue_dominoes.arrange(RIGHT, buff=0.2).next_to(red_dominoes, RIGHT, buff=0.2)
        
        # Create boundary line at q!
        boundary_line = Line(start=UP*2, end=DOWN*2, color=GOLD_E, stroke_width=6)
        boundary_line.next_to(red_dominoes, RIGHT, buff=0.05)
        
        # Create variable displays
        q_tracker = ValueTracker(6)
        p_tracker = ValueTracker(142)
        e_tracker = ValueTracker(2.71828)
        
        q_fact_label = always_redraw(lambda: DecimalNumber(q_tracker.get_value(), color=GOLD_E).scale(0.4).next_to(boundary_line, UP, buff=0.2))
        pq_label = always_redraw(lambda: MathTex(f"\\frac{{{int(p_tracker.get_value())}}}{{{int(q_tracker.get_value())}}}", color=GOLD_E).scale(0.5).next_to(boundary_line, DOWN, buff=0.2))
        e_label = always_redraw(lambda: MathTex("e", color=WHITE).scale(0.6).next_to(pq_label, LEFT, buff=0.5))
        eq_sign = always_redraw(lambda: MathTex("=", color=WHITE).scale(0.6).next_to(e_label, RIGHT, buff=0.2))
        
        # Animate red dominoes falling
        self.play(LaggedStart(*[Create(domino) for domino in red_dominoes], lag_ratio=0.2), run_time=2.0)
        self.play(FadeIn(q_fact_label), FadeIn(pq_label), Write(e_label), Write(eq_sign), run_time=1.0)
        
        # Animate blue dominoes appearing
        self.play(LaggedStart(*[Create(domino) for domino in blue_dominoes[:6]], lag_ratio=0.2), run_time=2.0)
        self.play(Create(boundary_line), run_time=1.0)
        
        # Pull back to reveal full setup
        self.play(self.camera.frame.animate.scale(1.3), run_time=1.0)

        # EVOLVE — Red dominoes multiply to form integers, blue continue with fractional remainders
        # Highlight the finite sum becoming integer
        finite_sum_label = MathTex("\\text{Integer Part}", color=RED).scale(0.5).next_to(red_dominoes, UP, buff=0.5)
        self.play(Write(finite_sum_label), run_time=1.0)
        
        # Animate blue dominoes continuing to fall
        for i in range(len(blue_dominoes)):
            self.play(blue_dominoes[i].animate.shift(DOWN*0.1), run_time=0.2)
        
        # Show infinite tail creating fractional remainders
        infinite_tail_label = MathTex("\\text{Fractional Remainder}", color=BLUE_E).scale(0.5).next_to(blue_dominoes, UP, buff=0.5)
        self.play(Write(infinite_tail_label), run_time=1.0)
        
        # Make boundary glow
        glow_line = boundary_line.copy().set_stroke(width=10).set_color(YELLOW)
        self.play(Create(glow_line), run_time=0.5)
        self.play(FadeOut(glow_line), run_time=0.5)

        # REVEAL — The contradiction becomes visible
        contradiction_text = Text("CONTRADICTION!", color=RED).scale(0.7).move_to(UP*2)
        self.play(Write(contradiction_text), run_time=1.0)
        
        # Show equation: Integer = Fraction < 1
        int_frac_eq = MathTex("\\text{Integer} = \\text{Fraction} < 1", color=WHITE).scale(0.6).move_to(ORIGIN)
        self.play(TransformFromCopy(finite_sum_label, int_frac_eq[0][:7]), run_time=1.0)
        self.play(Write(int_frac_eq[7:8]), run_time=0.5)  # equals sign
        self.play(TransformFromCopy(infinite_tail_label, int_frac_eq[8:15]), run_time=1.0)
        self.play(Write(int_frac_eq[15:18]), run_time=0.5)  # "< 1"
        
        # Illuminate the structure
        all_dominoes = VGroup(red_dominoes, blue_dominoes, boundary_line)
        self.play(all_dominoes.animate.set_stroke(WHITE, width=3), run_time=0.5)
        self.play(all_dominoes.animate.set_stroke(GRAY, width=1), run_time=0.5)

        # IDLE LOOP — One blue domino wobbles at the boundary
        wobble_domino = blue_dominoes[0].copy()
        self.add(wobble_domino)
        
        def wobble_updater(mob):
            angle = 0.05 * np.sin(self.time * 2)
            mob.rotate(angle).set_color(PURE_CYAN)
        
        wobble_domino.add_updater(wobble_updater)
        self.wait(3.0)  # This maintains the motion for the final frames