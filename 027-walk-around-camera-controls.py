from pathlib import Path
import numpy as np
import pyrr
import moderngl
import moderngl_window


# https://learnopengl.com/Getting-started/Camera
# https://moderngl-window.readthedocs.io/en/latest/guide/basic_usage.html
# https://moderngl-window.readthedocs.io/en/latest/guide/window_guide.html
# https://github.com/moderngl/moderngl-window/blob/master/examples/window_events.py

# fmt: off
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
# fmt: on

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Enable DEPTH_TEST
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.prog = self.ctx.program(
            vertex_shader=VERTEX_SHADER, fragment_shader=FRAGMENT_SHADER
        )

        self.texture = self.load_texture_2d("face.png")
        self.prog["ourTexture"].handle = self.texture.get_handle()

        self.vbo = self.ctx.buffer(VERTICES)
        self.vao = self.ctx.vertex_array(
            self.prog, self.vbo, "position", "in_texture_coords"
        )

        # Starting position of the Cube
        model = pyrr.matrix44.create_identity(dtype=np.float32)
        self.prog["model"] = model.flatten()
        # Setting-up camera
        self.eye = np.array([0, 0, 3], dtype=np.float32)  # cameraPos
        self.target = np.array([0, 0, -1], dtype=np.float32)  # cameraFront
        self.up = np.array([0, 1, 0], dtype=np.float32)  # cameraUp
        self.look_at = pyrr.matrix44.create_look_at(
            eye=self.eye, target=self.target, up=self.up, dtype=np.float32
        )
        self.prog["view"] = self.look_at.flatten()
        # create perspective projection
        perspective = pyrr.matrix44.create_perspective_projection(
            fovy=45.0, aspect=512 / 512, near=0.1, far=100.0
        )
        self.prog["projection"] = perspective.flatten()

        # create camera view state
        # fmt: off
        self.camera = {
            # x rot       y rot         z rot
            "roll": 0.0, "pitch": 0.0, "yaw": 0.0,
        }
        # fmt: on
        self.target_unit = self.target

        self.linear_speed = 0.05
        self.angle_speed = 1.0
        # forward-backward
        self.WS = 0.0
        # left-right strafing
        self.AD = 0.0
        # left-right rotation
        self.QE = 0.0

    def process_keys(self):
        if self.wnd.is_key_pressed(self.wnd.keys.W):
            self.WS = 1.0
            self.update_coords()
        if self.wnd.is_key_pressed(self.wnd.keys.S):
            self.WS = -1.0
            self.update_coords()
        if self.wnd.is_key_pressed(self.wnd.keys.A):
            self.AD = 1.0
            self.update_coords()
        if self.wnd.is_key_pressed(self.wnd.keys.D):
            self.AD = -1.0
            self.update_coords()
        if self.wnd.is_key_pressed(self.wnd.keys.Q):
            self.QE = 1.0
            self.update_coords()
        if self.wnd.is_key_pressed(self.wnd.keys.E):
            self.QE = -1.0
            self.update_coords()

    def update_coords(self):
        # 1. update target_unit via pitch, roll, yaw
        # 1.1 yaw
        self.camera["yaw"] += self.QE * self.angle_speed
        self.camera["yaw"] %= 360
        self.target_unit[0] = -np.sin(np.deg2rad(180 - self.camera["yaw"]))
        self.target_unit[2] = np.cos(np.deg2rad(180 - self.camera["yaw"]))

        # 2. update eye via strafings and forward/backward moves
        # 1.1 update forward/backward
        self.eye[0] -= (self.WS * self.linear_speed) * np.sin(
            np.deg2rad(self.camera["yaw"])
        )
        self.eye[2] -= (self.WS * self.linear_speed) * np.cos(
            np.deg2rad(self.camera["yaw"])
        )
        # 1.2 update strafings
        self.eye[0] -= (self.AD * self.linear_speed) * -np.cos(
            np.deg2rad(180 - self.camera["yaw"])
        )
        self.eye[2] -= (self.AD * self.linear_speed) * -np.sin(
            np.deg2rad(180 - self.camera["yaw"])
        )

        # 3. update target
        self.target = self.eye + self.target_unit

        # 4. reset
        self.AD = 0
        self.WS = 0
        self.QE = 0

    def render(self, time: float, frame_time: float):
        # Render stuff here
        self.vao.render(moderngl.TRIANGLES)
        self.look_at = pyrr.matrix44.create_look_at(
            eye=self.eye, target=self.target, up=self.up, dtype=np.float32
        )
        self.prog["view"] = self.look_at.flatten()
        self.process_keys()


if __name__ == "__main__":
    moderngl_window.run_window_config(Window)
