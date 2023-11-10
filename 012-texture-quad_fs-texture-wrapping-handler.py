from typing import Any
from PIL import Image, ImageShow
import moderngl
import moderngl_window
from moderngl_window.geometry.attributes import AttributeNames
from moderngl_window.conf import settings
import numpy as np


# https://learnopengl.com/Getting-started/Textures
# https://moderngl-window.readthedocs.io/en/latest/reference/geometry.html
# https://stackoverflow.com/questions/62500232/draw-objects-on-moderngl-context-in-pygame
# https://stackoverflow.com/questions/67161667/moderngl-project-photo-with-angle
# https://moderngl.readthedocs.io/en/latest/reference/texture.html
# https://moderngl.readthedocs.io/en/latest/reference/context.html#Context.texture
# https://moderngl.readthedocs.io/en/latest/reference/sampler.html
# https://github.com/moderngl/moderngl/blob/51d9549a2401e68f1f970530c4b4ab27bbd5ac21/examples/bindless_textures.py#L61C14-L61C21
# https://moderngl-window.readthedocs.io/en/latest/guide/basic_usage.html#resource-loading


VERTICES = np.array([
    # positions       # texture coords
     1.0,  1.0, 0.0,  0.5, 0.5,   # top right
     1.0, -1.0, 0.0,  0.5, 0.0,   # bottom right
    -1.0, -1.0, 0.0,  0.0, 0.0,   # bottom left
    -1.0,  1.0, 0.0,  0.0, 0.5,   # top left
], dtype=np.float32)


VERTEX_SHADER = """
    #version 330 core

    in vec3 position;
    in vec2 in_texture_coords;

    out vec2 texture_coord;

    void main()
    {
        gl_Position = vec4(position.xyz, 1.0);
        texture_coord = in_texture_coords * 2 - 0.5;
    }
"""

FRAGMENT_SHADER = """
    #version 330 core

    in vec2 texture_coord;

    uniform sampler2D image_texture;

    out vec4 fragemnt_color;

    void main()
    {
        fragemnt_color = texture(image_texture, texture_coord);
    } 
"""


def main():
    img = Image.open("./textures/face.png").convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)

    settings.WINDOW["size"] = (512, 512)
    settings.WINDOW["aspect_ratio"] = 1
    settings.WINDOW["title"] = "Hello, Texture!"

    window = moderngl_window.create_window_from_settings()

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)
    texture = window.ctx.texture(img.size, components=4, data=img.tobytes())
    texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
    texture.repeat_x = False
    texture.repeat_y = False
    # Only valid for uniform textures when using Bindless Textures.
    prog["image_texture"].handle = texture.get_handle()

    attrs = AttributeNames(position="position", texcoord_0="in_texture_coords")
    quad_fs = moderngl_window.geometry.quad_fs(attrs)
    moderngl_window.activate_context(ctx=window.ctx)

    while not window.is_closing:
        window.clear()
        # Render stuff here
        # vao.render(moderngl.TRIANGLE_FAN)
        quad_fs.render(prog)
        window.swap_buffers()


if __name__ == "__main__":
    main()
