from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Ornate gear mechanism with e=p/q assumption
        title = Text("Proof: e is Irrational", color=YELLOW).scale(0.6).to_edge(UP)
        subtitle = Text("Using contradiction with q! multiplication", color=YELLOW).scale(0.4).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle), run_time=1.5)

        # Create ornate gear with teeth instead of plain circle
        def create_gear(radius, num_teeth=12, color=YELLOW):
            gear = VGroup()
            outer_radius = radius
            inner_radius = radius * 0.7
            
            # Main gear body
            main_circle = Circle(radius=inner_radius, color=color, stroke_width=4).set_fill(BLACK, opacity=0.7)
            
            # Teeth
            for i in range(num_teeth):
                angle = 2 * PI * i / num_teeth
                tooth_start = np.array([inner_radius * np.cos(angle), inner_radius * np.sin(angle), 0])
                tooth_end = np.array([outer_radius * np.cos(angle), outer_radius * np.sin(angle), 0])
                
                # Create tooth as a small rectangle rotated appropriately
                tooth = Rectangle(width=0.15, height=(outer_radius-inner_radius)*0.8, 
                                 color=color, fill_color=color, fill_opacity=0.9)
                tooth.move_to(tooth_end)
                tooth.rotate(angle, about_point=tooth.get_center())
                gear.add(tooth)
            
            gear.add(main_circle)
            return gear

        # Large q! gear at center
        q_factorial = 24
        q_gear = create_gear(1.2, 16, YELLOW)
        q_label = MathTex("q!", "=", str(q_factorial), color=YELLOW).scale(1.0).move_to(q_gear.get_center())
        q_group = VGroup(q_gear, q_label).move_to(ORIGIN)

        # e=p/q assumption
        assumption = MathTex("e", "=", "{p \\over q}", color=YELLOW).scale(1.0).to_edge(UP, buff=1.5)

        self.play(Create(q_gear), Write(q_label), Write(assumption), run_time=2.0)

        # P and Q gears on left with proper spacing
        p_gear = create_gear(0.6, 12, YELLOW)
        p_label = MathTex("p", "=", "65", color=YELLOW).scale(0.7).move_to(p_gear.get_center())
        p_group = VGroup(p_gear, p_label).shift(LEFT*3 + UP*1.0)

        q_small_gear = create_gear(0.5, 10, YELLOW)
        q_small_label = MathTex("q", "=", "24", color=YELLOW).scale(0.6).move_to(q_small_gear.get_center())
        q_small_group = VGroup(q_small_gear, q_small_label).shift(LEFT*3 + DOWN*1.0)

        # Connect them with a line to show they're related
        connection_line = Line(p_gear.get_right(), q_small_gear.get_left(), color=YELLOW)

        self.play(Create(p_gear), Write(p_label), Create(q_small_gear), Write(q_small_label), run_time=2.0)
        self.play(Create(connection_line), run_time=1.0)

        # Floating series terms with better spacing
        series_terms = VGroup(
            MathTex("1", color=YELLOW).scale(0.6),
            MathTex("1", color=YELLOW).scale(0.6),
            MathTex("\\frac{1}{2!}", color=YELLOW).scale(0.6),
            MathTex("\\frac{1}{3!}", color=YELLOW).scale(0.6),
            MathTex("\\frac{1}{4!}", color=YELLOW).scale(0.6),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.5)

        self.play(LaggedStart(*[Write(term) for term in series_terms]), run_time=2.0)

        # Camera pull back
        all_elements = VGroup(q_group, p_group, q_small_group, connection_line, series_terms, assumption)
        self.play(all_elements.animate.scale(0.8), run_time=1.0)

        # EVOLVE — Gear accelerates, split into finite/infinite parts
        self.wait(1.0)

        # Animate the gear rotating faster
        self.play(Rotate(q_gear, angle=PI*6, about_point=q_gear.get_center()), run_time=3.0, rate_func=linear)

        # Split series into two groups with better layout
        finite_sum = MathTex("q! \\cdot \\left(1 + 1 + \\frac{1}{2!} + \\cdots + \\frac{1}{q!}\\right)", color=GREEN).scale(0.7).to_edge(UP, buff=2.0)
        infinite_tail = MathTex("q! \\cdot \\left(\\frac{1}{(q+1)!} + \\frac{1}{(q+2)!} + \\cdots \\right)", color=RED).scale(0.7).to_edge(DOWN, buff=2.0)

        self.play(
            FadeOut(series_terms),
            Write(finite_sum),
            Write(infinite_tail),
            run_time=2.0
        )

        # Highlight integer part with cleaner box
        int_part = SurroundingRectangle(finite_sum, color=GREEN, buff=0.1)
        self.play(Create(int_part), run_time=1.0)

        # Wobbling fractional parts
        frac_part = SurroundingRectangle(infinite_tail, color=RED, buff=0.1)
        self.play(Create(frac_part), run_time=1.0)

        # Add wobbling effect to fractional part
        def wobble(mob, dt):
            mob.rotate(np.sin(self.time * 2) * 0.02)
        
        frac_part.add_updater(wobble)

        # REVEAL — Contradiction appears
        self.wait(1.0)

        # Jam the gears with more dramatic effect
        def jam(mob, dt):
            mob.rotate(np.sin(self.time * 15) * 0.05)
        
        q_gear.add_updater(jam)
        p_gear.add_updater(jam)
        q_small_gear.add_updater(jam)

        # Red X over assumption
        contradiction_x = Cross(assumption, stroke_color=RED, stroke_width=8)
        contradiction_text = Text("CONTRADICTION!", color=RED).scale(0.8).next_to(contradiction_x, DOWN, buff=0.3)

        self.play(
            Create(contradiction_x),
            Write(contradiction_text),
            run_time=2.0
        )

        # Final statement with better composition
        final_statement = MathTex("e \\neq {p \\over q}", color=RED).scale(1.5).move_to(ORIGIN)
        
        # Fade out everything except the main gears which continue to jam
        self.play(
            FadeOut(finite_sum),
            FadeOut(infinite_tail),
            FadeOut(int_part),
            FadeOut(frac_part),
            FadeOut(assumption),
            FadeOut(contradiction_x),
            FadeOut(contradiction_text),
            FadeOut(title),
            FadeOut(subtitle),
            Write(final_statement),
            run_time=2.0
        )

        # IDLE LOOP - Continue jamming and wobbling effects
        def twitch(mob):
            mob.shift(0.01 * np.sin(self.time * 3) * RIGHT + 0.01 * np.cos(self.time * 3) * UP)
        
        final_statement.add_updater(twitch)
        self.wait(3.0)  # This creates the idle loop effect
        
        # Remove updaters at the end
        q_gear.remove_updater(jam)
        p_gear.remove_updater(jam)
        q_small_gear.remove_updater(jam)
        frac_part.remove_updater(wobble)
        final_statement.remove_updater(twitch)