"""gifcm - Gifcm is a context manager to simplify creation of animated gifs from
a sequence of matplotlib figures."""

__version__ = "0.2.0"
__author__ = "Martin Schubert <mfschubert@gmail.com>"

__all__ = ["AnimatedFigure", "Frame"]

from gifcm.animated_figure import AnimatedFigure, Frame
