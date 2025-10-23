# PCA animation manim code

## What is this repo

This repository contains all the code used to generate the animations for the video ["PCA在平面拟合中的应用"](bilibili.com/video/BV13bsVzMEAB/) on the bilibili channel [一YiMi n g](https://space.bilibili.com/496878537?spm_id_from=333.788.0.0).

All references to the script and the voiceover service have been removed, so you are left with only raw animations.

There is no guarantee that any of these scripts can actually run. The code was not meant to be re-used, so it might need some external data in some places that I may or may have not put in this repository.

You can reuse any piece of code to make the same visualizations, crediting the bilibili channel [一YiMi n g](https://space.bilibili.com/496878537?spm_id_from=333.788.0.0) would be nice but is not required.

## Environment

I recommend you use conda rather than original python env in case of dirtying your environment.
You should follow [manim-installation](https://docs.manim.community/en/stable/installation.html) to configure manim library in your own conda environment.

## Generate a scene

You should move to one of the subfolders then run the regular Manim commands to generate a video such as:

```bash
manim -pqh scene_1.py Scene1 --disable_caching
manim -pqh scene_2.py Scene2 --disable_caching
....
```

The video will then be written in the ``./media/videos/scene_1/1080p60/`` subdirectory.

I recommand the ``--disable_caching`` flag when using voiceover.

