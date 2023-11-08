from typing import Any
from PIL import Image, ImageShow
import moderngl
import moderngl_window
from moderngl_window.conf import settings
import numpy as np


# https://learnopengl.com/Getting-started/Textures
# https://moderngl.readthedocs.io/en/latest/reference/texture.html
# https://moderngl.readthedocs.io/en/latest/reference/context.html#Context.texture
# https://github.com/moderngl/moderngl/blob/51d9549a2401e68f1f970530c4b4ab27bbd5ac21/examples/bindless_textures.py#L61C14-L61C21
# https://moderngl-window.readthedocs.io/en/latest/guide/basic_usage.html#resource-loading


class Viewer(ImageShow.Viewer):
    command = "viewnior"

    def get_command(self, file: str, **options: Any) -> str:
        return f"{self.command} {file}"


viewer = Viewer()
ImageShow.register(viewer=viewer)

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

    out vec4 color;
    out vec2 texture_coord;

    void main()
    {
        gl_Position = vec4(position.xyz, 1.0);
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
    img = Image.open("./textures/face.png")
    # viewer.show(img)

    # OpenGL expects the 0.0 coordinate on the y-axis to be on the bottom side of the image,
    # but images usually have 0.0 at the top of the y-axis.
    img = img.convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)

    settings.WINDOW["size"] = (512, 512)
    settings.WINDOW["aspect_ratio"] = 1
    settings.WINDOW["title"] = "Hello, Texture!"

    window = moderngl_window.create_window_from_settings()

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)
    texture = window.ctx.texture(img.size, components=4, data=img.tobytes())
    prog["ourTexture"].handle = texture.get_handle()

    vbo = window.ctx.buffer(VERTICES)
    vao = window.ctx.vertex_array(prog, vbo, "position", "in_texture_coords")

    moderngl_window.activate_context(ctx=window.ctx)

    while not window.is_closing:
        window.clear()
        # Render stuff here
        vao.render(moderngl.TRIANGLE_FAN)
        window.swap_buffers()



if __name__ == "__main__":
    main()
