from manim import *


class Scene1(ThreeDScene):
    def construct(self):
        # 1. 问题引入
        question = Text("由3D点云构成的平面", font_size=36, color=BLUE)
        question.to_corner(UL)
        self.add_fixed_in_frame_mobjects(question)
        self.play(Write(question))
        self.wait(1)

        intro_text = Text("一组点云", font_size=28)
        intro_formula = MathTex(
            r"\mathbf{P} = \left\{ \mathbf{p}_1, \mathbf{p}_2, \ldots, \mathbf{p}_n \right\}",
        )
        intro_text1 = Text("其中每个点的值是：", font_size=28)
        intro_formula1 = MathTex(
            r"\mathbf{p}_i = \begin{bmatrix} x_i \\ y_i \\ z_i \end{bmatrix}",
        )

        intro_goal = VGroup(
            Text("目标：找到一个平面，其方程由单位法向量构成", font_size=28)
        ).arrange(DOWN)
       
        intro_group_left = VGroup(
            intro_text,
            intro_formula,
            intro_text1,
            intro_formula1,
        ).arrange(DOWN, buff=0.4)

        intro_goal.next_to(intro_group_left, DOWN)  

        self.play(
            LaggedStartMap(Write, intro_group_left, lag_ratio=0.5)
        )

        framebox1 = SurroundingRectangle(intro_formula, buff = .1)
        framebox2 = SurroundingRectangle(intro_formula1, buff = .1)

        self.play(
            Create(framebox1), 
            run_time = 1
        )
        
        self.wait(1)

        self.play(
            Uncreate(framebox1),
            Create(framebox2),
            run_time = 1.5
        )
        
        self.wait(1)

        self.play(
            FadeOut(framebox2),
            run_time = 0.5
        )
    
        self.wait(2)
        

        self.play(Write(intro_goal))

        self.wait(2)
        
        self.play(
            Uncreate(intro_group_left),
            Uncreate(intro_goal)
        )
        self.wait(1)

        normal_text = MathTex(
            r"\vec{n} = \begin{bmatrix} a \\ b \\ c \end{bmatrix}",
        )
        normal_text_constaint = Text("且满足:", font_size=28)
        # 描述向量n是归一化的: ||n||_2 = 1
        normalized_vector_text = MathTex(
            r"\|\vec{n}\|_2 = 1"
        )
        
  
        point_on_plane_text = Text("平面上的一点 P₀，方程为：", font_size=28)
        point_on_plane_formula = MathTex(
            r"\vec{n}^{\mathsf T}(\mathbf{P} - \mathbf{P}_0) = 0",
        )
        point_on_plane = VGroup(point_on_plane_text, point_on_plane_formula).arrange(DOWN, buff=0.3)


        # function = MathTex(
        #     r"\vec{n}^{\mathsf T}\left( \mathbf{P} - \mathbf{P}_0 \right) = 0",
        # )

        function_explain = MathTex(
            r"\quad a(x - x_0) + b(y - y_0) + c(z - z_0) = 0",
        )

        intro_group_right = VGroup(
            normal_text,
            normal_text_constaint,
            normalized_vector_text,
            point_on_plane           
        ).arrange(DOWN, buff=0.4).next_to(question, DOWN + RIGHT * 0.1, buff=0.5)

        function_explain.next_to(question, DOWN + RIGHT * 0.1, buff=0.2)

        # intro_group_right.move_to(ORIGIN)
    
        self.play(
            LaggedStartMap(Write, intro_group_right, lag_ratio = 0.5)
        )

        framebox3 = SurroundingRectangle(normalized_vector_text, buff = .1)
        framebox4 = SurroundingRectangle(point_on_plane_formula, buff = .1)

        self.wait(1)

        self.play(
            Create(framebox3), 
            run_time = 0.5
        )
        
        self.wait(1)

        self.play(
            Uncreate(framebox3),
            Create(framebox4),
            run_time = 1.5
        )

        self.wait(1.5)

        self.play(
            FadeOut(framebox4),
            run_time = 0.5
        )

        self.wait(1)

        self.play(Uncreate(intro_group_right))

        self.wait(1)
        
        self.play(Write(function_explain))
        
        self.wait(2)

        self.play(function_explain.animate.shift(ORIGIN + DOWN))
        
        self.play(function_explain.animate.scale(1.2))
        
        self.wait(1) 

        self.play(Uncreate(function_explain))

        self.wait(1)

        self.play(
            question.animate.shift(RIGHT),
            question.animate.set_fill(WHITE),
            run_time = 1.5
        )

        self.wait(1)
        
        # 问题定义的转换
        minimize_explain = Text("计算各个点p投影到该平面的平方和",font_size=36)
     
        
        minimize_math = MathTex(
            r"\mathbf{d}_i^2 = \left| \mathbf{n}^T (\mathbf{p} - \mathbf{P}_0) \right|^2"
        )
        
        minimize_group = VGroup(minimize_explain, minimize_math).arrange(DOWN, buff=0.1)
        minimize_group.next_to(question, DOWN, buff=0.1).shift(RIGHT * 3)
        self.play(ReplacementTransform(question, minimize_explain), run_time=2)
        
        self.wait(1)
    
        # TODO: 此时问题就转化成了 如何拟合一个平面。
         # Step 1: 投影误差定义
        eq1 = MathTex(
            r"d_i^2 = \left[\mathbf{n}^T(\mathbf{p}_i - \mathbf{P}_0)\right]^2"
        ).next_to(minimize_group, DOWN * 0.3)
        self.play(Write(eq1))
        self.wait(1)

        # Step 2: 结论 -> P0取点云质心（避免在 Tex 中使用中文，拆分为 Text + MathTex）
        conclusion_left = Text("可以证明，当 ", font_size=28)
        conclusion_mid = MathTex(r"\mathbf{P}_0")
        conclusion_right = Text(" 为点云质心时，误差最小", font_size=28)
        conclusion = VGroup(conclusion_left, conclusion_mid, conclusion_right).arrange(RIGHT, buff=0.12).scale(0.8)
        conclusion.next_to(eq1, DOWN * 0.5)
        self.play(Write(conclusion))
        self.wait(1)

        eq2 = MathTex(
            r"\bar{\mathbf{P}} = \frac{1}{N} \sum_{i=1}^N \mathbf{p}_i"
        ).next_to(conclusion, DOWN * 0.5)
        self.play(Write(eq2))
        self.wait(1)

        eq3 = MathTex(
            r"\min_{\mathbf{n}} \sum_{i=1}^N \left[\mathbf{n}^T(\mathbf{p}_i - \bar{\mathbf{P}})\right]^2",
            r", \quad \mathbf{n}^T\mathbf{n}=1"
        ).next_to(eq2, DOWN * 0.3)
        self.play(Write(eq3))
        self.wait(1)

        self.play(
            Uncreate(minimize_explain),
            Uncreate(eq1),
            Uncreate(conclusion),
            Uncreate(eq2),
        )

        self.wait(1)

        self.play(eq3.animate.shift(UP * 4.5))

        framebox5 = SurroundingRectangle(eq3, buff = .1)
        
        self.play(
            Create(framebox5)
        )

        self.wait(1)

        self.play(
            Uncreate(framebox5)
        )

        eq4 = Text(
            r"因此优化的目标就变成了最小化投影距离的和",
            font_size=28
        ).next_to(eq3, DOWN * 0.2)
        self.play(Write(eq4))
        self.wait(1)

        eq5_description = Text("定义去中心化后的点集为：", font_size=28)
        eq5  = MathTex(r"p_i' = p_i - \bar{p}")
        eq5_description.move_to(eq4.get_center() + DOWN).align_to(eq4, LEFT)
        eq5.move_to(eq5_description.get_center() + DOWN).align_to(eq4, LEFT)
        self.play(Write(eq5_description), Write(eq5))

        framebox6 = SurroundingRectangle(eq5, buff = 0.1)

        note1 = Text("则优化目标可以改写为: ", font_size=28)
        note1.move_to(eq5.get_center() + DOWN).align_to(eq5, LEFT)
        self.wait(1)

        self.play(Create(framebox6))

        self.wait(2)

        self.play(
            Uncreate(eq3),
            Uncreate(eq4),
            Uncreate(eq5),
            Uncreate(eq5_description),
            Uncreate(framebox6)
        )

        self.play(Write(note1))
        self.play(note1.animate.shift(UP * 4))

        eq6 = MathTex(r"\arg\min_{n}\ \frac{1}{N}\sum_{i=1}^{N}\big(n^{T}p_i'\big)^2")
        eq6.next_to(note1, DOWN, buff=0.2).align_to(note1, LEFT)
        self.play(Write(eq6))
        self.wait(1)

        eq7   = MathTex(
            r"\frac{1}{N}\sum_{i=1}^{N} n^{T}p_i'(p_i'^{T}n)"
            r" \;=\; n^{T}\!\left(\frac{1}{N}\sum_{i=1}^{N} p_i' p_i'^{T}\right)\!n",
        )
        eq7.next_to(eq6, DOWN).align_to(eq6, LEFT)
        self.play(Write(eq7))
        self.wait(1)


        note2 = Text("由协方差矩阵的定义:", font_size=28)
        note2.next_to(eq7, DOWN).align_to(eq7, LEFT)
        self.play(Write(note2))
        self.wait(1)

        eq8  = MathTex(r"C = \frac{1}{N}\sum_{i=1}^{N}(p_i-\bar{p})(p_i-\bar{p})^{T}")
        eq8.next_to(note2, DOWN).align_to(note2, LEFT)
        self.play(Write(eq8))
        self.wait(1)

        self.play(
            Uncreate(note1),
            Uncreate(eq6),
            Uncreate(eq7)
        )
        self.wait(1)
        
        self.play(
            note2.animate.shift(UP * 4),
            eq8.animate.shift(UP * 4)
        )

        eq9 = MathTex(r"\frac{1}{N}\sum_{i=1}^{N} p_i' p_i'^{T} \;=\; C")
        eq9.next_to(eq8, DOWN).align_to(eq8, LEFT)
        self.play(Write(eq9))
        self.wait(1)

        note3 = Text("因此优化问题变为:", font_size=28, color=GREEN)
        note3.next_to(eq9, DOWN).align_to(eq9, LEFT)
        self.play(Write(note3))
        self.wait(1)

        eq10 = MathTex(r"\arg\min_{n}\ n^{T} C\, n")
        eq10.next_to(note3, RIGHT * 2)
        self.play(Write(eq10))
        self.wait(1)

        eq11 = MathTex(r"n^{T} n = 1", color=BLUE_A)
        eq11.next_to(eq10, RIGHT * 2)
        self.play(Write(eq11))
        self.wait(1)

        framebox7 = SurroundingRectangle(eq11, buff=0.1)
        self.play(Create(framebox7))

        self.wait(1)

        self.play(
            Uncreate(framebox7),
            Uncreate(eq8),
            Uncreate(eq9),
            Uncreate(note2),
            Uncreate(eq10),
            Uncreate(eq11),
            Uncreate(note3)
        )

        self.wait(1)