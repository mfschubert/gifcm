"""Module for creating animations from matplotlib figures."""

from typing import Sequence

import io
import matplotlib.figure as mpl_figure
import numpy as onp
from PIL import Image


class AnimatedFigure:
    """Enables creation of a sequence of frames for an animation.
    
    Example usage is as follows:

        animated_figure = AnimatedFigure(figure=plt.figure())

        for i in range(10):
            with animated_figure.frame(clear_figure=False):
                plt.plot(i, j, 'o)

        animated_figure.save_gif('my_animation.gif')

    Attributes:
        figure: The matplotlib figure used to create frames of the animation.
        frames: List of arrays containing the rasterized frames.
    """

    def __init__(self, figure: mpl_figure.Figure) -> None:
        self.figure = figure
        self.frames = []

    def frame(self, clear_figure: bool = True) -> "Frame":
        """Returns a new `Frame` context manager."""
        return Frame(animated_figure=self, clear_figure=clear_figure)

    def save_gif(
        self,
        gif_path: str,
        duration: int = 100,
        loop: int = 0,
    ) -> None:
        """Saves the frames to an animated gif.
        
        Args:
            gif_path:
            duration:
            loop:
        """
        _save_frames_to_gif(
            frames=self.frames,
            gif_path=gif_path,
            duration=duration,
            loop=loop,
        )


class Frame:
    """Enables creation of a single frame in a sequence of frames."""

    def __init__(
        self,
        animated_figure: AnimatedFigure,
        clear_figure: bool,
    ) -> None:
        self.animated_figure = animated_figure
        self.clear_figure = clear_figure

    def __enter__(self):
        if self.clear_figure:
            self.animated_figure.figure.clf()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        frame = _save_figure_to_array(self.animated_figure.figure)
        self.animated_figure.frames.append(frame)


def _save_figure_to_array(figure: mpl_figure.Figure) -> onp.ndarray:
    """Saves a figure to a numpy array."""
    io_buffer = io.BytesIO()
    figure.savefig(io_buffer, format="raw")

    io_buffer.seek(0)
    flat_array = onp.frombuffer(io_buffer.getvalue(), dtype=onp.uint8)
    io_buffer.close()

    _, _, height, width = figure.bbox.bounds
    return flat_array.reshape((int(width), int(height), -1))


def _save_frames_to_gif(
    frames: Sequence[onp.ndarray],
    gif_path: str,
    duration: int,
    loop: int,
) -> None:
    """Saves frames to a gif image"""
    if len(frames) == 0:
        raise ValueError("At least one frame is required.")
    if frames[0].ndim != 3:
        raise ValueError(
            f"Frames must be rank-3, but first frame had shape {frames[0].shape}"
        )
    if not all(frame.shape == frames[0].shape for frame in frames):
        raise ValueError(
            f"All frames must have the same shape, but got shapes "
            f"{[frame.shape for frame in frames]}."
        )
    if not gif_path.endswith(".gif"):
        raise ValueError(f"Valid `gif_path` must end in '.gif', but got {gif_path}.")

    image, *images = [Image.fromarray(frame) for frame in frames]
    image.save(
        gif_path,
        save_all=True,
        append_images=images,
        duration=duration,
        loop=loop,
    )
