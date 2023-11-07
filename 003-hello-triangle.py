import moderngl
import moderngl_window
from moderngl_window.conf import settings
import numpy as np

# https://learnopengl.com/Getting-started/Hello-Triangle
# https://moderngl-window.readthedocs.io/en/latest/guide/window_guide.html


BLUE = (132/255, 151/255, 255/255)

VERTICES = np.array([   # x     y    z
                        -0.5, -0.5, 0.0,
                         0.5, -0.5, 0.0,
                         0.0,  0.5, 0.0,
], dtype=np.float32)

VERTEX_SHADER = """
    #version 330 core
    layout (location = 0) in vec3 position;

    void main()
    {
        gl_Position = vec4(position.x, position.y, position.z, 1.0);
    }
"""

FRAGMENT_SHADER = f"""
    #version 330 core
    out vec4 fragemnt_color;

    void main()
    {{
        fragemnt_color = vec4({BLUE[0]}, {BLUE[1]}, {BLUE[2]}, 1.0f);
    }} 
"""


def main():
    settings.WINDOW["size"] = (512, 512)
    settings.WINDOW["aspect_ratio"] = 1
    settings.WINDOW["title"] = "Hello, Triangle!"
    window = moderngl_window.create_window_from_settings()

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)

    vbo = window.ctx.buffer(VERTICES)
    vao = window.ctx.vertex_array(prog, vbo, "position")

    moderngl_window.activate_context(ctx=window.ctx)

    while not window.is_closing:
        window.clear()
        # Render stuff here
        vao.render(moderngl.TRIANGLES)
        window.swap_buffers()


if __name__ == "__main__":
    main()
