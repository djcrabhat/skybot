from util import hook

import ast
import random
import logging
import re

def say_bro(maxlen = 10):
    b = 'bro'
    for i in range(random.randrange(0,maxlen,1)):
        b += 'o'
    return b

@hook.command(autohelp=False)
def crabchat(inp, nick='', chan='', db=None):
    
    choice = random.randrange(0,1,1)
    
    if choice == 0:
        return say_bro;
        
    return say_bro;
         
     
    
@hook.regex(".")
def watch_chat(inp, nick='', chan='', db=None, match='', msg=''):
    """reads every message, respond if we feel like it"""
    logging.debug("processing msg by user "+nick+": '" + str(msg) + "'")
    
    markov_chain = create_chain(msg)
    update_user_profile(chan, nick, markov_chain, db)
    
    return

