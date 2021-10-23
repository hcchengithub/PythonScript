# -*- coding: utf-8 -*-
# 
# @hcchen said in Regular expression size limited 2048 chars How to make it longer?:
# https://community.notepad-plus-plus.org/topic/21973/regular-expression-size-limited-2048-chars-how-to-make-it-longer
# 
# how to get ‘Style token’ list
# Here’s a demo script for that:
# 

def highlight_indicator_range_tups_generator(indicator_number):
    # Author: Alan Kilborn https://community.notepad-plus-plus.org/user/alan-kilborn
    '''
    the following logic depends upon behavior that isn't exactly documented;
    it was noticed that calling editor.indicatorEnd() will yield the "edge"
    (either leading or trailing) of the specified indicator greater than the position
    specified by the caller
    this is definitely different than the scintilla documentation:
    "Find the start or end of a range with one value from a position within the range"
    '''
    if editor.indicatorEnd(indicator_number, 0) == 0:
        return
    indicator_end_pos = 0  # set special value to key a check the first time thru the while loop
    while True:
        if indicator_end_pos == 0 and editor.indicatorValueAt(indicator_number, 0) == 1:
            # we have an indicator starting at position 0!
            # when an indicator highlight starts at position 0, editor.indicatorEnd()
            #  gives us the END of the marking rather than the beginning;
            #  have to compensate for that:
            indicator_start_pos = 0
        else:
            indicator_start_pos = editor.indicatorEnd(indicator_number, indicator_end_pos)
        indicator_end_pos = editor.indicatorEnd(indicator_number, indicator_start_pos)
        if indicator_start_pos == indicator_end_pos: break  # no more matches
        yield (indicator_start_pos, indicator_end_pos)

#-----------------------------------------------------------------------------

def get_indicators(): 
    # 傳回 a list of currently ACTIVE indicators 也就是塗了顏色的 style tokens 

    # 可能的顏色就這些，掃描它們全部才知道有多少塗了顏色的 tokens 
    num_to_english_dict = {  
        25 : 'cyan;style1',
        24 : 'orange;style2',
        23 : 'yellow;style3',
        22 : 'purple;style4',
        21 : 'dark-green;style5',
        #31 : 'red;mark',
        }

    # 掃描全部顏色才知道有多少塗了顏色的 tokens 
    colors = {}
    for i in list(num_to_english_dict.keys()):  # i 是 color ID 全部掃一遍
        tokens = []
        for tup in highlight_indicator_range_tups_generator(i):
            (start, end) = tup
            tokens.append({'text':editor.getTextRange(start, end), 'color':num_to_english_dict[i], 'start':start, 'end':end})
        if tokens: 
            colors[i] = tokens
    return colors
    # 傳回 a dict: 
    #   {
    #       24: [{'color': 'orange;style2', 'text': 'blue screen', 'end': 351, 'start': 340}, {'color': 'orange;style2', 'text': 'BSOD', 'end': 366, 'start': 362}], 
    #       25: [{'color': 'cyan;style1', 'text': 'windows?.?10', 'end': 225, 'start': 213}, {'color': 'cyan;style1', 'text': 'win......?10', 'end': 245, 'start': 233}, {'color': 'cyan;style1', 'text': 'window.?10', 'end': 267, 'start': 257}]
    #   }

#-----------------------------------------------------------------------------
#def get_regex():
#    for color in get_indicators():
#        patterns = []
#        for items in color:
#            patterns.add(pattern)
        
#-----------------------------------------------------------------------------

ands = [] # sets that are to be AND 
for color in get_indicators().values():
    # color : 24 25 
    ors = set() # patterns to be OR 
    for instance in color:
        s = instance['text'].lower().strip()
        if s : ors.add(instance['text'].lower().strip()) # 有可能是空的
    if len(ors) : ands.append(ors) # 有可能是空的

regex = ""
for ors in ands:
    s = ""
    for p in tuple(ors):
        s += p + '|'
    regex += r"(?=.*?\s(%s)\s)" % s[:-1]
regex += ".*"

if notepad.messageBox(regex+"\n\nCopy to clipboard?", 'RegEx for Hubble2', 1)==1: # ok=1, cancel=2 
    editor.copyText(regex) # copy to clipboard

