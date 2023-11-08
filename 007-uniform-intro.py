import moderngl
import moderngl_window
from moderngl_window.conf import settings
from moderngl_window.timers.clock import Timer
import numpy as np

# https://learnopengl.com/Getting-started/Shaders
# https://moderngl-window.readthedocs.io/en/latest/guide/window_guide.html


VERTICES = np.array([
    # x                  y    z
   -0.5,               -0.5, 0.0,
    0.0,   np.sqrt(3)/2-0.5, 0.0,
    0.5,               -0.5, 0.0,

], dtype=np.float32)

VERTEX_SHADER = """
    #version 330 core
    layout (location = 0) in vec3 position;

    void main()
    {
        gl_Position = vec4(position.xyz, 1.0);
    }
"""

FRAGMENT_SHADER = """
    #version 330 core
    out vec4 FragColor;
    
    uniform vec4 ourColor; // we set this variable in the OpenGL code.

    void main()
    {
        FragColor = ourColor;
    }  
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

    timer = Timer()
    timer.start()
    while not window.is_closing:
        window.clear()
        # Render stuff here
        prog["ourColor"] = np.array([
            (np.sin(timer.time)            + 1) / 2,
            (np.sin(timer.time + np.pi)    + 1) / 2,
            (np.sin(timer.time + np.pi/2)  + 1) / 2,
            1.0], dtype=np.float32)
        vao.render(moderngl.TRIANGLES)
        window.swap_buffers()


if __name__ == "__main__":
    main()
