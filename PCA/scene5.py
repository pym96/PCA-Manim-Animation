from manim import *
from manim_voiceover import VoiceoverScene
import numpy as np

class Scene5(ThreeDScene):
    def construct(self):
        # Save initial camera position
        self.initial_phi = self.camera.phi_tracker.get_value()
        self.initial_theta = self.camera.theta_tracker.get_value()
        self.initial_focal = self.camera.focal_distance_tracker.get_value()

        self.wait(1)
        
        # Title
        text = Text("Principal Component Analysis", font_size=60)
        self.play(Write(text))
        self.wait(1)
        
        subtitle = Text("Plane Fitting in 3D", font_size=40).next_to(text, DOWN)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(Unwrite(text), Unwrite(subtitle))

        # Setup 3D axes
        axes = ThreeDAxes(
            x_range=[0, 9, 3],
            y_range=[0, 9, 3],
            z_range=[0, 9, 3],
            axis_config={
                "color": WHITE,
                "include_numbers": False,
                "include_tip": True,
                "font_size": 18
            },
        ).move_to(ORIGIN)
     
        self.set_camera_orientation(phi=75 * DEGREES, theta=-PI / 5, focal_distance=10)
        self.add(self.camera.light_source)
        
        self.play(Create(axes))
        self.wait(1)

        # Generate data points near a plane
        mean = np.array([4.5, 4.5, 4.5])
        # Covariance matrix with one small eigenvalue (flat distribution)
        cov = np.array([[2.0, 1.5, 0.1], 
                        [1.5, 2.0, 0.1], 
                        [0.1, 0.1, 0.2]])

        data = np.random.multivariate_normal(mean, cov, 150)
        scatter_plot = VGroup()
        
        for point in data:
            dot = Sphere(
                center=axes.c2p(point[0], point[1], point[2]),
                color=BLUE,
                radius=0.05,
                fill_opacity=0.7
            )
            scatter_plot.add(dot)

        # Animate data points creation
        step1_text = Text("Step 1: Generate 3D Data Points", font_size=36, color=YELLOW)
        step1_text.to_corner(UL).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(step1_text)
        
        self.play(Write(step1_text))
        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(LaggedStartMap(Create, scatter_plot, lag_ratio=0.01), run_time=4)
        self.wait(1)

        # Calculate PCA
        centered_data = data - mean
        cov_matrix = np.cov(centered_data.T)
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # Sort by eigenvalues
        sort_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sort_indices]
        eigenvectors = eigenvectors[:, sort_indices]

        # Step 2: Show mean point
        self.play(FadeOut(step1_text))
        step2_text = Text("Step 2: Find the Center (Mean)", font_size=36, color=YELLOW)
        step2_text.to_corner(UL).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(step2_text)
        
        self.play(Write(step2_text))
        
        mean_dot = Sphere(
            center=axes.c2p(*mean),
            color=YELLOW,
            radius=0.15,
            fill_opacity=1.0
        )
        self.play(GrowFromCenter(mean_dot))
        self.wait(1.5)

        # Step 3: Show principal components
        self.play(FadeOut(step2_text))
        step3_text = Text("Step 3: Compute Principal Components", font_size=36, color=YELLOW)
        step3_text.to_corner(UL).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(step3_text)
        
        self.play(Write(step3_text))
        self.stop_ambient_camera_rotation()
        
        # Move camera to better view
        self.play(
            self.camera.phi_tracker.animate.set_value(70 * DEGREES),
            self.camera.theta_tracker.animate.set_value(-PI / 4),
            run_time=2
        )

        # Create eigenvector arrows
        colors = [RED, GREEN, BLUE]
        labels = ["PC1 (Max Variance)", "PC2 (Medium Variance)", "PC3 (Min Variance)"]
        eigen_arrows = VGroup()
        
        for i in range(3):
            scale = np.sqrt(eigenvalues[i]) * 3
            vec = eigenvectors[:, i] * scale
            
            arrow = Arrow3D(
                start=axes.c2p(*mean),
                end=axes.c2p(*(mean + vec)),
                color=colors[i],
                thickness=0.03,
                height=0.3,
                base_radius=0.08
            )
            eigen_arrows.add(arrow)

        self.play(LaggedStartMap(Create, eigen_arrows, lag_ratio=0.4), run_time=3)
        self.wait(1)

        # Add labels for eigenvectors
        label_group = VGroup()
        for i, label_text in enumerate(labels):
            label = Text(label_text, font_size=24, color=colors[i])
            label.to_edge(RIGHT).shift(UP * (1 - i * 0.8))
            label_group.add(label)
        
        self.add_fixed_in_frame_mobjects(label_group)
        self.play(LaggedStartMap(FadeIn, label_group, lag_ratio=0.3), run_time=2)
        self.wait(2)

        # Step 4: Fit the plane
        self.play(FadeOut(step3_text), FadeOut(label_group))
        step4_text = Text("Step 4: Fit Plane Using PC1 & PC2", font_size=36, color=YELLOW)
        step4_text.to_corner(UL).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(step4_text)
        
        self.play(Write(step4_text))

        # Rotate camera for dramatic effect
        self.play(
            self.camera.phi_tracker.animate.set_value(60 * DEGREES),
            self.camera.theta_tracker.animate.set_value(-PI / 3),
            run_time=2
        )

        # Create the fitted plane using PC1 and PC2
        # Normal vector is PC3 (smallest eigenvalue)
        normal = eigenvectors[:, 2]
        pc1 = eigenvectors[:, 0]
        pc2 = eigenvectors[:, 1]
        
        # Create plane mesh
        u_range = np.linspace(-3, 3, 20)
        v_range = np.linspace(-3, 3, 20)
        
        plane_points = []
        for u in u_range:
            row = []
            for v in v_range:
                point = mean + u * pc1 + v * pc2
                row.append(axes.c2p(*point))
            plane_points.append(row)
        
        plane = Surface(
            lambda u, v: axes.c2p(*(mean + u * pc1 + v * pc2)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20),
            fill_opacity=0.4,
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_width=0.5,
        )

        self.play(Create(plane), run_time=3)
        self.wait(1)

        # Highlight the normal vector (PC3)
        self.play(
            eigen_arrows[2].animate.set_color(YELLOW),
            Flash(eigen_arrows[2], color=YELLOW, flash_radius=0.5),
        )
        
        normal_text = Text("Normal Vector\n(Perpendicular to Plane)", 
                          font_size=28, color=YELLOW)
        normal_text.to_corner(UR).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(normal_text)
        
        self.play(Write(normal_text))
        self.wait(2)

        # Final rotation to show the fit
        self.play(FadeOut(step4_text), FadeOut(normal_text))
        final_text = Text("PCA finds the best-fitting plane!", font_size=40, color=GREEN)
        final_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_text)
        
        self.play(Write(final_text))
        
        # Slow rotation to appreciate the result
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        # Show variance explained
        total_var = np.sum(eigenvalues)
        var_text = VGroup(
            Text(f"Variance Explained:", font_size=28, color=WHITE),
            Text(f"PC1: {eigenvalues[0]/total_var*100:.1f}%", font_size=24, color=RED),
            Text(f"PC2: {eigenvalues[1]/total_var*100:.1f}%", font_size=24, color=GREEN),
            Text(f"PC3: {eigenvalues[2]/total_var*100:.1f}%", font_size=24, color=BLUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        var_text.to_corner(UL).shift(DOWN * 0.5)
        self.add_fixed_in_frame_mobjects(var_text)
        
        self.play(FadeIn(var_text))
        self.wait(3)
        
        # Fade out everything
        self.play(
            *[FadeOut(mob) for mob in [axes, scatter_plot, mean_dot, eigen_arrows, 
                                       plane, final_text, var_text]],
            run_time=2
        )
        self.wait(1)

    def restore_perspective(self):
        self.play(
            self.camera.phi_tracker.animate.set_value(self.initial_phi),
            self.camera.theta_tracker.animate.set_value(self.initial_theta),
            self.camera.focal_distance_tracker.animate.set_value(self.initial_focal),
            run_time=2
        )