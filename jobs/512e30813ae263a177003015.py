"""AetherLab lesson scenes: uniformly accelerated rectilinear motion (STAGE L).

GENERATED FILE — do not edit by hand. Source: .qwen/tmp/lesson_template.py,
data baked by .qwen/tmp/gen_scenes.py from canonical.json (Stage F v2).
Language of on-screen captions: RU. No LaTeX anywhere (unicode Text only).

Blocks (budgets 20/50/40/50/40/30/30/40 = 300 s):
  BlockB0 hook, BlockB1 concept, BlockB2 velocity, BlockB3 displacement,
  BlockB4 graph, BlockB5 area check, BlockB6 pause task, BlockB7 traps+recap.
"""

from manim import *

# == GEN:DATA BEGIN ==
DATA = {"v0": 2, "a": 3, "t": 4, "v": 14, "s": 32, "b6": {"v0": 0, "a": 2, "t": 5, "s": 25}}
UNITS = {"vel": "м/с", "acc": "м/с²", "dist": "м", "time": "с"}
FORMULAS = {
        "F-accel-def": "a = Δv / Δt",
        "F-vel": "v = v₀ + at",
        "F-disp": "s = v₀ t + at²/2",
        "F-avg": "s = (v₀ + v)t/2"
}
CAPTIONS = {
        "B0": [
                "Сколько метров прошла машина?",
                "Ответ — двумя способами"
        ],
        "B1": [
                "v = s / t — равномерное",
                "a = Δv / Δt",
                "[a] = м/с²",
                "ось Ox →"
        ],
        "B2": [
                "v = v₀ + at",
                "2 + 3·4 = 14 м/с"
        ],
        "B3": [
                "s = v₀t + at²/2",
                "8 + 24 = 32 м",
                "направление не меняется"
        ],
        "B4": [
                "v = 2 + 3t",
                "наклон = a"
        ],
        "B5": [
                "S = (2+14)/2 · 4 = 32 м",
                "площадь = перемещение ✓"
        ],
        "B6": [
                "v₀ = 0, a = 2, t = 5, s = ?",
                "Поставь на паузу!",
                "s = 25 м"
        ],
        "B7": [
                "✗ 14·4 = 56",
                "наклон = a; площадь = s",
                "v = v₀ + at; s = v₀t + at²/2"
        ]
}
# == GEN:DATA END ==

V0, A, T_END = DATA["v0"], DATA["a"], DATA["t"]
V_END, S_END = DATA["v"], DATA["s"]
B6 = DATA["b6"]


def x_of(t: float) -> float:
    return V0 * t + 0.5 * A * t * t


def v_of(t: float) -> float:
    return V0 + A * t


C_V, C_A, C_S, C_T = BLUE, RED, GREEN, GRAY_B
C_AXIS, C_CAR, C_ROAD = GRAY, YELLOW, GRAY_D

ROAD_Y = -2.6
ROAD_X0, ROAD_X1 = -5.6, 5.6


def road_point(x_phys: float):
    frac = min(max(x_phys / S_END, 0.0), 1.0)
    return [ROAD_X0 + frac * (ROAD_X1 - ROAD_X0), ROAD_Y, 0]


def make_car():
    body = Rectangle(width=1.6, height=0.5, fill_color=C_CAR, fill_opacity=0.9,
                     stroke_color=YELLOW_E, stroke_width=2)
    top = Rectangle(width=0.8, height=0.35, fill_color=C_CAR, fill_opacity=0.9,
                    stroke_color=YELLOW_E, stroke_width=2)
    top.next_to(body, UP, buff=0).shift(LEFT * 0.15)
    w1 = Circle(radius=0.18, fill_color=GRAY_D, fill_opacity=1,
                stroke_width=1).move_to(body.get_bottom() + LEFT * 0.5 + DOWN * 0.02)
    w2 = Circle(radius=0.18, fill_color=GRAY_D, fill_opacity=1,
                stroke_width=1).move_to(body.get_bottom() + RIGHT * 0.5 + DOWN * 0.02)
    return VGroup(body, top, w1, w2)


def make_road():
    y = ROAD_Y - 0.5
    line = Line([ROAD_X0 - 0.4, y, 0], [ROAD_X1 + 0.4, y, 0],
                color=C_ROAD, stroke_width=6)
    tick0 = Line([ROAD_X0, y, 0], [ROAD_X0, y + 0.25, 0], color=GRAY, stroke_width=3)
    tick1 = Line([ROAD_X1, y, 0], [ROAD_X1, y + 0.25, 0], color=GRAY, stroke_width=3)
    return VGroup(line, tick0, tick1)


