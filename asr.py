#Getting the audio
#main
import re
import num2words
import speech_recognition as sr


def recording_voice():
    '''convert voice to string'''
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Tell Calendar what you have to do:")
        audio = r.listen(source, phrase_time_limit=10)
        print("Got it!")
    
    try:
        string = r.recognize_google(audio)
        print("Calendar think you said: " + string)
    except sr.UnknownValueError:
        print("Calendar could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    return string

def find_hour(string):
    '''detect the start and end hours of the event'''
    hour = 0
    #1st case: from _:_(am,pm) to _:_(am,pm)
    pattern = re.compile(r'(From|from)\s\w+\:\w+\s(am|pm)\sto\s\w+\:\w+\s(am|pm)')
    if(pattern):
        matches = pattern.finditer(string)
        for m in matches:
            hour = m[0] # from 10:30 am to 12:30 pm
            
    #2nd case: at _:_(am.pm). Without ending time
    pattern = re.compile(r'(At|at)\s\w+\:\w+\s(am|pm)')
    if(pattern):
        matches = pattern.finditer(string)
        for m in matches:
            hour = m[0] # at 10:30 pm
            
    #3rd case: from "hour_in_characters" (am,pm) to "hour_in_characters" (am,pm)
    pattern = re.compile(r'(From|from)\s(\w+\s)+(am|pm)')
    if(pattern):
        matches = pattern.finditer(string)
        for m in matches:
            hour = m[0] # from half past ten am to twelve thirty pm
            
    #4rth case: hour in characters + hour in numbers
    pattern = re.compile(r'(From|from)\s(\w+\s)+(am|pm)\sto\s\w+\:\w+\s(am|pm)')
    if(pattern):
        matches = pattern.finditer(string)
        for m in matches:
            hour = m[0] # from quarter to ten am to 12:30 pm
            
    # 5 case hour in numbers + hour in characters¡
    pattern = re.compile(r'(From|from)\s\w+\:\w+\s(am|pm)\sto\s(\w+\s)+(am|pm)')
    if(pattern):
        matches = pattern.finditer(string)
        for m in matches:
            hour = m[0] # from 10:30 am to eleven thirty am
            
    #6 case: hour in characters and without ending hour
    pattern = re.compile(r'(At|at)\s(\w+\s)+(am|pm)')
    if(pattern):
        matches = pattern.finditer(string)
        for m in matches:
            hour = m[0] #at twenty to eleven pm
            
    if(hour == 0):
        print("Hour not detected correctly!! Try to say it again.")
    return hour

def find_date(string):
    '''find the date of the event'''
    date = 0
    pattern = re.compile(r'(on|On|at\sthe|at|At\sthe|At)\s(\d+\w+|\w+)\s(of\s)?(\w+\s)')
    if(pattern):
        matches = pattern.finditer(string)
        for m in matches:
            date = m[0] #at twenty to eleven pm
    if(date == 0):
        print("Date not found. Try to specify it again")
    return date

def find_event(string):
    ''' find the content of the event'''
    event = 0
    strings = re.split("START_DATE|START_HOUR|END_HOUR|END_DATE",string)
    for l in strings:
        if("Calendar " in l):
            event = l
        if("calendar" in l):
            event = l
    if(event == 0):
        print("Event not understanded! Repeat it again.")
    return event

def Get_Event_Elements(Event_Content,date,hour):
    ''' re-arange the text to a proper structure for event creation'''
    #Get summary
    summary = re.sub(r'(Calendar|calendar)\s(I\s)?(have)\s(\w+\s)?',"SUMMARY",Event_Content)
    summary = re.split('SUMMARY',summary)
    summary = summary[-1]
    
    #Get date
    date = re.sub(r'\s?(on\s|at\sthe\s|at\s|On\s|At\sthe\s|At\s)','DATE ',date)
    date = re.split('DATE',date)
    date.remove('')
    date = date[0]

    #Get start and End Time
    hour= re.sub(r'\s?(From\s|from\s|at\s|At\s)',"START_HOUR",hour)
    hour = re.sub(r'\s?(to\s)',"END_HOUR",hour)
    
    if('END_HOUR' in hour):
        hour = re.split('START_HOUR|END_HOUR',hour)
        hour.remove('')
        start_time = date + hour[0]
        end_time = date + hour[1]
    else:
        hour = re.split('START_HOUR',hour)
        hour.remove('')
        start_time = date + hour[0]
        end_time = None
    return summary,start_time,end_time

def normalize_hour(string):
    '''returns hours in format 00:00'''
    string = string.lower()
    pattern1 = re.compile(r'half\spast\s(\d)')
    pattern2 = re.compile(r'quarter\sto\s(\d)')
    pattern3 = re.compile(r'quarter\spast\s(\d)')
    string = re.sub(pattern1, lambda x: x.group(1)+':30', string)
    string = re.sub(pattern2, lambda x: str(int(x.group(1))-1)+':45', string)
    string = re.sub(pattern3, lambda x: x.group(1)+':15', string)
    
    return string

def split_parts(string):
    ''' detect the different parts of the event and prepares the creation of the event'''
    new_line = re.sub(r'[\/\’\'\,\.\;\(\)\_\?\¿]',"",string) # remove punctuation marks
    auxiliar_string = new_line #Auxiliar string that will have all the field marked before recognising the content of the event
    
    #Find hour
    hour_unNorm = find_hour(new_line)
    hour = normalize_hour(hour_unNorm)
    
    auxiliar_string = auxiliar_string.replace(hour_unNorm,' START_HOUR '+hour + ' END_HOUR') #Mark where the HOUR starts in the string

    #Find date
    date = find_date(auxiliar_string)
    auxiliar_string = auxiliar_string.replace(date,' START_DATE '+date+' END_DATE ')
    ### Use Auxiliar string to find the SUMMARY OF THE EVENT
    auxiliar_string = re.sub(r' +'," ",auxiliar_string) ##remove double spaces
    Event_Content = find_event(auxiliar_string)
    
    #print("Exemple auxiliar string:",auxiliar_string)
    return Event_Content,date,hour
    #return summary,start_time_string,end_time_string

