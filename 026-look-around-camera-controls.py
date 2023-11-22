from pathlib import Path
from typing import Any
from moderngl_window.context.base import KeyModifiers
import pyrr
import moderngl
import moderngl_window
import numpy as np


# https://learnopengl.com/Getting-started/Camera
# https://moderngl-window.readthedocs.io/en/latest/guide/basic_usage.html
# https://moderngl-window.readthedocs.io/en/latest/guide/window_guide.html
# https://github.com/moderngl/moderngl-window/blob/master/examples/window_events.py


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


class Window(moderngl_window.WindowConfig):
    window_size = (512, 512)
    aspect_ratio = 512 / 512
    vsync = True
    title = "Hello, Camera!"
    resource_dir = (Path(__file__).parent / "textures").resolve()


    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        # Enable DEPTH_TEST
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.prog = self.ctx.program(vertex_shader=VERTEX_SHADER,
                                     fragment_shader=FRAGMENT_SHADER)

        self.texture = self.load_texture_2d("face.png")
        self.prog["ourTexture"].handle = self.texture.get_handle()

        self.vbo = self.ctx.buffer(VERTICES)
        self.vao = self.ctx.vertex_array(self.prog, self.vbo, "position", "in_texture_coords")

        # Starting position of the Cube
        model = pyrr.matrix44.create_identity(dtype=np.float32)
        self.prog["model"] = model.flatten()
        # Setting-up camera
        self.eye = [0, 0, 3]
        self.target = [0, 0, 0]
        self.up = [0, 1, 0]
        self.look_at = pyrr.matrix44.create_look_at(
            eye=self.eye,
            target=self.target,
            up=self.up,
            dtype=np.float32
        )
        self.prog["view"] = self.look_at.flatten()
        # create perspective projection
        perspective = pyrr.matrix44.create_perspective_projection(
            fovy=45.0, aspect=512/512, near=0.1, far=100.0
        )
        self.prog["projection"] = perspective.flatten()

        self.speed = 0.05
        # forward-backward
        self.WS = 0
        # left-right strafe
        self.AD = 0


    def key_event(self, key: Any, action: Any, modifiers: KeyModifiers):
        # print(f"key event: {key} | {action} | {modifiers}")
        ...


    def update_coords(self):
        self.eye = [
            self.eye[0]-(self.AD*self.speed),
            0,
            self.eye[2]-(self.WS*self.speed)
        ]
        self.target = [
            self.target[0]-(self.AD*self.speed),
            0,
            0
        ]
        self.AD = 0
        self.WS = 0


    def render(self, time: float, frame_time: float):
        # Render stuff here
        self.vao.render(moderngl.TRIANGLES)
        self.look_at = pyrr.matrix44.create_look_at(
            eye=self.eye,
            target=self.target,
            up=self.up,
            dtype=np.float32
        )

        self.prog["view"] = self.look_at.flatten()

        # make simple forward-backward and strafe moves
        if self.wnd.is_key_pressed(self.wnd.keys.W):
            self.WS = 1
            self.update_coords()
        if self.wnd.is_key_pressed(self.wnd.keys.S):
            self.WS = -1
            self.update_coords()
        if self.wnd.is_key_pressed(self.wnd.keys.A):
            self.AD = 1
            self.update_coords()
        if self.wnd.is_key_pressed(self.wnd.keys.D):
            self.AD = -1
            self.update_coords()


if __name__ == "__main__":
    moderngl_window.run_window_config(Window)
