# ev3dev_edit
This is a text editor.

For the ev3dev operating system. (Based on linux, alternative LEGO EV3 Mindstorm OS)
It makes use of a tiny lcd screen and 6 buttons, that are on the mindstorm brick. 

I just noticed that ev3dev displays a terminal there briefly and decided to abuse that.
It's written in python, and it uses the curses library for text based GUI.

It features:
  - Filesystem browser (To select the file to edit)
  - Error panel messages for IO exceptions.
  - Browsing of text files (Supports files Longer and Wider than the screen)
  - On Screen Keyboard (Position your cursor [Select] and navigate the keyboard to type a char)
  - Deleting Whole lines.
  - Creating new lines.
  - Continious typing mode (When you aren't just fixing a typo on the go {WHY?})
  - Can capitalise and type Special characters.
  - Can edit exectuable files, including itself.
  - Has a menu for Saving, Closing files, and Gracefully exiting.
  - Has a resolution that is just too small to read without squinting.
  - Has some Memes, hidden inside the code.
  - It's very very buggy. (Why are you developing something using it??)
  - Crashes in the beautiful, Curses way (Hard Reboot is the only thing that can save you)

I had planned, but never got around to:
  - Support for an actual keyboard. (But i guess at that point you could just install nano there)
  - Running Ad-Hoc bash commands using the onscreen Keyboard.
  - Copy Paste funtionality.
  - A readable resolution.
  

Developing it was an adventure, I used Nano over SSH, for almost a thousand lines.


> The resolution is too small, command {setfont} could help. 
> But the GUI Panels would have to be redesinged, 
> and all places where character size is mentioned (hardcoded) would have to be hunted down and updated
