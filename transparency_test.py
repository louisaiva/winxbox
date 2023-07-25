import os
import win32con, win32gui

import glfw
import OpenGL.GL as gl


def key_callback(window,key,scancode,action,mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        print("Escape pressed")
        glfw.set_window_should_close(window,True)


def main():

    glfw.init()
            
    ## position et taille de la fenetre
    # screen = glfw.get_monitors()
    # screen = glfw.get_video_mode(screen[0])

    # w,h = int(screen.size.width/2), int(screen.size.height/2)
    # x,y = int(screen.size.width/2-w/2), int(screen.size.height/2-h/2)


    # parametrage de la fenetre
    # glfw.window_hint(glfw.DECORATED , False)
    # glfw.window_hint(glfw.FLOATING , True)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER , True)
    # glfw.window_hint(glfw.VISIBLE , False)

    # creation de la fenetre
    title = "winxbox"
    window = glfw.create_window(800, 800, title, None, None)
    # glfw.set_window_pos(window, x, y)

    # paramétrage de la fonction de gestion des évènements
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    # paramétrage de la couleur de fond
    # gl.glClearColor(0.05, 0.05, 0.05, 0)
    # gl.glClearColor(0.0, 0.0, 0.0, 0.0)


    ## hide from taskbar & alt-tab
    # hw = win32gui.FindWindow(None, title)
    # style = win32gui.GetWindowLong(hw, win32con.GWL_EXSTYLE)
    # win32gui.SetWindowLong(hw, win32con.GWL_EXSTYLE, (style & ~win32con.WS_EX_APPWINDOW) | win32con.WS_EX_TOOLWINDOW)

    ## OPENGL
    # gl.glViewport(0, 0, w, h)
    # gl.glMatrixMode(gl.GL_PROJECTION)
    # gl.glLoadIdentity()
    # gl.glOrtho(0.0, w, h, 0.0, 0.0, 1.0)

    ## show the window
    # glfw.show_window(window)

    while not glfw.window_should_close(window):
        
        # gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        glfw.swap_buffers(window)
        
        glfw.poll_events()
        
    glfw.terminate()
    
    
    
    
    
if __name__ == '__main__':
    main()