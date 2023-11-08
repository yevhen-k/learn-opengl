import moderngl
import moderngl_window
from moderngl_window.conf import settings
import numpy as np

# https://learnopengl.com/Getting-started/Hello-Triangle
# https://moderngl-window.readthedocs.io/en/latest/guide/window_guide.html


BLUE = (132/255, 151/255, 255/255)
YELLOW = (240/255, 255/255, 133/255)

VERTICES = np.array([
    # x     y    z     r         g        b
    # first triangle
     0.5,  0.5, 0.0, BLUE[0],  BLUE[1], BLUE[2],        # top right
     0.5, -0.5, 0.0, BLUE[0],  BLUE[1], BLUE[2],        # bottom right
    -0.5,  0.5, 0.0, BLUE[0],  BLUE[1], BLUE[2],        # top left
    # second triangle
     0.5, -0.5, 0.0, YELLOW[0],  YELLOW[1], YELLOW[2],  # bottom right
    -0.5, -0.5, 0.0, YELLOW[0],  YELLOW[1], YELLOW[2],  # bottom left
    -0.5,  0.5, 0.0, YELLOW[0],  YELLOW[1], YELLOW[2],  # top left
], dtype=np.float32)

VERTEX_SHADER = """
    #version 330 core
    layout (location = 0) in vec3 position;
    in vec3 in_color;
    out vec3 color;

    void main()
    {
        gl_Position = vec4(position.x, position.y, position.z, 1.0);
        color = in_color;
    }
"""

FRAGMENT_SHADER = """
    #version 330 core
    in vec3 color;
    out vec4 fragemnt_color;

    void main()
    {
        fragemnt_color = vec4(color, 1.0f);
    } 
"""


def main():
    settings.WINDOW["size"] = (512, 512)
    settings.WINDOW["aspect_ratio"] = 1
    settings.WINDOW["title"] = "Hello, Triangle!"
    window = moderngl_window.create_window_from_settings()

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)

    vbo = window.ctx.buffer(VERTICES)
    vao = window.ctx.vertex_array(prog, vbo, "position", "in_color")

    moderngl_window.activate_context(ctx=window.ctx)

    while not window.is_closing:
        window.clear()
        # Render stuff here
        # vao.render(moderngl.LINE_LOOP)
        # vao.render(moderngl.LINES)
        # vao.render(moderngl.POINTS)
        # vao.render(moderngl.PATCHES)
        vao.render(moderngl.TRIANGLES)
        window.swap_buffers()


if __name__ == "__main__":
    main()
