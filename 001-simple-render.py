from typing import Any
import moderngl
import numpy as np
from PIL import Image, ImageShow


# https://moderngl.readthedocs.io/en/5.8.2/the_guide/rendering.html


class Viewer(ImageShow.Viewer):
    command = "viewnior"

    def get_command(self, file: str, **options: Any) -> str:
        return f"{self.command} {file}"


viewer = Viewer()
ImageShow.register(viewer=viewer)

ctx = moderngl.create_standalone_context()

prog = ctx.program(
    vertex_shader='''
        #version 330

        in vec2 in_vert;
        in vec3 in_color;

        out vec3 v_color;

        void main() {
            v_color = in_color;
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    ''',
    fragment_shader='''
        #version 330

        in vec3 v_color;

        out vec3 f_color;

        void main() {
            f_color = v_color;
        }
    ''',
)


def main():
    np.random.seed(1337)
    
    x = np.linspace(-1.0, 1.0, 50)
    y = np.random.rand(50) - 0.5
    r = np.ones(50)
    g = np.zeros(50)
    b = np.zeros(50)

    vertices = np.dstack([x, y, r, g, b])

    vbo = ctx.buffer(vertices.astype('f4').tobytes())
    vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_color')

    fbo = ctx.simple_framebuffer((512, 512))
    fbo.use()
    fbo.clear(0.0, 0.0, 0.0, 1.0)
    vao.render(moderngl.LINE_STRIP)
    # vao.render(moderngl.LINE_LOOP)
    # vao.render(moderngl.LINE_STRIP_ADJACENCY)
    # vao.render(moderngl.POINTS)
    # vao.render(moderngl.TRIANGLES)
    # vao.render(moderngl.TRIANGLES_ADJACENCY)

    img = Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)
    viewer.show(img)

if __name__ == "__main__":
    main()
