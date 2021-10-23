
# 這個 Notepad++ PythonScript 檔要存成 utf-8 BOM 格式否則跑起來會有問題

result = editor.replace("old", "new")
print result # <--- it's None 

# editor.pyreplace() 已經 deprecated 改用 editor.rereplace() 
# 這裡就有線索 http://npppythonscript.sourceforge.net/index.shtml
# editor.pyreplace(r"^Code: ([A-Z]{4,8})", r"The code is \1") 
editor.rereplace(r"^Code: ([A-Z]{4,8})", r"The code is \1")

# notepad.runMenuCommand("TextFX Tools", "Delete Blank Lines") # 這沒有了
# notepad.runMenuCommand("TextFX Tools", "T:Word Count") # 大小寫無關

notepad.save()


