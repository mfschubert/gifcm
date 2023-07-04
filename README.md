# gifcm

Gifcm provides a context manager for easy creation of gif animations from matplotlib figures. It does not offer capabilities beyond existing tools such as [gif](https://github.com/maxhumber/gif), but rather a different API making use of context managers.

## Installation
TODO

## Usage
Example usage is as follows:
```python
animated_figure = AnimatedFigure(figure=plt.figure())

for i in range(10):
  with animated_figure.frame():
    plt.plot(i, j, "o")

animated_figure.save_gif("my_animation.gif")
```
