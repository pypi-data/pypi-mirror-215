from .drawable import Drawable

import skia
import glfw

import numpy as np


def get_skia_surface(width, height):
    """Creates a Skia surface for rendering to on the GPU.

    Args:
        width: The width of the canvas.
        height: The height of the canvas.

    Returns:
        A SkSurface with the given dimensions.
    """

    if not glfw.init():
        raise RuntimeError("glfw.init() failed")

    # Round up width and height to the nearest integer.
    width = int(width + 0.5)
    height = int(height + 0.5)

    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    glfw.window_hint(glfw.STENCIL_BITS, 8)
    window = glfw.create_window(width, height, "", None, None)
    glfw.make_context_current(window)

    context = skia.GrDirectContext.MakeGL()
    info = skia.ImageInfo.MakeN32Premul(width, height)
    surface = skia.Surface.MakeRenderTarget(context, skia.Budgeted.kNo, info)

    return surface


class Renderer(object):
    def __init__(self, gpu: bool = True, skia_surface=None):
        """Creates a new Renderer.

        Args:
            gpu: Whether to use the GPU for rendering.
            skia_surface: A Skia surface to render to. If None, a new surface will be created.

        Returns:
            A new Renderer.
        """

        self._gpu = gpu
        self._skia_surface = skia_surface
        self._bounds = None
        self._drawable = None

    def _try_create_skia_surface(self, drawable: Drawable):
        self._drawable = drawable
        if self._skia_surface is None or self._bounds != drawable.bounds:
            self._bounds = drawable.bounds
            if self._gpu:
                self._skia_surface = self._create_gpu_surface()
            else:
                self._skia_surface = self._create_cpu_surface()

    def render(self, drawable: Drawable):
        """Renders the given Drawable to the surface.

        Note that calling this again and again with a differently sized Drawable will
        incur a performance penalty, as the surface will be resized to fit the Drawable.

        It is best called repeatedly with Drawables of the same size.

        This method does not return anything. To get the rendered image, call
        `get_rendered_image()`. To save the rendered image, call `save_rendered_image()`.

        Args:
            drawable: The Drawable to render.
        """

        self._try_create_skia_surface(drawable)

        with self._skia_surface as canvas:
            canvas.clear(skia.Color4f(0, 0, 0, 0))
            canvas.save()
            canvas.translate(-self._bounds.left, -self._bounds.top)
            drawable.draw(canvas)
            canvas.restore()

    def get_rendered_image(self) -> np.ndarray:
        """Returns the rendered image as a numpy array.

        Returns:
            The rendered image as a numpy array.
        """

        # TODO(revalo): Convert BGR to RGB via Skia.
        image = self._skia_surface.makeImageSnapshot()
        return image.toarray()[:, :, :3][:, :, ::-1]

    def save_rendered_image(self, path: str):
        """Saves the rendered image to the given path.

        Args:
            path: The path to save the image to.
        """

        image = self._skia_surface.makeImageSnapshot()
        image.save(path)

    def _create_gpu_surface(self):
        return get_skia_surface(self._bounds.width, self._bounds.height)

    def _create_cpu_surface(self):
        return skia.Surface(
            int(self._bounds.width + 0.5), int(self._bounds.height + 0.5)
        )
