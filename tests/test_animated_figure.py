"""Tests for `animated_figure`."""

import tempfile
import unittest

import matplotlib.pyplot as plt
import numpy as onp
import parameterized
from PIL import Image

import gifcm
from gifcm import animated_figure


class TestGifCreation(unittest.TestCase):
    @parameterized.parameterized.expand([[1], [2], [10]])
    def test_figure_imshow(self, num_frames):
        fig = plt.figure(figsize=(2, 2))
        anim = gifcm.AnimatedFigure(fig)
        for frame_idx in range(num_frames):
            with anim.frame():
                plt.imshow(onp.full((5, 5, 3), frame_idx * 25, dtype=onp.uint8))
                plt.subplots_adjust(left=0, bottom=0, right=1, top=1)

        with tempfile.TemporaryDirectory() as tempdir:
            fname = "/".join([tempdir, "anim.gif"])
            anim.save_gif(fname)
            im = Image.open(fname)
        self.assertEqual(im.n_frames, num_frames)

    @parameterized.parameterized.expand([[1], [2], [10]])
    def test_figure_plt(self, num_frames):
        fig = plt.figure(figsize=(2, 2))
        anim = gifcm.AnimatedFigure(fig)
        for frame_idx in range(num_frames):
            with anim.frame():
                plt.plot(frame_idx, frame_idx, "o")
                plt.xlim([0, num_frames])
                plt.ylim([0, num_frames])
                plt.subplots_adjust(left=0, bottom=0, right=1, top=1)

        with tempfile.TemporaryDirectory() as tempdir:
            fname = "/".join([tempdir, "anim.gif"])
            anim.save_gif(fname)
            im = Image.open(fname)
        self.assertEqual(im.n_frames, num_frames)


class SaveFigureTest(unittest.TestCase):
    def test_grayscale_image(self):
        fig = plt.figure()
        plt.imshow(onp.arange(100).reshape(10, 10), cmap="gray")
        array = animated_figure._save_figure_to_array(fig)
        self.assertEqual(array.ndim, 3)

    def test_rgb_image(self):
        fig = plt.figure()
        plt.imshow(onp.arange(100).reshape(10, 10), cmap="magma")
        array = animated_figure._save_figure_to_array(fig)
        self.assertEqual(array.ndim, 3)

    def test_rgba_image(self):
        fig = plt.figure()
        im = onp.linspace(0, 255, 10 * 10 * 4)
        im = im.astype(int).reshape((10, 10, 4))
        plt.imshow(im)
        array = animated_figure._save_figure_to_array(fig)
        self.assertEqual(array.ndim, 3)
