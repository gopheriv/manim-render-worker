from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Ornate gear mechanism with e=p/q assumption
        title = Text("Proof: e is Irrational", color=GOLD_E).scale(0.6).to_edge(UP)
        subtitle = Text("Using contradiction with q! multiplication", color=GOLD_E).scale(0.4).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle), run_time=1.5)

        # Large q! gear at center
        q_factorial = 24
        q_gear = Circle(radius=1.2, color=GOLD_E, stroke_width=8).set_fill(DARK_BLUE, opacity=0.7)
        q_label = MathTex("q!", "=", str(q_factorial), color=GOLD_E).scale(1.2).move_to(q_gear.get_center())
        q_group = VGroup(q_gear, q_label).move_to(ORIGIN)

        # e=p/q assumption
        assumption = MathTex("e", "=", "{p \\over q}", color=GOLD_E).scale(1.0).to_edge(UP, buff=1.5)

        self.play(Create(q_gear), Write(q_label), Write(assumption), run_time=2.0)

        # P and Q gears on left
        p_gear = Circle(radius=0.6, color=GOLD_E, stroke_width=6).set_fill(BLUE, opacity=0.6)
        p_label = MathTex("p", "=", "65", color=GOLD_E).scale(0.8).move_to(p_gear.get_center())
        p_group = VGroup(p_gear, p_label).shift(LEFT*3 + UP*0.5)

        q_small_gear = Circle(radius=0.5, color=GOLD_E, stroke_width=6).set_fill(BLUE, opacity=0.6)
        q_small_label = MathTex("q", "=", "24", color=GOLD_E).scale(0.8).move_to(q_small_gear.get_center())
        q_small_group = VGroup(q_small_gear, q_small_label).shift(LEFT*3 + DOWN*0.5)

        # Connect them with a line to show they're related
        connection_line = Line(p_gear.get_right(), q_small_gear.get_left(), color=GOLD_E)

        self.play(Create(p_gear), Write(p_label), Create(q_small_gear), Write(q_small_label), run_time=2.0)
        self.play(Create(connection_line), run_time=1.0)

        # Floating series terms
        series_terms = VGroup(
            MathTex("1", color=GOLD_E).scale(0.5),
            MathTex("1", color=GOLD_E).scale(0.5),
            MathTex("\\frac{1}{2!}", color=GOLD_E).scale(0.5),
            MathTex("\\frac{1}{3!}", color=GOLD_E).scale(0.5),
            MathTex("\\frac{1}{4!}", color=GOLD_E).scale(0.5),
        ).arrange(RIGHT, buff=0.5).to_edge(DOWN)

        self.play(LaggedStart(*[Write(term) for term in series_terms]), run_time=2.0)

        # Camera pull back
        all_elements = VGroup(q_group, p_group, q_small_group, connection_line, series_terms, assumption)
        self.play(all_elements.animate.scale(0.8), run_time=1.0)

        # EVOLVE — Gear accelerates, split into finite/infinite parts
        self.wait(1.0)

        # Animate the gear rotating faster
        self.play(Rotate(q_gear, angle=PI*4, about_point=q_gear.get_center()), run_time=3.0, rate_func=linear)

        # Split series into two groups
        finite_sum = MathTex("q! \\cdot \\left(1 + 1 + \\frac{1}{2!} + \\cdots + \\frac{1}{q!}\\right)", color=GOLD_E).scale(0.8).to_edge(LEFT, buff=1.0)
        infinite_tail = MathTex("q! \\cdot \\left(\\frac{1}{(q+1)!} + \\frac{1}{(q+2)!} + \\cdots \\right)", color=RED_D).scale(0.8).to_edge(RIGHT, buff=1.0)

        self.play(
            FadeOut(series_terms),
            Write(finite_sum),
            Write(infinite_tail),
            run_time=2.0
        )

        # Highlight integer part locking into place
        int_part = Rectangle(color=GREEN_A, fill_color=GREEN_A, fill_opacity=0.2, height=1.0, width=3.0).next_to(finite_sum, UP, buff=0.2)
        self.play(Create(int_part), run_time=1.0)

        # Wobbling fractional parts
        frac_part = Rectangle(color=RED_D, fill_color=RED_D, fill_opacity=0.2, height=1.0, width=3.0).next_to(infinite_tail, UP, buff=0.2)
        self.play(Create(frac_part), run_time=1.0)

        # Add wobbling effect to fractional part
        def wobble(mob, dt):
            mob.rotate(np.sin(self.time) * 0.05)
        
        frac_part.add_updater(wobble)

        # REVEAL — Contradiction appears
        self.wait(1.0)

        # Jam the gears
        def jam(mob, dt):
            mob.rotate(np.sin(self.time * 10) * 0.02)
        
        q_gear.add_updater(jam)
        p_gear.add_updater(jam)
        q_small_gear.add_updater(jam)

        # Red X over assumption
        contradiction_x = Cross(assumption, stroke_color=RED_D, stroke_width=10)
        contradiction_text = Text("CONTRADICTION!", color=RED_D).scale(0.8).next_to(contradiction_x, DOWN)

        self.play(
            Create(contradiction_x),
            Write(contradiction_text),
            run_time=2.0
        )

        # Final statement
        final_statement = MathTex("e \\neq {p \\over q}", color=RED_D).scale(1.5).move_to(ORIGIN)
        self.play(
            FadeOut(q_group),
            FadeOut(p_group),
            FadeOut(q_small_group),
            FadeOut(connection_line),
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

        # IDLE LOOP - Jammed gears twitch slightly, fractional pieces wobble chaotically
        # We'll simulate this with the final statement having slight movement
        def twitch(mob):
            mob.shift(0.01 * np.sin(self.time) * RIGHT + 0.01 * np.cos(self.time) * UP)
        
        final_statement.add_updater(twitch)
        self.wait(3.0)  # This creates the idle loop effect