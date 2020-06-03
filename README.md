# AST_FinalProject_Baldi_Marti_Bausa_Cesc_Verges_Eduard
Final project of Advances in Speech Technologies course in UPF (2019-2020)
### Description
Executing the main file calendar_main.py, you will be able to create a google calendar event with your voice.
For example, if you say *"William, I have to deliver the practice 3 on 15th of June at 4:30 pm"*, an event will be created at the *15th of June* in the corresponding hours and with the tittle *"Deliver the practice 3"*.
 
Notice that all your recordings must have the following structure for which the app will be able to recognize the different parts of the event:
- **William I have (SUMMARY) on/on the/at the (DATE) from/at (INIT HOUR) [ to (END HOUR) ]optional**

As observed the end hour is optional. Here some example of sentences that the app can recognize:
> Sentence1: William I have to deliver practice 3 on 1st of July from 3:15 pm to 5 pm
> Sentence2: William I have to deliver practice 3 on 2nd of July at 3:15 pm
> Sentence3: on 3rd of july, William, I have to go to my parents house at half past four pm.
### Dependencies:
For being able to run hour code you must have intsalled:
1. pip install google-api-python-client 
2. pip install google-auth-oauthlib (Linux/Mac: sudo pip install google-auth-oauthlib)
3. pip install datefinder 
4. pip install SpeechRecognition
5. pip install pipwin
6. pipwin install PyAudio

### Links used
- Sample code for [recording_voice](https://pythonprogramminglanguage.com/speech-recognition/) function.
- Sample code for [creating event with google calendar API](https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322).
- [Google Calendar API](https://developers.google.com/calendar). 

