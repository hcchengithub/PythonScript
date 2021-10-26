# --------------------------------------------------------------------------------------------------
# http://npppythonscript.sourceforge.net/docs/latest/pythonprimer.html
# 16:32 2021/10/26

console.write("Let's go")
x = 2
if x == 3:
    console.write("So x is 3 then\n")
    console.write("This line is also run if x is 3\n")
console.write("this line is run always")


''' comment
# --------------------------------------------------------------------------------------------------
# http://npppythonscript.sourceforge.net/docs/latest/intro.html
# 16:18 2021/10/26

# 同前的改良版

import datetime

def addSaveStamp(args):
        if notepad.getBufferFilename(args["bufferID"])[-4:] == '.log':
                currentBufferID = notepad.getCurrentBufferID() # save 
                notepad.activateBufferID(args["bufferID"]) # 先切過去，因為這個 .log file 可能 not active e.g. file > save all 的時候。
                editor.appendText("File saved on %s\r\n" % datetime.date.today())
                notepad.activateBufferID(currentBufferID) # restore 

notepad.callback(addSaveStamp, [NOTIFICATION.FILEBEFORESAVE])


# --------------------------------------------------------------------------------------------------
# http://npppythonscript.sourceforge.net/docs/latest/intro.html
# 15:47 2021/10/26 弄個檔名 1.log save 之就會在欓尾加上一行 time stamp 

import datetime

# This is the callback function 
def addSaveStamp(args): 
    print "Args: %s" % args 
    if notepad.getCurrentFilename()[-4:] == '.log':
        editor.appendText("File saved on %s\r\n" % datetime.datetime.now())

notepad.callback(addSaveStamp, [NOTIFICATION.FILEBEFORESAVE])

玩了幾次之後，變成每一次 save 印出 4 行或更多行如下，
    File saved on 2021-10-26
    File saved on 2021-10-26 16:05:19.432000
    File saved on 2021-10-26 16:05:19.433000
    File saved on 2021-10-26 16:05:19.434000
這表示先前 registered 的 callback function 一直都還在 memory 裡。Restart Notepadd++
就好了，果然！


# --------------------------------------------------------------------------------------------------
16:12 2021/10/26 

本來在 Notepad++ PythonScript 的基地這裡 
    c:\Users\8304018\AppData\Roaming\Notepad++\plugins\Config\PythonScript\scripts\1.py  
咱給他弄了一份 hard copy 在
    c:\Users\8304018\Documents\GitHub\PythonScript\scripts\Exercise\1.py 
跟著整個 project 保存實驗筆記

# --------------------------------------------------------------------------------------------------
# 14:25 2021/10/26

# I am the line 0 挖喜第 0 行 
# I am the line 0 挖喜第 0 行原來的樣子。注意看上面，跑過英文變成大寫。

# grab the first line
firstLine = editor.getLine(0)

# convert it to unicode
firstLineUnicode = firstLine.decode('utf8')

# make it upper case
firstLineUnicode = firstLineUnicode.upper()

# and put the line back
editor.replaceWholeLine(0, firstLineUnicode.encode('utf8')) # 原文上又有問題，這樣改好了。

# --------------------------------------------------------------------------------------------------
# 14:13 2021/10/26

# define a unicode variable
someUnicodeString = u'This häs fünny ünicode chäractêrs in it'

# append the text to the current buffer - assuming the current buffer is set to utf8
editor.addText(someUnicodeString.encode('utf8'))

# Run when cursor is here: This häs fünny ünicode chäractêrs in it



# --------------------------------------------------------------------------------------------------
# grab the first line
firstLine = editor.getLine(0)

# convert it to unicode
firstLineUnicode = firstLine.decode('utf8')

# make it upper case
firstLineUnicode = firstLineUnicode.upper()

# and put the line back
editor.replaceWholeLine(firstLineUnicode.encode('utf8')

editor.replace("old", "new") # 沒有傳回值 (it's None if you try to accept it) 注意是 editor 之下的，所以改到 active document

# editor.pyreplace() 已經 deprecated 改用 editor.rereplace() 
# 這裡就有線索 http://npppythonscript.sourceforge.net/index.shtml
# editor.pyreplace(r"^Code: ([A-Z]{4,8})", r"The code is \1") 
editor.rereplace(r"(?i)^Code: ([A-Z]{4,8})", r"The code is \1") # Code: aaaaa 跑過變成 The code is aaaaa. (?i) 是大小寫不分
	
# notepad.save() # 存檔 the active document. 






# Code: aaaaa
Code: aaaaa


'''