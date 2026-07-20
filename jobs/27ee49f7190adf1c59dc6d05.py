from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # ESTABLISH — Camera pulls back to reveal a pristine laboratory setup with two brass pendulum masses hanging vertically
        title = Text("Double Pendulum System", color=GOLD_E).scale(0.6).to_edge(UP)
        self.play(Write(title), run_time=1.2)

        # Setup parameters
        g = 9.81
        L1 = 1.0
        L2 = 1.0
        pivot = np.array([0, 2, 0])
        
        # Create pendulum components
        anchor = Dot(pivot, color=GOLD_E, radius=0.1)
        rod1 = Line(pivot, pivot + np.array([0, -L1*1.8, 0]), color=GREY_A, stroke_width=4)
        bob1 = Dot(pivot + np.array([0, -L1*1.8, 0]), color=GOLD_E, radius=0.15)
        
        rod2 = Line(pivot + np.array([0, -L1*1.8, 0]), 
                   pivot + np.array([0, -L1*1.8, 0]) + np.array([0, -L2*1.8, 0]), 
                   color=GREY_A, stroke_width=4)
        bob2 = Dot(pivot + np.array([0, -L1*1.8, 0]) + np.array([0, -L2*1.8, 0]), 
                   color=GOLD_E, radius=0.15)
        
        # Create angle arcs with proper spacing
        angle_arc1 = Arc(radius=0.5, start_angle=-PI/2, angle=0, color=BLUE_E)
        angle_arc2 = Arc(radius=0.4, start_angle=-PI/2, angle=0, color=BLUE_E)
        
        # Properly spaced labels
        theta1_label = MathTex(r"\theta_1", color=BLUE_E).scale(0.5).next_to(angle_arc1, LEFT, buff=0.2)
        theta2_label = MathTex(r"\theta_2", color=BLUE_E).scale(0.5).next_to(angle_arc2, RIGHT, buff=0.2)
        
        l1_label = MathTex(r"L_1 = 1.0", color=GOLD_E).scale(0.4).next_to(rod1, RIGHT, buff=0.3)
        l2_label = MathTex(r"L_2 = 1.0", color=GOLD_E).scale(0.4).next_to(rod2, RIGHT, buff=0.3)
        
        # Position vectors with consistent palette
        r1_vector = Arrow(pivot, bob1.get_center(), color=RED_E, buff=0, stroke_width=3, max_stroke_width_to_length_ratio=5)
        r2_vector = Arrow(pivot, bob2.get_center(), color=RED_E, buff=0, stroke_width=3, max_stroke_width_to_length_ratio=5)
        
        r1_label = MathTex(r"\vec{r}_1", color=RED_E).scale(0.4).next_to(r1_vector.get_center(), LEFT, buff=0.2)
        r2_label = MathTex(r"\vec{r}_2", color=RED_E).scale(0.4).next_to(r2_vector.get_center(), DOWN, buff=0.2)
        
        # Create coordinate grid with reduced opacity
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 2, 1],
            axis_config={"color": GREY_C, "stroke_opacity": 0.3},
            x_length=8,
            y_length=6
        ).scale(0.8).shift(DOWN * 0.5)
        
        self.play(
            Create(anchor),
            Create(rod1),
            Create(bob1),
            Create(rod2),
            Create(bob2),
            run_time=1.5
        )
        
        self.play(
            Create(angle_arc1),
            Create(angle_arc2),
            Write(theta1_label),
            Write(theta2_label),
            Write(l1_label),
            Write(l2_label),
            run_time=1.5
        )
        
        self.play(
            Create(axes),
            run_time=1.5
        )
        
        self.play(
            Create(r1_vector),
            Create(r2_vector),
            Write(r1_label),
            Write(r2_label),
            run_time=1.5
        )
        
        # EVOLVE — First pendulum begins a gentle swing, dragging the second along
        t_tracker = ValueTracker(0)
        
        def get_theta1(t):
            return 0.3 * np.sin(0.8 * t)
        
        def get_theta2(t):
            return 0.2 * np.sin(1.2 * t + PI/4)
        
        def get_bob1_position(t):
            theta = get_theta1(t)
            return pivot + L1 * 1.8 * np.array([np.sin(theta), -np.cos(theta), 0])
        
        def get_bob2_position(t):
            theta1 = get_theta1(t)
            theta2 = get_theta2(t)
            pos1 = get_bob1_position(t)
            return pos1 + L2 * 1.8 * np.array([np.sin(theta2), -np.cos(theta2), 0])
        
        def update_rod1(rod):
            rod.put_start_and_end_on(pivot, get_bob1_position(t_tracker.get_value()))
        
        def update_rod2(rod):
            rod.put_start_and_end_on(get_bob1_position(t_tracker.get_value()), 
                                    get_bob2_position(t_tracker.get_value()))
        
        def update_bob1(bob):
            bob.move_to(get_bob1_position(t_tracker.get_value()))
        
        def update_bob2(bob):
            bob.move_to(get_bob2_position(t_tracker.get_value()))
        
        def update_angle_arc1(arc):
            theta = get_theta1(t_tracker.get_value())
            new_arc = Arc(radius=0.5, start_angle=-PI/2, angle=theta if theta > 0 else theta, color=BLUE_E)
            new_arc.move_arc_center_to(pivot)
            arc.become(new_arc)
        
        def update_angle_arc2(arc):
            theta1 = get_theta1(t_tracker.get_value())
            theta2 = get_theta2(t_tracker.get_value())
            pos1 = get_bob1_position(t_tracker.get_value())
            new_arc = Arc(radius=0.4, start_angle=-PI/2 + theta1, angle=theta2, color=BLUE_E)
            new_arc.move_arc_center_to(pos1)
            arc.become(new_arc)
        
        def update_r1_vector(vec):
            vec.put_start_and_end_on(pivot, get_bob1_position(t_tracker.get_value()))
        
        def update_r2_vector(vec):
            vec.put_start_and_end_on(pivot, get_bob2_position(t_tracker.get_value()))
        
        def update_r1_label(lbl):
            lbl.next_to(r1_vector.get_center(), LEFT, buff=0.2)
        
        def update_r2_label(lbl):
            lbl.next_to(r2_vector.get_center(), DOWN, buff=0.2)
        
        def update_theta1_label(lbl):
            theta = get_theta1(t_tracker.get_value())
            direction = UR if theta >= 0 else DR
            lbl.next_to(angle_arc1, direction, buff=0.2)
        
        def update_theta2_label(lbl):
            theta = get_theta2(t_tracker.get_value())
            pos1 = get_bob1_position(t_tracker.get_value())
            direction = UR if theta >= 0 else DR
            lbl.next_to(angle_arc2, direction, buff=0.2)
        
        rod1.add_updater(update_rod1)
        rod2.add_updater(update_rod2)
        bob1.add_updater(update_bob1)
        bob2.add_updater(update_bob2)
        angle_arc1.add_updater(update_angle_arc1)
        angle_arc2.add_updater(update_angle_arc2)
        r1_vector.add_updater(update_r1_vector)
        r2_vector.add_updater(update_r2_vector)
        r1_label.add_updater(update_r1_label)
        r2_label.add_updater(update_r2_label)
        theta1_label.add_updater(update_theta1_label)
        theta2_label.add_updater(update_theta2_label)
        
        self.play(t_tracker.animate.set_value(8), run_time=8, rate_func=linear)
        
        # REVEAL — Complex chaotic motion emerges as both pendulums swing wildly
        def get_theta1_chaos(t):
            return 0.8 * np.sin(1.5 * t) + 0.3 * np.sin(2.3 * t) + 0.2 * np.sin(0.7 * t)
        
        def get_theta2_chaos(t):
            return 0.6 * np.sin(2.1 * t + PI/3) + 0.4 * np.sin(1.8 * t) + 0.5 * np.sin(1.2 * t + PI/6)
        
        def get_bob1_position_chaos(t):
            theta = get_theta1_chaos(t)
            return pivot + L1 * 1.8 * np.array([np.sin(theta), -np.cos(theta), 0])
        
        def get_bob2_position_chaos(t):
            theta1 = get_theta1_chaos(t)
            theta2 = get_theta2_chaos(t)
            pos1 = get_bob1_position_chaos(t)
            return pos1 + L2 * 1.8 * np.array([np.sin(theta2), -np.cos(theta2), 0])
        
        def update_rod1_chaos(rod):
            rod.put_start_and_end_on(pivot, get_bob1_position_chaos(t_tracker.get_value()))
        
        def update_rod2_chaos(rod):
            rod.put_start_and_end_on(get_bob1_position_chaos(t_tracker.get_value()), 
                                    get_bob2_position_chaos(t_tracker.get_value()))
        
        def update_bob1_chaos(bob):
            bob.move_to(get_bob1_position_chaos(t_tracker.get_value()))
        
        def update_bob2_chaos(bob):
            bob.move_to(get_bob2_position_chaos(t_tracker.get_value()))
        
        def update_angle_arc1_chaos(arc):
            theta = get_theta1_chaos(t_tracker.get_value())
            new_arc = Arc(radius=0.5, start_angle=-PI/2, angle=theta if theta > 0 else theta, color=RED_E)
            new_arc.move_arc_center_to(pivot)
            arc.become(new_arc)
        
        def update_angle_arc2_chaos(arc):
            theta1 = get_theta1_chaos(t_tracker.get_value())
            theta2 = get_theta2_chaos(t_tracker.get_value())
            pos1 = get_bob1_position_chaos(t_tracker.get_value())
            new_arc = Arc(radius=0.4, start_angle=-PI/2 + theta1, angle=theta2, color=RED_E)
            new_arc.move_arc_center_to(pos1)
            arc.become(new_arc)
        
        def update_r1_vector_chaos(vec):
            vec.put_start_and_end_on(pivot, get_bob1_position_chaos(t_tracker.get_value()))
        
        def update_r2_vector_chaos(vec):
            vec.put_start_and_end_on(pivot, get_bob2_position_chaos(t_tracker.get_value()))
        
        rod1.add_updater(update_rod1_chaos)
        rod2.add_updater(update_rod2_chaos)
        bob1.add_updater(update_bob1_chaos)
        bob2.add_updater(update_bob2_chaos)
        angle_arc1.add_updater(update_angle_arc1_chaos)
        angle_arc2.add_updater(update_angle_arc2_chaos)
        r1_vector.add_updater(update_r1_vector_chaos)
        r2_vector.add_updater(update_r2_vector_chaos)
        
        # Add gravity label
        gravity_label = MathTex(f"g = {g:.2f}", color=RED_E).scale(0.6).to_corner(UL)
        self.play(FadeIn(gravity_label), run_time=1)
        
        # Add equation labels
        eq1 = MathTex(r"T = \frac{1}{2}m_1|\dot{\vec{r}}_1|^2 + \frac{1}{2}m_2|\dot{\vec{r}}_2|^2", color=RED_E).scale(0.5).to_edge(DOWN, buff=0.5)
        eq2 = MathTex(r"V = m_1gy_1 + m_2gy_2", color=RED_E).scale(0.5).next_to(eq1, UP, buff=0.2)
        
        self.play(Write(eq1), Write(eq2), run_time=2)
        
        self.play(t_tracker.animate.set_value(14), run_time=6, rate_func=linear)
        
        # Hero frame: Both pendulum masses frozen mid-swing in a perfect geometric configuration
        self.play(
            t_tracker.animate.set_value(14 + PI/4),  # To get specific angles
            run_time=0.5
        )
        
        # Create the hero frame with golden axes
        golden_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 1, 1],
            axis_config={"color": GOLD_E, "stroke_width": 2},
            x_length=6,
            y_length=4
        ).scale(0.7).shift(DOWN * 0.5)
        
        # Freeze the current positions
        rod1.clear_updaters()
        rod2.clear_updaters()
        bob1.clear_updaters()
        bob2.clear_updaters()
        angle_arc1.clear_updaters()
        angle_arc2.clear_updaters()
        r1_vector.clear_updaters()
        r2_vector.clear_updaters()
        
        # Update to final chaotic positions
        final_theta1 = get_theta1_chaos(14 + PI/4)
        final_theta2 = get_theta2_chaos(14 + PI/4)
        final_pos1 = get_bob1_position_chaos(14 + PI/4)
        final_pos2 = get_bob2_position_chaos(14 + PI/4)
        
        rod1.put_start_and_end_on(pivot, final_pos1)
        rod2.put_start_and_end_on(final_pos1, final_pos2)
        bob1.move_to(final_pos1)
        bob2.move_to(final_pos2)
        
        # Create golden angle arcs at 45 degrees
        golden_arc1 = Arc(radius=0.5, start_angle=-PI/2, angle=PI/4, color=GOLD_E)
        golden_arc1.move_arc_center_to(pivot)
        golden_arc2 = Arc(radius=0.4, start_angle=-PI/2 + PI/4, angle=PI/4, color=GOLD_E)
        golden_arc2.move_arc_center_to(final_pos1)
        
        golden_theta1 = MathTex(r"\theta_1 = 45^\circ", color=GOLD_E).scale(0.6).next_to(golden_arc1, UR, buff=0.2)
        golden_theta2 = MathTex(r"\theta_2 = 45^\circ", color=GOLD_E).scale(0.6).next_to(golden_arc2, UR, buff=0.2)
        
        self.play(
            ReplacementTransform(axes, golden_axes),
            ReplacementTransform(angle_arc1, golden_arc1),
            ReplacementTransform(angle_arc2, golden_arc2),
            ReplacementTransform(theta1_label, golden_theta1),
            ReplacementTransform(theta2_label, golden_theta2),
            run_time=1.5
        )
        
        # IDLE LOOP - Dynamic motion continues with complex chaotic motion
        t_idle = ValueTracker(0)
        
        def idle_update_rod1(rod):
            current_t = t_idle.get_value() + 14 + PI/4
            theta = get_theta1_chaos(current_t)
            pos = pivot + L1 * 1.8 * np.array([np.sin(theta), -np.cos(theta), 0])
            rod.put_start_and_end_on(pivot, pos)
        
        def idle_update_rod2(rod):
            current_t = t_idle.get_value() + 14 + PI/4
            theta1 = get_theta1_chaos(current_t)
            pos1 = pivot + L1 * 1.8 * np.array([np.sin(theta1), -np.cos(theta1), 0])
            theta2 = get_theta2_chaos(current_t)
            pos2 = pos1 + L2 * 1.8 * np.array([np.sin(theta2), -np.cos(theta2), 0])
            rod.put_start_and_end_on(pos1, pos2)
        
        def idle_update_bob1(bob):
            current_t = t_idle.get_value() + 14 + PI/4
            theta = get_theta1_chaos(current_t)
            pos = pivot + L1 * 1.8 * np.array([np.sin(theta), -np.cos(theta), 0])
            bob.move_to(pos)
        
        def idle_update_bob2(bob):
            current_t = t_idle.get_value() + 14 + PI/4
            theta1 = get_theta1_chaos(current_t)
            pos1 = pivot + L1 * 1.8 * np.array([np.sin(theta1), -np.cos(theta1), 0])
            theta2 = get_theta2_chaos(current_t)
            pos2 = pos1 + L2 * 1.8 * np.array([np.sin(theta2), -np.cos(theta2), 0])
            bob.move_to(pos2)
        
        def idle_update_golden_axes(ax):
            current_t = t_idle.get_value()
            scale_factor = 0.7 + 0.02 * np.sin(current_t)
            ax_new = Axes(
                x_range=[-3, 3, 1],
                y_range=[-3, 1, 1],
                axis_config={"color": GOLD_E, "stroke_width": 2},
                x_length=6 * scale_factor,
                y_length=4 * scale_factor
            ).shift(DOWN * 0.5)
            ax.become(ax_new)
        
        rod1.add_updater(idle_update_rod1)
        rod2.add_updater(idle_update_rod2)
        bob1.add_updater(idle_update_bob1)
        bob2.add_updater(idle_update_bob2)
        golden_axes.add_updater(idle_update_golden_axes)
        
        # Keep the labels glowing softly
        golden_theta1.add_updater(lambda m: m.set_opacity(0.8 + 0.2 * np.sin(t_idle.get_value())))
        golden_theta2.add_updater(lambda m: m.set_opacity(0.8 + 0.2 * np.sin(t_idle.get_value())))
        gravity_label.add_updater(lambda m: m.set_opacity(0.8 + 0.2 * np.sin(t_idle.get_value()/1.5)))
        
        self.play(t_idle.animate.set_value(10), run_time=10, rate_func=linear)