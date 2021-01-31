from random import randint

__SOCIAL_QUOTES = [
    "left your Raid Shadow Legend clan",
    "left your Minecraft server",
    "unfollowed your Goodreads",
    "downvoted your Allrecipes",
    'unfollowed on twitch',
    "unsubbed on youtube",
    "unfriended on facebook",
    "un-starred on your github project",
    "rated 1 star on google maps",
    "downvoted on reddit"
]
__BF_LIST = [
    'Tom is Rumple\'s boyfriend',
    'Tom is Jay\'s better half',
    'Tom is Rumple\'s bae'
]
__WTF_LIST = [
    'wtf boyfriend?',
    'ehw, a better half?',
    'urgh, bae?'
]


def get_tom2_message():
    randnum = randint(0, len(__BF_LIST)-1)
    social_message = __SOCIAL_QUOTES[randint(0, len(__SOCIAL_QUOTES)-1)]

    bf_message = __BF_LIST[randnum]
    wtf_message = f"{__WTF_LIST[randnum]} {social_message}"

    return bf_message, wtf_message