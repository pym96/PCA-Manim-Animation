from manim import *
import numpy as np

from manim import *

class Scene4(Scene):
    def construct(self):

        A_description = Text("A = ", font_size=24)
        A_description.to_edge(LEFT).shift(UP * 2)
        A = np.array([[3.0, 1.0],
                      [1.0, 2.0]])

        vector_tex =  MathTex(
                r"\mathbf{x}(\theta) = \begin{pmatrix} \cos(\theta) \\ \sin(\theta) \end{pmatrix}",
                font_size=40
            )
        

        # Create a Matrix object
        matrix_A = Matrix(A,element_to_mobject=lambda e: MathTex(str(e), font_size=24))
        matrix_A.next_to(A_description)
        vector_tex.next_to(matrix_A, RIGHT)
        
        eigvals, eigvecs = np.linalg.eig(A)
        idx = np.argsort(eigvals)
        lam_min, lam_max = eigvals[idx[0]], eigvals[idx[-1]]
        v_min, v_max = eigvecs[:, idx[0]], eigvecs[:, idx[-1]]

        # -- Title --
        title = Text("Rayleigh Quotient(瑞利商)", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

         # -- Definition group
        def_line1 = VGroup(
            Text("定义：", font_size=28),
            MathTex(r"R_A(x)", "=", r"\frac{x^T A x}{x^T x}", font_size=28)
        ).arrange(RIGHT, aligned_edge=DOWN)
        # def_line1.to_edge(RIGHT).shift(UP * 0.5)
        def_line1.next_to(A_description, DOWN, buff=1.2, aligned_edge=LEFT)

        def_line2 = VGroup(
            Text("物理/几何意义：", font_size=24),
            MathTex(r"x^T A x", "=", r"\text{weighted length}", font_size=24)
        ).arrange(RIGHT, aligned_edge=DOWN)
        # def_line2.next_to(def_line1, DOWN, aligned_edge=LEFT)
        def_line2.next_to(def_line1, DOWN, aligned_edge=LEFT)
        
        # Display the matrix on the screen
        self.play(
            Write(A_description),
            Write(matrix_A),
            Write(vector_tex)
        )
        self.wait(2)

        self.play(FadeIn(def_line1, shift=UP), FadeIn(def_line2, shift=UP))
        self.wait(1)

         # -- Plane: unit circle and ellipse level set --
        axes = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=6, y_length=6)
        axes.center()
        axes.to_edge(RIGHT)

        circle = Circle(radius=1.0).move_to(axes.c2p(0,0)).set_style(stroke_width=2, stroke_color=BLUE)
        circle_label = Text("unit circle", font_size=20, color=BLUE)
        circle_label.next_to(circle, UP+RIGHT)

        def ellipse_points(num=200):
            thetas = np.linspace(0, TAU, num)
            pts = []
            for t in thetas:
                u = np.array([np.cos(t), np.sin(t)])
                denom = u.T @ A @ u
                r = 1.0 / np.sqrt(denom)
                p = r * u
                pts.append(axes.c2p(p[0], p[1]))
            return pts

        ellipse = VMobject()
        ellipse.set_points_smoothly(ellipse_points())
        ellipse.set_style(stroke_width=2, stroke_color=RED)
        ellipse_label = MathTex(r"x^T A x = 1", font_size=20, color=RED)
        ellipse_label.next_to(ellipse, DOWN+LEFT)


        self.play(Create(axes), Create(circle), FadeIn(circle_label))
        self.play(Create(ellipse), FadeIn(ellipse_label))
        self.wait(0.6)

         # -- Rotating vector on unit circle --
        angle = ValueTracker(0.0)

        def get_vector():
            t = angle.get_value()
            x = np.array([np.cos(t), np.sin(t)])
            tip = axes.c2p(x[0], x[1])
            return Arrow(axes.c2p(0,0), tip, buff=0, stroke_width=3)

        rotating_vec = always_redraw(get_vector)
        self.play(Create(rotating_vec))

        def get_tip_label():
            t = angle.get_value()
            x = np.array([np.cos(t), np.sin(t)])
            tex = MathTex(r"x(\theta)", font_size=24)
            tex.move_to(axes.c2p(x[0], x[1]) + 0.3 * RIGHT + 0.2 * UP)
            return tex

        tip_label = always_redraw(get_tip_label)
        self.add(tip_label)

         # -- Rayleigh quotient value
        def get_rayleigh_value():
            t = angle.get_value()
            x = np.array([np.cos(t), np.sin(t)])
            val = (x.T @ A @ x) / (x.T @ x)
            return val

        rq_val = DecimalNumber(0.0, num_decimal_places=4)
        rq_val.to_edge(RIGHT).shift(UP * 0.5)

        rq_label = VGroup(
            MathTex(r"R_A(x)", font_size=24),
            rq_val
        ).arrange(RIGHT)
        rq_label.to_edge(LEFT).shift(DOWN * 1)

        rq_val.add_updater(lambda m: m.set_value(get_rayleigh_value()))
        self.play(FadeIn(rq_label))
        self.wait(0.5)

        # -- Eigenvalue range text
        ev_text = Text(f"min eigenvalue = {lam_min:.4f}, max eigenvalue = {lam_max:.4f}", font_size=24)
        # ev_text.to_edge(DOWN)
        ev_text.next_to(axes, DOWN, aligned_edge=LEFT).shift(LEFT * 0.5)


        # -- Small plot R(theta) vs theta
        plot_axes = Axes(x_range=[0, TAU, PI/2], y_range=[lam_min - 0.5, lam_max + 0.5, 1], x_length=5, y_length=2.5)
        plot_axes.to_edge(LEFT).shift(DOWN * 2.5)

        thetas = np.linspace(0, TAU, 400)
        r_vals = [(np.array([np.cos(t), np.sin(t)]).T @ A @ np.array([np.cos(t), np.sin(t)])) for t in thetas]
        graph_points = [plot_axes.c2p(t, r) for t, r in zip(thetas, r_vals)]
        rq_graph = VMobject()
        rq_graph.set_points_smoothly(graph_points)
        rq_graph.set_style(stroke_width=2)

        self.play(Create(plot_axes), Create(rq_graph))
        self.wait(0.6)

        marker = Dot().move_to(plot_axes.c2p(0, r_vals[0]))
        marker.add_updater(lambda m: m.move_to(plot_axes.c2p(angle.get_value() % TAU, get_rayleigh_value())))
        self.add(marker)

        # Animate rotation
        self.play(angle.animate.set_value(TAU), run_time=8, rate_func=there_and_back)
        self.wait(0.8)

        rq_val.clear_updaters()
        marker.clear_updaters()

        self.play(FadeOut(marker), FadeOut(rotating_vec), FadeOut(tip_label))
        self.wait(0.6)

        # Highlight eigenvector directions
        v_min_arrow = Arrow(axes.c2p(0,0), axes.c2p(*v_min), buff=0, color=YELLOW)
        v_max_arrow = Arrow(axes.c2p(0,0), axes.c2p(*v_max), buff=0, color=ORANGE)
        self.play(GrowArrow(v_min_arrow), GrowArrow(v_max_arrow))
        self.wait(0.6)

        self.play(Write(ev_text))
        self.wait(0.6)

        framebox1 = SurroundingRectangle(ev_text, buff=0.1)
        self.play(
            Create(framebox1)
        )
        self.wait(0.6)

        # TODO: Uncreate直到留出足够的空间，然后结合scene4.py的内容进行最大值+最小值
        # -- Small plot R(theta) vs theta
        # Final text
        end_text = Text("在特征向量方向上，Rayleigh 商取到特征值", font_size=28, color=YELLOW)
        end_tex = MathTex(r"R_A(x)=\lambda", font_size=28, color=YELLOW)
        end_group = VGroup(end_text, end_tex).arrange(RIGHT, aligned_edge=DOWN)
        # end_group.to_edge(DOWN)
        # self.play(Write(end_group))
        # self.wait(2)

         # maximum 性质
        maximum_text = Text(
            "最大值 ⇒ 最大特征值 ", font_size=28, color=GREEN
        )
        maximum_lambda = MathTex(
            r"\lambda_{\max}", font_size=28, color=GREEN
        ).next_to(maximum_text, RIGHT, buff=0.1)
        maximum_eigenvector = Text(
            "，对应于最大特征向量", font_size=28, color=GREEN
        ).next_to(maximum_lambda, RIGHT, buff=0.1)
        maximum_group = VGroup(maximum_text, maximum_lambda, maximum_eigenvector)
        # maximum_group.next_to(rayleigh_quotient_explain2_group, DOWN, buff=0.6, aligned_edge=LEFT)
        # self.play(Write(maximum_group))
        # self.wait(2)

        # minimum 性质
        minimum_text = Text(
            "最小值 ⇒ 最小特征值 ", font_size=28, color=GREEN
        )
        minimum_lambda = MathTex(
            r"\lambda_{\min}", font_size=28, color=GREEN
        ).next_to(minimum_text, RIGHT, buff=0.1)
        minimum_eigenvector = Text(
            "，对应于最小特征向量", font_size=28, color=GREEN
        ).next_to(minimum_lambda, RIGHT, buff=0.1)
        minimum_group = VGroup(minimum_text, minimum_lambda, minimum_eigenvector)
        minimum_group.next_to(maximum_group, DOWN, buff=0.4, aligned_edge=LEFT)
        # self.play(Write(minimum_group))
        # self.wait(10)

        self.play(
            Uncreate(framebox1),
            Uncreate(A_description),
            Uncreate(matrix_A),
            Uncreate(vector_tex),
            Uncreate(def_line1),
            Uncreate(def_line2)
        )

        self.wait(2)

        maximum_group.to_edge(LEFT).shift(UP * 2)
        minimum_group.next_to(maximum_group, DOWN, aligned_edge=LEFT)

        self.play(Write(maximum_group))
        self.wait(2)

        self.play(Write(minimum_group))
        self.wait(2)

        end_group.next_to(minimum_group, DOWN, aligned_edge=LEFT)

        framebox2 = SurroundingRectangle(end_group, buff=0.1)
        self.play(Write(end_group))
        self.wait(1)

        self.play(
            Create(framebox2)
        )

        self.wait(2)

        self.play(
            Uncreate(title),
            Uncreate(axes),
            Uncreate(circle_label),
            Uncreate(ellipse_label),
            Uncreate(ev_text),
            Uncreate(plot_axes),
            Uncreate(rq_graph),
            Uncreate(maximum_group),
            Uncreate(minimum_group),
            Uncreate(framebox2),
            Uncreate(v_min_arrow),
            Uncreate(v_max_arrow),
            Uncreate(circle),
            Uncreate(ellipse),
            Uncreate(end_group),
            Uncreate(rq_label)
        )

        self.wait(2)

        # self.play(
        #     Uncreate(A_description),
        #     Uncreate(matrix_A)
        # )