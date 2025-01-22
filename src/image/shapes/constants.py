import pyglet

shape_batch = pyglet.graphics.Batch()

shape_front = pyglet.graphics.Group(order=0)  # last to draw (top)
shape_foreground = pyglet.graphics.Group(order=1)
shape_midground = pyglet.graphics.Group(order=2)
shape_background = pyglet.graphics.Group(order=3)
shape_back = pyglet.graphics.Group(order=4)  # first to draw (bottom)