CAP_Y0, CAP_DY = 3.45, 0.52


def cap_text(block: str, idx: int, font_size: int = 28):
    return Text(CAPTIONS[block][idx], font_size=font_size).move_to(
        [0, CAP_Y0 - idx * CAP_DY, 0])


GAUGE_C = [0, -0.9, 0]
GAUGE_R = 1.5
V_MAX = 16


def make_gauge():
    arc = Arc(radius=GAUGE_R, start_angle=0, angle=PI, color=GRAY,
              stroke_width=6).move_to(GAUGE_C)
    ticks = []
    for v in (0, 4, 8, 12, 16):
        ang = PI * (1 - v / V_MAX)
        direction = np.array([np.cos(ang), np.sin(ang), 0])
        p1 = np.array(GAUGE_C) + direction * (GAUGE_R - 0.2)
        p2 = np.array(GAUGE_C) + direction * GAUGE_R
        ticks.append(Line(p1, p2, color=GRAY, stroke_width=4))
    return VGroup(arc, *ticks)


def make_needle(v: float):
    ang = PI * (1 - v / V_MAX)
    tip = np.array(GAUGE_C) + 1.15 * np.array([np.cos(ang), np.sin(ang), 0])
    return Line(GAUGE_C, tip, color=C_A, stroke_width=6)


def make_readout(value: float):
    num = DecimalNumber(value, num_decimal_places=0, font_size=40,
                        color=C_V).move_to(np.array(GAUGE_C) + DOWN * 1.0)
    unit = Text(UNITS["vel"], font_size=30, color=C_V).next_to(num, RIGHT, buff=0.15)
    return num, unit


def make_vt_axes(x_length=5.6, y_length=3.0, center=[-2.2, -0.9, 0]):
    return Axes(x_range=[0, 5, 1], y_range=[0, 16, 2],
                x_length=x_length, y_length=y_length,
                axis_config={"include_tip": True, "color": C_AXIS}).move_to(center)


def axis_labels(ax):
    xl = Text(f"t, {UNITS['time']}", font_size=24, color=C_T).next_to(
        ax.x_axis.get_end(), DOWN, buff=0.15)
    yl = Text(f"v, {UNITS['vel']}", font_size=24, color=C_V).next_to(
        ax.y_axis.get_end(), RIGHT, buff=0.15)
    return VGroup(xl, yl)


class BlockB0(Scene):
    """Hook and goal, 20 s: j0a 6 + j0b 8 + j0c 6."""

    def construct(self):
        road, car = make_road(), make_car().move_to(road_point(0))
        cap0 = cap_text("B0", 0)
        num, unit = make_readout(V0)
        readout = VGroup(num, unit).move_to([4.6, 2.1, 0]).scale(0.8)
        # j0a (6): road + car + question.
        self.play(FadeIn(road), FadeIn(car), FadeIn(cap0), FadeIn(readout),
                  run_time=2)
        self.wait(4)
        # j0b (8): compressed journey T 0->4; speedo climbs 2->14.
        T = ValueTracker(0.0)
        car.add_updater(lambda m: m.move_to(road_point(x_of(T.get_value()))))
        num.add_updater(lambda m: m.set_value(v_of(T.get_value())))
        self.play(T.animate.set_value(T_END), run_time=8, rate_func=linear)
        car.clear_updaters()
        num.clear_updaters()
        num.set_value(V_END)
        car.move_to(road_point(S_END))
        # j0c (6): freeze + goal card.
        cap1 = cap_text("B0", 1)
        self.play(FadeIn(cap1), run_time=2)
        self.wait(4)


