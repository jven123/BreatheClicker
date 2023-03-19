
import win32api, win32con, win32gui, win32process, psutil, time, threading, random, winsound, os, json, subprocess, sys, asyncio, itertools, base64, re, pyMeow
import pynput, pyautogui
import dearpygui.dearpygui as dpg
from pypresence import Presence
import shutil
import win32com.client
from pynput.keyboard import Key, Controller


keyboard = Controller()


version = "1.3.25"
edition = " beta"
Ver = "1"
versionint = 1300



class configListener(dict):
    def __init__(self, initialDict):
        for k, v in initialDict.items():
            if isinstance(v, dict):
                initialDict[k] = configListener(v)

        super().__init__(initialDict)

    def __setitem__(self, item, value):
        if isinstance(value, dict):
            _value = configListener(value)
        else:
            _value = value

        super().__setitem__(item, _value)

        try:
            breatheClass
        except:
            while True:
                try:
                    breatheClass

                    break
                except:
                    time.sleep(0.1)

                    pass

        if breatheClass.config["misc"]["saveSettings"]:
            json.dump(breatheClass.config, open(f"{os.environ['LOCALAPPDATA']}\\temp\\{hwid}", "w", encoding="utf-8"), indent=4)




class breathe():
    def __init__(self, hwid: str):
        self.config = {
            "left": {
                "enabled": False,
                "mode": "Hold",
                "bind": 0,
                "maxCPS": 12,
                "minCPS": 12,
                "onlyWhenFocused": True,
                "stap1": False,
                "stap2": False,
                "stapChance": 8,
                "wtap1": False,
                "wtap2": False,
                "wtapChance": 8,
                "breakBlocks": False,
                "RMBLock": False,
                "allowBlockHit": False,
                "blockHit": False,
                "blockHitChance": 20,
                "shakeEffect": False,
                "shakeEffectForce": 5,
                "soundPath": "",
                "workInMenus": False,
                "blatant": False,
            },
            "right": {
                "enabled": False,
                "mode": "Hold",
                "bind": 0,
                "maxCPS": 12,
                "minCPS": 12,
                "onlyWhenFocused": True,
                "eatAndDrink": False,
                "LMBLock": False,
                "shakeEffect": False,
                "shakeEffectForce": False,
                "soundPath": "",
                "workInMenus": False,
                "blatant": False
            },
            "recorder": {
                "enabled": False,
                "record": [0.08] # Default 12 CPS  
            },
            "autohop": {
                "enabled": False,
                "bind": 0,
                "time": 1 #autojump time
            },
            "autobridge": {
                "enabled": False,
                "onlyWhenFocused": True,
                "bind": 0,
                "time": 1 #speedbridge time
            },
            "autosprint": {
                "enabled": False,
                "togglekey": 0,
            },
            "overlay": {
                "enabled": True,
                "onlyWhenFocused": True,
                "x": 0,
                "y": 0
            },
            "misc": {
                "saveSettings": True,
                "guiHidden": False,
                "bindHideGUI": 0,
                "discordRichPresence": True
            }     
        }

        if os.path.isfile(f"{os.environ['LOCALAPPDATA']}\\temp\\{hwid}"):
            try:
                config = json.loads(open(f"{os.environ['LOCALAPPDATA']}\\temp\\{hwid}", encoding="utf-8").read())

                isConfigOk = True
                for key in self.config:
                    if not key in config or len(self.config[key]) != len(config[key]):
                        isConfigOk = False

                        break

                if isConfigOk:
                    if not config["misc"]["saveSettings"]:
                        self.config["misc"]["saveSettings"] = False
                    else:
                        self.config = config
            except:
                pass

        self.config = configListener(self.config)

        self.record = itertools.cycle(self.config["recorder"]["record"])

        threading.Thread(target=self.discordRichPresence, daemon=True).start()
        
        threading.Thread(target=self.windowListener, daemon=True).start()
        threading.Thread(target=self.autoBridgeBindListener, daemon=True).start()
        threading.Thread(target=self.leftBindListener, daemon=True).start()
        threading.Thread(target=self.rightBindListener, daemon=True).start()
        threading.Thread(target=self.hideGUIBindListener, daemon=True).start()
        threading.Thread(target=self.autoHopBindListener, daemon=True).start()


        threading.Thread(target=self.autoHop, daemon=True).start()
        threading.Thread(target=self.autoBridge, daemon=True).start()
        threading.Thread(target=self.leftClicker, daemon=True).start()
        threading.Thread(target=self.rightClicker, daemon=True).start()
        threading.Thread(target=self.autoSprint, daemon=True).start()



    def discordRichPresence(self):
        asyncio.set_event_loop(asyncio.new_event_loop())

        discordRPC = Presence("1067741426521215037")
        discordRPC.connect()

        startTime = time.time()

        states = [
            "Breathe Client"
        ]

        while True:
            if self.config["misc"]["discordRichPresence"]:
                discordRPC.update(state=random.choice(states), start=startTime, large_text="Breathe Client", buttons=[{"label": "Discord Server", "url": "https://discord.gg/Jchr62cncP"}])
            else:
                discordRPC.clear()

            time.sleep(15)

    def windowListener(self):
        while True:
            currentWindow = win32gui.GetForegroundWindow()
            self.realTitle = win32gui.GetWindowText(currentWindow)
            self.window = win32gui.FindWindow("LWJGL", None)

            try:
                self.focusedProcess = psutil.Process(win32process.GetWindowThreadProcessId(currentWindow)[-1]).name()
            except:
                self.focusedProcess = ""

            time.sleep(0.5)

    def overlay(self):
        try: 
            self.focusedProcess
            self.realTitle
            self.config
        except:
            while True:
                try:
                    self.focusedProcess
                    self.realTitle
                    self.config

                    break
                except:
                    time.sleep(0.1)

                    pass

        pyMeow.overlay_init(title="Breathe - HUD")


        while pyMeow.overlay_loop():
            if not self.config["overlay"]["enabled"]:
                pyMeow.overlay_close()

                continue

            if self.config["overlay"]["onlyWhenFocused"]:
                if not "java" in self.focusedProcess and not "AZ-Launcher" in self.focusedProcess:

                    pyMeow.end_drawing()

                    time.sleep(0.5)

                    continue
                else:
                    rect = (0, 0)

            try:
                if not rect:
                    rect = pyMeow.get_window_info(self.realTitle)
            except:
                time.sleep(0.5)

                continue

            pyMeow.begin_drawing()




            logo = pyMeow.load_texture("assets/logopng.png")
            pyMeow.draw_texture(logo, rect[0]+self.config["overlay"]["x"]+2, rect[1]+self.config["overlay"]["y"]-78, pyMeow.get_color("white"), 0, 0.12)





            pyMeow.draw_text(f"Breathe Client", rect[0]+self.config["overlay"]["x"]+2, rect[1]+self.config["overlay"]["y"]-16.9, 19, pyMeow.get_color("blue"))


            pyMeow.draw_text(f"LeftClicker", rect[0]+self.config["overlay"]["x"]+2, rect[1]+self.config["overlay"]["y"]+0, 15, pyMeow.get_color("cyan"))
            pyMeow.draw_text(f"RightClicker", rect[0]+self.config["overlay"]["x"]+2, rect[1]+self.config["overlay"]["y"]+16.9, 15, pyMeow.get_color("cyan"))
            pyMeow.draw_text(f"WTap", rect[0]+self.config["overlay"]["x"]+2, rect[1]+self.config["overlay"]["y"]+32.8, 15, pyMeow.get_color("cyan"))
            pyMeow.draw_text(f"STap", rect[0]+self.config["overlay"]["x"]+2, rect[1]+self.config["overlay"]["y"]+49.6, 15, pyMeow.get_color("cyan"))
            pyMeow.draw_text(f"AutoBridge", rect[0]+self.config["overlay"]["x"]+2, rect[1]+self.config["overlay"]["y"]+66.5, 15, pyMeow.get_color("cyan"))
            pyMeow.draw_text(f"AutoSprint", rect[0]+self.config["overlay"]["x"]+2, rect[1]+self.config["overlay"]["y"]+83.4, 15, pyMeow.get_color("cyan"))
            pyMeow.draw_text(f"AutoHop", rect[0]+self.config["overlay"]["x"]+2, rect[1]+self.config["overlay"]["y"]+100.3, 15, pyMeow.get_color("cyan"))


            pyMeow.draw_text(f"[Enabled]" if self.config["left"]["enabled"] else "[Disabled]", rect[0]+self.config["overlay"]["x"]+84, rect[1]+self.config["overlay"]["y"]+0, 15, pyMeow.get_color("green") if self.config["left"]["enabled"] else pyMeow.get_color("red"))
            pyMeow.draw_text(f"[Enabled]" if self.config["right"]["enabled"] else "[Disabled]", rect[0]+self.config["overlay"]["x"]+90, rect[1]+self.config["overlay"]["y"]+16.9, 15, pyMeow.get_color("green") if self.config["right"]["enabled"] else pyMeow.get_color("red"))
            pyMeow.draw_text(f"[Enabled]" if self.config["left"]["wtap1"] or self.config["left"]["wtap2"] else "[Disabled]", rect[0]+self.config["overlay"]["x"]+43, rect[1]+self.config["overlay"]["y"]+32.8, 15, pyMeow.get_color("green") if self.config["left"]["wtap1"] or self.config["left"]["wtap2"] else pyMeow.get_color("red"))
            pyMeow.draw_text(f"[Enabled]" if self.config["left"]["stap1"] or self.config["left"]["stap2"] else "[Disabled]", rect[0]+self.config["overlay"]["x"]+41, rect[1]+self.config["overlay"]["y"]+49.6, 15, pyMeow.get_color("green") if self.config["left"]["stap1"] or self.config["left"]["stap2"] else pyMeow.get_color("red"))
            pyMeow.draw_text(f"[Enabled]" if self.config["autobridge"]["enabled"] else "[Disabled]", rect[0]+self.config["overlay"]["x"]+83, rect[1]+self.config["overlay"]["y"]+66.5, 15, pyMeow.get_color("green") if self.config["autobridge"]["enabled"] else pyMeow.get_color("red"))
            pyMeow.draw_text(f"[Enabled]" if self.config["autosprint"]["enabled"] else "[Disabled]", rect[0]+self.config["overlay"]["x"]+82, rect[1]+self.config["overlay"]["y"]+83.4, 15, pyMeow.get_color("green") if self.config["autosprint"]["enabled"] else pyMeow.get_color("red"))
            pyMeow.draw_text(f"[Enabled]" if self.config["autohop"]["enabled"] else "[Disabled]", rect[0]+self.config["overlay"]["x"]+64, rect[1]+self.config["overlay"]["y"]+100.3, 15, pyMeow.get_color("green") if self.config["autohop"]["enabled"] else pyMeow.get_color("red"))



            pyMeow.end_drawing()

            rect = None

            time.sleep(0.1)



    def autoSprint(self):
        while True:
            if self.config["autosprint"]["enabled"]:
                if not "java" in self.focusedProcess and not "AZ-Launcher" in self.focusedProcess:
                    time.sleep(1.0)

                    continue


         
            if self.config["autosprint"]["enabled"]:
                pyautogui.keyDown("r")


            time.sleep(0.001)


            
    def autoBridge(self):
        while True:
            if self.config["autobridge"]["onlyWhenFocused"]:
                if not "java" in self.focusedProcess and not "AZ-Launcher" in self.focusedProcess:
                    time.sleep(1.0)

                    continue
         
            if self.config["autobridge"]["enabled"]:
                pyautogui.keyDown("shift")
                time.sleep(0.1)
                win32api.SendMessage(self.window, win32con.WM_RBUTTONDOWN, 0, 0)
                time.sleep(0.6)
                pyautogui.keyUp("shift")
                time.sleep(0.02)
                win32api.SendMessage(self.window, win32con.WM_RBUTTONUP, 0, 0)
                time.sleep(0.06)

            time.sleep(0.0001)



    def autoBridgeBindListener(self):
        while True:
            if win32api.GetAsyncKeyState(self.config["autobridge"]["bind"]) != 0:
                if "java" in self.focusedProcess or "AZ-Launcher" in self.focusedProcess:
                    cursorInfo = win32gui.GetCursorInfo()[1]
                    if cursorInfo > 50000 and cursorInfo < 100000:
                        time.sleep(0.001)

                        continue

                self.config["autobridge"]["enabled"] = not self.config["autobridge"]["enabled"]

                while True:
                    try:
                        dpg.set_value(checkboxToggleAutobridge, not dpg.get_value(checkboxToggleAutobridge))

                        break
                    except:
                        time.sleep(0.1)

                        pass

                while win32api.GetAsyncKeyState(self.config["autobridge"]["bind"]) != 0:
                    time.sleep(0.001)

            time.sleep(0.001)


    def autoHop(self):
        while True:
            if self.config["autohop"]["enabled"]:
                if not "java" in self.focusedProcess and not "AZ-Launcher" in self.focusedProcess:
                    time.sleep(1.0)

                    continue


         
            if self.config["autohop"]["enabled"]:
                pyautogui.keyDown("space")
                time.sleep(1)


            time.sleep(0.001)



    def autoHopBindListener(self):
        while True:
            if win32api.GetAsyncKeyState(self.config["autohop"]["bind"]) != 0:
                if "java" in self.focusedProcess or "AZ-Launcher" in self.focusedProcess:
                    cursorInfo = win32gui.GetCursorInfo()[1]
                    if cursorInfo > 50000 and cursorInfo < 100000:
                        time.sleep(0.001)

                        continue

                self.config["autohop"]["enabled"] = not self.config["autohop"]["enabled"]

                while True:
                    try:
                        dpg.set_value(checkboxToggleAutoHop, not dpg.get_value(checkboxToggleAutoHop))

                        break
                    except:
                        time.sleep(0.1)

                        pass

                while win32api.GetAsyncKeyState(self.config["autohop"]["bind"]) != 0:
                    time.sleep(0.001)

            time.sleep(0.001)



    def leftClicker(self):
        while True:
            if not self.config["recorder"]["enabled"]:
                if self.config["left"]["blatant"]:
                    delay = 1 / random.choice([ self.config["left"]["maxCPS"] , self.config["left"]["minCPS"] ])
                else:
                    delay = random.random() % (2 / random.choice([ self.config["left"]["maxCPS"] , self.config["left"]["minCPS"] ]) )
            else:
                delay = float(next(self.record))

            if self.config["left"]["enabled"]:
                if self.config["left"]["mode"] == "Hold" and not win32api.GetAsyncKeyState(0x01) < 0:
                    time.sleep(delay)

                    continue
            
                if self.config["left"]["RMBLock"]:
                    if win32api.GetAsyncKeyState(0x02) < 0:
                        time.sleep(delay)

                        continue

                if self.config["left"]["onlyWhenFocused"]:
                    if not "java" in self.focusedProcess and not "AZ-Launcher" in self.focusedProcess:
                        time.sleep(delay)

                        continue

                    if not self.config["left"]["workInMenus"]:
                        cursorInfo = win32gui.GetCursorInfo()[1]
                        if cursorInfo > 50000 and cursorInfo < 100000:
                            time.sleep(delay)

                            continue

                if self.config["left"]["onlyWhenFocused"]:
                    threading.Thread(target=self.leftClick, args=(True,), daemon=True).start()
                else:
                    threading.Thread(target=self.leftClick, args=(None,), daemon=True).start()

            time.sleep(delay)

    def leftClick(self, focused):
        if focused != None:
            if self.config["left"]["breakBlocks"]:
                win32api.SendMessage(self.window, win32con.WM_LBUTTONDOWN, 0, 0)
            else:
                win32api.SendMessage(self.window, win32con.WM_LBUTTONDOWN, 0, 0)
                time.sleep(0.02)
                win32api.SendMessage(self.window, win32con.WM_LBUTTONUP, 0, 0)

            if self.config["left"]["blockHit"] or (self.config["left"]["blockHit"] and self.config["right"]["enabled"] and self.config["right"]["LMBLock"] and not win32api.GetAsyncKeyState(0x02) < 0):
                if random.uniform(0, 1) <= self.config["left"]["blockHitChance"] / 100.0:
                    win32api.SendMessage(self.window, win32con.WM_RBUTTONDOWN, 0, 0)
                    time.sleep(0.02)
                    win32api.SendMessage(self.window, win32con.WM_RBUTTONUP, 0, 0)

            if self.config["left"]["allowBlockHit"] or (self.config["left"]["allowBlockHit"] and self.config["right"]["enabled"] and self.config["right"]["LMBLock"] and not win32api.GetAsyncKeyState(0x02) < 0):
                    time.sleep(0.02)
                    win32api.SendMessage(self.window, win32con.WM_RBUTTONUP, 0, 0)
                    
            if self.config["left"]["stap1"] and self.config["left"]["onlyWhenFocused"]:
                if random.uniform(0, 1) <= self.config["left"]["stapChance"] / 100.0:
                    randomdelay = [0.100, 0.156, 0.145, 0.125, 0.187, 0.105]
                    pyautogui.keyDown("s")
                    time.sleep(random.choice(randomdelay))
                    pyautogui.keyUp("s")

            if self.config["left"]["stap2"]and self.config["left"]["onlyWhenFocused"]:
                if random.uniform(0, 1) <= self.config["left"]["stapChance"] / 100.0:
                    randomdelay = [0.100, 0.156, 0.145, 0.125, 0.187, 0.105]
                    keyboard.press("s")
                    time.sleep(random.choice(randomdelay))
                    keyboard.release("s")

            if self.config["left"]["wtap1"] and self.config["left"]["onlyWhenFocused"]:
                if random.uniform(0, 1) <= self.config["left"]["wtapChance"] / 100.0:
                    randomdelay = [0.100, 0.156, 0.145, 0.125, 0.187, 0.105]
                    pyautogui.keyDown("w")
                    time.sleep(0.001)
                    pyautogui.keyUp("w")
                    time.sleep(random.choice(randomdelay))

            if self.config["left"]["wtap2"]and self.config["left"]["onlyWhenFocused"]:
                if random.uniform(0, 1) <= self.config["left"]["wtapChance"] / 100.0:
                    randomdelay = [0.100, 0.156, 0.145, 0.125, 0.187, 0.105]
                    keyboard.press("w")
                    time.sleep(0.001)
                    keyboard.release("w")
                    time.sleep(random.choice(randomdelay))



        else:
            if self.config["left"]["breakBlocks"]:

                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                time.sleep(0.02)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

            if self.config["left"]["blockHit"] or (self.config["left"]["blockHit"] and self.config["right"]["enabled"] and self.config["right"]["LMBLock"] and not win32api.GetAsyncKeyState(0x02) < 0):
                if random.uniform(0, 1) <= self.config["left"]["blockHitChance"] / 100.0:
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                    time.sleep(0.02)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

            if self.config["left"]["allowBlockHit"] or (self.config["left"]["allowBlockHit"] and self.config["right"]["enabled"] and self.config["right"]["LMBLock"] and not win32api.GetAsyncKeyState(0x02) < 0):
                    time.sleep(0.02)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)




        if self.config["left"]["soundPath"] != "" and os.path.isfile(self.config["left"]["soundPath"]):
            winsound.PlaySound(self.config["left"]["soundPath"], winsound.SND_ASYNC)

        if self.config["left"]["shakeEffect"]:
            currentPos = win32api.GetCursorPos()
            direction = random.randint(0, 3)
            pixels = random.randint(-self.config["left"]["shakeEffectForce"], self.config["left"]["shakeEffectForce"])

            if direction == 0:
                win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] - pixels))
            elif direction == 1:
                win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] + pixels))
            elif direction == 2:
                win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] + pixels))
            elif direction == 3:
                win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] - pixels))

    def leftBindListener(self):
        while True:
            if win32api.GetAsyncKeyState(self.config["left"]["bind"]) != 0:
                if "java" in self.focusedProcess or "AZ-Launcher" in self.focusedProcess:
                    cursorInfo = win32gui.GetCursorInfo()[1]
                    if cursorInfo > 50000 and cursorInfo < 100000:
                        time.sleep(0.001)

                        continue
                    

                self.config["left"]["enabled"] = not self.config["left"]["enabled"]

                while True:
                    try:
                        dpg.set_value(checkboxToggleLeftClicker, not dpg.get_value(checkboxToggleLeftClicker))

                        break
                    except:
                        time.sleep(0.1)

                        pass

                while win32api.GetAsyncKeyState(self.config["left"]["bind"]) != 0:
                    time.sleep(0.001)

            time.sleep(0.001)

    def rightClicker(self):
        while True:
            if self.config["right"]["blatant"]:
                delay = 1 / random.choice([ self.config["right"]["maxCPS"] , self.config["right"]["minCPS"] ])
            else:
                delay = random.random() % (2 / random.choice([ self.config["right"]["maxCPS"] , self.config["right"]["minCPS"] ]) )

            if self.config["right"]["enabled"]:
                if self.config["right"]["mode"] == "Hold" and not win32api.GetAsyncKeyState(0x02) < 0:
                    time.sleep(delay)

                    continue

                if self.config["right"]["LMBLock"]:
                    if win32api.GetAsyncKeyState(0x01) < 0:
                        time.sleep(delay)

                        continue

                if self.config["right"]["onlyWhenFocused"]:
                    if not "java" in self.focusedProcess and not "AZ-Launcher" in self.focusedProcess:
                        time.sleep(delay)

                        continue
            
                    if not self.config["right"]["workInMenus"]:
                        cursorInfo = win32gui.GetCursorInfo()[1]
                        if cursorInfo > 50000 and cursorInfo < 100000:
                            time.sleep(delay)

                            continue

                if self.config["right"]["onlyWhenFocused"]:
                    threading.Thread(target=self.rightClick, args=(True,), daemon=True).start()
                else:
                    threading.Thread(target=self.rightClick, args=(None,), daemon=True).start()

            time.sleep(delay)

    def rightClick(self, focused):
        if focused != None:
            if self.config["right"]["eatAndDrink"]:
                win32api.SendMessage(self.window, win32con.WM_RBUTTONDOWN, 0, 0)
            else:
                win32api.SendMessage(self.window, win32con.WM_RBUTTONDOWN, 0, 0)
                time.sleep(0.02)
                win32api.SendMessage(self.window, win32con.WM_RBUTTONUP, 0, 0)

        else:
            if self.config["right"]["eatAndDrink"]:
                # time.sleep(0.02)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                # win32api.SendMessage(self.window, win32con.WM_RBUTTONUP, 0, 0)
            else:
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
                time.sleep(0.02)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

        if self.config["right"]["soundPath"] != "" and os.path.isfile(self.config["right"]["soundPath"]):
            winsound.PlaySound(self.config["right"]["soundPath"], winsound.SND_ASYNC)

        if self.config["right"]["shakeEffect"]:
            currentPos = win32api.GetCursorPos()
            direction = random.randint(0, 3)
            pixels = random.randint(-self.config["right"]["shakeEffectForce"], self.config["right"]["shakeEffectForce"])

            if direction == 0:
                win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] - pixels))
            elif direction == 1:
                win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] + pixels))
            elif direction == 2:
                win32api.SetCursorPos((currentPos[0] + pixels, currentPos[1] + pixels))
            elif direction == 3:
                win32api.SetCursorPos((currentPos[0] - pixels, currentPos[1] - pixels))

    def rightBindListener(self):
        while True:
            if win32api.GetAsyncKeyState(self.config["right"]["bind"]) != 0:
                if "java" in self.focusedProcess or "AZ-Launcher" in self.focusedProcess:
                    cursorInfo = win32gui.GetCursorInfo()[1]
                    if cursorInfo > 50000 and cursorInfo < 100000:
                        time.sleep(0.001)

                        continue

                self.config["right"]["enabled"] = not self.config["right"]["enabled"]

                while True:
                    try:
                        dpg.set_value(checkboxToggleRightClicker, not dpg.get_value(checkboxToggleRightClicker))

                        break
                    except:
                        time.sleep(0.1)

                        pass

                while win32api.GetAsyncKeyState(self.config["right"]["bind"]) != 0:
                    time.sleep(0.001)

            time.sleep(0.001)

    def hideGUIBindListener(self):
        while True:
            if win32api.GetAsyncKeyState(self.config["misc"]["bindHideGUI"]) != 0:
                self.config["misc"]["guiHidden"] = not self.config["misc"]["guiHidden"]

                if not self.config["misc"]["guiHidden"]:
                    win32gui.ShowWindow(guiWindows, win32con.SW_SHOW)
                else:
                    win32gui.ShowWindow(guiWindows, win32con.SW_HIDE)

                while win32api.GetAsyncKeyState(self.config["misc"]["bindHideGUI"]) != 0:
                    time.sleep(0.001)

            time.sleep(0.001)

