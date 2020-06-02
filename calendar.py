# Sentence1: Calendar I have to deliver practice 3 on 1st of July from 3:15 pm to 5 pm
# Sentence2: Calendar I have to deliver practice 3 on 2nd of July at 3:15 pm
# Sentence3: on 3rd of july, Calendar, I have to go to my parents house at half past four pm.
from asr import recording_voice, split_parts, Get_Event_Elements
from create_event import init_credentials, new_event

def main():
    # call scripts
    approved = False
    while not approved:
        string = recording_voice()
        print("Is that what you said? (Y/n)")
        if ('Y' or 'y') in input():
            approved = True
        
    eventContent, date, hour = split_parts(string)
    
    summary, start_time, end_time = Get_Event_Elements(eventContent, date, hour)

    #print("Summary:",summary,"\n")
    #print("Start time:", start_time,"\n")
    #print("End time:",end_time,"\n")

    init_credentials()
    new_event(start_time, summary, end_time)

    return

if __name__ == "__main__":
    main()
