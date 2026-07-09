from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # Define variables
        g = 9.8
        range_val = 91.837
        theta = 0.7854  # 45 degrees in radians
        time_flight = 4.33
        v0 = 30.0
        vx = 21.213
        vy = 21.213

        # ESTABLISH - Cannon positioned at origin fires ball upward at 45 degree angle
        # Set up coordinate system
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 50, 10],
            axis_config={"color": DARK_BLUE, "stroke_opacity": 0.3},
            x_length=10,
            y_length=5
        ).scale(0.7).shift(LEFT * 0.5)
        
        # Create cannon
        cannon = Rectangle(width=1.0, height=0.3, color=YELLOW, fill_color=YELLOW, fill_opacity=1)
        cannon.rotate(theta).move_to(axes.c2p(0, 0)).shift(UP*0.15)
        
        # Create initial ball
        ball = Circle(radius=0.2, color=YELLOW, fill_color=YELLOW, fill_opacity=1)
        ball.move_to(axes.c2p(0, 0.3))
        
        # Create initial velocity vector
        v_arrow = Arrow(
            start=axes.c2p(0, 0.3),
            end=axes.c2p(vx/3, vy/3),
            color=YELLOW,
            buff=0
        )
        v_label = MathTex("\\vec{v_0}", color=YELLOW).scale(0.5)
        v_label.next_to(v_arrow.get_end(), UR, buff=0.1)
        
        # Add title
        title = Text("Projectile Motion", color=YELLOW).scale(0.5).to_edge(UP)
        
        self.play(Write(title))
        self.play(Create(cannon), Create(ball))
        self.play(Create(axes), run_time=2.0)
        self.play(GrowArrow(v_arrow), Write(v_label))
        self.wait(1.0)

        # EVOLVE - Ball traces smooth parabolic curve
        # Define trajectory function
        def trajectory(t):
            x = vx * t
            y = vy * t - 0.5 * g * t**2
            return axes.c2p(x, max(y, 0))  # Ensure y >= 0
        
        # Create parabolic trajectory
        trajectory_curve = axes.plot_parametric_curve(
            lambda t: trajectory(t),
            t_range=[0, time_flight],
            color=YELLOW,
            stroke_width=4
        )
        
        # Create moving ball and trace
        t_tracker = ValueTracker(0)
        moving_ball = always_redraw(
            lambda: Circle(radius=0.2, color=YELLOW, fill_color=YELLOW, fill_opacity=1)
                    .move_to(trajectory(t_tracker.get_value()))
        )
        
        # Create gravity arrow
        g_arrow = Arrow(
            start=axes.c2p(range_val/2, 40),
            end=axes.c2p(range_val/2, 30),
            color=RED,
            buff=0
        )
        g_label = MathTex("\\vec{g}", color=RED).scale(0.5)
        g_label.next_to(g_arrow.get_end(), DOWN, buff=0.1)
        
        # Animate the ball along the trajectory
        self.play(
            t_tracker.animate.set_value(time_flight),
            Create(trajectory_curve),
            run_time=6.0,
            rate_func=linear
        )
        self.add(moving_ball)
        self.remove(ball)  # Remove the initial static ball
        self.play(Create(g_arrow), Write(g_label))
        self.wait(1.0)

        # REVEAL - Ball lands at calculated range distance of 91.8 meters
        # Create measuring tape
        tape_line = Line(
            start=axes.c2p(0, 0),
            end=axes.c2p(range_val, 0),
            color=RED,
            stroke_width=6
        )
        
        # Create range label
        range_text = Text(f"{range_val:.3f} m", color=RED, font_size=24)
        range_text.next_to(axes.c2p(range_val/2, -5), DOWN)
        
        # Create range box
        range_box = Rectangle(width=2.0, height=0.6, color=RED, fill_color=RED, fill_opacity=0.2)
        range_box.move_to(axes.c2p(range_val, 0)).shift(DOWN*0.8)
        
        # Create final range text in box
        final_range_text = Text(f"{range_val:.3f}", color=RED, font_size=20)
        final_range_text.move_to(range_box.get_center())
        
        self.play(Create(tape_line), run_time=2.0)
        self.play(Write(range_text), run_time=1.0)
        self.play(Create(range_box), Write(final_range_text), run_time=1.0)
        self.wait(1.0)

        # IDLE LOOP - The golden trajectory pulse gently brightens and dims
        # while the cannonball at the landing point has a subtle glow variation
        pulse_trajectory = trajectory_curve.copy()
        
        def pulse_animation(mob):
            alpha = (np.sin(self.time * 2) + 1) / 2  # Oscillate between 0 and 1
            new_alpha = 0.5 + 0.3 * alpha  # Vary between 0.5 and 0.8
            mob.set_stroke(opacity=new_alpha)
            return mob
        
        def glow_animation(mob):
            scale_factor = 1 + 0.1 * np.sin(self.time * 3)  # Small pulsing effect
            mob.scale(scale_factor)
            mob.scale(1/scale_factor)  # Reset scale but keep the animation running
            return mob
        
        pulse_trajectory.add_updater(pulse_animation)
        moving_ball.add_updater(glow_animation)
        
        self.add(pulse_trajectory)
        self.wait(4.0)  # Idle loop duration