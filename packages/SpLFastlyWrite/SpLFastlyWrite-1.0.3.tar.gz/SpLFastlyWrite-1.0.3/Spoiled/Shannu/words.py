import random
from english_words import get_english_words_set

WORDS_LIST = [] 

for x in get_english_words_set(["web2"]):
    if len(x) == 10:
        WORDS_LIST.append(x.lower())
        
five = []
        
def five_letter_words():
    global five
    if not five:
        for x in get_english_words_set(["web2"]):
            if len(x) == 5:
                five.append(x.lower())
    return five

def Word():
  x = random.choice(WORDS_LIST)
  return x
