'''This project is to implement a digital assistant named PyDA. PyDA will find answer for user queries using
Wolfram Alpha computational enginer and Wikipedia page articles.
PyDA returns the answer in both text and speech format. The speech format is implemented using pyttsx3 library.
Right now, the voice can be female/male. In future version, I plan to develop PyDA with voice being user choice
including a non-binary gender neutral voice.
'''

# Below are the libraries for GUI generation, accessing Wolframaplha search API , Wikipedia API,Text to speech conversion
import PySimpleGUI as gui
import wolframalpha
import mediawiki
from mediawiki import MediaWiki
import pyttsx3

# creating necessary objects of the required classes in the above libraries
wolframalpha_appId = "T7RH9E-X27PE7T483"
client = wolframalpha.Client(wolframalpha_appId)
wikipedia = MediaWiki()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# The below block of code creates a GUI window with welcome text and query text with Search and Cancel buttons
layout = [[gui.Text("What can I help you with today?"), gui.Input()],
          [gui.Button("Search"), gui.Cancel()]]
window = gui.Window("Welcome to PyDA,your digital assistant", layout)

'''The below block of code uses read() of PySimpleGUI to listen to 'Search' or 'Cancel' events. When 'Search' event 
is recorded,the user query is searched first in Wolfram Alpha. If not found, the user query is searched in Wikipedia 
article pages. If found, a brief summary is returned using the mediawiki summary(). 
If unable to retrieve any result from both the sources, PyDA gracefully exits with error message.
'''

while True:
    event, values = window.read()
    if event == 'Search':
        wa_result = client.query(values[0])
        '''If the user query is found in Wolfram Alpha(wa) , @success will be true. If the title and plaintext of result 
        is non-empty,further search is done in the Wolfram alpha computational engine. If not, query is searched 
        for in Wikipedia'''
        wa_success = wa_result['@success']
        if wa_success == 'true':
            wa_title = (wa_result['pod'][1]['subpod']['@title'])
            wa_plaintext = wa_result['pod'][1]['subpod']['plaintext']
            if wa_title != '' and wa_plaintext != None:
                gui.popup_non_blocking(next(wa_result.results).text)
                engine.say(next(wa_result.results).text)
                engine.runAndWait()
            elif wa_title == '' and wa_plaintext != None:
                gui.popup_non_blocking(wa_result['pod'][1]['subpod']['plaintext'])
                engine.say(wa_result['pod'][1]['subpod']['plaintext'])
                engine.runAndWait()
            else:
                ''' The user query is searched in Wikipedia if not found in Wolfram Alpha. 
                    If found in Wikipedia, summary is returned.
                    If not found,appropraite exception error is raised gracefully.
                '''
                Disambiguation_Error = "Sorry, the query is ambiguous. Please be specific"
                Page_Error = "Sorry! unable to help with this now"
                try:
                    wiki_summary = wikipedia.summary(values[0], sentences=2)
                    gui.popup_non_blocking(wiki_summary)
                    engine.say(wiki_summary)
                    engine.runAndWait()
                except mediawiki.exceptions.DisambiguationError:
                    gui.popup_non_blocking(Disambiguation_Error)
                    engine.say(Disambiguation_Error)
                    engine.runAndWait()
                except mediawiki.exceptions.PageError:
                    gui.popup(Page_Error)
                    engine.say(Page_Error)
                    engine.runAndWait()
    elif event in (gui.WIN_CLOSED, 'Cancel'):
        break
    else:
        break
window.close()
