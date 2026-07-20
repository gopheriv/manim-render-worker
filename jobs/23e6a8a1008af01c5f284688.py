from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Camera pulls back from central calculating device showing e ≈ 2.718
        title = Text("Euler's Number: e is Irrational", color=BLUE).scale(0.6).to_edge(UP)
        self.play(Write(title), run_time=1.0)

        # Central calculator device
        calc_bg = RoundedRectangle(width=3, height=2, color=GOLD, fill_opacity=0.2, stroke_width=3)
        calc_title = Text("Calculator", color=GOLD).scale(0.4).next_to(calc_bg, UP, buff=0.1)
        
        # Display e ≈ 2.718
        e_display = Text("e ≈ 2.718...", color=WHITE).scale(0.4)
        e_display.move_to(calc_bg.get_center())
        
        self.play(Create(calc_bg), Write(calc_title), Write(e_display), run_time=1.5)

        # First domino falls, revealing 1/0! = 1
        domino1 = Rectangle(width=1.2, height=0.6, color=BLUE, fill_opacity=0.7, stroke_width=2)
        domino1_label = MathTex(r"\frac{1}{0!} = 1", color=WHITE).scale(0.4)
        domino1_label.move_to(domino1.get_center())
        domino1_group = VGroup(domino1, domino1_label)
        domino1_group.next_to(calc_bg, DOWN, buff=0.5)
        
        self.play(FadeIn(domino1_group), run_time=0.8)
        self.play(Rotate(domino1_group, angle=-PI/2, about_point=domino1_group.get_top()), run_time=1.0)

        # Second domino shows 1/1! = 1
        domino2 = Rectangle(width=1.2, height=0.6, color=BLUE, fill_opacity=0.7, stroke_width=2)
        domino2_label = MathTex(r"\frac{1}{1!} = 1", color=WHITE).scale(0.4)
        domino2_label.move_to(domino2.get_center())
        domino2_group = VGroup(domino2, domino2_label)
        domino2_group.next_to(domino1_group, DOWN, buff=0.2)
        
        self.play(FadeIn(domino2_group), run_time=0.8)
        self.play(Rotate(domino2_group, angle=-PI/2, about_point=domino2_group.get_top()), run_time=1.0)

        # Third domino shows 1/2! = 0.5
        domino3 = Rectangle(width=1.2, height=0.6, color=BLUE, fill_opacity=0.7, stroke_width=2)
        domino3_label = MathTex(r"\frac{1}{2!} = 0.5", color=WHITE).scale(0.4)
        domino3_label.move_to(domino3.get_center())
        domino3_group = VGroup(domino3, domino3_label)
        domino3_group.next_to(domino2_group, DOWN, buff=0.2)
        
        self.play(FadeIn(domino3_group), run_time=0.8)
        self.play(Rotate(domino3_group, angle=-PI/2, about_point=domino3_group.get_top()), run_time=1.0)

        # Calculator updates mass = 1.0 as first term settles
        mass_tracker = ValueTracker(1.0)
        mass_text = always_redraw(lambda: Text(f"mass = {mass_tracker.get_value():.1f}", 
                                              color=WHITE).scale(0.3).next_to(calc_bg, LEFT, buff=0.2))
        self.play(Create(mass_text), run_time=0.5)
        self.wait(0.5)

        # EVOLVE — Dominoes accelerate as terms get smaller but accumulate faster
        # Add more dominoes with increasing speed
        domino_terms = [
            r"\frac{1}{3!} = \frac{1}{6}",
            r"\frac{1}{4!} = \frac{1}{24}",
            r"\frac{1}{5!} = \frac{1}{120}",
            r"\frac{1}{6!} = \frac{1}{720}"
        ]
        
        domino_groups = []
        for i, term in enumerate(domino_terms):
            domino = Rectangle(width=1.2, height=0.6, color=BLUE, fill_opacity=0.7, stroke_width=2)
            domino_lab = MathTex(term, color=WHITE).scale(0.35)
            domino_lab.move_to(domino.get_center())
            domino_grp = VGroup(domino, domino_lab)
            
            if i == 0:
                domino_grp.next_to(domino3_group, DOWN, buff=0.2)
            else:
                domino_grp.next_to(domino_groups[-1], DOWN, buff=0.2)
                
            domino_groups.append(domino_grp)
            self.play(FadeIn(domino_grp), run_time=0.6)
            self.play(Rotate(domino_grp, angle=-PI/2, about_point=domino_grp.get_top()), run_time=0.8)

        # Calculator shows stiffness = 1.0 while displaying growing sum
        stiffness_tracker = ValueTracker(1.0)
        stiffness_text = always_redraw(lambda: Text(f"stiffness = {stiffness_tracker.get_value():.1f}", 
                                                   color=WHITE).scale(0.3).next_to(calc_bg, RIGHT, buff=0.2))
        self.play(Create(stiffness_text), run_time=0.5)

        # Damping factor 0.15 appears as resistance slowing the final dominoes
        damping_tracker = ValueTracker(0.15)
        damping_text = always_redraw(lambda: Text(f"damping = {damping_tracker.get_value():.2f}", 
                                                 color=RED).scale(0.3).next_to(calc_bg, DOWN, buff=0.2))
        self.play(Create(damping_text), run_time=0.5)

        # REVEAL — Final domino attempts to fall but hits invisible barrier
        final_domino = Rectangle(width=1.2, height=0.6, color=RED, fill_opacity=0.7, stroke_width=2)
        final_label = MathTex(r"\sum_{n=0}^{\infty}\frac{1}{n!}", color=WHITE).scale(0.4)
        final_label.move_to(final_domino.get_center())
        final_domino_group = VGroup(final_domino, final_label)
        final_domino_group.next_to(domino_groups[-1], DOWN, buff=0.2)
        
        self.play(FadeIn(final_domino_group), run_time=0.5)
        # Attempt to rotate but stop mid-way to show resistance
        self.play(Rotate(final_domino_group, angle=-PI/4, about_point=final_domino_group.get_top()), run_time=1.0)

        # Calculator displays ERROR - rational assumption breaks the system
        error_text = Text("ERROR", color=RED).scale(0.6).move_to(calc_bg.get_center())
        self.play(Transform(e_display, error_text), run_time=1.0)

        # All dominoes reverse direction in impossible backward cascade
        all_dominoes = [domino1_group, domino2_group, domino3_group] + domino_groups
        for domino in reversed(all_dominoes):
            self.play(Rotate(domino, angle=PI/2, about_point=domino.get_top()), run_time=0.3)

        # Central device flashes red confirming e's irrationality
        flash = Circle(color=RED, fill_opacity=1, stroke_width=0).scale(0.1).move_to(calc_bg.get_center())
        self.play(Create(flash), run_time=0.3)
        self.play(FadeOut(flash), run_time=0.3)

        # Hero frame: Calculator surrounded by frozen dominoes with 'e is irrational' glowing in golden text
        hero_text = Text("e is irrational", color=GOLD).scale(0.8).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(hero_text), run_time=1.0)

        # Idle loop: Subtle flickering of the final unfallen domino while calculator digits shimmer
        final_domino_flicker = ValueTracker(0)
        def update_final_domino(domino):
            alpha = final_domino_flicker.get_value()
            scale_factor = 1 + 0.05 * np.sin(alpha * TAU)
            domino.scale(scale_factor)
            domino.set_opacity(0.7 + 0.3 * abs(np.sin(alpha * TAU)))
            return domino
        
        final_domino_group.add_updater(update_final_domino)
        self.add(final_domino_group)
        
        calc_shimmer = ValueTracker(0)
        def update_calc_display(text):
            alpha = calc_shimmer.get_value()
            text.set_opacity(0.8 + 0.2 * np.sin(alpha * TAU))
            return text
        
        error_text.add_updater(update_calc_display)
        self.add(error_text)
        
        # Continue the animation to maintain movement in final frames
        for _ in range(30):  # This ensures visible change in final frames
            self.play(
                final_domino_flicker.animate.set_value(final_domino_flicker.get_value() + 0.2),
                calc_shimmer.animate.set_value(calc_shimmer.get_value() + 0.2),
                run_time=0.1
            )