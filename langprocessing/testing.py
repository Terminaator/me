from estnltk.vabamorf.morf import synthesize, analyze
import time
import langprocessing.chatbot as cb
import langprocessing.sentenceProcesser as sp


bot = cb.chatbot()
print(bot.getResponse("mida tähendab MTAT"))
#s = sp.SentenceProcessor()
#print(s.getWords("mida tähendab lofy21"))
"""
cases = [
    ('n', 'nimetav'),
    ('g', 'omastav'),
    ('p', 'osastav'),
    ('ill', 'sisseütlev'),
    ('in', 'seesütlev'),
    ('el', 'seestütlev'),
    ('all', 'alaleütlev'),
    ('ad', 'alalütlev'),
    ('abl', 'alaltütlev'),
    ('tr', 'saav'),
    ('ter', 'rajav'),
    ('es', 'olev'),
    ('ab', 'ilmaütlev'),
    ('kom', 'kaasaütlev')]
"""