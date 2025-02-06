'''
Sometimes, you just need a lil' guy to sit on windows...
'''

import tkinter as tk
import pygetwindow as gw

snor = """
iVBORw0KGgoAAAANSUhEUgAAAFQAAABUCAMAAAArteDzAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjw
v8YQUAAAAwUExURSRNpgAAADR9x0WOzww0ff/3tufPnnV1df///3VlFM/Pz/fnrqZ9TcemVWVNHAAA
AN6mWNoAAAAQdFJOU////////////////////wDgI10ZAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAC4U
lEQVRYR+3W25LqIBAFUDYxBEg0//+3p7qBhDtRM1Xnwf1gzTi4bJpLRux/EJG/cUd+6P35oW9HCORv
pXkfFUJK2VdHaFGVkNP0JSrkJBELYpqmSRZflWaEEnGygLwBBRuEAI/HQ0pC6feu2kepgZMsIr5C4R
BXbor21CHqusi5DY3MaZrneQ7mFyiknOf5JJl1aEcdouzE5jx/iT6cSeppzuomNIkaqV2UJr8AWBzG
Py53oJUor/6HqJu+bwKjrH6FLtrwa1BvQWfjk6JNs4/u8EwSMhltqgO0tlIBbdfaQYFwSkvUbdRWsU
1U+Ls0J6NCm8U2UE/mYGHW1SrKj/YqmZqth1UNpSohci4kQfmZmH++gvLM22Z0S7n5VNQC5WZ2zUId
olfMU22UmqHOrB6kJH01Rd1GGhaaNaCPui++YKZqsa8S9HKhEerSRt8wczRVE1QPt+iR9Ky2UcGo+A
xN1AiFBv1RXEGzW+Wv0FiNUWjoa2h+/7VRVqnYnCjCJqE0+kDPx0B2ohgdqc7kSiMVuoHu+wU0Mqm+
Az3nX0W7qjePlnoW1rYqXXgIoHIqJJDRMtFTF7DN6S+WthW0hqqyB5ksPTSTrekvVmuAXoQq2FPMjy
hvm8aW2ncDa40x1hohiD3cGKzt0PS/ihNdAKNgzLquxijufkr5LG5hTLTuMUiJUK2xutBn/UdizhN8
mg216AJqtfVorOZZtNYwRmsbBhRm3NPF0tS3beuisNpiJdTQCg1Rmv32fD6fr44KwKyrMoCifUI7MP
Y4yYXizefz1UHPDrkelGaOwqEbqVU0mE6lvg7QHR7drqCrUqgXmqOK1I3Rnknf7Ds0RFmFMxX8TeES
o6+oQzUzv6VAI8Hjk5MX3IBufjZVM0d3EFsfTS6hLxI9mo9xyVFXVGPwDqyrOtHWsBLtByqg7UI/QZ
3aMd9Gnfripcz/dORttLeUIe+j/aXkfIIO80Pvzw+9P/8AWbIlto3XIW0AAAAASUVORK5CYII=
"""

aWindow = gw.Win32Window
'''it's a window! (actually a pygetwindow.Win32Window)'''


class point:
  '''A point, with x and y coordinates'''
  def __init__(self, x: int | float = 0, y: int | float = 0):
    self._x = x
    self._y = y
  
  @property
  def x(self) -> int | float:
    return self._x
  
  @property
  def y(self) -> int | float:
    return self._y
  
  def __str__(self) -> str:
    return f"({self.x}, {self.y})"
  
  def __repr__(self) -> str:
    return self.__str__()


class border(tk.Tk):
  colour_transparent = "#FF00FF"
  
  def __init__(self, pos:point, size:tuple[int,int]=(84,84)):
    super().__init__()
    self.title = "Border"
    self._pos = pos
    self._pixel_size = size
    self.resize()
    self.protocol("WM_DELETE_WINDOW", self.destroy)
    self.overrideredirect(True)  # Remove window decorations
    self.attributes(
      '-alpha', .8,  # Set transparency
      '-topmost', True,  # Keep it on top
      '-transparentcolor', self.colour_transparent, # Set transparent colour
    )
    self.bind("<ButtonPress>", self.on_click)
    self.target:str = "Calculator" # set some window to be the initial target
    self.update_position()
  
  @property
  def pos(self) -> point:
    return self._pos
  
  @property
  def pixel_size(self) -> tuple[int,int]:
    return self._pixel_size
  
  def resize(self):
    self.geometry(
      "{}x{}+{}+{}".format(
        self.pixel_size[0],
        self.pixel_size[1],
        self.pos.x,
        self.pos.y,
      )
    )
  
  def on_click(self, event):
    # we take in the event and do nothing with it
    self.destroy()
  
  def update_position(self):
    try:
      # check for new target window
      new_target = gw.getActiveWindow().title
      if self.target != new_target and new_target != "tk":
        print(new_target)
        self.target = new_target
      
      # get current target window's position, and update ours relative to it
      window: aWindow = gw.getWindowsWithTitle(self.target)[0]
      self._pos = point(
        (window.topleft.x + window.topright.x - self.pixel_size[0]) // 2,
        window.topleft.y - self.pixel_size[1] + 16,
      )
      self.resize()
      
      # queue this function up again in a specified number of milliseconds
      self.after(10, self.update_position)
      return
    # Some error catching, uncomment the prints for some extra info!
    except IndexError:
      #print(f"Window with title '{target}' not found.")
      pass
    except Exception as e:
      #print(f"{e}")
      pass
    # if something went wrong, wait a bit longer before trying again
    self.after(200, self.update_position)


if __name__ == "__main__":
  b = border(point(50,50))
  img = tk.PhotoImage(data=snor)
  label = tk.Label(b, image=img, bg=b.colour_transparent)
  label.grid(row=0, column=0, sticky="nsew")
  b.mainloop()