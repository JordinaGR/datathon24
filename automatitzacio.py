import json, re, string, time
import numpy as np
import pyautogui as auto

f = open('example_modified.json')

data = json.load(f)
n = len(data)

for i in range(n):
    for j in range(n):
        if i != j:
            q = "only give me the final score from 0 to 1. Would these two people work well together?"
            s = str(data[i])
            t = str(data[j])

            time.sleep(0.5)
            auto.moveTo(1402, 1027)
            auto.click()
            time.sleep(0.5)
            auto.write(q + s + t)
            time.sleep(0.5)
            auto.press("enter")
            time.sleep(3)
            auto.move(1333, 865)
            auto.hotkey('ctrl', 'shift', 'left')
            auto.hotkey('ctrl', 'c')
            auto.move(943, 673)
            auto.click()
            auto.hotkey('ctrl', 'v')

            break
    break

            
