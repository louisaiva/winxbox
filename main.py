import os,time
import inputs
import win32api, win32con

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
click(10,10)

## GLOBAL VARIABLES

MAX = 32767
SPEED = 10

## MAIN CLASS

class Winxbox:
    
    def __init__(self):
        
        
        ## find the controller
        self.controller = self.find_controller()
        print("Controller found: " + self.controller.name)
        
        
        ## initialize movement vectors
        self.XY_vector = [0,0]
        self.mouse_vector = [0,0]
        
        
        ## start the main loop
        self.playing = True
        self.gameloop()
    
    ## ONCE CALLED FUNCTIONS

    def quit(self):
        
        print("Program ended in " + str(self.ending_time - self.starting_time) + " seconds")
 
    def find_controller(self):
        
        global inputs
    
        from inputs import devices
        while len(devices.gamepads) == 0:
            print("waitin for controller...")
            time.sleep(5)
            import inputs
            
        
        return devices.gamepads[0]

    ## GAMELOOP FUNCTIONS

    def gameloop(self):
        
        ## loop until the controller is disconnected
        
        self.starting_time = time.time()
        
        # main loop
        
        while self.playing:
            
            ## READ controller
            
            """ try:
                events = self.controller.read()
            except inputs.UnpluggedError:
                print("Controller disconnected")
                break
            except KeyboardInterrupt:
                print("Keyboard interruption")
                break """
                
            print(self.controller.__read_device())
            events = self.controller.read()
            
            ## CONVERT controller events to vector
            
            for event in events:
                # print(event.ev_type, event.code, event.state)
                self.handle_event(event)
            
            print('ARGHHHHH')
            
            ## APPLY vector to mouse movement
            print(self.mouse_vector , self.XY_vector)
            if self.mouse_vector != [0,0]:
                self.move_mouse()
            
        
        # end of the program
        
        self.ending_time = time.time()
        self.quit()
        
    def handle_event(self, event):
        
        # this function handles the events from the controller
        # if the event is a button press, it will call the corresponding function
        # ex : if it works with mouse, it'll call the mouse function
        # ex : if it works with keyboard, it'll show the virtual keyboard and call the keyboard function
        
        if event.ev_type == "Absolute":
            
            ## cela concerne les axes
            
            if event.code == "ABS_X":
                self.mouse_vector[0] = int(event.state*SPEED)
                self.XY_vector[0] = event.state/MAX
            elif event.code == "ABS_Y":
                self.mouse_vector[1] = int(-event.state*SPEED)
                self.XY_vector[1] = event.state/MAX

    ## MOUSE FUNCTIONS
    
    def move_mouse(self):
        
        mouse_pos = win32api.GetCursorPos()
        dx = int(self.XY_vector[0]*SPEED)
        dy = int(self.XY_vector[1]*SPEED)
        
        win32api.SetCursorPos((mouse_pos[0] + dx, mouse_pos[1] + dy))
            
        

## MAIN FUNCTION
    
print(" --- WINXBOX --- v alpha 0.1\n\n")
program = Winxbox()