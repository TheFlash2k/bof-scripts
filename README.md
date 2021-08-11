# bof-scripts
A combination of some scripts that may assist during OSCP Buffer Overflow.

# For identify_bad_char.py:
You need to store the data dump from immunity debugger into a file, and just pass that specific file as an argument when calling this. Check the following screenshots for a better clarification as to how to use this script.


Step 1:
- You need to find the vulnerable point in your program and find the offset and then send badchars.
![img_1](imgs/1.png)

Step 2:
- Once you've sent the bad chars, select from 0x01 to 0xFF (Only select these characters otherwise the script won't work properly). Once you've selected these, right click, copy, copy to clipboard (Alternatively, you can use CTRL + C shortcut as well).
![img_2](imgs/2.png)

Step 3:
- Now, we will come to our linux machine (or windows, will work on both). We will create a new file (I will call it data.hex) and then we'll paste the dump in that file. Then we'll save it.
![img_3](imgs/3.png)

Step 4:
- Just run the script now and pass the file as an argument and we will have the script tell us about the badchars.
![img_4](imgs/4.png)

--
