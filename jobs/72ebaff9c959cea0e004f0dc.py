from manim import *
import numpy as np
import math


class AetherLabScene(Scene):
    def construct(self):
                # ------------------------------------------------------------------
                # Background room (dark) and shared scaffolding
                # ------------------------------------------------------------------
                self.camera.background_color = "#0B0B14"

                # Frequency axis (x) and intensity axis (y) — used in beats A2 onward.
                # y_range fits the RJ blow-up so the UV arrow stays inside the frame.
                axes = Axes(
                    x_range=[0, 1.0, 0.2],
                    y_range=[0, 2.4, 0.4],
                    x_length=10.0,
                    y_length=6.4,
                    axis_config={
                        "stroke_color": GREY_B,
                        "stroke_opacity": 0.55,
                        "include_tip": False,
                    },
                )
                axes.set_opacity(0.0)
                x_label = MathTex(r"\nu", color=GREY_B).scale(0.5)
                x_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.1)
                y_label = MathTex(r"B_\nu(T)", color=GREY_B).scale(0.5)
                y_label.next_to(axes.y_axis.get_end(), UP, buff=0.1)

                # ------------------------------------------------------------------
                # BEAT A1.B1 | 0.00-4.00 s
                # Hook: ingot fades in, temperature readout 5800 K slides in.
                # ------------------------------------------------------------------
                ingot = Rectangle(width=2.4, height=1.2, color=GREY_A, fill_color="#3A3A45", fill_opacity=1.0)
                ingot.set_stroke(color=GREY_B, width=2)
                ingot.move_to(np.array([-4.6, -2.3, 0.0]))

                glow = Circle(radius=0.7, color="#FF8C42", fill_opacity=0.35, stroke_opacity=0.0)
                glow.move_to(ingot.get_center())

                t_tracker = ValueTracker(5800.0)
                temp_label = Text("T =", color="#FFD166").scale(0.4)
                temp_label.next_to(ingot, RIGHT, buff=0.25)
                temp_num = DecimalNumber(t_tracker.get_value(), color="#FFD166", num_decimal_places=0)
                temp_num.next_to(temp_label, RIGHT, buff=0.15)
                unit_label = Text("K", color="#FFD166").scale(0.4)
                unit_label.next_to(temp_num, RIGHT, buff=0.1)

                self.play(FadeIn(ingot, shift=UP * 0.2), FadeIn(glow, scale=0.6), run_time=0.7)
                self.play(
                    Write(temp_label),
                    FadeIn(temp_num, shift=RIGHT * 0.2),
                    FadeIn(unit_label, shift=RIGHT * 0.2),
                    run_time=0.7,
                )
                self.wait(2.3)
                # End of A1.B1: nothing removed — ingot + readout persist for the room.

                # ------------------------------------------------------------------
                # BEAT A2.B1 | 4.00-10.00 s
                # Establish: frequency + intensity axes appear, Rayleigh-Jeans curve
                # is drawn and climbs toward the UV (right side).
                # ------------------------------------------------------------------
                self.play(axes.animate.set_opacity(1.0), FadeIn(x_label), FadeIn(y_label), run_time=1.1)

                # Rayleigh-Jeans curve B_RJ(nu) = 2*nu^2*kB*T/c^2 — monotonic rise.
                rj_curve = axes.plot(
                    lambda x: 0.05 + 1.45 * (x ** 2),
                    x_range=[0.0, 0.95, 0.01],
                    color="#9B5DE5",
                    stroke_width=5,
                )
                rj_eq = MathTex(r"B_\nu^{RJ}=\frac{2\nu^2 k_B T}{c^2}", color="#9B5DE5").scale(0.45)
                rj_eq.next_to(axes, UP, buff=0.15).align_to(axes, LEFT).shift(RIGHT * 0.4)

                self.play(Create(rj_curve, run_time=2.4, rate_func=linear), FadeIn(rj_eq, shift=DOWN * 0.15), run_time=2.4)
                self.wait(2.1)
                # End of A2.B1.

                # ------------------------------------------------------------------
                # BEAT A3.B1 | 10.00-14.00 s
                # Evolve: violet curve overshoots; UV catastrophe arrow points up.
                # ------------------------------------------------------------------
                # Extend the RJ curve past the visible band to dramatize the blow-up.
                rj_overshoot = axes.plot(
                    lambda x: 0.05 + 1.45 * (x ** 2),
                    x_range=[0.95, 1.0, 0.005],
                    color="#9B5DE5",
                    stroke_width=5,
                )
                # A vertical "escape" arrow rising off the top right of the plot.
                # Endpoints normalised to the camera frame so the arrow stays on-screen.
                uv_arrow_start = axes.c2p(0.98, 2.35)
                uv_arrow_end = np.array([uv_arrow_start[0], 3.6, 0.0])
                uv_arrow = Arrow(uv_arrow_start, uv_arrow_end, color="#FFD166", buff=0.0, stroke_width=6)
                uv_arrow.set_opacity(0.9)
                uv_label = Text("UV catastrophe", color="#FFD166").scale(0.34)
                uv_label.next_to(uv_arrow, RIGHT, buff=0.15)

                self.play(Create(rj_overshoot), GrowArrow(uv_arrow), FadeIn(uv_label, shift=LEFT * 0.15), run_time=1.0)
                self.wait(3.0)
                # End of A3.B1.

                # ------------------------------------------------------------------
                # BEAT A3.B2 | 14.00-18.00 s
                # Evolve: discrete energy packets h*nu drop from the ingot; the
                # violet RJ curve dissolves behind them.
                # ------------------------------------------------------------------
                packet_eq = MathTex(r"\varepsilon = h\nu", color="#FFD166").scale(0.5)
                packet_eq.next_to(ingot, UP, buff=0.25)

                # Build a small set of energy packets (gold coins) that fall.
                packets = VGroup()
                for i, dx in enumerate([-0.35, 0.0, 0.35]):
                    pkt = Dot(radius=0.12, color="#FFD166", fill_opacity=1.0)
                    pkt.set_stroke(color="#FF8C42", width=2)
                    pkt.move_to(ingot.get_center() + np.array([dx, 0.6, 0.0]))
                    packets.add(pkt)

                # Fade out the violet curve and arrow as quanta appear.
                self.play(
                    FadeOut(rj_curve),
                    FadeOut(rj_overshoot),
                    FadeOut(rj_eq, shift=UP * 0.2),
                    FadeOut(uv_arrow),
                    FadeOut(uv_label),
                    FadeIn(packet_eq, shift=UP * 0.2),
                    run_time=0.8,
                )
                self.play(
                    LaggedStart(
                        *[
                            pkt.animate.move_to(pkt.get_center() + np.array([0.0, -0.55, 0.0]))
                            for pkt in packets
                        ],
                        lag_ratio=0.25,
                    ),
                    run_time=1.2,
                )
                self.wait(2.0)
                # End of A3.B2.

                # ------------------------------------------------------------------
                # BEAT A4.B1 | 18.00-22.44 s
                # Reveal: warm orange Planck curve, peak marker, live peak-freq
                # readout in THz.
                # ------------------------------------------------------------------
                # Planck spectral radiance in normalized units: peak around x ~ 0.45.
                def planck(x):
                    xv = 0.1 + 6.0 * x  # map to a frequency-like argument
                    return 0.04 + 1.35 * (xv ** 3) / (math.exp(min(80.0, xv)) - 1.0)

                planck_curve = axes.plot(
                    planck,
                    x_range=[0.0, 1.0, 0.01],
                    color="#FF8C42",
                    stroke_width=6,
                )
                # Marker + live peak-frequency readout.
                peak_x = 0.45
                peak_y = planck(peak_x)
                peak_dot = Dot(axes.c2p(peak_x, peak_y), color="#FFD166", radius=0.09)
                peak_dot.set_stroke(color=WHITE, width=2)

                peak_readout_label = Text("peak  ", color="#FFD166").scale(0.32)
                peak_readout_num = DecimalNumber(peak_x * 1000.0, color="#FFD166", num_decimal_places=1)
                peak_readout_unit = Text("THz", color="#FFD166").scale(0.32)
                peak_group = VGroup(peak_readout_label, peak_readout_num, peak_readout_unit).arrange(
                    RIGHT, buff=0.08
                )
                peak_group.next_to(peak_dot, UP, buff=0.2)

                planck_eq = MathTex(
                    r"B_\nu=\frac{2h\nu^3}{c^2}\frac{1}{e^{h\nu/k_BT}-1}",
                    color="#FF8C42",
                ).scale(0.5)
                planck_eq.next_to(axes, DOWN, buff=0.25)

                self.play(
                    Create(planck_curve, run_time=2.9, rate_func=smooth),
                    FadeIn(peak_dot, scale=0.6),
                    FadeIn(peak_group, shift=UP * 0.15),
                    FadeIn(planck_eq, shift=UP * 0.15),
                    run_time=2.9,
                )
                self.wait(1.54)
                # End of A4.B1.

                # ------------------------------------------------------------------
                # BEAT A4.B2 | 22.22.46-26.00 s
                # Reveal: total emitted power readout settles, faded RJ ghost
                # reminds us it diverges.
                # ------------------------------------------------------------------
                # Faded RJ ghost that stays inside the new y_range.
                rj_ghost = axes.plot(
                    lambda x: 0.05 + 1.45 * (x ** 2),
                    x_range=[0.6, 0.95, 0.01],
                    color="#9B5DE5",
                    stroke_width=3,
                )
                rj_ghost.set_opacity(0.35)

                # Power readout beside the ingot (left zone).
                power_tracker = ValueTracker(0.0)
                power_label = Text("P =", color="#FFD166").scale(0.36)
                power_label.next_to(ingot, RIGHT, buff=0.25).align_to(temp_label, LEFT)
                power_num = DecimalNumber(power_tracker.get_value(), color="#FFD166", num_decimal_places=0)
                power_num.next_to(power_label, RIGHT, buff=0.12)
                power_unit = Text("MW/m²", color="#FFD166").scale(0.34)
                power_unit.next_to(power_num, RIGHT, buff=0.08)

                self.play(
                    FadeIn(rj_ghost),
                    FadeIn(power_label, shift=RIGHT * 0.15),
                    FadeIn(power_num, shift=RIGHT * 0.15),
                    FadeIn(power_unit, shift=RIGHT * 0.15),
                    run_time=0.7,
                )
                # Live updater for power readout (one of two live updaters).
                power_num.add_updater(lambda m: m.set_value(power_tracker.get_value()))
                self.play(power_tracker.animate.set_value(73.2), run_time=2.46, rate_func=smooth)
                self.wait(0.4)
                # End of A4.B2.

                # ------------------------------------------------------------------
                # BEAT A5.B1 | 26.00-30.00 s
                # Recap: side-by-side comparison, Planck equation under the plot.
                # Idle loop: Planck peak gently breathes (jitter 5799..5801 K).
                # ------------------------------------------------------------------
                # Compress current state to a compact comparison.
                # Remove the power readouts and ingot glow to free the left zone.
                self.play(
                    FadeOut(packets),
                    FadeOut(packet_eq),
                    FadeOut(power_label),
                    FadeOut(power_num),
                    FadeOut(power_unit),
                    FadeOut(ingot),
                    FadeOut(glow),
                    FadeOut(temp_label),
                    FadeOut(temp_num),
                    FadeOut(unit_label),
                    FadeOut(peak_group),
                    FadeOut(peak_dot),
                    FadeOut(rj_ghost),
                    run_time=0.6,
                )
                # Re-scale axes smaller and center, then add a compact ghost of RJ.
                axes.generate_target()
                axes.target.set(width=8.0, height=3.4).move_to(np.array([0.0, 0.6, 0.0]))

                rj_ghost_small = axes.plot(
                    lambda x: 0.05 + 1.45 * (x ** 2),
                    x_range=[0.0, 0.95, 0.01],
                    color="#9B5DE5",
                    stroke_width=3,
                )
                rj_ghost_small.set_opacity(0.45)

                planck_small = axes.plot(
                    planck,
                    x_range=[0.0, 1.0, 0.01],
                    color="#FF8C42",
                    stroke_width=5,
                )

                recap_eq = MathTex(
                    r"B_\nu=\frac{2h\nu^3}{c^2}\frac{1}{e^{h\nu/k_BT}-1}",
                    color="#FF8C42",
                ).scale(0.55)
                recap_eq.next_to(axes, DOWN, buff=0.3)

                comp_title = Text("Classical  vs  Quantum", color="#F1F1F5").scale(0.36)
                comp_title.next_to(axes, UP, buff=0.2)

                x_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.1)
                y_label.next_to(axes.y_axis.get_end(), UP, buff=0.1)
                self.play(
                    MoveToTarget(axes),
                    FadeIn(x_label),
                    FadeIn(y_label),
                    FadeIn(rj_ghost_small),
                    FadeIn(planck_small),
                    FadeIn(recap_eq, shift=UP * 0.15),
                    FadeIn(comp_title, shift=DOWN * 0.1),
                    run_time=0.9,
                )

                # Idle loop: peak intensity nudges up/down while T flickers 5799..5801.
                peak_tracker = ValueTracker(1.0)
                breathe_dot = always_redraw(
                    lambda: Dot(
                        axes.c2p(peak_x, peak_y * peak_tracker.get_value()),
                        color="#FFD166",
                        radius=0.08,
                    )
                )
                self.add(breathe_dot)

                # Ticker that flickers the displayed temperature between 5799 and 5801.
                jitter_tracker = ValueTracker(5800.0)
                temp_num = DecimalNumber(jitter_tracker.get_value(), color="#FFD166", num_decimal_places=0)
                temp_label.move_to(np.array([-5.6, -2.6, 0.0]))
                temp_num.next_to(temp_label, RIGHT, buff=0.12)
                unit_label.next_to(temp_num, RIGHT, buff=0.08)
                self.add(temp_num, temp_label, unit_label)

                # Drive the breath and the flicker together.
                self.play(
                    peak_tracker.animate.set_value(1.05),
                    jitter_tracker.animate.set_value(5801.0),
                    run_time=0.7,
                    rate_func=smooth,
                )
                self.play(
                    peak_tracker.animate.set_value(0.97),
                    jitter_tracker.animate.set_value(5799.0),
                    run_time=0.7,
                    rate_func=smooth,
                )
                self.play(
                    peak_tracker.animate.set_value(1.02),
                    jitter_tracker.animate.set_value(5800.0),
                    run_time=0.7,
                    rate_func=smooth,
                )
                # Hold a final frame so the loop ends on motion, not a freeze.
                self.wait(0.1)