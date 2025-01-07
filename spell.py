from PIL import ImageGrab
from bs4 import BeautifulSoup
import pyautogui, mouse, time, keyboard
import easyocr, numpy, threading, os
from rich import print
import win32gui
import win32con

# 현재 Python 콘솔 창의 핸들을 가져옵니다
hwnd = win32gui.GetForegroundWindow()

# 맨 위에 고정하는 스타일을 설정합니다
win32gui.SetWindowPos(
    hwnd, 
    win32con.HWND_TOPMOST,  # 맨 위에 고정
    0, 0, 0, 0, 
    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE  # 위치와 크기 유지
)

# 콘솔 항상 최상단에 고정
os.system("mode con cols=100 lines=30")

with open("classcard.html", "r", encoding="UTF-8") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")

# print(soup.prettify())
class_div = soup.find_all("div", {"class": "flip-card sentence done"})
sentences = {}
for text in class_div:
    korean = text.find("div", {"class": "ex_back"}).text
    sentences[korean] = text.find("div", {"class": "ex_front"}).text
print(sentences, len(sentences))

print("Start. 1번 지점을 클릭하세요.")
while mouse.is_pressed(button="left") == False:
    pos1 = pyautogui.position()

print("1번 지점: ", pos1)
time.sleep(1)
print("2번 지점을 클릭하세요.")

while mouse.is_pressed(button="left") == False:
    pos2 = pyautogui.position()

print("2번 지점: ", pos2)

time.sleep(1) 
reader = easyocr.Reader(['ko'], gpu=True)

def checks(item, sentence):
    chk = 0
    item = str(item).replace("\n", "").replace(" ", "")
    sentence = str(sentence).replace("\n", "").replace(" ", "")
    print(sentence, item)
    for i in range(len(item)):
        if item[i] != sentence[i]:
            chk += 1
        if chk > 6:
            return False
    return True

print("ins 키를 누르면 해석이 출력됩니다.")
while True:
    # is press ins
    if keyboard.is_pressed("ins"):
        image = ImageGrab.grab(bbox=(pos1.x, pos1.y, pos2.x, pos2.y))
        npimage = numpy.array(image)
        print("byteimage: ", npimage)
        result = reader.readtext(npimage)
        for i in result:
            print(i[1])
            for sentence in sentences:
                if checks(i[1], sentence):
                    # clear console
                    os.system("cls")
                    print(f"{sentences[sentence]}")
                    break
                else:
                    pass
    elif keyboard.is_pressed("del"):
        print("Start. 1번 지점을 클릭하세요.")
        while mouse.is_pressed(button="left") == False:
            pos1 = pyautogui.position()

        print("1번 지점: ", pos1)
        time.sleep(1)
        print("2번 지점을 클릭하세요.")

        while mouse.is_pressed(button="left") == False:
            pos2 = pyautogui.position()

        print("2번 지점: ", pos2)

        time.sleep(1)
    time.sleep(0.1)  # 루프 속도를 제한