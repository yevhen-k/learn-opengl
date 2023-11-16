import pyrr
from PIL import Image
import moderngl
import moderngl_window
from moderngl_window.conf import settings
import numpy as np
from moderngl_window.timers.clock import Timer


# https://learnopengl.com/Getting-started/Coordinate-Systems
# https://codeloop.org/python-modern-opengl-perspective-projection/
# https://stackoverflow.com/questions/45514353/pyopengl-perspective-projection

"""
As the documentation for pyrr states, matrices are laid out as row-major in memory, 
which is the opposite of GL's default convention. 
Furthermore, pyrr creates the matrices transposed to standrad GL conventions. 
"""


VERTICES = np.array([
    # positions        # texture coords
     0.5,  0.5, 0.0,   1.0, 1.0,   # top right
     0.5, -0.5, 0.0,   1.0, 0.0,   # bottom right
    -0.5, -0.5, 0.0,   0.0, 0.0,   # bottom left
    -0.5,  0.5, 0.0,   0.0, 1.0,   # top left
], dtype=np.float32)

VERTEX_SHADER = """
    #version 330 core

    in vec3 position;
    in vec2 in_texture_coords;
    
    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;


    out vec4 color;
    out vec2 texture_coord;

    void main()
    {   
        gl_Position = projection * view * model * vec4(position.xyz, 1.0);
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
    settings.WINDOW["aspect_ratio"] = 512/512
    settings.WINDOW["title"] = "Hello, 3D!"

    window = moderngl_window.create_window_from_settings()

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)
    texture = window.ctx.texture(img.size, components=4, data=img.tobytes())
    prog["ourTexture"].handle = texture.get_handle()

    vbo = window.ctx.buffer(VERTICES)
    vao = window.ctx.vertex_array(prog, vbo, "position", "in_texture_coords")

    # Going 3D paragraph
    # rotate in X axis
    model = pyrr.matrix44.create_from_x_rotation(theta=np.deg2rad(55), dtype=np.float32)
    prog["model"] = model.flatten()
    # translate in Z axis
    # raw numpy implementation won't work due to row/col layout
    # view = np.eye(4, dtype=np.float32)
    # view[2, 3] = -3
    # prog["view"] = view.flatten()
    # print(view)
    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0,0.0,-3.0] ))
    prog["view"] = view.flatten()
    # create perspective projection
    perspective = pyrr.matrix44.create_perspective_projection(
        fovy=45.0, aspect=512/512, near=0.1, far=100.0
    )
    prog["projection"] = perspective.flatten()

    moderngl_window.activate_context(ctx=window.ctx)

    timer = Timer()
    timer.start()
    while not window.is_closing:
        window.clear()
        # Render stuff here
        vao.render(moderngl.TRIANGLE_FAN)
        # rotate model on X axis
        model_rot = pyrr.matrix44.create_from_axis_rotation(axis=np.array([0, 2, 0.5]),
                                                                    theta=np.deg2rad(50*timer.time),
                                                                    dtype=np.float32)
        prog["model"] = model_rot.flatten()
        window.swap_buffers()


if __name__ == "__main__":
    main()
