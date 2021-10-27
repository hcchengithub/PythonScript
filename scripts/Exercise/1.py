
# --------------------------------------------------------------------------------------------------
# Editor Objec
# http://npppythonscript.sourceforge.net/docs/latest/scintilla.html 
# 09:52 2021/10/27

# SCI_ADDTEXT(int length, const char *text)  C language 的 argument format 
editor.addText("added text") # 轉成 python  

# SCI_GETTEXT(int length, char *text)  C language 的 argument format 
text = editor.getText() # 轉成 python. 讀整個 buffer 


''' comment

# --------------------------------------------------------------------------------------------------
# Notepad Object 
# http://npppythonscript.sourceforge.net/docs/latest/notepad.html
# 09:52 2021/10/27



# 最底下 status bar 的文字可以亂改，切出切回會被覆寫掉。

notepad.setStatusBar(STATUSBARSECTION.UNICODETYPE, "lalalalala ;-)")

#     STATUSBARSECTION.CURPOS
#     STATUSBARSECTION.DOCSIZE
#     STATUSBARSECTION.DOCTYPE
#     STATUSBARSECTION.EOFFORMAT
#     STATUSBARSECTION.TYPINGMODE
#     STATUSBARSECTION.UNICODETYPE

# --------------------------------------------------------------------------------------------------
# http://npppythonscript.sourceforge.net/docs/latest/notepad.html
# 09:43 2021/10/27


# 這個應該很有用。我寫筆記需要用 .py 以方便內縮之收合-展開。有了這個 function 就可以把 .txt 暫時搞成 .py 的效果了。
notepad.setLangType(LANGTYPE.PYTHON)  # 成功！真的把 active buffer 設定為 python 模式。
# notepad.setCurrentLang(LANGTYPE.PYTHON) # 這個 function 不存在

# --------------------------------------------------------------------------------------------------
# http://npppythonscript.sourceforge.net/docs/latest/notepad.html
# 16:35 2021/10/26

notepad.menuCommand(MENUCOMMAND.EDIT_DUP_LINE) # 執行 built-in commands
notepad.runMenuCommand("TextFX Tools", "T:Word Count") # 執行 plugin commands 
notepad.runMenuCommand("TextFX Tools", "T:Word Count") # 執行 plugin commands 
notepad.runMenuCommand("color picker","color picker") # 不分大小寫
notepad.runPluginCommand('Python Script', 'Hubble2 RegEx') # 執行 Python Script 
notepad.runPluginCommand('Python Script', 'GotoLineCol') # 'GotoLineCol' 藏很深也被找出來執行！


# [X] index 啥意思？ Tab 由左到右的順序
# [X] view  啥意思？ document window 由上到下由左到右的順序
Notepad.getCurrentDocIndex(view)
Gets the current active index for the given view (0 or 1)

    >>> notepad.getCurrentDocIndex(0)
    5
    >>> notepad.getCurrentDocIndex(1)
    4294967295L <----------------------- view 1 根本不存在時傳回怪值。


# --------------------------------------------------------------------------------------------------
# http://npppythonscript.sourceforge.net/docs/latest/notepad.html
# 16:35 2021/10/26

# 切到某個 buffer (tab)
bufferID = notepad.getCurrentBufferID()
print bufferID
# 切走到別的 buffer (tab) 然後在 console 執行： notepad.activateBufferID(bufferID) 切回來。


# --------------------------------------------------------------------------------------------------

# 取得 buffers 裡的 files  --> tuples of (filename, bufferID, index, view)
notepad.getFiles()
    # [('c:\\Users\\8304018\\Downloads\\1.log', 49611952, 0, 0), 
    # ('C:\\Users\\8304018\\AppData\\Roaming\\Notepad++\\plugins\\Config\\PythonScript\\scripts\\1.py', 101963704, 1, 0), 
    # ('new 2', 49665104, 2, 0), 
    # ('new 3', 49666040, 3, 0), 
    # ('new 4', 49666352, 4, 0), 
    # ('C:\\Users\\8304018\\AppData\\Local\\Packages\\Microsoft.Office.OneNote_8wekyb3d8bbwe\\LocalState\\EmbeddedFileFolder\\2\\Objects of Notepad++ PythonScript.txt', 49664792, 5, 0)]

# 切換過去到某個 file 
notepad.activateFile('new 4')
notepad.activateFile('C:\\Users\\8304018\\AppData\\Local\\Packages\\Microsoft.Office.OneNote_8wekyb3d8bbwe\\LocalState\\EmbeddedFileFolder\\2\\Objects of Notepad++ PythonScript.txt')

# --------------------------------------------------------------------------------------------------
# http://npppythonscript.sourceforge.net/docs/latest/pythonprimer.html
# 16:32 2021/10/26

console.write("Let's go")
x = 2
if x == 3:
    console.write("So x is 3 then\n")
    console.write("This line is also run if x is 3\n")
console.write("this line is run always")


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

把所有 callback 都清掉：
    notepad.clearCallbacks()

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