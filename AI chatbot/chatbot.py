import time
import pyperclip
import pyautogui as py

py.click(1108,869)#1108,869,527,202,527,773
time.sleep(1) #wait for one second to ensure the click is registered
py.moveTo(564,208)

py.dragTo(902,804 ,duration = 0.9, button='left')

#copying
py.hotkey("ctrl",'c')
time.sleep(1)
py.click(564,208)
#pasting test
text = pyperclip.paste()
print(text)
