from PIL import Image
import moderngl
import moderngl_window
from moderngl_window.conf import settings
from time import perf_counter
import numpy as np


# https://learnopengl.com/Getting-started/Transformations
# https://github.com/moderngl/moderngl/blob/master/examples/simple_camera.py
# https://github.com/adamlwgriffiths/Pyrr/issues/97


VERTICES = np.array([
    # positions        # texture coords
    -0.5,  0.5, 0.0,   0.0, 1.0,   # top left
     0.5,  0.5, 0.0,   1.0, 1.0,   # top right
     0.5, -0.5, 0.0,   1.0, 0.0,   # bottom right
    -0.5, -0.5, 0.0,   0.0, 0.0,   # bottom left
], dtype=np.float32)

VERTEX_SHADER = """
    #version 330 core

    in vec3 position;
    in vec2 in_texture_coords;
    uniform float time;

    out vec4 color;
    out vec2 texture_coord;

    void main()
    {   
        mat4 rot_z = mat4(
            cos(time), -sin(time), 0, 0,
            sin(time),  cos(time), 0, 0,
            0,          0,         1, 0,
            0,          0,         0, 1
        );
        gl_Position = rot_z * vec4(position.xyz, 1.0);
        texture_coord = in_texture_coords * 2 - 0.5;
    }
"""

FRAGMENT_SHADER = """
    #version 330 core

    in vec2 texture_coord;

    uniform sampler2D ourTexture;

    out vec4 fragemnt_color;

    void main()
    {
        fragemnt_color = texture(ourTexture, texture_coord);
    } 
"""


def main():
    img = Image.open("./textures/face.png").convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)

    settings.WINDOW["size"] = (512, 512)
    settings.WINDOW["aspect_ratio"] = 1
    settings.WINDOW["title"] = "Hello, Rotation!"
    settings.WINDOW["vsync"] = False

    window = moderngl_window.create_window_from_settings()

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)
    texture = window.ctx.texture(img.size, components=4, data=img.tobytes())
    texture.repeat_x = True
    texture.repeat_y = True
    prog["ourTexture"].handle = texture.get_handle()

    vbo = window.ctx.buffer(VERTICES)
    vao = window.ctx.vertex_array(prog, vbo, "position", "in_texture_coords")

    # no rotation at the beginning
    prog["time"] = 0.0

    moderngl_window.activate_context(ctx=window.ctx)

    time_start = perf_counter()
    time_end = 0
    frames_start = 0
    frames_end = 0
    while not window.is_closing:
        window.clear()
        # Render stuff here
        vao.render(moderngl.TRIANGLE_FAN)
        time_end = perf_counter()
        prog["time"] = time_end
        window.swap_buffers()

        # get framerate
        # experiment with vsync=False and vsync=True
        frames_end = window.frames
        if time_end - time_start >= 1.0:  # 1.0s or more elapsed
            fps = (frames_end - frames_start) / (time_end - time_start)
            print("\r", int(fps), "FPS", end="")
            time_start = time_end
            frames_start = frames_end


if __name__ == "__main__":
    main()
