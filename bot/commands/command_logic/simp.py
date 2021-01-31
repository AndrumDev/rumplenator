from random import randint

 # Can be anywhere, or can set up a dedicated file import instead. Currently as a list.

__SIMP_QUOTES = [
    "do you have onlyfans?", 
    "do you talk?", 
    "does she speak", 
    "notice me senpai.", 
    "u r beetiful asian quenn.", 
    "can i wife u?",
    "oh you have a bf? im out.", 
    "hiiiiooi can u be my girlfriend", 
    "did it hurt when you fell from the vending machine cause you thicka then a snicka", 
    "Burp for bits?"
]

async def get_simp_quote():
    return __SIMP_QUOTES[randint(0, len(__SIMP_QUOTES)-1)]
