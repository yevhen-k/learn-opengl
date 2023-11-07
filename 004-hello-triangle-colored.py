import moderngl
import moderngl_window
from moderngl_window.conf import settings
import numpy as np

# https://learnopengl.com/Getting-started/Hello-Triangle
# https://moderngl-window.readthedocs.io/en/latest/guide/window_guide.html


BLUE = (132/255, 151/255, 255/255)

VERTICES = np.array([   # x     y    z    r    g    b
                        -0.5, -0.5, 0.0, 0.5, 0.6, 1.0,
                         0.5, -0.5, 0.0, 1.0, 0.5, 0.6,
                         0.0,  0.5, 0.0, 0.6, 1.0, 0.5,
], dtype="f4")

EQULATERAL_TRIANGLE = np.array([
    # x                       y    z    r    g    b
   -0.5,                    -0.5, 0.0, 0.5, 0.6, 1.0,
    0.0,   np.sqrt(3)/2-0.5, 0.0, 1.0, 0.5, 0.6,
    0.5,                    -0.5, 0.0, 0.6, 1.0, 0.5,

], dtype=np.float32)

VERTEX_SHADER = """
    #version 330 core
    layout (location = 0) in vec3 position;
    in vec3 color;
    out vec3 out_color;

    void main()
    {
        gl_Position = vec4(position.x, position.y, position.z, 1.0);
        out_color = color;
    }
"""

FRAGMENT_SHADER = """
    #version 330 core
    in vec3 out_color;
    out vec4 FragColor;

    void main()
    {
        FragColor = vec4(out_color, 1.0f);
    } 
"""


def main():
    settings.WINDOW["size"] = (512, 512)
    settings.WINDOW["aspect_ratio"] = 1
    settings.WINDOW["title"] = "Hello, Equilateral Colored Triangle!"
    window = moderngl_window.create_window_from_settings()

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)

    vbo = window.ctx.buffer(EQULATERAL_TRIANGLE)
    vao = window.ctx.vertex_array(prog, vbo, "position", "color")

    # same options:
    # moderngl_window.activate_context(ctx=window.ctx)
    moderngl_window.activate_context(window=window)

    while not window.is_closing:
        window.clear()
        # Render stuff here
        vao.render(moderngl.TRIANGLES)
        window.swap_buffers()


if __name__ == "__main__":
    main()
