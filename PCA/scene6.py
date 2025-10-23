from manim import *
import numpy as np

class Scene6(ThreeDScene):
    def construct(self):
        # ========== 场景1: PCA回顾 ==========
        self.recap_pca()
        
        # ========== 场景2: 揭示真相 - PCA是SVD的特例 ==========
        self.reveal_connection()
        
        # ========== 场景3: SVD预告 ==========
        self.svd_teaser()
        
 

    def recap_pca(self):
        title = Text("核心回顾", font_size=48, gradient=(BLUE, PURPLE)).to_edge(UP)
        self.play(Write(title), run_time=1)
        
        # PCA的三个关键点
        key_points = VGroup(
            self.create_key_point("1", "降维", "高维 → 低维", BLUE),
            self.create_key_point("2", "最大方差", "保留主要信息", GREEN),
            self.create_key_point("3", "特征值分解", "协方差矩阵", YELLOW)
        ).arrange(DOWN, buff=0.8, aligned_edge=LEFT).shift(DOWN * 0.3)
        
        for point in key_points:
            self.play(FadeIn(point, shift=RIGHT), run_time=0.8)
        
        self.wait(1.5)

        # 清场
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)

    def create_key_point(self, number, main_text, sub_text, color):
        """创建关键点卡片"""
        circle = Circle(radius=0.4, color=color, fill_opacity=0.3, stroke_width=3)
        num = Text(number, font_size=36, color=color).move_to(circle)
        circle_group = VGroup(circle, num)
        
        main = Text(main_text, font_size=32, color=color).next_to(circle_group, RIGHT, buff=0.5)
        sub = Text(sub_text, font_size=24, color=GRAY).next_to(main, DOWN, aligned_edge=LEFT, buff=0.2)
        
        return VGroup(circle_group, main, sub)

    def reveal_connection(self):
        """揭示PCA与SVD的联系"""
        # 标题
        title = Text("Nature", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title), run_time=1)
        
        # PCA公式（左侧）
        pca_label = Text("PCA", font_size=36, color=BLUE).shift(LEFT * 4 + UP * 1.5)
        pca_box = SurroundingRectangle(pca_label, color=BLUE, buff=0.3, corner_radius=0.1)
        
        pca_formula = MathTex(
            r"\text{Cov}(X) = V \Lambda V^T",
            font_size=36,
            color=BLUE
        ).next_to(pca_label, DOWN, buff=0.8)
        
        pca_explain = VGroup(
            Text("协方差矩阵", font_size=22, color=GRAY),
            Text("特征值分解", font_size=22, color=GRAY)
        ).arrange(DOWN, buff=0.15).next_to(pca_formula, DOWN, buff=0.5)
        
        pca_group = VGroup(pca_label, pca_box, pca_formula, pca_explain)
        
        self.play(FadeIn(pca_group, shift=RIGHT), run_time=1.5)
        self.wait()
        
        # 瑞利商（右侧）
        rayleigh_label = Text("Rayleigh商", font_size=36, color=GREEN).shift(RIGHT * 4 + UP * 1.5)
        rayleigh_box = SurroundingRectangle(rayleigh_label, color=GREEN, buff=0.3, corner_radius=0.1)
        
        rayleigh_formula = MathTex(
            r"\max_v \frac{v^T A v}{v^T v}",
            font_size=36,
            color=GREEN
        ).next_to(rayleigh_label, DOWN, buff=0.8)
        
        rayleigh_explain = VGroup(
            Text("最大化方向", font_size=22, color=GRAY),
            Text("最优化问题", font_size=22, color=GRAY)
        ).arrange(DOWN, buff=0.15).next_to(rayleigh_formula, DOWN, buff=0.5)
        
        rayleigh_group = VGroup(rayleigh_label, rayleigh_box, rayleigh_formula, rayleigh_explain)
        
        self.play(FadeIn(rayleigh_group, shift=LEFT), run_time=1.5)
        self.wait(1.5)
        
        # 显示等价性
        equals_arrow1 = Arrow(pca_group.get_bottom(), DOWN * 0.5, color=YELLOW, buff=0.3)
        equals_arrow2 = Arrow(rayleigh_group.get_bottom(), DOWN * 0.5, color=YELLOW, buff=0.3)
        
        self.play(GrowArrow(equals_arrow1), GrowArrow(equals_arrow2))
        
        # 大揭秘
        revelation = Text("都是", font_size=32, color=WHITE).shift(DOWN * 1.5)
        self.play(Write(revelation))
        
        # SVD登场（带震撼效果）
        svd_text = Text("SVD", font_size=72, 
                       gradient=(RED, ORANGE, YELLOW),
                       weight=BOLD).next_to(revelation, DOWN, buff=0.5)
        
        svd_full = Text("Singular Value Decomposition", 
                       font_size=28, color=GRAY).next_to(svd_text, DOWN, buff=0.3)
        
        svd_chinese = Text("奇异值分解", font_size=32, color=ORANGE).next_to(svd_full, DOWN, buff=0.2)
        
        # 震撼登场动画
        self.play(
            FadeIn(svd_text, scale=1.5),
            Flash(svd_text, color=YELLOW, line_length=0.5, num_lines=20),
            run_time=1.5
        )
        self.play(
            Write(svd_full),
            Write(svd_chinese),
            run_time=1
        )
        
        # 添加"特例"标注
        special_case = Text("的特例！", font_size=36, color=RED).next_to(svd_chinese, DOWN, buff=0.4)
        self.play(Write(special_case), run_time=0.8)
        
        self.wait(2.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)

    def svd_teaser(self):
        """SVD预告 - 展示其强大之处"""
        title = Text("什么是 SVD？", font_size=48, color=ORANGE).to_edge(UP)
        self.play(Write(title), run_time=1)
        
        svd_formula = MathTex(
            r"X = U \Sigma V^T",
            font_size=56
        ).shift(UP * 0.5)
        
        components = VGroup(
            self.create_matrix_explanation("U", "左奇异向量", "行空间的正交基", BLUE, LEFT * 3.5),
            self.create_matrix_explanation(r"\Sigma", "奇异值", "重要性权重", YELLOW, ORIGIN),
            self.create_matrix_explanation("V^T", "右奇异向量", "列空间的正交基", GREEN, RIGHT * 3.5)
        ).shift(DOWN * 1.2)
        
        self.play(Write(svd_formula), run_time=1.5)
        self.wait(0.5)
        
        for comp in components:
            self.play(FadeIn(comp, shift=UP), run_time=0.8)
            self.wait(0.5)
        
        self.wait(1.5)
    
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)

    def create_matrix_explanation(self, symbol, name, description, color, position):
        symbol_text = MathTex(symbol, font_size=48, color=color)
        name_text = Text(name, font_size=24, color=color)
        desc_text = Text(description, font_size=20, color=GRAY)
        
        card = VGroup(symbol_text, name_text, desc_text).arrange(DOWN, buff=0.25)
        box = SurroundingRectangle(card, color=color, buff=0.3, corner_radius=0.15, stroke_width=2)
        
        return VGroup(box, card).move_to(position)