class BlockB1(Scene):
    """What 'uniformly accelerated' means, 50 s: 10+12+12+16."""

    def construct(self):
        # j1a (10): uniform-motion contrast, steady speedo + equal ticks.
        cap0 = cap_text("B1", 0)
        gauge = make_gauge()
        needle = make_needle(4)
        num, unit = make_readout(4)
        ticks = VGroup(*[
            Line([-3.0 + i * 1.2, ROAD_Y - 0.5, 0], [-3.0 + i * 1.2, ROAD_Y - 0.1, 0],
                 color=C_V, stroke_width=5)
            for i in range(4)])
        self.play(FadeIn(cap0), FadeIn(gauge), FadeIn(needle), FadeIn(num),
                  FadeIn(unit), run_time=2)
        for tick in ticks:
            self.play(FadeIn(tick), run_time=1.5)
            self.wait(0.5)
        # j1b (12): close-up, four equal +3 needle jumps.
        T = ValueTracker(0.0)
        dyn_needle = always_redraw(lambda: make_needle(v_of(T.get_value())))
        num.add_updater(lambda m: m.set_value(v_of(T.get_value())))
        self.add(dyn_needle)
        self.remove(needle)
        num.set_value(V0)
        plus_labels = []
        for i in range(4):
            self.play(T.animate.set_value(i + 1), run_time=2, rate_func=linear)
            lab = Text("+3", font_size=30, color=C_A).move_to(
                [-2.7 + i * 1.8, -2.9, 0])
            plus_labels.append(lab)
            self.play(FadeIn(lab), run_time=0.5)
            self.wait(0.5)
        num.clear_updaters()
        num.set_value(V_END)
        self.remove(dyn_needle)
        needle = make_needle(V_END)
        self.add(needle)
        # j1c (12): a-vector + definition + unit.
        cap1 = cap_text("B1", 1)
        cap2 = cap_text("B1", 2)
        self.play(FadeOut(VGroup(gauge, needle, num, unit, ticks, *plus_labels)),
                  run_time=2)
        avec = Arrow([-2.5, -0.9, 0], [0.5, -0.9, 0], color=C_A,
                     stroke_width=8, buff=0)
        alabel = Text("a", font_size=44, color=C_A).next_to(avec, UP, buff=0.2)
        self.play(Create(avec), FadeIn(alabel), run_time=3)
        self.play(FadeIn(cap1), run_time=2)
        self.play(FadeIn(cap2), run_time=2)
        self.wait(3)
        # j1d (16): Ox axis + sign rule + recap.
        cap3 = cap_text("B1", 3)
        axis = Arrow([-5.5, -2.2, 0], [5.5, -2.2, 0], color=C_AXIS,
                     stroke_width=5, buff=0)
        ox = Text("Ox", font_size=36, color=C_AXIS).next_to(axis.get_end(),
                                                            DOWN, buff=0.2)
        plus = Text("+", font_size=44, color=C_S).move_to([4.6, -1.5, 0])
        self.play(Create(axis), FadeIn(ox), run_time=4)
        self.play(FadeIn(cap3), FadeIn(plus), run_time=3)
        self.play(Indicate(avec, scale_factor=1.15), run_time=3)
        self.wait(6)


class BlockB2(Scene):
    """Velocity v = v0 + at, 40 s: j2a 12 + j2b 16 + j2c 12."""

    def construct(self):
        cap0 = cap_text("B2", 0)
        cap1 = cap_text("B2", 1)
        # j2a (12): formula assembles in coloured parts.
        p1 = Text("v =", font_size=52, color=C_V).move_to([-3.6, -0.5, 0])
        p2 = Text("v₀", font_size=52, color=C_V).move_to([-1.9, -0.5, 0])
        p3 = Text("+", font_size=52).move_to([-0.9, -0.5, 0])
        p4 = Text("at", font_size=52, color=C_A).move_to([0.4, -0.5, 0])
        self.play(Write(p1), FadeIn(cap0), run_time=3)
        for part in (p2, p3, p4):
            self.play(Write(part), run_time=3)
        # j2b (16): numeric substitution + result box.
        self.play(FadeIn(cap1), run_time=4)
        box = SurroundingRectangle(cap1, color=C_S, buff=0.15)
        self.play(Create(box), run_time=3)
        self.wait(9)
        # j2c (12): unit check + stamp.
        units = Text(f"({UNITS['acc']})·{UNITS['time']} → {UNITS['vel']}",
                     font_size=40).move_to([0, -2.2, 0])
        stamp = Text("✓", font_size=64, color=C_S).move_to([4.9, -2.2, 0])
        self.play(FadeIn(units), run_time=4)
        self.play(FadeIn(stamp), run_time=3)
        self.wait(5)


