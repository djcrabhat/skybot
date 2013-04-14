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


def get_chain_from_db(nick,chan,db):
    chains_for_user = db.execute("select w1, w2, chain  from chat_chainPairs where  "
            " chan=? and lower(nick)=lower(?) ",
            (chan, nick)).fetchall()
    
    markov_chain = { }
    for x in chains_for_user:
        w1,w2,chain = x
        list_chain = ast.literal_eval(chain)
        for z in list_chain:
            markov_chain.setdefault((w1,w1), []).append(z)
            
            
    return markov_chain
        
def create_chain(msg):
    markov_chain = {}
    w1 = "\n"
    w2 = "\n"
    
    splitMsg = msg.split()
    if splitMsg.count > 2:
        for word in splitMsg:
            if(w1 != "\n" and w2 != "\n"):
                markov_chain.setdefault((w1,w2), [] ).append(word)
                
                
            w1, w2 = w2, word
            
        return markov_chain
    else:
        return None
    
def update_user_profile(chan, nick, chain, db):
    logging.debug("adding chain for " + nick)

    db.execute("create table if not exists chat_chainPairs"
        "(chan, nick, w1, w2, chain"
        ",primary key (chan, nick, w1, w2)"
        ")")
    db.commit()
    
    
    for x in chain.keys():
        try:
            z = get_by_word_pair(db, chan,nick,x[0],x[1])
            if z == None:  
                #insert
                db.execute('''insert or fail into chat_chainPairs (chan, nick, w1,
                            w2, chain) values(?,?,?,?,?)''',
                            (chan, nick, x[0], x[1], str(chain[x]) ))
                logging.debug("inserted new pair " + x[0] + x[1] )
            else:
                #update
                rowid,w1,w2,oldChain = z
                logging.debug("update rowID " + str(rowid))
            
                list_chain = ast.literal_eval(oldChain)
                logging.debug("old chain: " + str(list_chain))
            
                for newChainMember in x:
                    if not newChainMember in list_chain:
                        list_chain.append(newChainMember)
            
                logging.debug("new chain: " + str(list_chain))
            
                #save to db
                db.execute('''update chat_chainPairs set chain = ? where rowid = ?''', (str(list_chain), rowid) )
                db.commit()
                logging.debug("updated db")
            
        except db.IntegrityError:
            #pair already exists
            print 'ERROR UPDATING!'
            pass
    
    
    
    db.commit()
    
def get_by_word_pair(db, chan,nick,w1,w2):
    logging.debug("looking up " + chan + " " + nick + " " + w1 +", " + w2)
    
    chain_for_pair = db.execute("select rowid, w1, w2, chain  from chat_chainPairs where  "
            " chan=? and lower(nick)=lower(?) and w1=? and w2=?",
            (chan,nick,w1,w2)).fetchone()
    
    return chain_for_pair

def construct_sentence(markov_chain, word_count=30):
    generated_sentence = ""
    
    if len(markov_chain) < 2:
        return
    
    word_tuple = random.choice(markov_chain.keys())
    w1 = word_tuple[0]
    w2 = word_tuple[1]
    
    for i in xrange(word_count):
        if markov_chain.has_key( (w1, w2) ):
            newword = random.choice(markov_chain[(w1, w2)])
            generated_sentence = generated_sentence + " " + str(newword)
            
            w1 = w2
            w2 = newword
        else:
            #miss, start somwhere fresh
            word_tuple = random.choice(markov_chain.keys())
            w1 = word_tuple[0]
            w2 = word_tuple[1]
            
            pass
        
        
    
    return generated_sentence

