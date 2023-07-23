import os,time,threading,math
import inputs
import win32api, win32con

# def click(x,y):
#     win32api.SetCursorPos((x,y))
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
# click(10,10)

## CONTROLER CLASS

            
class Controller:
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        
        self.connected = True

        # axis values
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        
        # btns values
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        # start the monitoring thread (to read controller inputs while the main thread is doing other things)
        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def _monitor_controller(self):
        while self.connected:
            try:
                events = inputs.get_gamepad()
                for event in events:
                    if event.code == 'ABS_Y':
                        self.LeftJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_X':
                        self.LeftJoystickX = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_RY':
                        self.RightJoystickY = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_RX':
                        self.RightJoystickX = event.state / Controller.MAX_JOY_VAL # normalize between -1 and 1
                    elif event.code == 'ABS_Z':
                        self.LeftTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                    elif event.code == 'ABS_RZ':
                        self.RightTrigger = event.state / Controller.MAX_TRIG_VAL # normalize between 0 and 1
                    elif event.code == 'BTN_TL':
                        self.LeftBumper = event.state
                    elif event.code == 'BTN_TR':
                        self.RightBumper = event.state
                    elif event.code == 'BTN_SOUTH':
                        self.A = event.state
                    elif event.code == 'BTN_NORTH':
                        self.X = event.state
                    elif event.code == 'BTN_WEST':
                        self.Y = event.state
                    elif event.code == 'BTN_EAST':
                        self.B = event.state
                    elif event.code == 'BTN_THUMBL':
                        self.LeftThumb = event.state
                    elif event.code == 'BTN_THUMBR':
                        self.RightThumb = event.state
                    elif event.code == 'BTN_SELECT':
                        self.Back = event.state
                    elif event.code == 'BTN_START':
                        self.Start = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY1':
                        self.LeftDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY2':
                        self.RightDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY3':
                        self.UpDPad = event.state
                    elif event.code == 'BTN_TRIGGER_HAPPY4':
                        self.DownDPad = event.state
            
            except inputs.UnpluggedError:
                print("Controller disconnected")
                break
            
        self.connected = False

    @property
    def name(self):
        return inputs.devices.gamepads[0].name

    @property
    def btns(self):
        s = "A : " + str(self.A) + "   " + "X : " + str(self.X) + "   " + "Y : " + str(self.Y) + "   " + "B : " + str(self.B) + "   "
        s += "L2 : " + str(self.LeftBumper) + "   " + "R2 : " + str(self.RightBumper) + "   "
        s += "L3 : " + str(self.LeftThumb) + "   " + "R3 : " + str(self.RightThumb) + "   "
        s += "Start : " + str(self.Start) + "   " + "Back : " + str(self.Back) + "   "
        
        return s

    def __str__(self):
        # print the values of all the controller inputs
        
        s = self.btns

        return s

## GLOBAL VARIABLES

SPEED = 40

## MAIN CLASS

class Winxbox:
    
    def __init__(self):
        
        ## find the controller
        self.controller = Controller()
        print("Controller found: " + self.controller.name)
        
        ## start the main loop
        self.playing = True
        self.gameloop()
    
    ## ONCE CALLED FUNCTIONS

    def quit(self):
        
        print("Program ended in " + str(self.ending_time - self.starting_time) + " seconds")

    ## GAMELOOP FUNCTIONS

    def gameloop(self):
        
        self.starting_time = time.time()
        
        # main loop
        
        while self.playing and self.controller.connected:
            
            print(self.controller)
            
            ## UPDATE mouse movement
            self.update_mouse()
            
            time.sleep(0.000001)
        
        # end of the program
        
        self.ending_time = time.time()
        self.quit()
        
    def update_mouse(self):
        
        # check LeftJoystickX and LeftJoystickY
        dx = self.controller.LeftJoystickX
        dy = self.controller.LeftJoystickY

        mouse_depl = [0,0]
        
        if abs(dx) > 0.1:
            mouse_depl[0] = int(dx*SPEED)
        if abs(dy) > 0.1:
            mouse_depl[1] = -int(dy*SPEED)

        if mouse_depl != [0,0]:
            mouse_pos = win32api.GetCursorPos()
            win32api.SetCursorPos((mouse_pos[0] + mouse_depl[0], mouse_pos[1] + mouse_depl[1]))



## MAIN FUNCTION
    
print(" --- WINXBOX --- v alpha 0.1\n\n")
program = Winxbox()