class BlockB3(Scene):
    """Displacement s = v0t + at^2/2, 50 s: j3a 12 + j3b 14 + j3c 24."""

    def construct(self):
        road = make_road()
        # j3a (12): displacement arrow + direction guard.
        cap2 = cap_text("B3", 2)
        arrow = Arrow(road_point(0) + UP * 0.7, road_point(S_END) + UP * 0.7,
                      color=C_S, stroke_width=8, buff=0)
        self.play(FadeIn(road), Create(arrow), run_time=4)
        self.play(FadeIn(cap2), run_time=4)
        self.wait(4)
        # j3b (14): two coloured terms.
        cap0 = cap_text("B3", 0)
        term1 = Text("v₀t", font_size=52, color=C_V).move_to([-3.4, 0.0, 0])
        term2 = Text("at²/2", font_size=52, color=C_A).move_to([-1.2, 0.0, 0])
        self.play(Write(term1), run_time=4)
        self.play(Write(term2), run_time=4)
        self.play(FadeIn(cap0), run_time=3)
        self.wait(3)
        # j3c (24): bars grow with T; car replays x(T); totals 8+24=32.
        GROUND = -2.0
        BAR_H = 2.4
        car = make_car().move_to(road_point(0))
        self.add(car)
        T = ValueTracker(0.0)
        self.play(FadeOut(arrow), run_time=2)

        def bar_h1():
            return max(0.03, (V0 * T.get_value()) / S_END * BAR_H)

        def bar_h2():
            return max(0.03, (0.5 * A * T.get_value() ** 2) / S_END * BAR_H)

        def bar1():
            h = bar_h1()
            return Rectangle(width=1.4, height=h, fill_color=C_V,
                             fill_opacity=0.8, stroke_width=1).move_to(
                                 [-3.4, GROUND + h / 2, 0])

        def bar2():
            h = bar_h2()
            return Rectangle(width=1.4, height=h, fill_color=C_A,
                             fill_opacity=0.8, stroke_width=1).move_to(
                                 [-1.2, GROUND + h / 2, 0])

        def upd1(m):
            m.set_value(V0 * T.get_value())
            m.move_to([-3.4, GROUND + bar_h1() + 0.3, 0])

        def upd2(m):
            m.set_value(0.5 * A * T.get_value() ** 2)
            m.move_to([-1.2, GROUND + bar_h2() + 0.3, 0])

        def upd_car(m):
            m.move_to(road_point(x_of(T.get_value())))

        d1, d2 = always_redraw(bar1), always_redraw(bar2)
        n1 = DecimalNumber(0, num_decimal_places=0, font_size=32, color=C_V)
        n2 = DecimalNumber(0, num_decimal_places=0, font_size=32, color=C_A)
        n1.add_updater(upd1)
        n2.add_updater(upd2)
        car.add_updater(upd_car)
        self.add(d1, d2, n1, n2)
        self.play(T.animate.set_value(T_END), run_time=18, rate_func=linear)
        for m in (d1, d2, n1, n2, car):
            m.clear_updaters()
        self.remove(d1, d2, n1, n2)
        cap1 = cap_text("B3", 1)
        fh1 = (V0 * T_END) / S_END * BAR_H
        fh2 = (0.5 * A * T_END ** 2) / S_END * BAR_H
        fb1 = Rectangle(width=1.4, height=fh1, fill_color=C_V,
                        fill_opacity=0.8, stroke_width=1).move_to(
                            [-3.4, GROUND + fh1 / 2, 0])
        fb2 = Rectangle(width=1.4, height=fh2, fill_color=C_A,
                        fill_opacity=0.8, stroke_width=1).move_to(
                            [-1.2, GROUND + fh2 / 2, 0])
        fl1 = Text(f"{V0 * T_END}", font_size=32, color=C_V).move_to(
            [-3.4, GROUND + fh1 + 0.3, 0])
        fl2 = Text(f"{int(0.5 * A * T_END ** 2)}", font_size=32,
                   color=C_A).move_to([-1.2, GROUND + fh2 + 0.3, 0])
        self.play(FadeIn(cap1), FadeIn(fb1), FadeIn(fb2), FadeIn(fl1),
                  FadeIn(fl2), run_time=2)
        self.wait(2)


