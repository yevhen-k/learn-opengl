import moderngl_window
from moderngl_window.conf import settings

# https://learnopengl.com/Getting-started/Hello-Window
# https://moderngl-window.readthedocs.io/en/latest/guide/window_guide.html


BLUE = (132/255, 151/255, 255/255)


def main():
    settings.WINDOW["size"] = (512, 512)
    settings.WINDOW["aspect_ratio"] = 1
    settings.WINDOW["title"] = "Just Window"
    window = moderngl_window.create_window_from_settings()
    moderngl_window.activate_context(ctx=window.ctx)
    while not window.is_closing:
        window.clear(*BLUE)
        # Render stuff here
        window.swap_buffers()


if __name__ == "__main__":
    main()
