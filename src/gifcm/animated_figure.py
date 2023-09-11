"""Module for creating animations from matplotlib figures."""

import io
from typing import List, Sequence, Tuple

import matplotlib.figure as mpl_figure
import numpy as onp
from PIL import Image


class AnimatedFigure:
    """Enables creation of a sequence of frames for an animation.

    Example usage is as follows:

        animated_figure = AnimatedFigure(figure=plt.figure())

        for i in range(10):
            with animated_figure.frame(clear_figure=False):
                plt.plot(i, j, 'o')

        animated_figure.save_gif('my_animation.gif')

    Attributes:
        figure: The matplotlib figure used to create frames of the animation.
        frames: List of arrays containing the rasterized frames.
    """

    def __init__(self, figure: mpl_figure.Figure) -> None:
        self.figure = figure
        self.frames: List[onp.ndarray] = []

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
            gif_path: The path where the image will be saved.
            duration: The duration of each frame, in milliseconds.
            loop: Determines whether or how many times the animation should loop.
                A value of `0` means the animation should loop infinitely.
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
    with io.BytesIO() as bytes_io:
        figure.savefig(bytes_io, bbox_inches="tight", pad_inches=0.0, format="png")
        bytes_io.seek(0)
        return onp.asarray(Image.open(bytes_io, mode="r"))


def _save_frames_to_gif(
    frames: Sequence[onp.ndarray],
    gif_path: str,
    duration: int,
    loop: int,
) -> None:
    """Saves frames to a gif image.

    Args:
        frames: The frames to be converted to a gif image.
        gif_path: The path where the image will be saved.
        duration: The duration of each frame, in milliseconds.
        loop: Determines whether or how many times the animation should loop.
            A value of `0` means the animation should loop infinitely.
    """
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

    frames, palette = _quantize_frames(frames)
    image, *images = (Image.fromarray(frame) for frame in frames)
    image.save(
        gif_path,
        save_all=True,
        append_images=images,
        duration=duration,
        loop=loop,
        palette=palette,
    )


def _quantize_frames(
    frames: Sequence[onp.ndarray],
) -> Tuple[List[onp.ndarray], List[int]]:
    """Returns quantized frames and the corresponding palette."""
    merged = Image.fromarray(onp.concatenate(frames))
    quantized = merged.quantize(colors=256, dither=0)
    quantized_frames = onp.split(onp.asarray(quantized), len(frames))
    palette: List[int] = quantized.getpalette()  # type: ignore[misc]
    return list(quantized_frames), palette
