from manim import *
import numpy as np


class AetherLabScene(Scene):
    def construct(self):
        # Define parameters
        g = 9.81
        L1 = 1.0
        L2 = 1.0
        m1 = 1.0
        m2 = 1.0
        
        # Pivot point
        pivot = np.array([0, 2, 0])
        
        # Initial angles
        theta1_0 = PI / 3
        theta2_0 = PI / 4
        
        # Time tracker
        t = ValueTracker(0)
        
        # Define angle functions (simplified harmonic approximation for visualization)
        def theta1(t_val):
            return theta1_0 * np.cos(np.sqrt(g / L1) * t_val)
        
        def theta2(t_val):
            return theta2_0 * np.cos(np.sqrt(g / L2) * t_val)
        
        # Position functions
        def pos1(t_val):
            th1 = theta1(t_val)
            return pivot + L1 * np.array([np.sin(th1), -np.cos(th1), 0])
        
        def pos2(t_val):
            th1 = theta1(t_val)
            th2 = theta2(t_val)
            p1 = pos1(t_val)
            return p1 + L2 * np.array([np.sin(th2), -np.cos(th2), 0])
        
        # Velocity functions (derivatives)
        def vel1(t_val):
            th1 = theta1(t_val)
            dth1_dt = -theta1_0 * np.sqrt(g / L1) * np.sin(np.sqrt(g / L1) * t_val)
            return L1 * np.array([np.cos(th1) * dth1_dt, np.sin(th1) * dth1_dt, 0])
        
        def vel2(t_val):
            th1 = theta1(t_val)
            th2 = theta2(t_val)
            dth1_dt = -theta1_0 * np.sqrt(g / L1) * np.sin(np.sqrt(g / L1) * t_val)
            dth2_dt = -theta2_0 * np.sqrt(g / L2) * np.sin(np.sqrt(g / L2) * t_val)
            
            # Velocity of second mass
            dx1 = L1 * np.cos(th1) * dth1_dt
            dy1 = L1 * np.sin(th1) * dth1_dt
            dx2 = dx1 + L2 * np.cos(th2) * dth2_dt
            dy2 = dy1 + L2 * np.sin(th2) * dth2_dt
            return np.array([dx2, dy2, 0])
        
        # Create pendulum parts
        rod1 = always_redraw(lambda: Line(pivot, pos1(t.get_value()), 
                                         color=GOLD_E, stroke_width=5))
        rod2 = always_redraw(lambda: Line(pos1(t.get_value()), pos2(t.get_value()), 
                                         color=GOLD_E, stroke_width=5))
        
        mass1 = always_redraw(lambda: Dot(pos1(t.get_value()), 
                                          color=BLUE_E, radius=0.2))
        mass2 = always_redraw(lambda: Dot(pos2(t.get_value()), 
                                          color=BLUE_E, radius=0.2))
        
        # Velocity vectors
        vel_vec1 = always_redraw(lambda: Arrow(
            pos1(t.get_value()),
            pos1(t.get_value()) + 0.3 * vel1(t.get_value()),
            color=TEAL_A, buff=0, max_tip_length_to_length_ratio=0.3
        ))
        
        vel_vec2 = always_redraw(lambda: Arrow(
            pos2(t.get_value()),
            pos2(t.get_value()) + 0.3 * vel2(t.get_value()),
            color=TEAL_A, buff=0, max_tip_length_to_length_ratio=0.3
        ))
        
        # Live derivative displays
        dx1_tracker = ValueTracker()
        dy1_tracker = ValueTracker()
        dx2_tracker = ValueTracker()
        dy2_tracker = ValueTracker()
        
        dx1_label = always_redraw(lambda: DecimalNumber(dx1_tracker.get_value(), 
                                                        num_decimal_places=2, 
                                                        color=WHITE).scale(0.3).next_to(mass1.get_center(), UR, buff=0.1))
        dy1_label = always_redraw(lambda: DecimalNumber(dy1_tracker.get_value(), 
                                                        num_decimal_places=2, 
                                                        color=WHITE).scale(0.3).next_to(mass1.get_center(), DR, buff=0.1))
        dx2_label = always_redraw(lambda: DecimalNumber(dx2_tracker.get_value(), 
                                                        num_decimal_places=2, 
                                                        color=WHITE).scale(0.3).next_to(mass2.get_center(), UR, buff=0.1))
        dy2_label = always_redraw(lambda: DecimalNumber(dy2_tracker.get_value(), 
                                                        num_decimal_places=2, 
                                                        color=WHITE).scale(0.3).next_to(mass2.get_center(), DR, buff=0.1))
        
        dx1_text = always_redraw(lambda: Text("dx₁/dt =", color=WHITE).scale(0.3).next_to(dx1_label, LEFT, buff=0.1))
        dy1_text = always_redraw(lambda: Text("dy₁/dt =", color=WHITE).scale(0.3).next_to(dy1_label, LEFT, buff=0.1))
        dx2_text = always_redraw(lambda: Text("dx₂/dt =", color=WHITE).scale(0.3).next_to(dx2_label, LEFT, buff=0.1))
        dy2_text = always_redraw(lambda: Text("dy₂/dt =", color=WHITE).scale(0.3).next_to(dy2_label, LEFT, buff=0.1))
        
        # Group for easy removal
        labels_group = VGroup(dx1_text, dy1_text, dx2_text, dy2_text, 
                              dx1_label, dy1_label, dx2_label, dy2_label)
        
        # ACT 1: ESTABLISH
        title = Text("Double Pendulum System", color=WHITE).scale(0.5).to_edge(UP)
        self.play(Write(title))
        
        # Show initial state
        self.play(Create(rod1), Create(rod2), 
                  FadeIn(mass1), FadeIn(mass2))
        self.wait(1)
        
        # Start motion and show first velocity
        self.play(t.animate.set_value(0.5), run_time=1.5)
        self.play(Create(vel_vec1))
        
        # Update trackers and show first derivatives
        def update_derivatives(dt):
            current_t = t.get_value()
            v1 = vel1(current_t)
            dx1_tracker.set_value(v1[0])
            dy1_tracker.set_value(v1[1])
        
        self.add_updater(update_derivatives)
        self.play(t.animate.set_value(1.5), run_time=3)
        self.remove_updater(update_derivatives)
        
        # Show first derivatives
        self.play(FadeIn(dx1_text), FadeIn(dy1_text), 
                  FadeIn(dx1_label), FadeIn(dy1_label))
        self.wait(0.5)
        
        # ACT 2: EVOLVE
        # Add second velocity vector and more motion
        self.play(t.animate.set_value(2.0), run_time=1)
        self.play(Create(vel_vec2))
        
        # More complex motion
        def update_all_derivatives(dt):
            current_t = t.get_value()
            v1 = vel1(current_t)
            v2 = vel2(current_t)
            dx1_tracker.set_value(v1[0])
            dy1_tracker.set_value(v1[1])
            dx2_tracker.set_value(v2[0])
            dy2_tracker.set_value(v2[1])
        
        self.add_updater(update_all_derivatives)
        self.play(t.animate.set_value(4.0), run_time=4)
        
        # Show second derivatives
        self.play(FadeIn(dx2_text), FadeIn(dy2_text), 
                  FadeIn(dx2_label), FadeIn(dy2_label))
        self.wait(0.5)
        
        # Show velocity squared calculations
        v1_squared = always_redraw(lambda: MathTex(
            f"v_1^2 = ({dx1_tracker.get_value():.2f})^2 + ({dy1_tracker.get_value():.2f})^2",
            color=WHITE
        ).scale(0.4).to_edge(LEFT).shift(UP * 1.5))
        
        v2_squared = always_redraw(lambda: MathTex(
            f"v_2^2 = ({dx2_tracker.get_value():.2f})^2 + ({dy2_tracker.get_value():.2f})^2",
            color=WHITE
        ).scale(0.4).to_edge(LEFT).shift(UP * 0.5))
        
        self.play(Write(v1_squared), Write(v2_squared))
        self.wait(1)
        
        # Show energy bars
        energy_bar1 = Rectangle(height=0.2, width=2, color=BLUE_E, fill_opacity=0.6)
        energy_bar2 = Rectangle(height=0.2, width=2, color=BLUE_E, fill_opacity=0.6)
        energy_bar1.next_to(v1_squared, DOWN, buff=0.3).align_to(v1_squared, LEFT)
        energy_bar2.next_to(v2_squared, DOWN, buff=0.3).align_to(v2_squared, LEFT)
        
        def update_energy_bars():
            v1_mag = np.linalg.norm(vel1(t.get_value()))
            v2_mag = np.linalg.norm(vel2(t.get_value()))
            k1 = 0.5 * m1 * v1_mag**2
            k2 = 0.5 * m2 * v2_mag**2
            
            energy_bar1.width = min(k1 * 2, 3)
            energy_bar2.width = min(k2 * 2, 3)
            energy_bar1.stretch_to_fit_width(max(energy_bar1.width, 0.1))
            energy_bar2.stretch_to_fit_width(max(energy_bar2.width, 0.1))
        
        energy_bar1.add_updater(lambda m: update_energy_bars())
        energy_bar2.add_updater(lambda m: update_energy_bars())
        
        self.play(Create(energy_bar1), Create(energy_bar2))
        self.wait(1)
        
        # ACT 3: REVEAL
        # Total kinetic energy formula
        total_ke = MathTex("T = \\frac{1}{2}m_1v_1^2 + \\frac{1}{2}m_2v_2^2", 
                           color=GOLD_E).scale(0.6).to_edge(UP).shift(DOWN*0.5)
        
        self.play(Write(total_ke), run_time=1.5)
        
        # Slow down motion to show precision
        self.play(t.animate.set_value(5.0), run_time=2, rate_func=linear)
        self.wait(1)
        
        # Final synchronization
        self.play(t.animate.set_value(6.0), run_time=2, rate_func=linear)
        
        # Remove updater to finalize values
        self.remove_updater(update_all_derivatives)
        
        # Final update to lock values
        final_v1 = vel1(t.get_value())
        final_v2 = vel2(t.get_value())
        dx1_tracker.set_value(final_v1[0])
        dy1_tracker.set_value(final_v1[1])
        dx2_tracker.set_value(final_v2[0])
        dy2_tracker.set_value(final_v2[1])
        
        # IDLE LOOP setup
        def idle_loop(dt):
            current_t = t.get_value()
            # Small oscillation for idle loop
            small_t = current_t * 2
            v1 = vel1(small_t)
            v2 = vel2(small_t)
            dx1_tracker.set_value(v1[0] * 0.3)
            dy1_tracker.set_value(v1[1] * 0.3)
            dx2_tracker.set_value(v2[0] * 0.3)
            dy2_tracker.set_value(v2[1] * 0.3)
            
            # Update velocity arrow opacities
            vel_vec1.set_stroke(opacity=0.5 + 0.3 * np.sin(small_t))
            vel_vec2.set_stroke(opacity=0.5 + 0.3 * np.sin(small_t))
            vel_vec1.set_fill(opacity=0.5 + 0.3 * np.sin(small_t))
            vel_vec2.set_fill(opacity=0.5 + 0.3 * np.sin(small_t))
        
        self.add_updater(idle_loop)
        self.play(t.animate.set_value(t.get_value() + 3), run_time=3, rate_func=linear)
        self.remove_updater(idle_loop)