from manim import *
from manim_voiceover import VoiceoverScene
import numpy as np

class Scene3(ThreeDScene):
    def construct(self):

        # 且满足:
        rayleigh_quotient_quota = Text(
            "优化目标:", font_size=28
        )
        rayleigh_quotient_quota.to_corner(UL)

        # 描述向量n是归一化的: ||n||_2 = 1
        rayleigh_quotient_formula = MathTex(
            r"\arg\min_{n} \; n^T C n", font_size=36
        ).next_to(rayleigh_quotient_quota, DOWN, aligned_edge=LEFT)

        self.play(
            Write(rayleigh_quotient_quota),
            Write(rayleigh_quotient_formula)
        )

        self.wait(2)

        # 解释文字
        rayleigh_quotient_explain1 = Text(
            "这是一个瑞利商问题", font_size=28
        ).next_to(rayleigh_quotient_formula, DOWN, aligned_edge=LEFT)
        self.play(Write(rayleigh_quotient_explain1))

        self.wait(2)

        rayleigh_quotient_explain2 = Text(
            "对于实对称矩阵 C，瑞利商问题：",
            font_size=28,
        )
        rayleigh_quotient_explain2_formula = MathTex(
            r"n^T C n, n^T n = 1", 
        )

  
        rayleigh_quotient_explain2_lastpart = Text(
        "有以下性质：", font_size=28
        )

        rayleigh_quotient_explain2_group = VGroup(rayleigh_quotient_explain2, 
                                                  rayleigh_quotient_explain2_formula
                                                  ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        
        rayleigh_quotient_explain2_group.next_to(
            rayleigh_quotient_explain1, DOWN, buff=0.4, aligned_edge=LEFT
        )


        self.play(Write(rayleigh_quotient_explain2_group))
        self.wait(2)

        framebox1 = SurroundingRectangle(rayleigh_quotient_explain2_group, buff=.1)
        self.play(Create(framebox1))
        self.wait(4)

        self.play(Uncreate(framebox1))
        self.wait(4)


        self.play(Write(rayleigh_quotient_explain2_lastpart))
        self.wait(2)

        framebox2 = SurroundingRectangle(rayleigh_quotient_explain2_group[1], buff=.1)
        self.play(Create(framebox2))

        # maximum 性质
        maximum_text = Text(
            "最大值 ⇒ C 的最大特征值 ", font_size=28, color=GREEN
        )
        maximum_lambda = MathTex(
            r"\lambda_{\max}", font_size=28, color=GREEN
        ).next_to(maximum_text, RIGHT, buff=0.1)
        maximum_eigenvector = Text(
            "，对应于最大特征向量", font_size=28, color=GREEN
        ).next_to(maximum_lambda, RIGHT, buff=0.1)
        maximum_group = VGroup(maximum_text, maximum_lambda, maximum_eigenvector)
        maximum_group.next_to(rayleigh_quotient_explain2_group, DOWN, buff=0.6, aligned_edge=LEFT)
        self.play(Write(maximum_group))
        self.wait(2)

        
        # minimum 性质
        minimum_text = Text(
            "最小值 ⇒ C 的最小特征值 ", font_size=28, color=GREEN
        )
        minimum_lambda = MathTex(
            r"\lambda_{\min}", font_size=28, color=GREEN
        ).next_to(minimum_text, RIGHT, buff=0.1)
        minimum_eigenvector = Text(
            "，对应于最小特征向量", font_size=28, color=GREEN
        ).next_to(minimum_lambda, RIGHT, buff=0.1)
        minimum_group = VGroup(minimum_text, minimum_lambda, minimum_eigenvector)
        minimum_group.next_to(maximum_group, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(Write(minimum_group))
        self.wait(10)

        self.play(
            Uncreate(rayleigh_quotient_quota),
            Uncreate(rayleigh_quotient_formula),
            Uncreate(rayleigh_quotient_explain1),
            Uncreate(rayleigh_quotient_explain2_group),
            Uncreate(rayleigh_quotient_explain2_lastpart),
            Uncreate(maximum_group),
            Uncreate(minimum_group),
            Uncreate(framebox2)
        )
        self.wait(2)

        question = Text("什么是瑞利商问题呢？", font_size=28).move_to(UP)
        self.play(
            Write(question),
            question.animate.shift(ORIGIN),
            question.animate.scale(2)
        )
        
        self.wait(2)

        self.play(
            Uncreate(question)
        )
        
        self.wait(1)