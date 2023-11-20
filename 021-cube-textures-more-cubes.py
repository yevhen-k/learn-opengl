import pyrr
from PIL import Image
import moderngl
import moderngl_window
from moderngl_window.conf import settings
import numpy as np
from moderngl_window.timers.clock import Timer


# https://learnopengl.com/Getting-started/Coordinate-Systems
# https://github.com/moderngl/moderngl-window/blob/master/examples/geometry_cube.py
# https://github.com/moderngl/moderngl-window/blob/master/examples/resources/programs/cube_simple.glsl
# https://learnopengl.com/code_viewer.php?code=getting-started/cube_vertices


VERTICES = np.array([
    # positions        # texture coords
    -0.5, -0.5, -0.5,  0.0, 0.0,
     0.5, -0.5, -0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 0.0,

    -0.5, -0.5,  0.5,  0.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5,  0.5,  0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,

    -0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5,  0.5,  1.0, 0.0,

     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5,  0.5,  0.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,

    -0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  1.0, 1.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,

    -0.5,  0.5, -0.5,  0.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5, -0.5,  0.0, 1.0
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

    settings.WINDOW["size"] = (1280, 720)
    settings.WINDOW["aspect_ratio"] = 1280/720
    settings.WINDOW["vsync"] = True
    settings.WINDOW["title"] = "MOAR CUBES!"

    window = moderngl_window.create_window_from_settings()

    # Enable DEPTH_TEST
    window.ctx.enable(moderngl.DEPTH_TEST)

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)
    texture = window.ctx.texture(img.size, components=4, data=img.tobytes())
    prog["ourTexture"].handle = texture.get_handle()

    vbo = window.ctx.buffer(VERTICES)
    vao = window.ctx.vertex_array(prog, vbo, "position", "in_texture_coords")

    # Going 3D paragraph
    # rotate in X axis
    model = pyrr.matrix44.create_from_x_rotation(theta=np.deg2rad(45), dtype=np.float32)
    prog["model"] = model.flatten()
    # translate in Z axis
    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -3.0]))
    prog["view"] = view.flatten()
    # create perspective projection
    perspective = pyrr.matrix44.create_perspective_projection(
        fovy=60.0, aspect=1280/720, near=0.1, far=100.0
    )
    prog["projection"] = perspective.flatten()

    moderngl_window.activate_context(ctx=window.ctx)

    cube_positions = np.array(
        [
            pyrr.matrix44.create_from_translation(pyrr.Vector3([ 0.0,  0.0,  0.0])),
            pyrr.matrix44.create_from_translation(pyrr.Vector3([ 2.0,  5.0, -15.0])),
            pyrr.matrix44.create_from_translation(pyrr.Vector3([-1.5, -2.2, -2.5])),
            pyrr.matrix44.create_from_translation(pyrr.Vector3([-3.8, -2.0, -12.3])),
            pyrr.matrix44.create_from_translation(pyrr.Vector3([ 2.4, -0.4, -3.5])),
            pyrr.matrix44.create_from_translation(pyrr.Vector3([-1.7,  3.0, -7.5])),
            pyrr.matrix44.create_from_translation(pyrr.Vector3([ 1.3, -2.0, -2.5])),
            pyrr.matrix44.create_from_translation(pyrr.Vector3([ 1.5,  2.0, -2.5])),
            pyrr.matrix44.create_from_translation(pyrr.Vector3([ 1.5,  0.2, -1.5])),
            pyrr.matrix44.create_from_translation(pyrr.Vector3([-1.3,  1.0, -1.5])),
        ],
        dtype=np.float32)

    timer = Timer()
    timer.start()
    while not window.is_closing:
        window.clear()
        # Render stuff here
        for idx, cube in enumerate(cube_positions):
            vao.render(moderngl.TRIANGLES)
            # just some random rotatation
            model_rot = pyrr.matrix44.create_from_axis_rotation(axis=np.array([0+idx, 2-idx, 0.5+idx]),
                                                                theta=np.deg2rad(50*timer.time),
                                                                dtype=np.float32)
            prog["model"] = (model_rot.dot(cube)).flatten()
        window.swap_buffers()


if __name__ == "__main__":
    main()
