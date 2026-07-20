from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Golden pendulum inside bell jar with parameters
        # Create bell jar
        jar = Circle(radius=2.5, color=GOLD, stroke_width=4)
        jar.shift(UP * 0.5)
        
        # Pendulum setup
        pivot = UP * 2.5
        bob = Dot(pivot + DOWN * 2.0, color=GOLD, radius=0.15)
        string = Line(pivot, bob.get_center(), color=GOLD, stroke_width=2)
        
        # Parameter displays
        damping_tracker = ValueTracker(0.15)
        mass_tracker = ValueTracker(1.0)
        stiffness_tracker = ValueTracker(1.0)
        
        damping_label = VGroup(
            Text("damping =", color=BLUE).scale(0.4),
            DecimalNumber(damping_tracker.get_value(), color=BLUE).scale(0.4)
        ).arrange(RIGHT, buff=0.2).to_corner(UL)
        
        mass_label = VGroup(
            Text("mass =", color=BLUE).scale(0.4),
            DecimalNumber(mass_tracker.get_value(), color=BLUE).scale(0.4)
        ).arrange(RIGHT, buff=0.2).next_to(damping_label, DOWN, buff=0.3)
        
        stiffness_label = VGroup(
            Text("stiffness =", color=BLUE).scale(0.4),
            DecimalNumber(stiffness_tracker.get_value(), color=BLUE).scale(0.4)
        ).arrange(RIGHT, buff=0.2).next_to(mass_label, DOWN, buff=0.3)
        
        # Update decimal numbers
        damping_label[1].add_updater(lambda d: d.set_value(damping_tracker.get_value()))
        mass_label[1].add_updater(lambda d: d.set_value(mass_tracker.get_value()))
        stiffness_label[1].add_updater(lambda d: d.set_value(stiffness_tracker.get_value()))
        
        # Fraction p/q
        p_val = mass_tracker.get_value() * stiffness_tracker.get_value() / damping_tracker.get_value()
        q_val = 1.0
        frac_label = MathTex(r"\frac{p}{q}", color=RED).scale(1.2).next_to(jar, UP, buff=0.5)
        
        # Add all initial elements
        self.play(
            Create(jar),
            Create(string),
            Create(bob),
            Write(damping_label),
            Write(mass_label),
            Write(stiffness_label),
            Write(frac_label),
            run_time=2.0
        )
        
        # Pendulum swinging motion
        def update_pendulum(mob):
            angle = 0.5 * np.sin(self.time * 2)
            new_pos = pivot + 2.0 * (np.sin(angle) * RIGHT + np.cos(angle) * DOWN)
            mob.become(Line(pivot, new_pos, color=GOLD, stroke_width=2))
        
        def update_bob(mob):
            angle = 0.5 * np.sin(self.time * 2)
            new_pos = pivot + 2.0 * (np.sin(angle) * RIGHT + np.cos(angle) * DOWN)
            mob.move_to(new_pos)
        
        string.add_updater(update_pendulum)
        bob.add_updater(update_bob)
        
        # Exponential decay visualization
        decay_curve = always_redraw(lambda: 
            ParametricFunction(
                lambda t: (0.5 * np.exp(-0.15 * t) * np.cos(2*t)) * RIGHT + 
                         (-0.5 * t) * UP,
                t_range=[0, 4],
                color=BLUE,
                stroke_width=2
            ).shift(UP * 1.5 + LEFT * 1.5)
        )
        
        self.play(Create(decay_curve), run_time=4.0)
        self.wait(2.0)
        
        # EVOLVE — Rational grids appear and become chaotic
        # Grid lines around jar
        grid_lines = VGroup()
        for i in range(-3, 4):
            line_h = Line(LEFT * 3, RIGHT * 3, color=BLUE, stroke_width=1).shift(UP * i * 0.5)
            line_v = Line(UP * 3, DOWN * 3, color=BLUE, stroke_width=1).shift(RIGHT * i * 0.5)
            grid_lines.add(line_h, line_v)
        
        grid_group = grid_lines.scale(0.8).move_to(jar.get_center())
        
        self.play(Create(grid_group), run_time=2.0)
        
        # Update fraction as pendulum fails to sync
        def update_frac():
            p_new = mass_tracker.get_value() * stiffness_tracker.get_value() / damping_tracker.get_value()
            return MathTex(f"\\frac{{{int(p_new):d}}}{{1}}", color=RED).scale(1.2).next_to(jar, UP, buff=0.5)
        
        frac_anim = always_redraw(update_frac)
        self.add(frac_anim)
        
        # Make grid chaotic
        def chaotic_grid(mob):
            for line in mob:
                offset = 0.1 * np.sin(self.time * 3 + hash(str(line.get_center())) % 10)
                line.shift(offset * (RIGHT + UP).normalize())
        
        grid_group.add_updater(chaotic_grid)
        
        # Complexify the exponential curve
        complex_curve = always_redraw(lambda: 
            ParametricFunction(
                lambda t: (0.5 * np.exp(-0.15 * t) * np.cos(2*t + 0.3*np.sin(3*t))) * RIGHT + 
                         (-0.5 * t) * UP,
                t_range=[0, 6],
                color=RED,
                stroke_width=2
            ).shift(UP * 1.5 + LEFT * 1.5)
        )
        
        self.play(Transform(decay_curve, complex_curve), run_time=3.0)
        self.wait(3.0)
        
        # REVEAL — All rational grids dissolve, e emerges
        self.play(
            FadeOut(grid_group),
            FadeOut(frac_anim),
            run_time=2.0
        )
        
        # Fraction breaks apart
        p_part = MathTex("p", color=RED).scale(1.0).move_to(LEFT * 2)
        q_part = MathTex("q", color=RED).scale(1.0).move_to(RIGHT * 2)
        
        self.play(
            Transform(frac_label, VGroup(p_part, q_part)),
            run_time=1.5
        )
        
        # The number e emerges
        e_symbol = MathTex("e", color=GOLD).scale(2.5).move_to(pivot + DOWN * 1.0)
        e_glow = Circle(color=GOLD, fill_opacity=0.2, stroke_width=0).scale(0.5).move_to(e_symbol.get_center())
        
        self.play(
            Create(e_glow),
            Write(e_symbol),
            run_time=2.0
        )
        
        # Trace the transcendental path
        transcendental_path = always_redraw(lambda: 
            ParametricFunction(
                lambda t: (0.8 * np.exp(-0.1 * t) * np.cos(2.3*t + 0.4*np.sin(1.7*t))) * RIGHT + 
                         (-0.4 * t) * UP,
                t_range=[0, 8],
                color=GOLD,
                stroke_width=3
            ).shift(UP * 1.0 + LEFT * 1.0)
        )
        
        self.play(Create(transcendental_path), run_time=3.0)
        self.wait(1.0)
        
        # IDLE LOOP setup - pendulum oscillates minimally, e pulses
        def gentle_oscillation(mob):
            angle = 0.1 * np.sin(self.time * 0.5)
            new_pos = pivot + 2.0 * (np.sin(angle) * RIGHT + np.cos(angle) * DOWN)
            mob.become(Line(pivot, new_pos, color=GOLD, stroke_width=2))
        
        def gentle_bob(mob):
            angle = 0.1 * np.sin(self.time * 0.5)
            new_pos = pivot + 2.0 * (np.sin(angle) * RIGHT + np.cos(angle) * DOWN)
            mob.move_to(new_pos)
        
        def pulse_e(mob):
            scale_factor = 1 + 0.1 * np.sin(self.time * 2)
            mob.scale_to_fit_height(2.5 * scale_factor)
        
        string.remove_updater(update_pendulum)
        bob.remove_updater(update_bob)
        string.add_updater(gentle_oscillation)
        bob.add_updater(gentle_bob)
        e_symbol.add_updater(pulse_e)
        
        self.wait(5.0)  # This creates the idle loop with continuous motion