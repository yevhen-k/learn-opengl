import pyrr
from PIL import Image
import moderngl
import moderngl_window
from moderngl_window.conf import settings
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
    uniform mat4 transform;

    out vec4 color;
    out vec2 texture_coord;

    void main()
    {
        gl_Position = transform * vec4(position.xyz, 1.0);
        texture_coord = in_texture_coords;
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

    window = moderngl_window.create_window_from_settings()

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)
    texture = window.ctx.texture(img.size, components=4, data=img.tobytes())
    prog["ourTexture"].handle = texture.get_handle()

    vbo = window.ctx.buffer(VERTICES)
    vao = window.ctx.vertex_array(prog, vbo, "position", "in_texture_coords")

    # set rotation
    rot_deg = 45
    rot_rad = np.deg2rad(rot_deg)

    quat_rot = pyrr.Quaternion.from_z_rotation(theta=rot_rad, dtype=np.float32)
    m44_rot = pyrr.matrix44.create_from_z_rotation(theta=rot_rad, dtype=np.float32)
    rot_from_quat = pyrr.matrix44.create_from_quaternion(quat_rot)

    # m44_rot == rot_from_quat
    assert np.allclose(m44_rot, rot_from_quat)

    # prog["transform"] = m44_rot.flatten()
    prog["transform"] = rot_from_quat.flatten()

    moderngl_window.activate_context(ctx=window.ctx)

    while not window.is_closing:
        window.clear()
        # Render stuff here
        vao.render(moderngl.TRIANGLE_FAN)
        window.swap_buffers()



if __name__ == "__main__":
    main()
