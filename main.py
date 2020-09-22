from pymouse import PyMouse
import PyHook3
import pythoncom
import threading
import time
import win32api

# time line to record [character_num, time, delay]
timeline = [
    [[2, 85, 0.1], [2, 70, 0.1], [2, 60, 0.1], [2, 50, 0.1], [2, 40, 0.1], [2, 30, 0.1], [2, 20, 0.1]],
    [[2, 85, 0.1], [2, 70, 0.1], [2, 60, 0.1], [2, 50, 0.1], [2, 40, 0.1], [2, 30, 0.1], [2, 20, 0.1]],
]

enable_collect_character_position = 0
if enable_collect_character_position:
    character_position = []
else:
    character_position = [(4757, 250), (4693, 277), (4741, 308), (4801, 353), (4672, 389)]
start_record = False


def mouse_event(event):
    global start_record
    print("Position:", event.Position)
    if start_record:
        character_position.append(event.Position)
        if len(character_position) > 4:
            win32api.PostQuitMessage()
    return True


def keyboard_event(event):
    global start_record
    print("Key:", event.Key)
    if str(event.Key) == 'F11':
        start_record = True
    if str(event.Key) == 'F12':
        win32api.PostQuitMessage()
    return True


class MouseCollectProcessor(threading.Thread):
    def __init__(self):
        super(MouseCollectProcessor, self).__init__()
        self.event = threading.Event()
        self.terminated = False

    def run(self):
        global character_position
        character_position = []
        hm = PyHook3.HookManager()
        hm.MouseAllButtonsDown = mouse_event
        hm.HookMouse()
        hm.KeyDown = keyboard_event
        hm.HookKeyboard()
        pythoncom.PumpMessages()
        hm.UnhookMouse()
        hm.UnhookKeyboard()


def main():
    global timeline, character_position
    print("press F11 to record the location of five character")
    if enable_collect_character_position:
        mouse_thread = MouseCollectProcessor()
        mouse_thread.start()
        while len(character_position) < 5:
            time.sleep(1)
    print(character_position)
    print("the location of five character has been record")
    s_num = input("your script number：")
    s_num = int(s_num)
    print(s_num)
    step = 0
    input("press enter to start")
    time_s = time.time()
    print("script start!")
    m = PyMouse()

    while 1:
        script = timeline[s_num - 1]
        if 90 - (time.time() - time_s) > script[step][1] > 90 - (time.time() - time_s) - script[step][2]:
            print(script[step])
            m.click(character_position[script[step][0]][0], character_position[script[step][0]][1])
        time.sleep(0.01)


if __name__ == '__main__':
    main()
