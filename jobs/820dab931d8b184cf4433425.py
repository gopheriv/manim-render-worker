from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # Define constants
        g = 9.8
        v0 = 30.0
        theta = 0.7854  # 45 degrees in radians
        vx = v0 * np.cos(theta)  # 21.213
        vy = v0 * np.sin(theta)  # 21.213
        time_flight = 2 * vy / g  # 4.33
        range_val = vx * time_flight  # 91.837

        # Create coordinate system
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 30, 10],
            axis_config={"color": BLUE, "stroke_opacity": 0.3}
        ).scale(0.6).center()
        
        # Add ground line
        ground = Line(
            start=axes.c2p(0, 0),
            end=axes.c2p(100, 0),
            color=GREEN,
            stroke_width=3
        )

        # Create cannon
        cannon_base = Rectangle(width=1.5, height=0.5, fill_color=GRAY, fill_opacity=1, stroke_width=0)
        cannon_base.move_to(axes.c2p(0, 0)).shift(UP*0.25)
        cannon_tube = Rectangle(width=3, height=0.3, fill_color=GRAY, fill_opacity=1, stroke_width=0)
        cannon_tube.rotate(theta).next_to(cannon_base, UR, buff=-0.15)

        # Create cannonball
        cannonball = Circle(radius=0.2, color=ORANGE, fill_color=ORANGE, fill_opacity=1)
        cannonball.move_to(axes.c2p(vx*0.05, vy*0.05))  # Position at cannon tip

        # Create initial velocity vector
        vel_arrow = Arrow(
            start=axes.c2p(vx*0.05, vy*0.05),
            end=axes.c2p(vx*0.05 + 2, vy*0.05 + 2),
            color=YELLOW,
            buff=0,
            max_tip_length_to_length_ratio=0.2
        )
        vel_label = MathTex("v_0 = 30 \\text{ m/s}", color=YELLOW).scale(0.4)
        vel_label.next_to(vel_arrow.get_end(), UR, buff=0.1)

        # Add elements to scene
        self.play(Create(axes), run_time=1.0)
        self.play(Create(ground), run_time=0.5)
        self.play(Create(cannon_base), Create(cannon_tube), run_time=0.8)
        self.play(Create(cannonball), run_time=0.5)
        self.play(GrowArrow(vel_arrow), Write(vel_label), run_time=1.0)

        # Launch flash animation
        flash = Circle(color=YELLOW, fill_color=YELLOW, fill_opacity=1).scale(0.3)
        flash.move_to(cannonball.get_center())
        self.play(Create(flash), run_time=0.3)
        self.play(FadeOut(flash), run_time=0.2)

        # Remove initial velocity vector and label
        self.play(FadeOut(vel_arrow), FadeOut(vel_label), run_time=0.5)

        # Create parabolic trajectory
        trajectory = axes.plot(
            lambda x: (vy/vx)*x - (g/(2*vx**2))*x**2,
            x_range=[0, range_val],
            color=BLUE
        )

        # Create trail for cannonball
        trail = VGroup()

        # Animation for the flight
        t_tracker = ValueTracker(0)
        
        def update_cannonball(ball):
            t = t_tracker.get_value()
            x = vx * t
            y = vy * t - 0.5 * g * t**2
            ball.move_to(axes.c2p(x, y))
            
            # Add to trail occasionally
            if int(t * 10) % 3 == 0:  # Add point every 0.3 seconds
                new_point = cannonball.copy().scale(0.3)
                trail.add(new_point)
                
        cannonball.add_updater(update_cannonball)

        # Create velocity vectors during flight
        v_x_arrow = always_redraw(
            lambda: Arrow(
                start=cannonball.get_center(),
                end=cannonball.get_center() + RIGHT * 0.8,
                color=YELLOW,
                buff=0,
                max_tip_length_to_length_ratio=0.2
            )
        )
        
        v_y_arrow = always_redraw(
            lambda: Arrow(
                start=cannonball.get_center(),
                end=cannonball.get_center() + UP * (vy - g * t_tracker.get_value()) * 0.04,
                color=YELLOW,
                buff=0,
                max_tip_length_to_length_ratio=0.2
            )
        )

        # Velocity labels
        v_x_label = always_redraw(
            lambda: MathTex("v_x", color=YELLOW).scale(0.3).next_to(v_x_arrow.get_end(), DOWN, buff=0.1)
        )
        v_y_label = always_redraw(
            lambda: MathTex("v_y", color=YELLOW).scale(0.3).next_to(v_y_arrow.get_end(), RIGHT, buff=0.1)
        )

        # Animate the flight
        self.play(
            t_tracker.animate.set_value(time_flight),
            Create(trail, run_time=time_flight),
            Create(trajectory, run_time=time_flight),
            run_time=time_flight,
            rate_func=linear
        )

        # At the end of flight, add velocity vectors
        self.play(
            Create(v_x_arrow),
            Create(v_y_arrow),
            Write(v_x_label),
            Write(v_y_label),
            run_time=1.0
        )

        # Create range marker
        range_flag = LabeledDot(
            label=MathTex(f"{range_val:.3f} \\text{{m}}", color=YELLOW).scale(0.4),
            color=YELLOW,
            radius=0.3
        )
        range_flag.move_to(axes.c2p(range_val, 0))

        # Impact effect
        impact_circles = VGroup(*[
            Circle(radius=r, color=YELLOW, stroke_width=2).move_to(axes.c2p(range_val, 0))
            for r in [0.2, 0.4, 0.6]
        ])
        
        self.play(
            Create(range_flag),
            *[Create(circle) for circle in impact_circles],
            run_time=0.8
        )
        self.play(
            FadeOut(impact_circles),
            run_time=0.5
        )

        # Highlight the complete trajectory
        self.play(
            trajectory.animate.set_stroke(width=4),
            run_time=1.0
        )

        # Create range measurement line
        range_line = DashedLine(
            start=axes.c2p(0, 0),
            end=axes.c2p(range_val, 0),
            color=YELLOW,
            dash_length=0.1
        )
        self.play(Create(range_line), run_time=0.8)

        # Create range label
        range_text = MathTex(f"\\text{{Range}} = {range_val:.3f} \\text{{ m}}", color=YELLOW).scale(0.4)
        range_text.move_to(axes.c2p(range_val/2, -3))

        self.play(Write(range_text), run_time=0.8)

        # Idle loop - subtle pulsing of range value and soft glow of trajectory
        range_number = range_text[0][1]  # Get the numerical part
        
        def pulse_range(mob):
            scale_factor = 1 + 0.05 * np.sin(self.time * 2)
            mob.scale(scale_factor)
            mob.set_color(YELLOW)
            return mob

        range_number.add_updater(pulse_range)
        
        # Make trajectory gently glow
        def glow_trajectory(mob):
            alpha = 0.7 + 0.1 * np.sin(self.time)
            mob.set_stroke(opacity=alpha)
            return mob

        trajectory.add_updater(glow_trajectory)

        # Continue the animation in idle loop
        self.wait(5)  # This maintains the idle loop effect

        # Clean up updaters
        cannonball.clear_updaters()
        range_number.clear_updaters()
        trajectory.clear_updaters()