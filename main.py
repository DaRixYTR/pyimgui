# pylint: disable=no-member, import-error

import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import win32gui
import win32con

def main():
    if not glfw.init():
        raise Exception("Could not initialize GLFW")

    glfw.window_hint(glfw.FLOATING, True)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
    glfw.window_hint(glfw.DECORATED, False)

    monitor = glfw.get_primary_monitor()
    video_mode = glfw.get_video_mode(monitor)
    screen_width, screen_height = video_mode.size.width, video_mode.size.height

    window = glfw.create_window(
        screen_width, screen_height - 1, "Overlay", None, None)
    glfw.set_window_pos(window, 0, 0)
    glfw.make_context_current(window)

    hwnd = glfw.get_win32_window(window)
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(
        hwnd,
        win32con.GWL_EXSTYLE,
        ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST)

    win32gui.SetLayeredWindowAttributes(
        hwnd, 0x000000, 255, win32con.LWA_COLORKEY)

    # init
    imgui.create_context()
    impl = GlfwRenderer(window)

    # variables
    slider_value = 0.5
    slider_int = 5
    checkbox_value = False
    text_val = "Dear ImGui"
    current_item = 0
    items = ["Option A", "Option B", "Option C"]
    title_color = [0.2, 0.6, 1.0, 1.0]  # light blue
    show_gui = True

    # loop
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        # insert key
        if glfw.get_key(window, glfw.KEY_INSERT) == glfw.PRESS:
            show_gui = not show_gui
            
            while glfw.get_key(window, glfw.KEY_INSERT) == glfw.PRESS:
                glfw.poll_events()

        imgui.new_frame()

        if show_gui:
            # apply chosen color
            imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND, *title_color)
            imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, *title_color)
            imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_COLLAPSED, *title_color)

            # imgui window
            imgui.begin("Cool Window")
            imgui.text("Hello there, Dear ImGui")
            imgui.text("made by: dannyext")
            imgui.separator()

            if imgui.button("Click me"):
                print("Button Clicked!")

            changed, checkbox_value = imgui.checkbox("Enable", checkbox_value)
            if changed:
                print(f"[Checkbox] now set to: {checkbox_value}")

            changed, slider_value = imgui.slider_float("Slider", slider_value, 0.0, 1.0)
            if changed:
                print(f"Slider Value: {slider_value:.2f}")

            changed, slider_int = imgui.slider_int("Integer Slider", slider_int, 0, 10)
            if changed:
                print(f"[Int slider] Value = {slider_int}")

            changed, text_val = imgui.input_text("Input Text", text_val, 256)
            if changed:
                print(f"[Text Input] New text = {text_val}")

            changed, current_item = imgui.combo("Options", current_item, items)
            if changed:
                print(f"[Combo] Option = {items[current_item]}")

            changed, title_color = imgui.color_edit4("Title bar color", *title_color)
            if changed:
                print(f"[Color picker] New Color RGB: {title_color}")

            imgui.text_colored(f"Preview: {text_val}", *title_color)
            imgui.end()
            imgui.pop_style_color(3)

        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
