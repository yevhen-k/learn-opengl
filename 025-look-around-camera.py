import pyrr
from PIL import Image
import moderngl
import moderngl_window
from moderngl_window.conf import settings
import numpy as np
from moderngl_window.timers.clock import Timer


# https://learnopengl.com/Getting-started/Camera


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

    settings.WINDOW["size"] = (512, 512)
    settings.WINDOW["aspect_ratio"] = 512/512
    settings.WINDOW["vsync"] = True
    settings.WINDOW["title"] = "Hello, Camera!"

    window = moderngl_window.create_window_from_settings()

    # Enable DEPTH_TEST
    window.ctx.enable(moderngl.DEPTH_TEST)

    prog = window.ctx.program(vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER)
    texture = window.ctx.texture(img.size, components=4, data=img.tobytes())
    prog["ourTexture"].handle = texture.get_handle()

    vbo = window.ctx.buffer(VERTICES)
    vao = window.ctx.vertex_array(prog, vbo, "position", "in_texture_coords")

    # Going 3D paragraph
    # Starting position of the Cube
    model = pyrr.matrix44.create_identity(dtype=np.float32)
    prog["model"] = model.flatten()
    # Setting-up camera
    look_at = pyrr.matrix44.create_look_at(
        eye=[0, 0, 3],
        target=[0, 0, 0],
        up=[0, 1, 0],
        dtype=np.float32
    )
    prog["view"] = look_at.flatten()
    # create perspective projection
    perspective = pyrr.matrix44.create_perspective_projection(
        fovy=45.0, aspect=512/512, near=0.1, far=100.0
    )
    prog["projection"] = perspective.flatten()


    moderngl_window.activate_context(ctx=window.ctx)

    timer = Timer()
    timer.start()
    radius = 3.0
    while not window.is_closing:
        window.clear()
        # Render stuff here
        vao.render(moderngl.TRIANGLES)
        time = timer.time
        cam_x = np.sin(time) * radius
        cam_z = np.cos(time) * radius
        look_at = pyrr.matrix44.create_look_at(
            eye=[cam_x, 0, cam_z],
            target=[0, 0, 0],
            up=[0, 1, 0],
            dtype=np.float32
        )
        prog["view"] = look_at.flatten()
        window.swap_buffers()


if __name__ == "__main__":
    main()
