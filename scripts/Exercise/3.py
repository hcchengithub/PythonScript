import re                                                                                       # needed if whole word should be searched

_g = globals()                                                                                  # get global variables
if not _g.get('AUTO_SELECT_IS_RUNNING'):                                                        # if variable not defined yet,
    AUTO_SELECT_IS_RUNNING = False                                                              # define it
                                                                                                # 
if not _g.get('COLORED_DOCS_LIST'):                                                             # -"-
    COLORED_DOCS_LIST = []                                                                      # -"-
                                                                                                # 
SELECTED_TEXT = None                                                                            # variable to hold our selection
JUMP_TO_FIRST_OCCURANCE = True                                                                  # set to false if jump should be avoided
CURRENT_DOCUMENT = None                                                                         # document which initiates the coloring
                                                                                                
# -----------------------------------------------------------------------------                 
                                                                                                
def track_document(buffer_id):                                                                  # track which documents get colored
    global COLORED_DOCS_LIST                                                                    # by using the global document list 
    if not buffer_id in COLORED_DOCS_LIST:                                                      # if current doc isn't in list yet
        COLORED_DOCS_LIST.append(buffer_id)                                                     # add it
    
# -----------------------------------------------------------------------------         

def toggle_view():                                                                              # function used when both views visible
    current_doc_index_main_view = notepad.getCurrentDocIndex(0)                                 # get current doc index of view 1 and
    current_doc_index_second_view = notepad.getCurrentDocIndex(1)                               # current doc index of view 2
                                                                                                # 
    if notepad.getCurrentView() == 0:                                                           # if main view is active
        notepad.activateIndex(1, current_doc_index_second_view)                                 # activate second view with current open doc
    else:                                                                                       # else
        notepad.activateIndex(0, current_doc_index_main_view)                                   # the other view ...
                                                                                                # 
# -----------------------------------------------------------------------------                 
                                                                                                 
def clear_indicator():                                                                          # clearing indicators by
    text_end_position = editor.getLength()                                                      # getting the document text length
    editor.setIndicatorCurrent(8)                                                               # setting the inidcator id
    editor.indicatorClearRange(0, text_end_position)                                            # and calling the clearing function
                                                                                                 
# -----------------------------------------------------------------------------                  
                                                                                                 
def colorize():                                                                                 # coloring the selected text by
                                                                                                # 
    clear_indicator()                                                                           # first clearing old marks
                                                                                                # 
    matches = []                                                                                # initializing match list
    # editor.research('\\b{0}\\b'.format(SELECTED_TEXT), lambda m: matches.append(m.span(0)))            # (use this if whold word should be searched only)
    editor.research('{0}'.format(SELECTED_TEXT), lambda m: matches.append(m.span(0)),re.IGNORECASE)      # search document for selected text and append it to list

    editor.indicSetStyle(8,INDICATORSTYLE.ROUNDBOX)                                             # set the indicator properties like roundbox
    editor.indicSetFore(8,(117,217,117))                                                        # foreground color
    editor.indicSetAlpha(8,55)                                                                  # alpha setting
    editor.indicSetOutlineAlpha(8,255)                                                          # outline setting and
    editor.indicSetUnder(8,True)                                                                # if it should be colored under text
                                                                                                 
    for match in matches:                                                                       # for each found match
        editor.setIndicatorCurrent(8)                                                           # set the indicator and
        editor.indicatorFillRange(match[0], match[1] - match[0])                                # color the match
                                                                                                
    not_original_doc = notepad.getCurrentBufferID() != CURRENT_DOCUMENT                         # is the current doc the doc which initiated the coloring?
                                                                                                
    if JUMP_TO_FIRST_OCCURANCE and len(matches) > 0 and not_original_doc:                       # if we should jump, do have matches and doc is different then
        first_visible_line = editor.getFirstVisibleLine()                                       # get the first visible line and
        line_from_position = editor.lineFromPosition(matches[0][0])                             # get the line from the match position
        delta = (line_from_position - 1 - first_visible_line)                                   # build a delta out of it
        editor.lineScroll(0, delta)                                                             # and scroll to it
                                                                                                 
# -----------------------------------------------------------------------------                  
                                                                                                                                                                                                                                                                                                 
def prepare_and_run():                                                                          # stuff which needs to be done prior to the coloring
    global CURRENT_DOCUMENT                                                                     # 
    CURRENT_DOCUMENT = notepad.getCurrentBufferID()                                             # set current doc to global var
    
    global SELECTED_TEXT                                                                        # 
    SELECTED_TEXT = editor.getSelText()                                                         # set selection to global var
                                                                                                
    colorize()                                                                                  # and color current doc
    
    both_views_visible = True if editor1 and editor2 else False                                 # are both views visible?
    if both_views_visible:                                                                      # if so
        toggle_view()                                                                           # switch to other view

# -----------------------------------------------------------------------------                  
                                                                                                 
def callback_MARGINCLICK(args):                                                                 # callback gets called when clicking bookmark margin
    prepare_and_run()                                                                           # function self explanatory, isn't it
                                                                                                
# -----------------------------------------------------------------------------                  
                                                                                                 
def callback_DOUBLECLICK(args):                                                                 # callback gets called when user double clicks
    prepare_and_run()                                                                           # deja vu
    
# -----------------------------------------------------------------------------                  
                                                                                                 
def callback_BUFFERACTIVATED(args):                                                             # callback gets called when doc gets switched
                                                                                                 
    if AUTO_SELECT_IS_RUNNING:                                                                  # when sript is in running state
        colorize()                                                                              # call colorize
        track_document(args['bufferID'])                                                        # and track which document was colored
    else:                                                                                       # otherwise it is in stopped state and
        global COLORED_DOCS_LIST                                                                # therefore we need to clear colored docs
        if args['bufferID'] in COLORED_DOCS_LIST:                                               # by checking if current id is in the list
            clear_indicator()                                                                   # if so call clearing function and
            COLORED_DOCS_LIST.remove(args['bufferID'])                                          # remove id from list
                                                                                                
        if len(COLORED_DOCS_LIST) == 0:                                                         # if list of colored docs is empty
            notepad.clearCallbacks([NOTIFICATION.BUFFERACTIVATED])                              # callback isn't needed anymore, clear it.

# ----------------------------------------------------------------------------- 

def main():                                                                                     # main function to handle start/stop behavior
    global AUTO_SELECT_IS_RUNNING                                                               # assining to global variable
    if AUTO_SELECT_IS_RUNNING:                                                                  # if script is currently running
        AUTO_SELECT_IS_RUNNING = False                                                          # this call should stop it, so set flag to False
        editor.clearCallbacks([SCINTILLANOTIFICATION.DOUBLECLICK])                              # clear callbacks
        editor.clearCallbacks([SCINTILLANOTIFICATION.MARGINCLICK])                              # -"-
        clear_indicator()                                                                       # and start clearing indicator marks
        print('Toggle off')
    else:                                                                                       # else
        AUTO_SELECT_IS_RUNNING = True                                                           # set the flag to true and
        editor.callback(callback_DOUBLECLICK, [SCINTILLANOTIFICATION.DOUBLECLICK])              # register needed callbacks
        editor.callback(callback_MARGINCLICK, [SCINTILLANOTIFICATION.MARGINCLICK])              # -"-
        notepad.callback(callback_BUFFERACTIVATED, [NOTIFICATION.BUFFERACTIVATED])              # -"-     
        print('Toggle on')
                                                                                            
# ----------------------------------------------------------------------------- 
        
main()                                                                                          # main entry