if __name__ == "__main__":
    try:
        if os.name != "nt":
            input("Breathe Client supports windows 10,11")

            os._exit(0)

        (suppost_sid, error) = subprocess.Popen("wmic useraccount where name='%username%' get sid", stdout=subprocess.PIPE, shell=True).communicate()
        hwid = suppost_sid.split(b"\n")[1].strip().decode()

        currentWindow = win32gui.GetForegroundWindow()
        processName = psutil.Process(win32process.GetWindowThreadProcessId(currentWindow)[-1]).name()
        if processName == "cmd.exe" or processName in sys.argv[0]:
            win32gui.ShowWindow(currentWindow, win32con.SW_HIDE)

        breatheClass = breathe(hwid)
        dpg.create_context()


        def toggleLeftClicker(id: int, value: bool):
            breatheClass.config["left"]["enabled"] = value

        waitingForKeyLeft = False
        def statusBindLeftClicker(id: int):
            global waitingForKeyLeft

            if not waitingForKeyLeft:
                with dpg.handler_registry(tag="Left Bind Handler"):
                    dpg.add_key_press_handler(callback=setBindLeftClicker)

                dpg.set_item_label(buttonBindLeftClicker, "...")

                waitingForKeyLeft = True

        def setBindLeftClicker(id: int, value: str):
            global waitingForKeyLeft

            if waitingForKeyLeft:
                breatheClass.config["left"]["bind"] = value

                dpg.set_item_label(buttonBindLeftClicker, f"Bind: {chr(value)}")
                dpg.delete_item("Left Bind Handler")

                waitingForKeyLeft = False

        def setLeftMode(id: int, value: str):
            breatheClass.config["left"]["mode"] = value

        def setLeftMaxCPS(id: int, value: int):
            breatheClass.config["left"]["maxCPS"] = value

        def setLeftMinCPS(id: int, value: int):
            breatheClass.config["left"]["minCPS"] = value

        def toggleLeftOnlyWhenFocused(id: int, value:bool):
            breatheClass.config["left"]["onlyWhenFocused"] = value

        def toggleLeftStap1(id: int, value:bool):
            breatheClass.config["left"]["stap1"] = value

        def toggleLeftStap2(id: int, value:bool):
            breatheClass.config["left"]["stap2"] = value

        def toggleLeftWtap1(id: int, value:bool):
            breatheClass.config["left"]["wtap1"] = value

        def toggleLeftWtap2(id: int, value:bool):
            breatheClass.config["left"]["wtap2"] = value

        def setLeftWtapChance(id: int, value: int):
            breatheClass.config["left"]["wtapChance"] = value

        def setLeftStapChance(id: int, value: int):
            breatheClass.config["left"]["stapChance"] = value

        def toggleLeftBreakBlocks(id: int, value: bool):
            breatheClass.config["left"]["breakBlocks"] = value

        def toggleLeftRMBLock(id: int, value: bool):
            breatheClass.config["left"]["RMBLock"] = value
            
        def toggleLeftAllowBlockHit(id: int, value: bool):
            breatheClass.config["left"]["allowBlockHit"] = value

        def toggleLeftBlockHit(id: int, value: bool):
            breatheClass.config["left"]["blockHit"] = value

        def setLeftBlockHitChance(id: int, value: int):
            breatheClass.config["left"]["blockHitChance"] = value

        def toggleLeftShakeEffect(id: int, value: bool):
            breatheClass.config["left"]["shakeEffect"] = value

        def setLeftShakeEffectForce(id: int, value: int):
            breatheClass.config["left"]["shakeEffectForce"] = value

        def setLeftClickSoundPath(id: int, value: str):
            breatheClass.config["left"]["soundPath"] = value

        def toggleLeftWorkInMenus(id: int, value: bool):
            breatheClass.config["left"]["workInMenus"] = value

        def toggleLeftBlatantMode(id: int, value: bool):
            breatheClass.config["left"]["blatant"] = value
            
        def toggleRightClicker(id: int, value: bool):
            breatheClass.config["right"]["enabled"] = value

        waitingForKeyRight = False
        def statusBindRightClicker(id: int):
            global waitingForKeyRight

            if not waitingForKeyRight:
                with dpg.handler_registry(tag="Right Bind Handler"):
                    dpg.add_key_press_handler(callback=setBindRightClicker)

                dpg.set_item_label(buttonBindRightClicker, "...")

                waitingForKeyRight = True

        def setBindRightClicker(id: int, value: str):
            global waitingForKeyRight

            if waitingForKeyRight:
                breatheClass.config["right"]["bind"] = value

                dpg.set_item_label(buttonBindRightClicker, f"Bind: {chr(value)}")
                dpg.delete_item("Right Bind Handler")

                waitingForKeyRight = False

        def setRightMode(id: int, value: str):
            breatheClass.config["right"]["mode"] = value

        def setRightMaxCPS(id: int, value: int):
            breatheClass.config["right"]["maxCPS"] = value

        def setRightMinCPS(id: int, value: int):
            breatheClass.config["right"]["minCPS"] = value

        def toggleRightOnlyWhenFocused(id: int, value: int):
            breatheClass.config["right"]["onlyWhenFocused"] = True

        def toggleRightEatAndDrink(id: int, value: bool):
            breatheClass.config["right"]["eatAndDrink"] = value

        def toggleRightLMBLock(id: int, value: bool):
            breatheClass.config["right"]["LMBLock"] = value

        def toggleRightShakeEffect(id: int, value: bool):
            breatheClass.config["right"]["shakeEffect"] = value

        def setRightShakeEffectForce(id: int, value: int):
            breatheClass.config["right"]["shakeEffectForce"] = value

        def setRightClickSoundPath(id: int, value: str):
            breatheClass.config["right"]["soundPath"] = value

        def toggleRightWorkInMenus(id: int, value: bool):
            breatheClass.config["right"]["workInMenus"] = value

        def toggleRightBlatantMode(id: int, value: bool):
            breatheClass.config["right"]["blatant"] = value

        def toggleAutoSprint(id: int, value: bool):
            breatheClass.config["autosprint"]["enabled"] = value

        def toggleAutobridge(id: int, value:bool):
            breatheClass.config["autobridge"]["enabled"] = value

        
        waitingForKeyAutobridge = False
        def statusBindAutobridge(id: int):
            global waitingForKeyAutobridge

            if not waitingForKeyAutobridge:
                with dpg.handler_registry(tag="Autobridge Bind Handler"):
                    dpg.add_key_press_handler(callback=setBindAutobridge)

                dpg.set_item_label(buttonBindAutobridge, "...")

                waitingForKeyAutobridge = True

        def setBindAutobridge(id: int, value: str):
            global waitingForKeyAutobridge

            if waitingForKeyAutobridge:
                breatheClass.config["autobridge"]["bind"] = value

                dpg.set_item_label(buttonBindAutobridge, f"Bind: {chr(value)}")
                dpg.delete_item("Autobridge Bind Handler")

                waitingForKeyAutobridge = False

        def toggleAutoHop(id: int, value:bool):
            breatheClass.config["autohop"]["enabled"] = value

        
        waitingForKeyAutoHop = False
        def statusBindAutoHop(id: int):
            global waitingForKeyAutoHop

            if not waitingForKeyAutoHop:
                with dpg.handler_registry(tag="AutoHop Bind Handler"):
                    dpg.add_key_press_handler(callback=setBindAutoHop)

                dpg.set_item_label(buttonBindAutoHop, "...")

                waitingForKeyAutoHop = True

        def setBindAutoHop(id: int, value: str):
            global waitingForKeyAutoHop

            if waitingForKeyAutoHop:
                breatheClass.config["autohop"]["bind"] = value

                dpg.set_item_label(buttonBindAutoHop, f"Bind: {chr(value)}")
                dpg.delete_item("AutoHop Bind Handler")

                waitingForKeyAutoHop = False

        def toggleRecorder(id: int, value: bool):
            breatheClass.config["recorder"]["enabled"] = value

        recording = False
        def recorder():
            global recording

            recording = True
            dpg.set_value(recordingStatusText, f"Recording: True")

            recorded = []
            start = 0

            while True:
                if not recording:
                    if len(recorded) < 2: # Avoid saving a record with 0 click
                        recorded[0] = 0.08
                    else:
                        recorded[0] = 0 # No delay for the first click

                        del recorded[-1] # Deleting last record time because that's when you click on stop button and it can take some time

                    breatheClass.config["recorder"]["record"] = recorded

                    breatheClass.record = itertools.cycle(recorded)

                    totalTime = 0
                    for clickTime in recorded:
                        totalTime += float(clickTime)

                    dpg.set_value(averageRecordCPSText, f"Average CPS of previous Record: {round(len(recorded) / totalTime, 2)}")

                    break

                if win32api.GetAsyncKeyState(0x01) < 0:
                    recorded.append(time.time() - start)

                    dpg.set_value(recordingStatusText, f"Recording: True - Recorded clicks: {len(recorded)}")

                    start = time.time()

                    while win32api.GetAsyncKeyState(0x01) < 0:
                        time.sleep(0.001)

        def startRecording():
            if not recording:
                threading.Thread(target=recorder, daemon=True).start()

        def stopRecording():
            global recording

            recording = False

            dpg.set_value(recordingStatusText, f"Recording: False")


        def backupsettings():
            path = os.getenv("LOCALAPPDATA")
            shutil.copyfile(path + f'\\temp\\{hwid}',f'{hwid}')



        def selfDestruct():
            dpg.destroy_context()

        waitingForKeyHideGUI = False
        def statusBindHideGUI():
            global waitingForKeyHideGUI

            if not waitingForKeyHideGUI:
                with dpg.handler_registry(tag="Hide GUI Bind Handler"):
                    dpg.add_key_press_handler(callback=setBindHideGUI)

                dpg.set_item_label(buttonBindHideGUI, "...")

                waitingForKeyHideGUI = True

        def setBindHideGUI(id: int, value: str):
            global waitingForKeyHideGUI

            if waitingForKeyHideGUI:
                breatheClass.config["misc"]["bindHideGUI"] = value

                dpg.set_item_label(buttonBindHideGUI, f"Bind: {chr(value)}")
                dpg.delete_item("Hide GUI Bind Handler")

                waitingForKeyHideGUI = False

        def toggleOverlay(id: int, value: bool):
            breatheClass.config["overlay"]["enabled"] = value

            if value:
                threading.Thread(target=breatheClass.overlay, daemon=True).start()

        def toggleOverlayOnlyWhenFocused(id: int, value: bool):
            breatheClass.config["overlay"]["onlyWhenFocused"] = value

        def setOverlayX(id: int, value: int):
            breatheClass.config["overlay"]["x"] = value

        def setOverlayY(id: int, value: int):
            breatheClass.config["overlay"]["y"] = value

        def toggleSaveSettings(id: int, value: bool):
            breatheClass.config["misc"]["saveSettings"] = value

        def toggleAlwaysOnTop(id: int, value: bool):
            if value:
                win32gui.SetWindowPos(guiWindows, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            else:
                win32gui.SetWindowPos(guiWindows, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        def toggleDiscordRPC(id: int, value: bool):
            breatheClass.config["misc"]["discordRichPresence"] = value


        dpg.create_viewport(title=f"Breathe Client V{Ver}[v{version}{edition}]", width=820, height=445)
        dpg.set_viewport_small_icon("assets/logo.ico")


        with dpg.window(tag="Primary Window"):
            with dpg.tab_bar():

                with dpg.tab(label="AutoClicker"):
                    dpg.add_spacer(width=75)


                    leftclicktext = dpg.add_text("Left Clicker")
                    with dpg.group(horizontal=True):
                        checkboxToggleLeftClicker = dpg.add_checkbox(label="On/Off", default_value=breatheClass.config["left"]["enabled"], callback=toggleLeftClicker)
                        buttonBindLeftClicker = dpg.add_button(label="Click to Bind", callback=statusBindLeftClicker)
                        dropdownLeftMode = dpg.add_combo(label="Mode", items=["Hold", "Always"], default_value=breatheClass.config["left"]["mode"], callback=setLeftMode)

                        bind = breatheClass.config["left"]["bind"]
                        if bind != 0:
                            dpg.set_item_label(buttonBindLeftClicker, f"Bind: {chr(bind)}")

                    dpg.add_spacer(width=75)

                    sliderLeftAverageCPS = dpg.add_slider_int(label="Maximum CPS", default_value=breatheClass.config["left"]["maxCPS"], min_value=1, max_value=100, callback=setLeftMaxCPS)

                    dpg.add_spacer(width=75)

                    sliderLeftAverageCPS = dpg.add_slider_int(label="Minimum CPS", default_value=breatheClass.config["left"]["minCPS"], min_value=1, max_value=100, callback=setLeftMinCPS)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    checkboxLeftOnlyWhenFocused = dpg.add_checkbox(label="Only In Game", default_value=breatheClass.config["left"]["onlyWhenFocused"], callback=toggleLeftOnlyWhenFocused)

                    dpg.add_spacer(width=75)

                    dpg.add_spacer(width=75)

                    checkBoxLeftAllowBlockHit = dpg.add_checkbox(label="Allow BlockHit", default_value=breatheClass.config["left"]["allowBlockHit"], callback=toggleLeftAllowBlockHit)

                    dpg.add_spacer(width=75)

                    checkBoxLeftBreakBlocks = dpg.add_checkbox(label="Break Blocks", default_value=breatheClass.config["left"]["breakBlocks"], callback=toggleLeftBreakBlocks)

                    dpg.add_spacer(width=75)

                    checkboxLeftRMBLock = dpg.add_checkbox(label="RMB-Lock", default_value=breatheClass.config["left"]["RMBLock"], callback=toggleLeftRMBLock)

                    dpg.add_spacer(width=125)

                    checkboxLeftBlockHit = dpg.add_checkbox(label="AutoBlockHit", default_value=breatheClass.config["left"]["blockHit"], callback=toggleLeftBlockHit)
                    sliderLeftBlockHitChance = dpg.add_slider_int(label="AutoBlockHit Chance", default_value=breatheClass.config["left"]["blockHitChance"], min_value=1, max_value=100, callback=setLeftBlockHitChance)

                    dpg.add_spacer(width=125)
                    dpg.add_separator()
                    dpg.add_spacer(width=125)

                    checkboxLeftShakeEffect = dpg.add_checkbox(label="Jitter Effect", default_value=breatheClass.config["left"]["shakeEffect"], callback=toggleLeftShakeEffect)
                    sliderLeftShakeEffectForce = dpg.add_slider_int(label="Jitter Effect Force", default_value=breatheClass.config["left"]["shakeEffectForce"], min_value=1, max_value=20, callback=setLeftShakeEffectForce)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    inputLeftClickSoundPath = dpg.add_input_text(label="Click Sound Path", default_value=breatheClass.config["left"]["soundPath"], hint="Example: assets/clicksound.wav", callback=setLeftClickSoundPath)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    checkboxLeftWorkInMenus = dpg.add_checkbox(label="Work in Menus", default_value=breatheClass.config["left"]["workInMenus"], callback=toggleLeftWorkInMenus)
                    checkboxLeftBlatantMode = dpg.add_checkbox(label="Blatant Mode", default_value=breatheClass.config["left"]["blatant"], callback=toggleLeftBlatantMode)
                    
                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)
                    dpg.add_spacer(width=75)


                    rightclicktext = dpg.add_text("Right Clicker")

                    with dpg.group(horizontal=True):
                        checkboxToggleRightClicker = dpg.add_checkbox(label="On/Off", default_value=breatheClass.config["right"]["enabled"], callback=toggleRightClicker)
                        buttonBindRightClicker = dpg.add_button(label="Click to Bind", callback=statusBindRightClicker)
                        dropdownRightMode = dpg.add_combo(label="Mode", items=["Hold", "Always"], default_value=breatheClass.config["right"]["mode"], callback=setRightMode)

                        bind = breatheClass.config["right"]["bind"]
                        if bind != 0:
                            dpg.set_item_label(buttonBindRightClicker, f"Bind: {chr(bind)}")

                    dpg.add_spacer(width=75)

                    sliderRightAverageCPS = dpg.add_slider_int(label="Maximum CPS", default_value=breatheClass.config["right"]["maxCPS"], min_value=1, max_value=80, callback=setRightMaxCPS)

                    dpg.add_spacer(width=75)

                    sliderRightAverageCPS = dpg.add_slider_int(label="Minimum CPS", default_value=breatheClass.config["right"]["minCPS"], min_value=1, max_value=80, callback=setRightMinCPS)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    checkboxRightOnlyWhenFocused = dpg.add_checkbox(label="Only In Game", default_value=breatheClass.config["right"]["onlyWhenFocused"], callback=toggleRightOnlyWhenFocused)

                    dpg.add_spacer(width=75)
                    
                    checkBoxRightEatAndDrink = dpg.add_checkbox(label="Eat And Drink", default_value=breatheClass.config["right"]["eatAndDrink"], callback=toggleRightEatAndDrink)
                    
                    dpg.add_spacer(width=75)

                    checkboxRightLMBLock = dpg.add_checkbox(label="LMB-Lock", default_value=breatheClass.config["right"]["LMBLock"], callback=toggleRightLMBLock)

                    dpg.add_spacer(width=75)

                    checkboxRightShakeEffect = dpg.add_checkbox(label="Jitter Effect", default_value=breatheClass.config["right"]["shakeEffect"], callback=toggleRightShakeEffect)
                    sliderRightShakeEffectForce = dpg.add_slider_int(label="Jitter Effect Force", default_value=breatheClass.config["right"]["shakeEffectForce"], min_value=1, max_value=20, callback=setRightShakeEffectForce)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    inputRightClickSoundPath = dpg.add_input_text(label="Click Sound Path", default_value=breatheClass.config["right"]["soundPath"], hint="Example: clicksound.wav", callback=setRightClickSoundPath)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    checkboxRightWorkInMenus = dpg.add_checkbox(label="Work in Menus", default_value=breatheClass.config["right"]["workInMenus"], callback=toggleRightWorkInMenus)
                    checkboxRightBlatantMode = dpg.add_checkbox(label="Blatant Mode", default_value=breatheClass.config["right"]["blatant"], callback=toggleRightBlatantMode)

                with dpg.tab(label="Recorder"):
                    dpg.add_spacer(width=75)

                    recorderInfoText = dpg.add_text(default_value="Records your clicking and also makes it more undetectable.\nAfter pressing the \"Start\" button, click for a few seconds. Then press the \"Stop\" button.\nOnly works for the left click.")

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    checkboxRecorderEnabled = dpg.add_checkbox(label="Enabled", default_value=breatheClass.config["recorder"]["enabled"], callback=toggleRecorder)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    with dpg.group(horizontal=True):
                        buttonStartRecording = dpg.add_button(label="Start Recording", callback=startRecording)
                        buttonStopRecording = dpg.add_button(label="Stop Recording", callback=stopRecording)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    averageRecordCPSText = dpg.add_text(default_value="Average CPS of previous Record: ")
                    
                    totalTime = 0
                    for clickTime in breatheClass.config["recorder"]["record"]:
                        totalTime += float(clickTime)

                    dpg.set_value(averageRecordCPSText, f"Average CPS of previous Record: {round(len(breatheClass.config['recorder']['record']) / totalTime, 2)}")

                    recordingStatusText = dpg.add_text(default_value="Recording: ")
                    dpg.set_value(recordingStatusText, f"Recording: {recording}")

                with dpg.tab(label="Movement"):
                    dpg.add_spacer(width=75)

                    staptext = dpg.add_text("STap")

                    dpg.add_text("Only works for left clicker and \"Only in game\" enabled.")
                    
                    checkboxLeftSTap = dpg.add_checkbox(label="STap (Type 1)", default_value=breatheClass.config["left"]["stap1"], callback=toggleLeftStap1)

                    dpg.add_spacer(width=75)

                    checkboxLeftSTap = dpg.add_checkbox(label="STap (Type 2)", default_value=breatheClass.config["left"]["stap2"], callback=toggleLeftStap2)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=125)
                    
                    sliderLeftSTapChance = dpg.add_slider_int(label="STap Chance", default_value=breatheClass.config["left"]["stapChance"], min_value=1, max_value=100, callback=setLeftStapChance)

                    dpg.add_spacer(width=125)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)


                    wtaptext = dpg.add_text("WTap(Buggy)")

                    dpg.add_text("Only works for left clicker and \"Only in game\" enabled.")
                    
                    checkboxLeftWTap = dpg.add_checkbox(label="WTap (Type 1)", default_value=breatheClass.config["left"]["wtap1"], callback=toggleLeftWtap1)

                    dpg.add_spacer(width=75)

                    checkboxLeftWTap = dpg.add_checkbox(label="WTap (Type 2)", default_value=breatheClass.config["left"]["wtap2"], callback=toggleLeftWtap2)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=125)
                    
                    sliderLeftWTapChance = dpg.add_slider_int(label="WTap Chance", default_value=breatheClass.config["left"]["wtapChance"], min_value=1, max_value=100, callback=setLeftWtapChance)

                    dpg.add_spacer(width=125)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)
                    
                    autosprinttext = dpg.add_text("AutoSprint(Unstable)")
                    dpg.add_text("\"Only in game\" is automatically enabled.(this module is still unstable because its new and still in development)")
                    with dpg.group(horizontal=True):
                        checkboxToggleAutobridge = dpg.add_checkbox(label="On/Off", default_value=breatheClass.config["autosprint"]["enabled"], callback=toggleAutoSprint)


                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    autobridgetext = dpg.add_text("AutoBridge(Undone)")
                    dpg.add_text("\"Only in game\" is automatically enabled.(this module is still pretty bad and its still in development)")
                    with dpg.group(horizontal=True):
                        checkboxToggleAutobridge = dpg.add_checkbox(label="On/Off", default_value=breatheClass.config["autobridge"]["enabled"], callback=toggleAutobridge)
                        buttonBindAutobridge = dpg.add_button(label="Click to Bind", callback=statusBindAutobridge)

                        
                        bind = breatheClass.config["autobridge"]["bind"]
                        if bind != 0:
                            dpg.set_item_label(buttonBindAutobridge, f"Bind: {chr(bind)}")


                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    autohoptext = dpg.add_text("AutoHop")
                    dpg.add_text("\"Only in game\" is automatically enabled.")
                    with dpg.group(horizontal=True):
                        checkboxToggleAutoHop = dpg.add_checkbox(label="On/Off", default_value=breatheClass.config["autohop"]["enabled"], callback=toggleAutoHop)
                        buttonBindAutoHop = dpg.add_button(label="Click to Bind", callback=statusBindAutoHop)

                        
                        bind = breatheClass.config["autohop"]["bind"]
                        if bind != 0:
                            dpg.set_item_label(buttonBindAutoHop, f"Bind: {chr(bind)}")


                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                with dpg.tab(label="Settings"):
                    dpg.add_spacer(width=75)

                    buttonSelfDestruct = dpg.add_button(label="Self Destruct", callback=selfDestruct)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    with dpg.group(horizontal=True):
                        buttonBindHideGUI = dpg.add_button(label="Click to Bind", callback=statusBindHideGUI)
                        hideGUIText = dpg.add_text(default_value="Hide GUI")

                        bind = breatheClass.config["misc"]["bindHideGUI"]
                        if bind != 0:
                            dpg.set_item_label(buttonBindHideGUI, f"Bind: {chr(bind)}")

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    hudtext = dpg.add_text("HUD")

                    dpg.add_spacer(width=75)
                    
                    overlayInfoText = dpg.add_text(default_value="Displays an in-game GUI with Breathe's modules status info. Useful but does not work in fullscreen mode (F11).")
                    overlayInfoTextTwo = dpg.add_text(default_value="(turn on both if it doesn't work)")

                    with dpg.group(horizontal=True):
                        overlayToggle = dpg.add_checkbox(label="HUD", default_value=breatheClass.config["overlay"]["enabled"], callback=toggleOverlay)

                        if breatheClass.config["overlay"]["enabled"]:
                            toggleOverlay(1, True)

                        overlayOnlyWhenFocusedToggle = dpg.add_checkbox(label="Only in game(Important)", default_value=breatheClass.config["overlay"]["onlyWhenFocused"], callback=toggleOverlayOnlyWhenFocused)

                    overlayXSlider = dpg.add_slider_int(label="X Position", default_value=breatheClass.config["overlay"]["x"], min_value=0, max_value=1920, callback=setOverlayX)
                    overlayYSlider = dpg.add_slider_int(label="Y Position", default_value=breatheClass.config["overlay"]["y"], min_value=0, max_value=1080, callback=setOverlayY)

                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    otherstext = dpg.add_text("Others")

                    dpg.add_spacer(width=75)
                    
                    checkboxAlwaysOnTop = dpg.add_checkbox(label="Always On Top", callback=toggleAlwaysOnTop)

                    dpg.add_spacer(width=75)

                    checkboxAlwaysOnTop = dpg.add_checkbox(label="Discord Rich Presence", default_value=breatheClass.config["misc"]["discordRichPresence"], callback=toggleDiscordRPC)


                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)
                    
                    configtext = dpg.add_text("Config")

                    dpg.add_spacer(width=125)

                    with dpg.group(horizontal=True):
                        saveSettings = dpg.add_checkbox(label="Save config", default_value=breatheClass.config["misc"]["saveSettings"], callback=toggleSaveSettings)


                        buttonSelfDestruct = dpg.add_button(label="Backup config", callback=backupsettings)


                    dpg.add_spacer(width=75)
                    dpg.add_separator()
                    dpg.add_spacer(width=75)

                    creditsText = dpg.add_text(default_value="Credits: jven830 (Developer)")
                    githubText = dpg.add_text(default_value="https://discord.gg/Jchr62cncP")


        with dpg.font_registry():
            default_font = dpg.add_font("assets/fonts/Roboto-Medium.ttf", 15)
            large_font = dpg.add_font("assets/fonts/Roboto-Medium.ttf", 22)


        dpg.bind_font(default_font)



        dpg.bind_item_font(rightclicktext, large_font)
        dpg.bind_item_font(leftclicktext, large_font)
        dpg.bind_item_font(staptext, large_font)
        dpg.bind_item_font(wtaptext, large_font)
        dpg.bind_item_font(autobridgetext, large_font)
        dpg.bind_item_font(autohoptext, large_font)
        dpg.bind_item_font(autosprinttext, large_font)
        dpg.bind_item_font(configtext, large_font)
        dpg.bind_item_font(hudtext, large_font)
        dpg.bind_item_font(otherstext, large_font)




        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 2)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 16)
                dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 3)
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, (35, 180, 346))
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (38, 200, 346))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (35, 180, 346))
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (35, 180, 346))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabHovered, (35, 180, 346))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrabActive, (35, 180, 346))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrab, (35, 180, 346))
                dpg.add_theme_color(dpg.mvThemeCol_SliderGrabActive, (38, 200, 346))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (71, 71, 77))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (71, 71, 77))

        dpg.bind_theme(global_theme)


        dpg.create_context()
        dpg.show_viewport()
        
        guiWindows = win32gui.GetForegroundWindow()

        dpg.setup_dearpygui()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()

        selfDestruct()
    except KeyboardInterrupt:
        os._exit(0)
