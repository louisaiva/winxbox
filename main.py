import os,time,threading,math
import inputs
import win32api, win32con
import ctypes



##############################################
## CONTROLER CLASS           
##############################################

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
        
        # hats values
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
                        self.Y = event.state
                    elif event.code == 'BTN_WEST':
                        self.X = event.state
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



##############################################
## GLOBAL VARIABLES
##############################################

SPEED = 40



##############################################
## MAIN CLASS
##############################################

class Winxbox:
    
    def __init__(self):
        
        ## find the controller
        self.controller = Controller()
        print("Controller found: " + self.controller.name)
        
        
        
        
        ## initialise btns and axis to follow the controller        
        self.btns = {
            "A":0,
            "X":0,
            "Y":0,
            "B":0,
            "Start":0,
            "Back":0,
            "L2":0,
            "R2":0,
            "L3":0,
            "R3":0
        }
        self.axis = {
            "LY":0,
            "LX":0,
            "RX":0,
            "RY":0,
            "L1":0,
            "R1":0,
        }
        
        self.old_btns = self.btns.copy()
        self.old_axis = self.axis.copy()
        
        ## initialise the dict of buttons
        # 1 : just pressed
        # 0 : same as previous state
        # -1 : just released
        self.btn_events = self.btns.copy()
        self.axis_events = {
            "LY":[0,0],
            "LX":[0,0],
            "RX":[0,0],
            "RY":[0,0],
            "L1":[0,0],
            "R1":[0,0]
            }
      
      
      
      
        
        ## init mouse
        self.mouse_pos = win32api.GetCursorPos()
        
        # MENU MODE
        self.in_menu = False
        self.menu_mode = "normal"
        
        # ingame mode
        self.ingame = False
        
        
        
        
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
            
            ## UPDATE controller inputs & btns events
            self.follow_controller()
    
            if not self.ingame:
        
                ## UPDATE mouse
                self.update_mouse()
                
            ## EVENTS
            self.events()
            
            time.sleep(0.000001)
        
        # end of the program
        
        self.ending_time = time.time()
        self.quit()
        
    def follow_controller(self):
        
        ## follow the controller inputs
        
        # last frame
        self.old_btns = self.btns.copy()
        self.old_axis = self.axis.copy()
        
        # btns
        self.btns["A"] = self.controller.A
        self.btns["X"] = self.controller.X
        self.btns["Y"] = self.controller.Y
        self.btns["B"] = self.controller.B
        self.btns["Start"] = self.controller.Start
        self.btns["Back"] = self.controller.Back
        self.btns["L2"] = self.controller.LeftBumper
        self.btns["R2"] = self.controller.RightBumper
        self.btns["L3"] = self.controller.LeftThumb
        self.btns["R3"] = self.controller.RightThumb
        
        # axis
        self.axis["LY"] = self.controller.LeftJoystickY
        self.axis["LX"] = self.controller.LeftJoystickX
        self.axis["RX"] = self.controller.RightJoystickX
        self.axis["RY"] = self.controller.RightJoystickY
        self.axis["L1"] = self.controller.LeftTrigger
        self.axis["R1"] = self.controller.RightTrigger
        
        self.update_events()

    def update_events(self):
        
        ## update the dict of buttons compared to the previous frame
        for btn in self.btns:
            if self.btns[btn] == self.old_btns[btn]:
                self.btn_events[btn] = 0
            elif self.btns[btn] == 0 and self.old_btns[btn] == 1:
                self.btn_events[btn] = -1
            elif self.btns[btn] == 1 and self.old_btns[btn] == 0:
                self.btn_events[btn] = 1
                
        ## update the dict of axis compared to the previous frame
        for axis in self.axis:
            
            if self.old_axis[axis] > 0.8:
                if self.axis[axis] > 0.8:
                    self.axis_events[axis] = [0,0]
                elif (self.axis[axis] > -0.8):
                    self.axis_events[axis] = [0,-1]
                elif (self.axis[axis] < -0.8):
                    self.axis_events[axis] = [1,-1]
                    
            elif self.old_axis[axis] > -0.8:
                if self.axis[axis] > 0.8:
                    self.axis_events[axis] = [0,1]
                elif (self.axis[axis] > -0.8):
                    self.axis_events[axis] = [0,0]
                elif (self.axis[axis] < -0.8):
                    self.axis_events[axis] = [1,0]
                    
            elif self.old_axis[axis] < -0.8:
                if self.axis[axis] > 0.8:
                    self.axis_events[axis] = [-1,1]
                elif (self.axis[axis] > -0.8):
                    self.axis_events[axis] = [-1,0]
                elif (self.axis[axis] < -0.8):
                    self.axis_events[axis] = [0,0]
     
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
            win32api.SetCursorPos((self.mouse_pos[0] + mouse_depl[0], self.mouse_pos[1] + mouse_depl[1]))

        # update mouse_pos
        self.mouse_pos = win32api.GetCursorPos()
        
    def events(self):
        

        # START : menu btn
        if self.btn_events["Start"] == 1:
            self.in_menu = True
            self.menu_mode = "normal"
            print("entering menu")
        elif self.btn_events["Start"] == -1:
            self.in_menu = False
            self.menu_mode = "normal"
            self.key_depress(0x12)
            print("exiting menu")
        
        # menu
        if self.in_menu:
            
            if self.menu_mode == "normal":
                
                if self.axis_events["RX"][0] == 1:
                    # switch ingame mode
                    self.ingame = not self.ingame
                    if self.ingame:
                        print("In game mode activated")
                    else:
                        print("In game mode deactivated")
                elif self.axis_events["RX"][1] == 1:
                    # menu mode : alt-tab
                    self.menu_mode = "alt-tab"
                    self.key_press(0x12) # alt
                    self.key_click(0x09) # tab
                    
                elif self.axis_events["RY"][0] == 1:
                    # windows D (desktop)
                    self.windows_d()
                elif self.axis_events["RY"][1] == 1:
                    # windows search (search bar)
                    self.windows_s()
    
            elif self.menu_mode == "alt-tab":
                
                print("alt-tab mode")
                
                if self.axis_events["RX"][0] == 1:
                    # click shift + tab
                    self.key_press(0x10) # shift
                    self.key_press(0x09) # tab
                    self.key_depress(0x10) # shift
                    self.key_depress(0x09) # tab
                    
                elif self.axis_events["RX"][1] == 1:
                    self.key_click(0x09) # tab
                
                elif self.axis_events["RY"][0] == 1 or self.axis_events["RY"][1] == 1:
                    self.menu_mode = "normal"
                    self.key_depress(0x12)
                
    
        if not self.ingame:
        
            # Back : keyboard
            
            # A : click
            if self.btn_events["A"] == 1:
                self.mouse_click()
            elif self.btn_events["A"] == -1:
                self.mouse_declick()
            
            # X : right click
            if self.btn_events["X"] == 1:
                self.mouse_click(True)
            elif self.btn_events["X"] == -1:
                self.mouse_declick(True)
    
    
    ## ACTIONS FUNCTIONS
    
    def mouse_click(self,right=False):
        if not right:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,self.mouse_pos[0],self.mouse_pos[1],0,0)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,self.mouse_pos[0],self.mouse_pos[1],0,0)
    
    def mouse_declick(self,right=False):
        if not right:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,self.mouse_pos[0],self.mouse_pos[1],0,0)
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,self.mouse_pos[0],self.mouse_pos[1],0,0)


    ## KEYBOARD FUNCTIONS
    
    def key_press(self,key):
        win32api.keybd_event(key,0,0,0)
    
    def key_depress(self,key):
        win32api.keybd_event(key,0,2,0)
    
    def key_click(self,key):
        self.key_press(key)
        self.key_depress(key)
    
    def alt_tab(self):
        win32api.keybd_event(0x12,0,0,0)
        win32api.keybd_event(0x09,0,0,0)
        win32api.keybd_event(win32con.VK_TAB,0,2,0)
        win32api.keybd_event(0x12,0,2,0)
        
    def windows_d(self):
        win32api.keybd_event(win32con.VK_LWIN,0,0,0)
        win32api.keybd_event(0x44,0,0,0)
        win32api.keybd_event(0x44,0,2,0)
        win32api.keybd_event(win32con.VK_LWIN,0,2,0)
        
    def windows_s(self):
        win32api.keybd_event(win32con.VK_LWIN,0,0,0)
        win32api.keybd_event(0x53,0,0,0)
        win32api.keybd_event(0x53,0,2,0)
        win32api.keybd_event(win32con.VK_LWIN,0,2,0)

##############################################
## MAIN FUNCTION
##############################################

print(" --- WINXBOX --- v alpha 0.1\n\n")
program = Winxbox()