class BlockB4(Scene):
    """Graph v(t), 40 s: j4a 14 + j4b 14 + j4c 12."""

    def construct(self):
        ax = make_vt_axes()
        labels = axis_labels(ax)
        cap0 = cap_text("B4", 0)
        # j4a (14): axes + self-drawing line with tracer.
        self.play(Create(ax), FadeIn(labels), FadeIn(cap0), run_time=4)
        T = ValueTracker(0.0)
        dyn_line = always_redraw(lambda: ax.plot(
            v_of, x_range=[0, max(T.get_value(), 0.02)], color=C_V))
        tracer = always_redraw(lambda: Dot(
            ax.c2p(T.get_value(), v_of(T.get_value())), color=YELLOW, radius=0.09))
        self.add(dyn_line, tracer)
        self.play(T.animate.set_value(T_END), run_time=10, rate_func=linear)
        self.remove(dyn_line, tracer)
        line = ax.plot(v_of, x_range=[0, T_END], color=C_V)
        dot = Dot(ax.c2p(T_END, V_END), color=YELLOW, radius=0.09)
        self.add(line, dot)
        # j4b (14): slope triangle dv/dt -> a = 3.
        cap1 = cap_text("B4", 1)
        p0, p1, p2 = ax.c2p(0, V0), ax.c2p(T_END, V0), ax.c2p(T_END, V_END)
        base = Line(p0, p1, color=C_T, stroke_width=5)
        rise = Line(p1, p2, color=C_V, stroke_width=5)
        dt_lab = Text(f"Δt = {T_END}", font_size=26, color=C_T).next_to(
            base.get_center(), DOWN, buff=0.15)
        dv_lab = Text(f"Δv = {V_END - V0}", font_size=26, color=C_V).next_to(
            rise.get_center(), RIGHT, buff=0.15)
        aval = Text(f"a = {A}", font_size=40, color=C_A).move_to([4.3, 0.6, 0])
        self.play(Create(base), Create(rise), FadeIn(dt_lab), FadeIn(dv_lab),
                  run_time=5)
        self.play(FadeIn(aval), run_time=4)
        self.play(FadeIn(cap1), run_time=3)
        self.wait(2)
        # j4c (12): rule frozen.
        box = SurroundingRectangle(cap1, color=C_A, buff=0.15)
        self.play(Create(box), run_time=4)
        self.wait(8)


class BlockB5(Scene):
    """Area check, 30 s: j5a 16 + j5b 14."""

    def construct(self):
        ax = make_vt_axes(x_length=5.2, y_length=2.6, center=[-2.6, -0.6, 0])
        labels = axis_labels(ax)
        line = ax.plot(v_of, x_range=[0, T_END], color=C_V)
        road, car = make_road(), make_car().move_to(road_point(0))
        cap0 = cap_text("B5", 0)
        # j5a (16): trapezoid fills in sync with the car; counter runs to 32.
        self.play(Create(ax), FadeIn(labels), FadeIn(line), FadeIn(road),
                  FadeIn(car), FadeIn(cap0), run_time=4)
        T = ValueTracker(0.0)
        fill = always_redraw(lambda: ax.get_area(
            line, x_range=[0, max(T.get_value(), 0.02)], color=C_S, opacity=0.35))
        counter = DecimalNumber(0, num_decimal_places=0, font_size=56, color=C_S)
        counter.move_to([4.3, 0.2, 0])
        cunit = Text(UNITS["dist"], font_size=36, color=C_S).next_to(
            counter, RIGHT, buff=0.15)
        counter.add_updater(lambda m: m.set_value(
            V0 * T.get_value() + 0.5 * A * T.get_value() ** 2))
        car.add_updater(lambda m: m.move_to(road_point(x_of(T.get_value()))))
        self.add(fill, counter, cunit)
        self.play(T.animate.set_value(T_END), run_time=12, rate_func=linear)
        fill.clear_updaters()
        counter.clear_updaters()
        car.clear_updaters()
        counter.set_value(S_END)
        car.move_to(road_point(S_END))
        # j5b (14): stamp — 32 matches 32.
        cap1 = cap_text("B5", 1)
        stamp = Text("✓", font_size=72, color=C_S).move_to([4.3, -1.6, 0])
        self.play(FadeIn(cap1), FadeIn(stamp), run_time=5)
        self.wait(9)


