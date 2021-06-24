import pyttsx3

class Agent:
    engine = None
    def __init__(self , rate:int=125 , volume:float=0.1 , sex:str='male'):
        #setting up volume level  between 0 and 1
        #changing index, changes voices sex male or female
        #setting up new voice rate
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id) if sex=='male' else self.engine.setProperty('voice', voices[1].id)
    def say_string(self , sentence):
        self.engine.say(sentence)
        self.engine.runAndWait()
        self.engine.stop()