class BlockB6(Scene):
    """Pause task, 30 s: j6a 10 + j6b 12 + j6c 8."""

    def construct(self):
        # j6a (10): condition card, no solution visible. The card itself shows
        # caption B6[0], so no separate top-band copy (avoids duplication).
        card = Rectangle(width=10.0, height=1.6, color=GRAY, stroke_width=3)
        card.move_to([0, 0.4, 0])
        cond = Text(CAPTIONS["B6"][0], font_size=30).move_to(card.get_center())
        self.play(Create(card), FadeIn(cond), run_time=4)
        self.wait(6)
        # j6b (12): pause card with pulsing icon (no numbers tick).
        cap1 = cap_text("B6", 1)
        icon = VGroup(
            Rectangle(width=0.45, height=1.4, fill_color=WHITE, fill_opacity=0.95,
                      stroke_width=0).move_to([-0.35, -1.8, 0]),
            Rectangle(width=0.45, height=1.4, fill_color=WHITE, fill_opacity=0.95,
                      stroke_width=0).move_to([0.35, -1.8, 0]))
        self.play(FadeIn(icon), FadeIn(cap1), run_time=3)
        for _ in range(3):
            self.play(icon.animate.scale(1.1), run_time=1)
            self.play(icon.animate.scale(1 / 1.1), run_time=1)
        self.wait(3)
        # j6c (8): short solution revealed after the pause.
        cap2 = cap_text("B6", 2)
        steps = Text(f"0·{B6['t']} + {B6['a']}·{B6['t'] ** 2}/2",
                     font_size=40).move_to([0, -1.8, 0])
        self.play(FadeOut(icon), FadeIn(steps), FadeIn(cap2), run_time=3)
        box = SurroundingRectangle(cap2, color=C_S, buff=0.15)
        self.play(Create(box), run_time=1)
        self.wait(4)


class BlockB7(Scene):
    """Traps and recap, 40 s: j7a 14 + j7b 12 + j7c 14."""

    def construct(self):
        # j7a (14): trap E1 crossed out. The big trap text IS caption B7[0],
        # so no separate top-band copy (avoids duplication).
        trap = Text(CAPTIONS["B7"][0], font_size=56).move_to([0, 0.6, 0])
        self.play(FadeIn(trap), run_time=5)
        cross = Cross(trap, color=RED, stroke_width=8)
        self.play(Create(cross), run_time=4)
        hint = Text(FORMULAS["F-avg"], font_size=44, color=C_S).move_to([0, -1.4, 0])
        self.play(FadeIn(hint), run_time=3)
        self.wait(2)
        # j7b (12): slope (red arrow) vs area (green fill) side by side.
        cap1 = cap_text("B7", 1)
        self.play(FadeOut(VGroup(trap, cross, hint)), run_time=2)
        ax_l = make_vt_axes(x_length=2.6, y_length=1.8, center=[-3.6, -1.2, 0])
        ax_r = make_vt_axes(x_length=2.6, y_length=1.8, center=[3.6, -1.2, 0])
        line_l = ax_l.plot(v_of, x_range=[0, T_END], color=C_V)
        line_r = ax_r.plot(v_of, x_range=[0, T_END], color=C_V)
        sparr = Arrow(ax_l.c2p(1, v_of(1)), ax_l.c2p(3, v_of(3)), color=C_A,
                      stroke_width=7, buff=0)
        sfill = ax_r.get_area(line_r, x_range=[0, T_END], color=C_S, opacity=0.4)
        self.play(Create(ax_l), Create(line_l), Create(sparr), run_time=4)
        self.play(Create(ax_r), Create(line_r), FadeIn(sfill), FadeIn(cap1),
                  run_time=4)
        self.wait(2)
        # j7c (14): formula triptych + ENT bridge.
        cap2 = cap_text("B7", 2)
        parts = [p.strip() for p in CAPTIONS["B7"][2].split(";")]
        formulas = VGroup(*[
            Text(parts[0], font_size=40, color=C_V).move_to([-3.4, 0.4, 0]),
            Text(parts[1], font_size=40, color=C_S).move_to([2.6, 0.4, 0]),
            Text(FORMULAS["F-avg"], font_size=40, color=C_T).move_to([0, -0.7, 0])])
        self.play(FadeOut(VGroup(ax_l, line_l, sparr, ax_r, line_r, sfill)),
                  FadeIn(formulas), FadeIn(cap2), run_time=6)
        bridge = Text("✓", font_size=64, color=C_S).move_to([0, -2.2, 0])
        self.play(FadeIn(bridge), run_time=4)
        self.wait(4)
