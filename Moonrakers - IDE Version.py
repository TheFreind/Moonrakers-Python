#############  Importing functions from other files. 
## IMPORTS ##  
#############

import random, time

#################  All unresolved bugs are documented here; remove when solved.
## BUG HUNTING ##  
#################

# CODE READJUSTMENT - See if you can "import" functions or information like the cards.
# CODE READJUSTMENT - Remake "discard and draw" effects. Use Myla Dystra as an example of a GOOD code. (CARDS[12])

###############  Functions automate sections of code and important events.
## FUNCTIONS ##   
###############


# The player calls from which deck he will draw, how many cards, and to where those cards would go.
# Creates a copy of the card from origin deck and adds it to destination deck. Then, deletes original card.
# In the event that the draw deck is empty, reshuffle the discard deck to form a new draw deck.
def drawCards(origin, number_drawn, destination):
    numb_drawn = 0
    while numb_drawn < number_drawn:
        if origin == draw_deck and ( len(draw_deck) == 0 and len(discard) == 0 ):
            print("You can't draw more cards! You're trying to draw more cards than you have in total.")
            break
        
        elif origin == draw_deck and len(draw_deck) == 0:
            shuffle(discard, draw_deck)
            print("\n **** Discards have been reshuffled! **** \n")
        
        elif origin == contracts_deck and len(contracts_deck) == 0:
            shuffle(contracts_discard, contracts_deck)
            print("\n **** Contracts have been reshuffled! **** \n")

        elif origin == mercenary_deck and len(mercenary_deck) == 0:
            shuffle(mercenary_discard, mercenary_deck)
            print("\n **** Mercenary's cards have been reshuffled! **** \n")
            
        else:
            destination.append( origin[0] )
            del origin[0]
            numb_drawn += 1

# Shuffle cards in a random order.
# Select deck to shuffle, create copies and delete originals, then send them to the destination.
def shuffle(shufflee, receiver):
    random.shuffle(shufflee)
    for k in range( len(shufflee) ):
        receiver.append( shufflee[0])
        del shufflee[0]

# At the end of a contract, discard all cards that were played or in hand.
# 'Discarded' cards are copied over to your discard deck. Delete original versions to prevent duplication.
def discardf():
    for x in range( len(hand) ):
        discard.append( hand[0] )
        del hand[0]
    for y in range( len(cards_in_play) ):
        discard.append( cards_in_play[0] )
        del cards_in_play[0]

# Modified version of discardf(). Exact same process for the mercenary's hand instead of the player.
# However, crewmembers are instead discarded to the Armory's crew deck. Draw a new crewmember for the mercenary until 3/3.
def discardM():  
    for z in range( len(mercenary_hand) ):
        if ( mercenary_hand[0][-1] ) > 6: # All crewmembers have ID's greater than 6.
            crew_deck.append( mercenary_hand[0] )
            del mercenary_hand[0]
            drawCards(crew_deck, 1, mercenary_discard)
        else:
            mercenary_discard.append( mercenary_hand[0] )
            del mercenary_hand[0]
            
    for v in range( len(cards_in_play_MERC) ):  
        if ( cards_in_play_MERC[0][-1] ) > 6:
            crew_deck.append( cards_in_play_MERC[0] )
            del cards_in_play_MERC[0]
            drawCards(crew_deck, 1, mercenary_discard)
        else:
            mercenary_discard.append( cards_in_play_MERC[0] )
            del cards_in_play_MERC[0]
            


        
        
# This function lets the player zoom in on a card and read all of its details when prompted.
def inspect(deck):
    inspecting = True           
    while inspecting == True:
        printm(deck)        # Special print function for lists; look below for structure.
        entry = input("\nENTER: CARD NUMBER TO INSPECT:\n")
        if entry.isdigit() and int(entry) <= len(deck):
            print( deck[ (int(entry) - 1) ][0] + ":" , deck[ (int(entry) - 1) ][1] ) # Name : Detailed description
            if deck == objectives:
                if int(entry) <= len(objectives):
                    objectives_code( objectives[ (int(entry) - 1) ] , (int(entry) - 1) ) # Auto-score objectives when previewing them.
                                   
            cycle = input("\nWould you like to inspect again, sir? \nENTER: [Y], [N] \n")
            if cycle == "Y" or cycle == "y":
                pass
            elif cycle == "N" or cycle == "n":
                inspecting = False
                break
            else:
                print("INPUT ERROR DETECTED. GOING BACK")
        else:
            print("INPUT ERROR DETECTED. RETRY.")

# Used for purchasing crew members or ship parts from the Armory in PHASE 3.
# - (Argument 'card') Identity and specifics of card. Provided to function by code when selecting a card 
# - (Argument 'category') The code will tell the function if its about a ship part or crewmember using a simple string
# - (Argument 'index') Player chooses a card to buy from stock 
def purchase(card, category, index):
    global COINS, tinkerObjTurn
    
    if card[2] > COINS:
        print("You do not have enough credits to purchase this!")

    elif "ship_parts" in category:          
        for x in card[-3]:              # This for loop will add every additional action card from installing the ship part.
            if x == "":
                pass
            else:
                discard.append( x )
        
        COINS -= card[2]
        if len(ship_parts) == 4: # Maximum ship parts allowed is 4. Replace a part to proceed.
            print("WARNING: MAXIMUM CAPACITY OF 4 SHIP PARTS REACHED.")
            printm(ship_parts)
            validation = True
            while validation == True:
                replace = input("ENTER: NUMBER OF PART YOU WISH TO REPLACE:\n") 
                if int(replace) >= 1 and int(replace) <= 4:
                    ship_parts.insert( (int(replace) - 1) , card )
                    del ship_parts_selection[index]
                    drawCards(ship_parts_deck, 1, ship_parts_selection)
                    print("Modification successful." , card[0] , "has replaced " + ship_parts[int(replace)][0] + ".\n\n")
                    del ship_parts[ int(replace) ]
                    validation = False
                    tinkerObjTurn = TURN # Special code for the Tinker Objective to activate
                else:
                    print("NUMBER INPUT INVALID. RETRY.")
            
        else:           # Installing the ship part to the ship.
            ship_parts.append( card )   
            del ship_parts_selection[index]
            drawCards(ship_parts_deck, 1, ship_parts_selection)
            print("Transaction complete." , card[0] , "is now installed on your ship. \n\n")
        
        
    elif "crew" in category:
        COINS -= card[2]
        discard.append( card )   
        del crew_selection[index]   
        drawCards(crew_deck, 1, crew_selection)
        print("Transaction complete." , card[0] , "is now in your discards. \n\n")
        
# Short for "printModified", this function artistically prints the first index of every item in a deck (which is always the "name")
# - Objectives are important. Print out the description alongside the name, and put it on a new line.
# - It's easy to forget your ship parts. Print out their abilities, and their brand as a reminder for certain objectives.
def printm(deck):           
    n = 1
    if len(deck) == 0:
        print ( "None", end=' ' )
    elif deck == objectives or deck == objectives_selection:
        for card in deck:
            print ( "#" + str(n) + ":" , card[0] , "-" , card[1])
            n += 1
    elif deck == ship_parts: # Identical to objective printm, except this also includes the part's brand.
        for card in deck:
            print ( "#" + str(n) + ":" , card[0] , "-[" + card[-2][0] + "]-" , card[1])
            n += 1
    elif deck == contracts_selection:
        for card in deck:
            if n == 5: 
                print("") # Create a new row every 4 cards
            print ( "#" + str(n) + ":" , card[0] , end=' | ' )
            n += 1
    elif deck == hand or draw_deck:
        for card in deck:
            if n == 7 or n == 14: 
                print("") # Create a new row every 6 cards
            print ( "#" + str(n) + ":" , card[0] , end=' | ' )
            n += 1            
    else:
        for card in deck:
            print ( "#" + str(n) + ":" , card[0] , end=' | ' )
            n += 1
    print("")
    
# When inspecting or attempting contracts, print out all details from the mission, such as rewards and requirements.
# The 'key' argument should be LIST[KEY] 
def print_contract(key):
    print( "CONTRACT NAME: {" , key[0] , "}" )
    print( "CONTRACT TYPE: {" , key[-1] , "}" )
    if key[1][0] != 0:
        print( "PRESTIGE:\t  " + str(key[1][0]) )
    if key[1][1] != 0:
        print( "CREDITS:\t  " + str(key[1][1]) )
    if key[1][2] != 0:
        print( "BONUS CARDS:\t  " + str(key[1][2]) )
    print ( "HAZARD DICE:\t  " + str(key[2]) )
    print ( "REQUIREMENTS: " )
    if key[3][0] != 0:
        print( str(key[3][0]) + " Reactors" )
    if key[3][1] != 0:
        print( str(key[3][1]) + " Thrusters" )
    if key[3][2] != 0:
        print( str(key[3][2]) + " Damage" )
    if key[3][3] != 0:
        print( str(key[3][3]) + " Shields" )
    if key[3][4] != 0:
        print( str(key[3][4]) + " Crewmembers" )
    print ("")


# Function checks to see if requirements are met after each action.
# It'll only print the fulfilled requirements IF the mission has those at all. (why we use 'and' as well as 'or')
def printRequirements():
    if R >= mission[0][3][0] and mission[0][3][0] > 0 or mission[0][3][0] < 0:
        print(" === Reactor requirements fulfilled! ===")
    if T >= mission[0][3][1] and mission[0][3][1] > 0 or mission[0][3][1] < 0:
        print(" === Thruster requirements fulfilled! ===")
    if D >= mission[0][3][2] and  mission[0][3][2] > 0 or mission[0][3][2] < 0:
        print(" === Damage requirements fulfilled! ===")
    if S >= mission[0][3][3] and mission[0][3][3] > 0 or mission[0][3][3] < 0:
        print(" === Shield requirements fulfilled! ===")
    if C >= mission[0][3][4] and mission[0][3][4] > 0 or mission[0][3][4] < 0:
        print(" === Crew requirements fulfilled! ===")
    print("\n") 

# This function limits the amount of times you may use a ship part per contract. It takes the exact name of a ship part as an argument in string form.
# How it works: It uses an outside list called "shipLimitedUses". This tracks the number of times each ship part was used. Defaults to 0.
# Then, we define the global variable 'partIndex'. The function will find the requested ship part's index (or "place") in the ship's inventory.
# Using shipLimitedUses[ partIndex ], we can set a limit to the number of uses a part may be used per contract. Increment it once after every use.
def limitedUses(part_name):
    global partIndex
    counter = 0
    for part in ship_parts:
        if part_name in part[0]:
            partIndex = counter
            break
        else:
            counter += 1
    # Don't forget to increment shipLimitedUses[ partIndex ] += 1
        # after a successful usage in the ship part code.

# Used only during setup. Draw 3 objectives, choose one to discard and keep the rest.
def setup_objectives():
    drawCards(objectives_deck, 3, objectives_selection)
    print("\nGAME ELEMENTS SHUFFLED AND IN PLAY. DRAW 3 OBJECTIVES AND KEEP 2 TO COMPLETE SETUP.")
    printm(objectives_selection)
    obj = input("\nENTER [1], OR [2], OR [3] TO DISCARD. THE OTHER OBJECTIVES WILL BE KEPT. \n")
    while (obj.isdigit() == False) or int(obj) < 1 or int(obj) > len(objectives_selection):
        obj = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
        
    if obj == "1":
        objectives.append( objectives_selection[1] )
        objectives.append( objectives_selection[2] )
        objectives_deck.insert( len(objectives_deck), objectives_selection[0] )

    elif obj == "2":
        objectives.append( objectives_selection[0] )
        objectives.append( objectives_selection[2] )
        objectives_deck.insert( len(objectives_deck), objectives_selection[1] )

    elif obj == "3":
        objectives.append( objectives_selection[0] )
        objectives.append( objectives_selection[1] )
        objectives_deck.insert( len(objectives_deck), objectives_selection[2] )

    del( objectives_selection[:] ) # Empty the whole list


###################  All of the information in the game is given here for the code to refer and call upon.
## GAME ELEMENTS ##
###################

# Dictionary containing every possible basic action and crewmember card in the game 
# Format - KEY # : [ Name , Description , Cost, "Title" , "Class" , KEY number for code ]
# The code when played MUST reference the last number in a card (seen in code as Card[-1]). This is the identity of the card.
CARDS = {
    0 : [ "Miss"     , "System Error."    , 0 , "", "", 0 ],
    1 : [ "Damage 1" , "Deal 1 Damage."   , 0 , "", "", 1 ],
    2 : [ "Damage 2" , "Deal 2 Damage."   , 0 , "", "", 2 ],
    3 : [ "Damage 3" , "Deal 3 Damage."   , 0 , "", "", 3 ],
    4 : [ "Reactors" , "Gain +2 Actions." , 0 , "", "", 4 ],
    5 : [ "Thrusters", "Draw +2 Cards."   , 0 , "", "", 5 ],
    6 : [ "Shields"  , "Block 1 Hazard."  , 0 , "", "", 6 ],
    
    7 : [ "Crusse Parke"    , "Play as Damage 5. Trash the top card from your draw pile."                   , 2 , "Hot Shot"        , "MERC"    , 7 ],
    8 : [ "Nella van Daval" , "+3 Cards. Requirement for Thruster is 1 less."                               , 3 , "Engine Mechanic" , "PILOT"   , 8 ],
    9 : [ "Bill Bendo"      , "Negate 1 Hazard. Requirements for Shield is 1 less. +1 Card or +1 Action."   , 2 , "Supply Sergeant" , "PALADIN" , 9 ],
    10: [ "Dana Powalki"    , "Play as a 1 Damage 3, +1 Action."                                            , 4 , "Bounty Hunter"   , "MERC"    , 10 ],
    11: [ "Meg Gallak"      , "Trash a card from your hand. Subtract 2 from any 1 requirement. +1 Action."  , 4 , "Mine Engineer"   , "AGENT"   , 11 ],
    12: [ "Myla Dystra"     , "Discard any number of Cards and draw an equal number. +1 Action."            , 3 , "Fearless Pilot"  , "PILOT"   , 12 ],
    13: [ "AT-8K"           , "Negate 1 Hazard Die. Play as Damage equal to Hazard negated."                , 3 , "Tactical AI"     , "PALADIN" , 13 ],
    14: [ "Ada Massa"       , "+3 Actions. Requirement for Reactor is 1 less."                              , 3 , "Reactor Expert"  , "TECH"    , 14 ],
    15: [ "Sella Pelleon"   , "Subtract 1 from ANY requirement. +1 Card and +1 Action."                     , 4 , "Ensign"          , "AGENT"   , 15 ],
    16: [ "Sol Forst"       , "+2 Cards OR pay 1 Credit for +4 Cards."                                      , 2 , "Navigator"       , "PILOT"   , 16 ],
    17: [ "Rez Vondu"       , "+2 Actions OR pay 1 Credit for +4 Actions."                                  , 2 , "Reactor Expert"  , "TECH"    , 17 ],
    18: [ "Metaxis"         , "Use the special ability of any one face up Crew in the Armory."              , 3 , "Ensign"          , "AGENT"   , 18 ],
    19: [ "Kary Powalk"     , "All players Damage cards are +1 Damage. +1 Action."                          , 3 , "Fleet Admiral"   , "MERC"    , 19 ],
    20: [ "Zardon the Enforcer" , "Play all Damage in your hand without using an Action. +1 Action."        , 3 , "Bounty Hunter"   , "MERC"    , 20 ],
    21: [ "Strada Rysh"     , "+1 Prestige, roll an additional Hazard Die. +1 Action."                      , 4 , "Sergeant"        , "PALADIN" , 21 ],
    22: [ "Baz"             , "Play as 1 Damage. If you complete the Contract, block 2 Hazards."            , 3 , "Munitions Expert", "MERC"    , 22 ],
    23: [ "Lila al Bindar"  ,"Trash a card from your hand and add a Reactor to your discard pile. +1 Action.",2 , "2nd Lieutenant"  , "TECH"    , 23 ],
    24: [ "Lee van Cribb"   , "Look at the next 3 Cards in your draw pile, play 1 without an action, discard others. +1 Action.", 2 , "Scout" , "TECH" , 24 ],
    25: [ "Tantin al Vale"  , "Play as a Damage 2 or a Shield."                                             , 2 , "Deck Officer"    , "MERC"    , 25 ],
    26: [ "B3-AR"           , "Retrieve a Crew Member from your played or discarded Cards. +1 Action."      , 2 , "Communications AI" , "PILOT" , 26 ],
    27: [ "[REDACTED]"      , "Play as a Shield. Re-roll any number of your Hazard Dice."                   , 3 , "Strike Leader"   , "PALADIN" , 27 ],
    28: [ "Kal Damar"       , "+2 Cards. Optional: Trash 1 Card from your hand."                            , 2 , "Scavenger"       , "PILOT"   , 28 ],
    29: [ "Karma Kesa"      , "+3 Actions, or draw an Objective Card."                                      , 3 , "Reactor Expert"  , "TECH"    , 29 ],
    30: [ "Ryle al Wren"    , "Negate 2 Hazard or reduce Shield requirement by 2."                          , 3 , "Sergeant"        , "PALADIN" , 30 ],
    31: [ "Moro Mada"       , "Subtract 2 from any 1 requirement."                                          , 4 , "Saboteur"        , "AGENT"   , 31 ],
    32: [ "Col Dervok"      , "Trash a card from your hand. +3 Credits, +1 Action."                         , 4 , "Engine Mechanic" , "PILOT"   , 32 ],
    33: [ "Lok Tekt"        , "Discard ANY number of Shields from your hand. Then gain +2 Cards for each Shield discarded." , 3, "Priest", "PALADIN" , 33],
    34: [ "Jes Ofra"        , "Add a Reactor, Thruster, Shield, or Damage 1 to your hand from the supply."  , 4 , "Diplomat"        , "AGENT"   , 34 ],
    35: [ "Zek Zarag"       , "Search your draw pile for any Card and play it without an action. Shuffle your draw pile.", 2,"Navigator","PILOT", 35 ],
    36: [ "Ryan Rogal"      , "+2 Cards. If you draw a Damage, play one without an Action as a Damage 5."   , 3 , "Munitions Expert", "MERC"    , 36 ]
}   


# Each action card has an effect. This function will execute an effect when the matching key of the card is played.
# Function interacts with outside variables, so they are set to GLOBAL. Requirements of a contract are all set to 0, and each card played will increment it.
# (Argument 'merc') If you play a card from the Mercenary, you do not benefit from the effects UNLESS its a crew card.
# 'Derivative' is a boolean argument referenced rarely - only if a card duplicates another card does it activate.
#     - It ensures that certain effects of a card are not duplicated, per game rules.
def card_code(card, merc, derivative):
    global ACTIONS, COINS, PRESTIGE, HAZARDS, diceHAZARDS, HAZARDS_BLOCKED, R, T, D, S, C, KARY_POWALK, BAZ
    identity = card[-1]
    if identity > 6 and derivative == False:    # If playing a crew card, always increment Crew requirements by 1 (Unless its a forged copy)
        C += 1

            ###### BASIC CARDS #######
    if identity == 0:       # Miss
        pass
    
    elif identity == 1:     # Damage 1
        D += 1
        if KARY_POWALK == True: # If Kary Powalk is in play, increase all damage cards by +1 damage
            D += 1
    elif identity == 2:     # Damage 2
        D += 2
        if KARY_POWALK == True:
            D += 1
    elif identity == 3:     # Damage 3
        D += 3
        if KARY_POWALK == True:
            D += 1
                
    elif identity == 4:     # Reactor
        if merc == False:
            ACTIONS += 2
        R += 1
        
    elif identity == 5:     # Thruster
        if merc == False:
            drawCards(draw_deck, 2, hand)
        T += 1
        
    elif identity == 6:     # Shields
        if merc == False:
            HAZARDS -= 1
            HAZARDS_BLOCKED += 1 # Flare Shard part will earn you money for each shield played.
            ship_parts_code("Siphon", 0, 0) # Siphon gives actions.
        if derivative == False:
            S += 1
            

            ##### CREWMEMBERS #####
    elif identity == 7:     # Crusse Parke
        if len(draw_deck) > 0:
            del draw_deck[0]
            D += 5
            print("Crusse Park: 'Won't even know what hit 'em!' ")
        else:
            print("Crusse Park: 'We're going DOWN!!' ")
        
    elif identity == 8:     # Nella van Daval
        drawCards(draw_deck, 3, hand)
        if mission[0][3][1] > 0: # Thruster requirements is 1 less
            mission[0][3][1] -= 1
        print("Nella van Daval: 'Fuel consumption calibrated... engines nominal.' ")
        
    elif identity == 9:     # Bill Bendo
        HAZARDS -= 1
        if mission[0][3][3] > 0: # Shields requirements is 1 less
            mission[0][3][3] -= 1
        print("Bill Bendo: 'Ship fuel? Bombs? Ammunition? It's yours, partner.' ")
        bill_bendo = input("ENTER: +1 [C]ard, OR  +1 [A]ction: \n")
        while ( bill_bendo != "Card" and bill_bendo != "C" and bill_bendo != "c" and
                bill_bendo != "Action" and bill_bendo != "A" and bill_bendo != "a"):
            print("Bill Bendo: 'Ok, I admit I exaggerated my inventory.' ")
            bill_bendo = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
        if ("Card" in bill_bendo) or ("C" in bill_bendo) or ("c" in bill_bendo):
            drawCards(draw_deck, 1, hand)
        elif ("Action" in bill_bendo) or ("A" in bill_bendo) or ("a" in bill_bendo):
            ACTIONS += 1
        print("Bill Bendo: 'Ain't no problem out there that I ain't prepared for.' ")
        
    elif identity == 10:    #Dana Powalki
        ACTIONS += 1
        D += 3
        print("Dana Powalki: 'No one walks away!' ")
        
    elif identity == 11:    #Meg Gallak
        printm(hand)
        print("Trash a card from your hand to subtract 2 from any 1 requirement.")
        meg_gallak = input("ENTER: NUMBER OF CARD TO TRASH:\n")
        while (meg_gallak.isdigit() == False) or int(meg_gallak) < 1 or int(meg_gallak) > len(hand):
            meg_gallak = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
            
        missedOpportunity = True # If you chose a requirement not present in mission, re-enter the reduction.
        while missedOpportunity == True:
            meg_gallak_ability = input("ENTER: 'RCTR' OR 'THRU' OR 'DMG' OR 'SHLD' OR 'CREW':\n")
            while ( meg_gallak_ability != "RCTR" and meg_gallak_ability != "THRU" and 
                    meg_gallak_ability != "DMG"  and meg_gallak_ability != "SHLD" and meg_gallak_ability != "CREW"):
                meg_gallak_ability = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
                
            if "RCTR" in meg_gallak_ability:
                if mission[0][3][0] > 0: 
                    mission[0][3][0] -= 2
                    missedOpportunity = False    
            elif "THRU" in meg_gallak_ability:
                if mission[0][3][1] > 0: 
                    mission[0][3][1] -= 2
                    missedOpportunity = False
            elif "DMG" in meg_gallak_ability:
                if mission[0][3][2] > 0: 
                    mission[0][3][2] -= 2
                    missedOpportunity = False
            elif "SHLD" in meg_gallak_ability:
                if mission[0][3][3] > 0: 
                    mission[0][3][3] -= 2
                    missedOpportunity = False
            elif "CREW" in meg_gallak_ability:
                if mission[0][3][4] > 0: 
                    mission[0][3][4] -= 2
                    missedOpportunity = False

            if missedOpportunity == True:
                print("ERROR: NOT MISSION REQUIREMENT. TRY AGAIN.")

        print( hand[ int(meg_gallak) - 1 ][0] , "has been trashed.")            
        del hand[ int(meg_gallak) - 1 ]
        ACTIONS += 1        
        print("Meg Gallak: 'Yeah, yeah, I.H.A., I'm sure we all know what we got ourselves into by making improvised explosives.' ")
        
    elif identity == 12:    #Myla Distra
        cardsChosen = 0
        repeat = True
        print("Myla Dystra: 'Be a lad and push that 'EMERGENCY' button for me, would you?' ")
        while repeat == True:
            printm(hand)
            Myla_Dystra = input("ENTER: NUMBER OF CARD TO DISCARD. CONTINUE CHOOSING UNTIL YOU [E]nd.\n")
            if "End" in Myla_Dystra or "E" in Myla_Dystra or "e" in Myla_Dystra:
                if cardsChosen > 0:
                    drawCards(draw_deck, cardsChosen, hand)    
                repeat = False

            elif "Myla Dystra" in hand[ int(Myla_Dystra) - 1 ][0] :
                print("Myla Dystra: 'One wrong coordinate, and we'll jump into a Black Hole.' ")
                print("ERROR: CANNOT DISCARD THE SAME CARD PREVIOUSLY CHOSEN.\n")
                  
            elif Myla_Dystra.isdigit() and ( int(Myla_Dystra) > 0 and int(Myla_Dystra) < len(hand) ):
                discard.append( hand[ int(Myla_Dystra) - 1 ] )
                del hand[ int(Myla_Dystra) - 1 ]
                cardsChosen += 1

            else:
                print("ERROR. RE-ENTER NUMBER.\n")
                
        ACTIONS += 1
        print("Myla Dystra: 'Keep her circling around.' ")

    elif identity == 13:  # AT-8K
        diceNumber = 1
        for dice in die:
            print("Dice #" + str(diceNumber) , "-" , die[dice], "Hazards")
            diceNumber += 1
            
        print("AT-8K: 'DANGER IMMINENT. APPROPRIATE COUNTERMEASURES PREPARED.' ")    
        AT_8K = input("ENTER: NUMBER OF DICE TO NEGATE ITS HAZARDS AND DEAL DAMAGE:\n")
        while (AT_8K.isdigit() == False) or int(AT_8K) < 1 or int(AT_8K) > len(die):
            AT_8K = input("ERROR. RE-ENTER NUMBER.\n")

        HAZARDS -= die[ int(AT_8K) - 1]
        D += die[ int(AT_8K) - 1]
        die[ int(AT_8K) - 1] = 0
        print("AT-8K: 'SUGGESTING RE-ROUTE WITH 99.42% CHANCE OF SURVIVAL.' ")        
                        
    elif identity == 14:  # Ada Massa
        ACTIONS += 3
        if mission[0][3][0] > 0:
            mission[0][3][0] -= 1
        print("Ada Massa: 'No I.H.A. safety manual will tell you this, but this is how you maximize the juice!' ")

    elif identity == 15:  # Sella Pelleon
        missedOpportunity = True # If you chose a requirement not present in mission, re-enter the reduction.
        print("Sella Pelleon: 'Greetings, Captain. How can I be of service today?' ")
        while missedOpportunity == True:
            sella_Pelleon = input("ENTER: 'RCTR' OR 'THRU' OR 'DMG' OR 'SHLD' OR 'CREW':\n")
            while ( sella_Pelleon != "RCTR" and sella_Pelleon != "THRU" and 
                    sella_Pelleon != "DMG"  and sella_Pelleon != "SHLD" and sella_Pelleon != "CREW"):
                print("Sella Pelleon: 'Come again?' ")
                sella_Pelleon = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
                
            if "RCTR" in sella_Pelleon:
                if mission[0][3][0] > 0: 
                    mission[0][3][0] -= 1
                    missedOpportunity = False    
            elif "THRU" in sella_Pelleon:
                if mission[0][3][1] > 0: 
                    mission[0][3][1] -= 1
                    missedOpportunity = False
            elif "DMG" in sella_Pelleon:
                if mission[0][3][2] > 0: 
                    mission[0][3][2] -= 1
                    missedOpportunity = False
            elif "SHLD" in sella_Pelleon:
                if mission[0][3][3] > 0: 
                    mission[0][3][3] -= 1
                    missedOpportunity = False
            elif "CREW" in sella_Pelleon:
                if mission[0][3][4] > 0: 
                    mission[0][3][4] -= 1
                    missedOpportunity = False

            if missedOpportunity == True:
                print("ERROR: NOT MISSION REQUIREMENT. TRY AGAIN.")

        ACTIONS += 1
        drawCards(draw_deck, 1, hand)
        print("Sella Pelleon: 'Anyone can be convinced to have it our way.' ")

    elif identity == 16:  # Sol Forst
        print("Sol Forst: 'I know a few contacts 'cross the galaxy. Grease my hands, and I'll get the best ones.' ")
        sol_Forst = input("ENTER: +2 [C]ards, OR [P]ay -1$ for +4 Cards:\n")
        while ( sol_Forst != "Card" and sol_Forst != "C" and sol_Forst != "c" and
                sol_Forst != "Pay" and sol_Forst != "P" and sol_Forst != "p"):
            print("Sol Forst: 'Hate to break it to ya, but time is money.' ")
            sol_Forst = input("ERROR. RE-ENTER CHOICE:\n")

        if ("Card" in sol_Forst) or ("C" in sol_Forst) or ("c" in sol_Forst):
            drawCards(draw_deck, 2, hand)
            print("Sol Forst: 'There's plenty o' people out there that'll work for peanuts. Let me stir the pot real quick.' ")
        elif ("Pay" in sol_Forst) or ("P" in sol_Forst) or ("p" in sol_Forst):
            COINS -= 1
            drawCards(draw_deck, 4, hand)
            print("Sol Forst: 'That's my boy! You'll get 'em boots squeaky clean and by the next sunrise.' ")
        

    elif identity == 17:  # Rez Vondu
        print("Rez Vondu: 'Need something fixed?' ")
        rez_Vondu = input("ENTER: +2 [A]ctions, OR [P]ay -1$ for +4 Actions:\n")
        while ( rez_Vondu != "Actions" and rez_Vondu != "A" and rez_Vondu != "a" and
                rez_Vondu != "Pay" and rez_Vondu != "P" and rez_Vondu != "p"):
            print("Rez Vondu: 'Sure, how about you give me the ship's schematics instead?' ")
            rez_Vondu = input("ERROR. RE-ENTER CHOICE:\n")

        if ("Actions" in rez_Vondu) or ("A" in rez_Vondu) or ("a" in rez_Vondu):
            ACTIONS += 2
            print("Rez Vondu: 'Three thousand more hours like this, and I might be able to afford a ship of my own...")
        elif ("Pay" in rez_Vondu) or ("P" in rez_Vondu) or ("p" in rez_Vondu):
            COINS -= 1
            ACTIONS += 4
            print("Rez Vondu: 'Unlike you, the I.H.A. don't pay a damn for expertise.' ")

    elif identity == 18:  # Metaxis  # QUESTION - does Metaxis need to be the last crewmember to use his ability?
        printm(crew_selection)
        print("Metaxis: 'Relax, my friend. You sweat too much for your own work. Let me get someone for you...' ")
        metaxis = input("ENTER: NUMBER CREWMEMBER TO USE ITS ABILITY:\n")
        while (metaxis.isdigit() == False) or int(metaxis) < 1 or int(metaxis) > len(crew_selection):
            print("Metaxis: 'Looks like that one is no longer with us. Oh well.' ")
            metaxis = input("ERROR. RE-ENTER NUMBER.\n")

        card_code( crew_selection[ ( int(metaxis) - 1) ] , False, True) # Derivative is True - Copied crewmember does NOT contribute to crewmember requirements
        print("Metaxis: 'Blackmail is the most convincing argument, no?' ")
        
        
    elif identity == 19:  # Kary Powalk
        KARY_POWALK = True
        ACTIONS += 1
        print("Kary Powalk: 'All units: Alpha strike their shields and focus fire their connection points! You know the rest.' ")

    elif identity == 20:  # Zardon the Enforcer
        for card in range( len(hand)-1 , 0, -1): # Start counting from the end, then delete as you go to the front.
            if "Damage 1" in hand[card] or "Damage 2" in hand[card] or "Damage 3" in hand[card]: 
                card_code(hand[card] , False, False)
                cards_in_play.append( hand[card] )
                del( hand[card] )
        ACTIONS += 1
        print("Zardon the Enforcer: 'My will is law.' ")
        
    elif identity == 21:  # Strada Rysh
        dice = random.randint(1, 3)
        hazard = 0
        if dice == 1:      # 2 Hazards on the dice
            hazard = 2
            die.append(2)
            print("Strada Rysh: 'Command, we might be in some trouble.' ")
        elif dice == 2:    # 1 Hazard on the die
            hazard = 1
            die.append(1)
            print("Strada Rysh: 'The house wins today. We'll see about that after slighting some margins.' ")
        elif dice == 3:     # 0 Hazard on the die
            die.append(0)
            print("Strada Rysh: 'No such thing as luck! It's all in your decision making.' ")
            
        if hazard > 0:
            print("Strada is risking", hazard , "hazards!\n")
            HAZARDS += hazard
        PRESTIGE += 1
        ACTIONS += 1

    elif identity == 22:  # Baz
        D += 1
        BAZ = True
        print("Baz: 'GET ME IN COACH, THESE FUSES ARE JUST WAITING TO BE LIT!' ")
        
    elif identity == 23:  # Lila al Bindar
        printm(hand)
        print("Lila al Bindar: 'Sir, I suggest we dismantle some of the ship armaments for their power components.' ")
        lila_bindar = input("ENTER: NUMBER OF CARD TO TRASH:\n")
        while (lila_bindar.isdigit() == False) or int(lila_bindar) < 1 or int(lila_bindar) > len(hand):
            print("Lila al Bindar: 'Ah, this one doesn't have a power core in it. What else is there?' ")
            lila_bindar = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
            
        discard.append(CARDS[4])
        del( hand[ int(lila_bindar) - 1] )
        ACTIONS += 1
        print("Lila al Bindar: 'Shipwright, get these circuits connected to the mainframe on the double!' ")
        
    elif identity == 24:  # Lee van Cribb
        peakingCards = []
        drawCards(draw_deck, 3, peakingCards)
        printm(peakingCards)
        print("Lee van Cribb: Jumping ahead to get a recon on the A.O.")
        vanCribb = input("ENTER: NUMBER OF CARD TO PLAY:\n")
        while (vanCribb.isdigit() == False) or int(vanCribb) < 1 or int(vanCribb) > len(hand):
            print("Lee van Cribb: 'Command, my signal's dropping this far out. How copy, over?' ")
            vanCribb = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")

        card_code( peakingCards[ ( int(vanCribb) - 1) ] , False, False)
        cards_in_play.append( peakingCards[ int(vanCribb) - 1 ] )
        del( peakingCards[ int(vanCribb) - 1 ] )
        for x in range( len(peakingCards) ):    # Identical code to discard()
            discard.append( peakingCards[0] )
            del peakingCards[0]
        ACTIONS += 1
        print("Lee van Cribb: 'Transmitting tactical data. Watch out for those bogeys, over.' ")
        
    elif identity == 25:  # Tantin al Vale
        print("Tantin al Vale: 'It's the sight of glorious battle. How shall we win it?' ")
        tantin_Vale = input("ENTER: PLAY AS 2 [D]amage, OR [S]hields: \n")
        while ( tantin_Vale != "Damage" and tantin_Vale != "D" and tantin_Vale != "d" and
                tantin_Vale != "Shields" and tantin_Vale != "S" and tantin_Vale != "s"):
            print("Tantin al Vale: 'Settle down boys! Command's on the line.' ")
            tantin_Vale = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
            
        if ("Damage" in tantin_Vale) or ("D" in tantin_Vale) or ("d" in tantin_Vale):
            D += 2
            print("Tantin al Vale: 'We'll dispose of this rubbish.' ")
        elif ("Shields" in tantin_Vale) or ("S" in tantin_Vale) or ("s" in tantin_Vale):
            card_code(CARDS[6] , False, False)
            print("Tantin al Vale: 'Techies, divert power from subsections 3-8 to shields.' ")
            
    elif identity == 26:  # B3-AR
        crewRetrieved = []
        for crew in discard: # Retrieve all crewmembers in the discard pile and put into the imaginary 'crewRetrieved' list
            if crew[-1] > 6:
                crewRetrieved.append( crew )
        for crew in cards_in_play: # Same as above, but look through cards in play.
            if crew[-1] > 6:
                crewRetrieved.append( crew )
                
        printm(crewRetrieved)
        print("B3-AR: 'ALerT. aleRT. COMmANDING OFFICER REQUESTSss ALL {priority}-CLASS CREEWwWMATES TO ATTEND.' ")
        B3_AR = input("ENTER: NUMBER OF CARD TO RETRIEVE:\n")
        while (B3_AR.isdigit() == False) or int(B3_AR) < 1 or int(B3_AR) > len(crewRetrieved):
            print("B3-AR: 'PROBLEM. USER IDENTIFICAtioooon NOT FIND. MAY I CALL AnOTHEr, m-moTheR-r-r?' ")
            B3_AR = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")

        hand.append( crewRetrieved[ int(B3_AR) - 1 ] )
        index = 0
        for card in discard:
            if card[0] == crewRetrieved[ int(B3_AR) - 1 ][0]: # If your choice was in discard, find and delete duplicate
                del discard[index]
            index += 1
            
        index = 0
        for card in cards_in_play:
            if card[0] == crewRetrieved[ int(B3_AR) - 1 ][0]: # Same as above but for cards in play
                del cards_in_play[index]
            index += 1

        ACTIONS += 1
        print("B3-AR: 'ROAR! USER {" + crewRetrieved[ int(B3_AR) - 1 ][0] + "} HAS reeeeTuRnED.' ")
                
    elif identity == 27:  # [REDACTED]
        for x in range( len(die) ):
            print("Dice #" + str( (x+1) ) , "-" , die[x], "hazards")
        
        diceToBeRerolled = []
        repeat = True
        print("\n[REDACTED]: 'You're lucky that I'm around.' ")
        print("ENTER: NUMBER OF THE DICE TO REROLL. CONTINUE CHOOSING UNTIL YOU [E]nd.")
        while repeat == True:
            REDACTED = input("")
            if "End" in REDACTED or "E" in REDACTED or "e" in REDACTED:
                for y in diceToBeRerolled:
                    y = int(y)
                    dice = random.randint(1, 3)
                    if dice == 1:      # 2 Hazards on the dice
                        die[y-1] = 2
                        print("DANGER - HACK DETECTED - ENEMY ON ALERT")
                    elif dice == 2:    # 1 Hazard on the die
                        die[y-1] = 1
                        print("THREAT - SUSPICION RAISED")
                    elif dice == 3:     # 0 Hazard on the die
                        die[y-1] = 0
                        print("CLEAR - FALSE NARRATIVE PLANTED")
                        
                repeat = False

            elif REDACTED in diceToBeRerolled:
                print("ERROR. YOU MAY NOT REROLL THE SAME DICE YOU CHOSE BEFORE. TRY AGAIN.")
                  
            elif REDACTED.isdigit() and ( int(REDACTED) > 0 and int(REDACTED) <= len(die) ):
                diceToBeRerolled.append( REDACTED )

            else:
                print("ERROR. RE-ENTER NUMBER.\n")

        diceHAZARDS = sum(die)
        card_code(CARDS[6] , False, False)
        print("[REDACTED]: 'Pay up in 6 solar cycles from now, or there will be consequences.' ")

    elif identity == 28:  # Kal Damar
        drawCards(draw_deck, 2, hand)
        printm(hand)
        print("Kal Damar: 'Never sweat the small things, my friend.' ")
        kal_damar = input("ENTER: OPTIONAL - TRASH A CARD, OR [S]kip:\n")
        while ( int(kal_damar) < 1 or int(kal_damar) > len(hand) or
                ( kal_damar != "Skip" and kal_damar != "S" and kal_damar != "s" ) ):
            print("Kal Damar: 'No dream has ever been accomplished only by a hasty thought.' ")
            kal_damar = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")

        if kal_damar.isdigit():    
            del( hand[ int(kal_damar) - 1] )
        print("Kal Damar: 'Life should be taken easy, but remember to take it.' ")
        
    elif identity == 29:  # Karma Kesa
        print("Karma Kesa: 'She lives in us all, just like how She lives in you.' ")
        karma_kesa = input("ENTER: +3 [A]ctions, OR draw an [O]bjective:\n")
        while ( karma_kesa != "Actions" and karma_kesa != "A" and karma_kesa != "a" and
                karma_kesa != "Objective" and karma_kesa != "O" and karma_kesa != "o"):
            print("Karma Kesa: 'Fret not - Her words are arcane, but always well-meaning.' ")
            karma_kesa = input("ERROR. RE-ENTER CHOICE:\n")

        if ("Actions" in karma_kesa) or ("A" in karma_kesa) or ("a" in karma_kesa):
            ACTIONS += 3
            print("Karma Kesa: 'Energy and life, Her doing, moves us forward...' ")
        elif ("Objective" in karma_kesa) or ("O" in karma_kesa) or ("o" in karma_kesa):
            drawCards(objectives_deck, 1, objectives)
            print("Karma Kesa: '... but what point would there be, without beholding Her wonders?' ")

    elif identity == 30:  # Ryle al Wren
        print("Ryle al Wren: 'There are civilians in the area - where do we shield?' ")
        ryle_wren = input("ENTER: Negate 2 [H]azards, OR  reduce [S]hield requirements by 2: \n")
        while ( ryle_wren != "Hazards" and ryle_wren != "H" and ryle_wren != "h" and
                ryle_wren != "Shield" and ryle_wren != "S" and ryle_wren != "s"):
            print("Ryle al Wren: 'I'm already on it!' ")
            ryle_wren = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
        if ("Hazards" in ryle_wren) or ("H" in ryle_wren) or ("h" in ryle_wren):
            HAZARDS -= 2
        elif ("Shield" in ryle_wren) or ("S" in ryle_wren) or ("s" in ryle_wren):
            if mission[0][3][3] > 0:
                mission[0][3][3] -= 2
            else:
                if HAZARDS >= 2:
                    HAZARDS -= 2
                elif HAZARDS == 1:
                    HAZARDS -= 1
                print("\nALERT: Due to there being no shield requirements, Ryle al Wren reduced the Hazards instead.")
                
        print("Ryle al Wren: 'Vigilo Confido.' ")
        
    elif identity == 31:  # Moro Mada
        print("Moro Mada: 'Provide me your smallest shuttle, and I'll take care of the rest.' ")
        missedOpportunity = True # If you chose a requirement not present in mission, re-enter the reduction.
        while missedOpportunity == True:
            moro_mada = input("ENTER: 'RCTR' OR 'THRU' OR 'DMG' OR 'SHLD' OR 'CREW':\n")
            while ( moro_mada != "RCTR" and moro_mada != "THRU" and 
                    moro_mada != "DMG"  and moro_mada != "SHLD" and moro_mada != "CREW"):
                print("Moro Mada: 'Don't waste my time.' ")
                moro_mada = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
                
            if "RCTR" in moro_mada:
                if mission[0][3][0] > 0: 
                    mission[0][3][0] -= 2
                    missedOpportunity = False    
            elif "THRU" in moro_mada:
                if mission[0][3][1] > 0: 
                    mission[0][3][1] -= 2
                    missedOpportunity = False
            elif "DMG" in moro_mada:
                if mission[0][3][2] > 0: 
                    mission[0][3][2] -= 2
                    missedOpportunity = False
            elif "SHLD" in moro_mada:
                if mission[0][3][3] > 0: 
                    mission[0][3][3] -= 2
                    missedOpportunity = False
            elif "CREW" in moro_mada:
                if mission[0][3][4] > 0: 
                    mission[0][3][4] -= 2
                    missedOpportunity = False

            if missedOpportunity == True:
                print("ERROR: NOT MISSION REQUIREMENT. TRY AGAIN.")

        print("Moro Mada: 'Remember the new encryption ID. I was never here.' ")

    elif identity == 32:  # Col Dervok
        printm(hand)
        print("Col Dervok: 'Met a guy in 2749, I know he'll love paying for any junk he can get.' ")
        col_dervok = input("ENTER: NUMBER OF CARD TO TRASH FOR +3 Credits:\n")
        while (col_dervok.isdigit() == False) or int(col_dervok) < 1 or int(col_dervok) > len(hand):
            print("Col Dervok: 'Hold on, hold on, as your mechanic, I must point out that that's too important to trash.' ")
            col_dervok = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")

        del( hand[ int(col_dervok) - 1 ] )
        COINS += 3
        ACTIONS += 1
        print("Col Dervok: 'Yeah, he'll like that. I'll arrange a sale after the mission.' ")
        
    elif identity == 33:  # Lok Tekt
        cardsChosen = 0
        repeat = True
        print("Lok Tekt: 'The cycle of life demands sacrifices in order to be maintained.' ")
        while repeat == True:
            printm(hand)
            lok_tekt = input("ENTER: NUMBER OF SHIELD TO DISCARD. CONTINUE CHOOSING UNTIL YOU [E]nd.\n")
            if "End" in lok_tekt or "E" in lok_tekt or "e" in lok_tekt:
                if cardsChosen > 0:
                    drawCards(draw_deck, (2*cardsChosen), hand)    
                repeat = False

            elif "Lok Tekt" in hand[ int(lok_tekt) - 1 ][0] :
                print("Lok Tekt: '...' ")
                print("ERROR: CANNOT DISCARD THE SAME CARD WHEN USING.\n")
                  
            elif ( lok_tekt.isdigit() and ("Shields" in hand[int(lok_tekt) - 1][0]) and
                  (int(lok_tekt) > 0 and int(lok_tekt) < len(hand)) ):
                discard.append( hand[ int(lok_tekt) - 1 ] )
                del hand[ int(lok_tekt) - 1 ]
                cardsChosen += 1

            else:
                print("Lok Tekt: 'You must not displease Her! She can sense us all!' ")  
                print("ERROR. RE-ENTER NUMBER.\n")
                
        print("Lok Tekt: 'This devotion to the sanctity of life will please Her.' ")
              
    elif identity == 34:  # Jes Ofra
        print("Jes Ofra: 'These.. 'Moonrakers' value reputation greatly. We can leverage that.' ")
        jes_ofra = input("ENTER: 'RCTR' OR 'THRU' OR 'DMG' OR 'SHLD':\n")
        while ( jes_ofra != "RCTR" and jes_ofra != "THRU" and 
                jes_ofra != "DMG"  and jes_ofra != "SHLD"):
            print("Jes Ofra: 'Perhaps we can schmooze a few parts off some traders.' ")
            jes_ofra = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")
            
        if "RCTR" in jes_ofra:
            hand.append( CARDS[4] )
              
        elif "THRU" in jes_ofra:
            hand.append( CARDS[5] )
              
        elif "DMG" in jes_ofra:
            hand.append( CARDS[1] )
              
        elif "SHLD" in jes_ofra:
            hand.append( CARDS[6] )
            
        print("Jes Ofra: 'People barter for things that they lack most. For us - assistance; to them - your recognition.' ")

    elif identity == 35: # Zek Zarag
        if len(draw_deck) > 0:
            printm(draw_deck)
            print("Zek Zarag: 'Need someone to take a look around?' ")
            zek_zarag = input("ENTER: NUMBER OF CARD TO PLAY WITHOUT AN ACTION:\n")
            while (zek_zarag.isdigit() == False) or int(zek_zarag) < 1 or int(zek_zarag) > len(draw_deck):
                print("Zek Zarag: 'I wouldn't mind taking a little break. Just a suggestion!' ")
                zek_zarag = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")

            card_code(draw_deck[int(zek_zarag)-1] , False, False)
            cards_in_play.append( draw_deck[int(zek_zarag)-1] )
            del( draw_deck[int(zek_zarag)-1] )
            random.shuffle(draw_deck)
            print("Zek Zarag: 'Right away!' ")

        else:
            print("Zek Zarag: 'Sorry sir, but there appears to be nothing in here!' ")

    elif identity == 36: # Ryan Rogal
        drawCards(draw_deck, 2, hand)
        ryan_rogal = False
        for X in range(1, 3):
            if ("Damage 1" in hand[-X][0] or "Damage 2" in hand[-X][0] or "Damage 3" in hand[-X][0]) and ryan_rogal == False:
                ryan_rogal = True
                D += 5
                print("Ryan Rogal: 'As I promised, here is your shipment, captain.' ")
                print("Ryan Rogal dealt 5 damage with a", hand[-X][0] + "!")
                cards_in_play.append( hand[-X] )
                del( hand[-X] )
                
        if ryan_rogal == False:
            print("Ryan Rogal: 'Well, uhh... all purchases are final!' ")
                
              
    # After each card, print new line    
    print("\n")                  


# Dictionary containing ship parts
# FORMAT --- KEY : [ Name , Description, Cost, Cards added to deck, Brand, KEY number for code ]
# Very similar to how basic and crew cards work.
SHIP_PARTS = {
    0 : [ "Sapphire mk2"    , "Requirements for Reactors is 1 less."                                            , 4 ,
          "+1 RCTR"         , [CARDS[4]] , "KOMEK"  , 0 ], #StartContract # IDEA - Make this the 4th index
                                                        # Or just hard code it into the ship_parts code
    1 : [ "MG2 Quad Laser"  , "At the START of a contract, +2 Cards if you have no Damage cards in your hand."  , 4 ,
          "+1 DMG3"         , [CARDS[3]] , "MAGNOMI", 1 ], #StartContract
    2 : [ "Cloaking Device" , "Roll 1 less Hazard Dice."                                                        , 5 ,
          "None"            , ""         , "HENKO"  , 2 ], #StartContract OR Special ???
    3 : [ "Vector Jets E3"  , "As Mission Leader, +1 Card at the START of a contract."                          , 3 ,
          "+1 THRU"         , [CARDS[5]] , "VENTUS" , 3 ], #StartContract
    4 : [ "Symbiote 9000"   , "Once per contract, you may trash a Card from your hand to negate 1 Hazard."      , 2 ,
          "+1 SHLD"         , [CARDS[6]] , "HENKO"  , 4 ], #Manual
    5 : [ "MG1 Rail Gun"    , "Requirement is 1 less for Damage if you don't play a Shield."                    , 4 ,
          "+1 DMG2; +1 MISS", [CARDS[2] , CARDS[0]] , "MAGNOMI" , 5 ], #PlayCardBasis
    6 : [ "Defender 5000"   , "As 1 Action, discard 2 Cards of ANY type to use as a Shield."                    , 3 ,
          "+1 SHLD"         , [CARDS[6]] , "HENKO"  , 6 ], #Manual
    7 : [ "The Dauntless"   , "Each Shield played also counts as 1 Damage."                                     , 6 ,
          "+2 SHLD"         , [CARDS[6] , CARDS[6]] , "SORELIA" , 7 ], #PlayCardBasis
    8 : [ "Flare Shard"     , "Gain +1 Credit for each of your Hazard blocked."                                 , 4 ,
          "+1 SHLD"         , [CARDS[6]] , "HENKO"  , 8 ], #Special
    9 : [ "Barrier A3"      , "At the START of a contract, +1 Card if you have no Shields in your hand."        , 2 ,
          "+1 SHLD"         , [CARDS[6]] , "VENTUS" , 9 ], #StartContract
    10: [ "DOOM"            , "When you stay at base, gain +4 Credits instead of 1."                            , 4 ,
          "+1 DMG3"         , [CARDS[3]] , "MAGNOMI", 10], #Special
    11: [ "MG Charge Core"  , "As 1 Action, you may play a Damage 1 as a Damage 3. Then add a Miss to your discard." , 3 ,
          "+1 RCTR"         , [CARDS[4]] , "MAGNOMI", 11], #Manual
    12: [ "MG Warp"         , "+2 Cards when you play your first Damage card."                                  , 5 ,
          "+1 THRU"         , [CARDS[5]] , "VENTUS" , 12], #PlayCardBasis
    13: [ "Multi Stage M1"  , "Once per contract you may discard up to 3 Cards, allies draw an equal number."   , 4 ,
          "+2 THRU"         , [CARDS[5] , CARDS[5]] , "VENTUS"  , 13 ], #Manual
    14: [ "Pulsor mk1"      , "Allies start with an extra Action."                                              , 2 ,
          "+1 RCTR"         , [CARDS[4]] , "KOMEK"  , 14], #StartContract
    15: [ "Hypershift"      , "Before playing cards, you may discard your entire hand. If you do, +5 cards."    , 4 ,
          "+1 THRU"         , [CARDS[5]] , "VENTUS" , 15], #StartContract ???
    16: [ "Ghost"           , "Your first Thruster played negates a Hazard Die."                                , 6 ,
          "+1 THRU"         , [CARDS[5]] , "VENTUS" , 16], #PlayCardBasis
    17: [ "Twin Jets E4"    , "Requirement for Thruster is 1 less."                                             , 3 ,
          "+1 THRU"         , [CARDS[5]] , "VENTUS" , 17], #StartContract
    18: [ "Flash"           , "Your hand limit becomes 6 instead of 5."                                         , 6 ,
          "None"            , ""         , "VENTUS" , 18], #Special
    19: [ "Jump Jets E2"    , "Allies receive +1 Card at the start of a contract."                              , 2 ,
          "+1 THRU"         , [CARDS[5]] , "VENTUS" , 19], #StartContract
    20: [ "Predator mk1"    , "All players can play 1 Damage 1 without using an Action."                        , 3 ,
          "+1 DMG2; +1 MISS", [CARDS[2] , CARDS[0]] , "KOMEK" , 20], #PlayCardBasis
    21: [ "Fission"         , "Reactor cards don't require an Action to play."                                  , 5 ,
          "+1 RCTR"         , [CARDS[4]] , "KOMEK"  , 21], #PlayCardBasis
    22: [ "Daburu mk1"      , "Start EVERY contract with +1 Action."                                            , 6 ,
          "None"            , ""         , "KOMEK"  , 22], #StartContract
    23: [ "The Quantum Driver" , "Your first Damage 1 played counts as a Damage 3."                             , 7 ,
          "+1 DMG3; +1 MISS", [CARDS[3] , CARDS[0]] , "SORELIA" , 23], #PlayCardBasis
    24: [ "The Clone Bay"   , "Once per contract, you may play a Crew Member twice. Each use requires an Action." , 6 ,
          "None"            , ""         , "SORELIA", 24], #Manual
    25: [ "505"             , "You may play Miss cards as a Shield, Thruster, Reactor, or Damage 1."            , 6 ,
          "+1 MISS"         , [CARDS[0]] , "SORELIA", 25], #PlayCardBasis
    26: [ "EM - TR4"        , "Once per contract, you may pay 2 Credits to draw a default loadout card from the supply to your hand" , 2 ,
          "None"            , ""         , "SORELIA", 26], #Manual
    27: [ "Shard Spear"     , "You may trash a Damage and a Card from your hand to add a Damage of one tier higher into your hand." , 4 ,
          "+1 DMG2"         , [CARDS[2]], "MAGNOMI" , 27], #Manual
    28: [ "The Pursuer"     , "Once per contract, you may discard up to 3 Cards and draw an equal number."      , 6 ,
          "+2 THRU"         , [CARDS[5] , CARDS[5]], "SORELIA" , 28], #Manual
    29: [ "Siphon"          , "Gain an Action for each Hazard you block with a shield."                         , 5 ,
          "+1 SHLD"         , [CARDS[6]] , "HENKO"  , 29], #PlayCardBasis
    30: [ "MG Phase core"   , "If you play 2 Reactors, the requirement for Damage is 1 less."                   , 3 ,
          "+1 RCTR"         , [CARDS[4]] , "MAGNOMI", 30], #PlayCardBasis
    31: [ "Refractor"       , "You may trash a Reactor to gain +4 Action."                                      , 3 ,
          "+1 RCTR"         , [CARDS[4]] , "KOMEK"  , 31], #Manual
    32: [ "MG2 Laser Turrets", "As 1 Action, play 2 Damage 1 cards to deal 4 Damage."                           , 2 ,
          "+2 DMG1"         , [CARDS[1] , CARDS[1]] , "MAGNOMI" , 32], #Manual
    33: [ "Projector S2"    , "+1 Card per Hazard Dice targetting YOU."                                         , 4 ,
          "+2 SHLD"         , [CARDS[6] , CARDS[6]] , "VENTUS" , 33], #StartContract
    34: [ "MG1 Kinetic"     , "Trash a Damage 1 from your hand, requirement for Damage is 3 less."              , 3 ,
          "+2 DMG1; +1 MISS", [CARDS[1] , CARDS[1] , CARDS[0]] , "MAGNOMI" , 34], #Manual
    35: [ "The Gatling Laser", "Requirement for Damage is 1 less."                                              , 5 ,
          "+1 DMG3; +1 MISS", [CARDS[3] , CARDS[0]] , "SORELIA" , 35], #StartContract
    36: [ "Emulator mk2"    , "Play your first shield without using an Action."                                 , 3 ,
          "+1 SHLD"         , [CARDS[6]] , "KOMEK"  , 36], #PlayCardBasis
    37: [ "Dark Matter mk3" , "As 1 Action, play a Damage 1 and a Damage 2 to deal 5 Damage."                   , 4 ,
          "+1 DMG2"         , [CARDS[2]] , "KOMEK"  , 37], #Manual
    38: [ "Absorption K2"   , "At the START of a contract, +1 Card if you have no Reactors in your hand."       , 3 ,
          "+1 RCTR"         , [CARDS[4]] , "VENTUS" , 38], #StartContract
    39: [ "Titan 3000"      , "Requirements for Shields is 1 less."                                             , 3 ,
          "+1 SHLD"         , [CARDS[6]] , "HENKO"  , 39], #StartContract
    40: [ "The Leech"       , "As Mission Leader or Ally, gain +1 Action for each ally."                        , 5 ,
          "+2 RCTR"         , [CARDS[4] , CARDS[4]] , "SORELIA" , 40], #StartContract, but practically PlayCardBasis
    41: [ "MG Support Core" , "Play your first Damage card without using an Action."                            , 3 ,
          "+2 RCTR"         , [CARDS[4] , CARDS[4]] , "MAGNOMI" , 41], #PlayCardBasis
    42: [ "Accelerator mk3" , "Your first Reactor played gives an extra Action."                                , 4 ,
          "+1 RCTR"         , [CARDS[4]] , "KOMEK"  , 42], #PlayCardBasis
    43: [ "Escape Jets E1"  , "At the START of a contract, +1 Card if you have no Thrusters in your hand"       , 3 ,
          "+1 THRU"         , [CARDS[5]] , "VENTUS" , 43], #StartContract
    44: [ "Replicator mk1"  , "Discard 2 of the same card as 1 Action and play as a Shield, Thruster, Reactor, or Damage 1." , 3 ,
          "+1 THRU"         , [CARDS[5]] , "KOMEK" , 44],  #Manual
    45: [ "Duo 1000"        , "Your first Shield played counts as 2 Shields."                                   , 4 ,
          "+1 SHLD"         , [CARDS[6]] , "HENKO"  , 45], #PlayCardBasis
    46: [ "Swarm mk1"       , "Discard a Damage 1 from your hand, +2 Actions."                                  , 4 ,
          "+1 DMG2; +1 MISS", [CARDS[2], CARDS[0]], "KOMEK" , 46] #Manual
}


# There are 4 possible 'species' of parts:
    # Manual - Activate the ship card manually during a contract
    # StartContract - Automatically activates at the start of a contract
    # PlayCardBasis - Every time you play a card, the code automatically activates
    # Special - Super special circumstances that warrants this type. Typically a name of its own.
def ship_parts_code(species, selected, rememberCard):
    global ACTIONS, HAZARDS, PRESTIGE, R, T, D, S, C, COINS, HAND_LIMIT, HAZARDS_BLOCKED

    for part in ship_parts:          # This for loop will go through all your ship parts and apply them where applicable. I must indent ALL ship code under this loop to use it. 
        if "manual" in species:
            identity = ship_parts[selected][-1]
        else:
            identity = part[-1]
    
        if identity == 0 and "startContract" in species:       # Sapphire mk2
            if mission[0][3][0] > 0:
                mission[0][3][0] -= 1
                print("Sapphire mk2's generator satisfies 1 of the Reactor requirements!")
        
        elif identity == 1 and "startContract" in species:     # MG2 Quad Laser
            if ( CARDS[1] not in hand ) and ( CARDS[2] not in hand ) and ( CARDS[3] not in hand ):
                drawCards(draw_deck, 2, hand)
                print("Reload engaged. MG2 Quad Laser has drawn you 2 extra cards!") 
                
        elif identity == 2 and "startContract" in species:     # Cloaking Device
            if mission[0][2] > 0:
                mission[0][2] -= 1
                print("The Cloaking Device grants you considerable safety in conducting the mission.")
                
        elif identity == 3 and "startContract" in species:     # Vector Jets E3
            drawCards(draw_deck, 1, hand)
            print("Vector Jets E3 to maximum! +1 Card")

        elif identity == 4 and "manual" in species:     # Symbiote 9000
            limitedUses("Symbiote 9000")
            if shipLimitedUses[ partIndex ] < 1:
                printm(hand)
                Symbiote_9000 = input("ENTER CARD NUMBER TO TRASH, OR ' Cancel ' \n")
                if "Cancel" in Symbiote_9000:
                    print("Canceled using the Symbiote 9000.\n\n")
                elif int(Symbiote_9000) > 0 and int(Symbiote_9000) <= len(hand):
                    print("The Symbiote 9000 trashed the" , hand[ int(Symbiote_9000) - 1 ][0] + ".\n\n")
                    del hand[ int(Symbiote_9000) - 1 ]
                    HAZARDS -= 1
                    shipLimitedUses[ partIndex ] += 1
                else:
                    print("INPUT ERROR DETECTED. CANCELLING..")
            else:
                print("You've already used the Symbiote 9000!\n\n")
 
        elif identity == 5 and ( "playCardBasis" in species or "startContract" in species ): # MG1 Rail Gun
            if mission[0][3][2] > 0: # Only works if the mission has damage requirements
                limitedUses("MG1 Rail Gun") 
                if CARDS[6] in cards_in_play:
                    if shipLimitedUses[ partIndex ] > 0 and shipLimitedUses[ partIndex ] < 2:
                        mission[0][3][2] += 1
                        print("The shields nullified your MG1 Rail Gun!\n")
                        shipLimitedUses[ partIndex ] += 1 # Special code for this part only

                elif CARDS[6] not in cards_in_play:
                    if shipLimitedUses[ partIndex ] < 1:
                        mission[0][3][2] -= 1
                        print("MG1 Rail Gun successfully tore apart a target. \n")
                        shipLimitedUses[ partIndex ] += 1
                    
                    
        elif identity == 6 and "manual" in species:     # Defender 5000
            if ACTIONS <= 0: # You must pay an action to use this part. 
                print("No actions available for this part. Cancelling...")
                break
            
            printm(hand)
            Defender_5000 = input("ENTER 1ST CARD TO DISCARD, OR ' Cancel ' \n")
            if "Cancel" in Defender_5000:
                print("Canceled using the Defender 5000.\n\n")
            elif int(Defender_5000) > 0 and int(Defender_5000) <= len(hand):
                Defender_5000_2 = input("ENTER 2ND CARD TO DISCARD, OR ' Cancel ' \n")
                if "Cancel" in Defender_5000_2:
                    print("Canceled using the Defender 5000.\n\n")
                elif int(Defender_5000_2) > 0 and int(Defender_5000_2) <= len(hand):
                    print("Discarded",hand[int(Defender_5000)-1][0],"and",hand[int(Defender_5000_2)-1][0],
                          "with the Defender 5000.\n\n")
                    discard.append(hand[int(Defender_5000)-1])
                    discard.append(hand[int(Defender_5000_2)-1])
                    if Defender_5000 > Defender_5000_2:
                        del(hand[int(Defender_5000)-1])
                        del(hand[int(Defender_5000_2)-1])
                    elif Defender_5000 < Defender_5000_2:
                        del(hand[int(Defender_5000_2)-1])
                        del(hand[int(Defender_5000)-1])
                    S += 1
                    HAZARDS -= 1
                else:
                    print("INPUT ERROR DETECTED. CANCELLING..")
            else:
                print("INPUT ERROR DETECTED. CANCELLING..")

        elif identity == 7 and ("playCardBasis" in species): # The Dauntless
            if rememberCard[0] == "Shields": 
                print("Dauntless speed! SHLD --> +1 DMG\n")
                D += 1

        elif identity == 8 and "Flare Shard" in species: # Flare Shard
            COINS += HAZARDS_BLOCKED
            if HAZARDS_BLOCKED > 0:
                print("\nDebris collected - Flare Shard earned you +$" + str(HAZARDS_BLOCKED) , "credits.")


        elif identity == 9 and "startContract" in species: # Barrier A3
            if CARDS[6] not in hand:
                drawCards(draw_deck, 1, hand)
                print("Emergency [SHIELD] protocols engaged. Barrier A3 has drawn you an extra card!\n") 

        elif identity == 10 and "DOOM" in species: # DOOM
            COINS += 3
            print("Out of fear for the DOOM, the station commander compensated you handsomely.\n")

        elif identity == 11 and "manual" in species: # MG Charge Core
            if ACTIONS <= 0: # You must pay an action to use this part. 
                print("No actions available for this part. Cancelling...")
                break
            
            if CARDS[1] in hand:
                printm(hand)
                MGChargeCore = input("ENTER THE NUMBER OF A DMG1 TO PLAY AS DMG3, OR ' Cancel ' \n")
                if "Cancel" in MGChargeCore:
                    print("Canceled using the MG Charge Core.\n\n")
                elif int(MGChargeCore) > 0 and int(MGChargeCore) <= len(hand):
                    if hand[int(MGChargeCore)-1][0] == "Damage 1":
                        print("Supercharging rounds! MG Charge Core fired +3 DMG, but caused some overheating.\n")
                        cards_in_play.append(hand[int(MGChargeCore)-1])
                        del(hand[int(MGChargeCore)-1])
                        D += 3
                        discard.append(CARDS[0])
                        ACTIONS -= 1
                    else:
                        print("ERROR: DMG1 NOT SELECTED. CANCELLING..\n")
                
            elif CARDS[1] not in hand:
                print("ERROR: NO DMG1s DETECTED IN HAND. CANCELLING..\n")

        elif identity == 12 and "playCardBasis" in species: # MG Warp
            limitedUses("MG Warp")
            if shipLimitedUses[ partIndex ] < 1:
                if (rememberCard[0] == "Damage 1") or (rememberCard[0] == "Damage 2") or (rememberCard[0] == "Damage 3"):
                    print("MG Warp sustained fire cycle calibrated. +2 Cards!\n")
                    drawCards(draw_deck, 2, hand)
                    shipLimitedUses[ partIndex ] += 1

        elif identity == 13 and "manual" in species: # Multi Stage M1
            limitedUses("Multi Stage M1")
            if shipLimitedUses[ partIndex ] < 1:
                counter = 0
                printm(hand)
                intention = input("ENTER 1-3 FOR INTENDED NUMBER OF DISCARDS, OR ' Cancel '\n")
                if int(intention) > 0 and int(intention) < 4:
                    while counter < int(intention):
                        printm(hand)
                        MStgM1 = input("ENTER CARD NUMBER TO DISCARD, OR ' End '\n")
                        if "End" in MStgM1:
                            print("Ended discarding early with Multi Stage M1.")
                            break # This will break the loop
                        elif int(MStgM1) > 0 and int(MStgM1) <= len(hand):
                            counter += 1
                            discard.append(hand[int(MStgM1)-1])
                            del(hand[int(MStgM1)-1])
                    drawCards(mercenary_deck, counter, mercenary_hand)
                    print("All allies have drawn +" + str(counter) , "cards due to the Multi Stage M1!")
                    shipLimitedUses[ partIndex ] += 1
                    
                elif intention == "Cancel":
                    print("CANCELLING Multi Stage M1..\n")
                else:
                    print("INPUT ERROR DETECTED. CANCELLING Multi Stage M1..\n")
            else:
                print("ERROR: Multi Stage M1 has already been used.")

        elif identity == 14 and "startContract" in species: # Pulsor mk1
            ACTIONS += 1
            print("The Pulsor mk1 generates +1 Action for yourself in solo mode.")

        elif identity == 15 and "manual" in species: # Hypershift
            limitedUses("Hypershift")
            if shipLimitedUses[ partIndex ] < 1:
                if len(cards_in_play) == 0:
                    choice = input("Hypershift primed and ready. Engage warp? \nENTER: [Y], [N] ")
                    if "Y" in choice or "y" in choice:
                        discardf()
                        drawCards(draw_deck, 5, hand)
                        print("Hypershift successful. Armaments recalibrated.") 
                        shipLimitedUses[ partIndex ] += 1

                    elif "N" in choice or "n" in choice:
                        break

                elif len(cards_in_play) > 0:
                    print("We can't divert power to the Hypershift drive whilst in combat!") 
            
            
        elif identity == 16 and "playCardBasis" in species: # Ghost
            limitedUses("Ghost")
            if shipLimitedUses[ partIndex ] < 1:
                if rememberCard[0] == "Thrusters":
                    for dice in die:
                        if die[dice] == 2:
                            die[dice] = 0
                            HAZARDS -= 2
                            print("Ghost engaged: heat signature's gone dark. Major threat neutralized.")
                            shipLimitedUses[ partIndex ] += 1
                            break
                        elif die[dice] == 1:
                            die[dice] = 0
                            HAZARDS -= 1
                            print("Ghost engaged: heat signature's gone dark. Minor threat neutralized.")
                            shipLimitedUses[ partIndex ] += 1
                            break
                    


        elif identity == 17 and "startContract" in species: # Twin Jets E4
            if mission[0][3][1] > 0:
                mission[0][3][1] -= 1
                print("Twin Jets E4 satisfies 1 of the Thruster requirements!\n")

        elif identity == 18 and "Flash" in species: # Flash
            HAND_LIMIT = 6

        elif identity == 19 and "startContract" in species: # Jump Jets E2
            drawCards(mercenary_deck, 1, mercenary_hand)
            print("Your allies may draw +1 Card due to your Jump Jets E2!\n")

        elif identity == 20 and "playCardBasis" in species: # Predator mk1
            limitedUses("Predator mk1")
            if shipLimitedUses[ partIndex ] < 1:
                if rememberCard[0] == "Damage 1":
                    ACTIONS += 1
                    print("The Predator automatically launched a missile!")
                    shipLimitedUses[ partIndex ] += 1

        elif identity == 21 and "playCardBasis" in species: # Fission
            if rememberCard[0] == "Reactors":
                ACTIONS += 1
                print("Power... Unlimited Fission power...")

        elif identity == 22 and "startContract" in species: # Daburu mk1
            ACTIONS += 1
            print("The Daburu mk1 has generated an additional action for you!\n")

        elif identity == 23 and "playCardBasis" in species: # The Quantum Driver
            limitedUses("The Quantum Driver")
            if shipLimitedUses[ partIndex ] < 1:
                if rememberCard[0] == "Damage 1":
                    D += 2
                    print("Munitions multiplied by Quantums: D1 --> D3!")
                    
        elif identity == 24 and "manual" in species: # The Clone Bay
            if ACTIONS <= 0: # You must pay an action to use this part. 
                print("No actions available for this part. Cancelling...")
                break
            
            limitedUses("The Clone Bay")
            if shipLimitedUses[ partIndex ] < 1:
                printm(hand)
                cloneBay = input("ENTER THE NUMBER OF A CREWMEMBER TO CLONE, OR ' Cancel ':\n")
                if "Cancel" in cloneBay:
                    print("CANCELLING USING THE CLONE BAY..")
                    
                elif ( int(cloneBay) >= 1) and ( int(cloneBay) <= len(cloneBay) ):
                    if hand[int(cloneBay)-1][-1] > 6:
                        card_code(hand[int(cloneBay)-1] , False, False)
                        ACTIONS -= 1
                        print("You have cloned" , hand[int(cloneBay)-1][0] + ".\n")
                        shipLimitedUses[ partIndex ] += 1

                    else:
                        print("ERROR: THAT IS NOT A CREWMEMBER. CANCELLING..")

            else:
                print("ERROR: YOU'VE ALREADY USED THE CLONE BAY THIS MISSION.")
                    

        elif identity == 25 and "playCardBasis" in species: # 505
            if rememberCard[0] == "Miss":
                choosing = True
                while choosing == True:
                    input505 = input("CONVERT A MISS TO A RCTR, THRU, SHLD, OR DMG1, OR [C]ancel:\n")
                    if "RCTR" in input505:
                        card_code(CARDS[4] , False, False)
                        choosing = False
                    elif "THRU" in input505:
                        card_code(CARDS[5] , False, False)
                        choosing = False
                    elif "SHLD" in input505:
                        card_code(CARDS[6] , False, False)
                        choosing = False
                    elif "DMG1" in input505:
                        card_code(CARDS[1] , False, False)
                        choosing = False
                    elif "Cancel" in input505 or "C" in input505 or "c" in input505:
                        print("Cancelling using the 505...\n")
                        choosing = False
                    else:
                        print("INPUT ERROR DETECTED. PLEASE RETRY...")

        elif identity == 26 and "manual" in species: # EM - TR4
            limitedUses("EM - TR4")
            if shipLimitedUses[ partIndex ] < 1:
                if COINS >= 2:
                    choosing = True
                    while choosing == True:
                        print("DRAW A RCTR, THRU, SHLD, DMG1, OR MISS TO YOUR HAND.")
                        emTR4 = input("YOU MUST PAY $2, OR ' Cancel ':\n")
                        if "RCTR" in emTR4:
                            hand.append(CARDS[4])
                            choosing = False
                            shipLimitedUses[ partIndex ] += 1
                            COINS -= 2
                        elif "THRU" in emTR4:
                            hand.append(CARDS[5])
                            choosing = False
                            shipLimitedUses[ partIndex ] += 1
                            COINS -= 2
                        elif "SHLD" in emTR4:
                            hand.append(CARDS[6])
                            choosing = False
                            shipLimitedUses[ partIndex ] += 1
                            COINS -= 2
                        elif "DMG1" in emTR4:
                            hand.append(CARDS[1])
                            choosing = False
                            shipLimitedUses[ partIndex ] += 1
                            COINS -= 2
                        elif "Miss" in emTR4:
                            hand.append(CARDS[0])
                            choosing = False
                            shipLimitedUses[ partIndex ] += 1
                            COINS -= 2
                        elif "Cancel" in emTR4:
                              print("CANCELLING EM - TR4..")
                              choosing = False
                        else:
                            print("INPUT ERROR DETECTED. PLEASE RETRY...")
                else:
                    print("YOU DO NOT HAVE COINS FOR THE EM - TR4. CANCELLING..")
            else:
                print("ERROR: YOU'VE ALREADY USED THE EM - TR4 THIS MISSION.")

        elif identity == 27 and "manual" in species: # Shard Spear
            printm(hand)
            Shard_Spear = input("ENTER: NUMBER OF DESIRED DAMAGE CARD TO UPGRADE, OR [C]ancel \n")
            if "Cancel" in Shard_Spear or "C" in Shard_Spear or "c" in Shard_Spear: # Go through several checks
                print("Canceled using the Shard Spear.\n\n")
            elif "Damage 3" in hand[int(Shard_Spear)-1][0]:
                print("You may not upgrade a Damage 3. Cancelling Shard Spear.\n\n")
            elif ( "Damage 1" not in hand[int(Shard_Spear)-1][0]
                and "Damage 2" not in hand[int(Shard_Spear)-1][0] and "Damage 3" not in hand[int(Shard_Spear)-1][0] ):
                print("That's not a Damage card. Cancelling Shard Spear.\n\n")
            elif int(Shard_Spear) > 0 and int(Shard_Spear) <= len(hand):
                Shard_Spear_2 = input("ENTER: ANY OTHER CARD TO TRASH, OR [C]ancel \n")
                if "Cancel" in Shard_Spear_2 or "C" in Shard_Spear_2 or "c" in Shard_Spear_2:
                    print("Canceled using the Shard Spear.\n\n")
                elif int(Shard_Spear_2) > 0 and int(Shard_Spear_2) <= len(hand):
                    print("Upgraded",hand[int(Shard_Spear)-1][0],"and trashed",hand[int(Shard_Spear_2)-1][0],
                          "with the Shard Spear.\n\n") 

                    if hand[int(Shard_Spear)-1][0] == "Damage 1": # Add the upgraded damage to hand
                        hand.append(CARDS[2])
                    elif hand[int(Shard_Spear)-1][0] == "Damage 2":
                        hand.append(CARDS[3])
                        
                    if Shard_Spear > Shard_Spear_2: # Delete selected cards. Mindful of list shifting due to deletion.
                        del(hand[int(Shard_Spear)-1])
                        del(hand[int(Shard_Spear_2)-1])
                    elif Shard_Spear < Shard_Spear_2:
                        del(hand[int(Shard_Spear_2)-1])
                        del(hand[int(Shard_Spear)-1])
                    

                else:
                    print("INPUT ERROR DETECTED. CANCELLING..")
            else:
                print("INPUT ERROR DETECTED. CANCELLING..")

        elif identity == 28 and "manual" in species: # The Pursuer
            limitedUses("The Pursuer")
            if shipLimitedUses[ partIndex ] < 1:
                printm(hand)
                print("Pursuer fuel cells full. How much boost are we talking?")
                drawAmount = int( input("ENTER: DISCARD AND DRAW UP TO 3 CARDS\n") )
                
                while int(drawAmount) < 0 or int(drawAmount) > 3: #or isinstance(drawAmount, int) == False:
                    drawAmount = input("Error. Enter valid number of cards.")
                    
                choice1 = input("ENTER: CARD 1 TO DISCARD, OR [C]ancel.\n") # Choose cards for the pursuer. Input validation for all choices.
                if "Cancel" in choice1 or "C" in choice1 or "c" in choice1:
                    print("Canceling using The Pursuer.")
                    break
                while int(choice1) <= 0 or int(choice1) >= len(hand):
                    choice1 = input("Error. Enter valid card number.\n")
                if drawAmount == 2 or drawAmount == 3:
                    choice2 = input("ENTER: CARD 2 TO DISCARD, OR [C]ancel.\n")
                    if "Cancel" in choice2 or "C" in choice2 or "c" in choice2:
                        print("Canceling using The Pursuer.")
                        break
                    while int(choice2) <= 0 or int(choice2) >= len(hand):
                        choice2 = input("Error. Enter valid card number.\n")
                if drawAmount == 3:
                    choice3 = input("ENTER: CARD 3 TO DISCARD, OR [C]ancel.\n")
                    if "Cancel" in choice3 or "C" in choice3 or "c" in choice3:
                        print("Canceling using The Pursuer.")
                        break
                    while int(choice3) <= 0 or int(choice3) >= len(hand):
                        choice3 = input("Error. Enter valid card number.\n")

                if drawAmount == 1:
                    discard.append(hand[int(choice1)-1])
                    del(hand[int(choice1)-1])
                elif drawAmount == 2:
                    if choice1 > choice2: # Discard selected cards. Mindful of list shifting due to deletion.
                        discard.append(hand[int(choice1)-1])
                        discard.append(hand[int(choice2)-1])
                        del(hand[int(choice1)-1])
                        del(hand[int(choice2)-1])
                    elif choice1 < choice2:
                        discard.append(hand[int(choice1)-1])
                        discard.append(hand[int(choice2)-1])
                        del(hand[int(choice2)-1])
                        del(hand[int(choice1)-1])
                elif drawAmount == 3:
                    if choice1 > choice2 and choice1 > choice3: # If 1st is biggest 
                        discard.append(hand[int(choice1)-1])
                        del(hand[int(choice1)-1])
                        if choice2 > choice3:
                            discard.append(hand[int(choice2)-1])
                            discard.append(hand[int(choice3)-1])
                            del(hand[int(choice2)-1])
                            del(hand[int(choice3)-1])
                        elif choice2 < choice3:
                            discard.append(hand[int(choice3)-1])
                            discard.append(hand[int(choice2)-1])
                            del(hand[int(choice3)-1])
                            del(hand[int(choice2)-1])

                    elif choice2 > choice1 and choice2 > choice3: # If 2nd is biggest
                        discard.append(hand[int(choice2)-1])
                        del(hand[int(choice2)-1])
                        if choice1 > choice3:
                            discard.append(hand[int(choice1)-1])
                            discard.append(hand[int(choice3)-1])
                            del(hand[int(choice1)-1])
                            del(hand[int(choice3)-1])
                        elif choice1 < choice3:
                            discard.append(hand[int(choice3)-1])
                            discard.append(hand[int(choice1)-1])
                            del(hand[int(choice3)-1])
                            del(hand[int(choice1)-1])

                    elif choice3 > choice1 and choice3 > choice2: # If 3rd is biggest
                        discard.append(hand[int(choice3)-1])
                        del(hand[int(choice3)-1])
                        if choice1 > choice2:
                            discard.append(hand[int(choice1)-1])
                            discard.append(hand[int(choice2)-1])
                            del(hand[int(choice1)-1])
                            del(hand[int(choice2)-1])
                        elif choice1 < choice2:
                            discard.append(hand[int(choice2)-1])
                            discard.append(hand[int(choice1)-1])
                            del(hand[int(choice2)-1])
                            del(hand[int(choice1)-1])

                print("The Pursuer's mobility is unmatched. The space is ours.")
                drawCards(draw_deck, int(drawAmount) , hand)
                shipLimitedUses[ partIndex ] += 1
                
            else:
                print("The Pursuer has already been used this battle!\n")

 
        elif identity == 29 and "Siphon" in species: # Siphon
            ACTIONS += 1
            print("The Siphon converted the kinetic energy absorbed into reactor power!")

        elif identity == 30 and "playCardBasis" in species: # MG Phase core
            limitedUses("MG Phase core")
            if shipLimitedUses[ partIndex ] < 1:
                reactorsFound = 0
                for card in cards_in_play:
                    if card[0] == "Reactors":
                        reactorsFound += 1

                if reactorsFound >= 2:
                    if mission[0][3][2] > 0:
                        mission[0][3][2] -= 1
                        shipLimitedUses[ partIndex ] += 1
                        print("Excess reactor power has charged up the MG Phase core!")
                        print("Damage requirements is 1 less.")

            

        elif identity == 31 and "manual" in species: # Refractor
            printm(hand)
            Refractor = input("ENTER: NUMBER OF REACTOR CARD TO TRASH, OR [C]ancel \n")
            if "Cancel" in Refractor or "C" in Refractor or "c" in Refractor:
                print("Canceled using the Refractor.\n\n")
            elif hand[ int(Refractor)-1][0] != "Reactors":
                print("That is not a Reactor. Cancelling...")
            elif int(Refractor) > 0 and int(Refractor) <= len(hand):
                print("The Refractor scrapped the Reactor for 4 additional actions.\n\n")
                del hand[ int(Refractor) - 1 ]
                ACTIONS += 4
            else:
                print("INPUT ERROR DETECTED. CANCELLING..")

        elif identity == 32 and "manual" in species: # MG2 Laser Turrets
            if ACTIONS <= 0: # You must pay an action to use this part. 
                print("No actions available for this part. Cancelling...")
                break
            
            printm(hand)
            MG2Laser = input("ENTER: NUMBER OF A DAMAGE 1, OR [C]ancel \n")
            if "Cancel" in MG2Laser or "C" in MG2Laser or "c" in MG2Laser:
                print("Canceled using the MG2 Laser Turrets.\n\n")
            elif int(MG2Laser) > 0 and int(MG2Laser) <= len(hand):
                MG2Laser_2 = input("ENTER: NUMBER OF ANOTHER DAMAGE 1, OR [C]ancel \n")
                if "Cancel" in MG2Laser_2 or "C" in MG2Laser_2 or "c" in MG2Laser_2:
                    print("Canceled using the  MG2 Laser Turrets.\n\n")
                elif int(MG2Laser_2) > 0 and int(MG2Laser_2) <= len(hand):
                    print("Target in range, unleash the MG2 Laser Turrets!")
                    print("Played two Damage 1s for 4 Damage and 1 action.\n")
                    cards_in_play.append(hand[int(MG2Laser)-1])
                    cards_in_play.append(hand[int(MG2Laser_2)-1])
                    if MG2Laser > MG2Laser_2:
                        del(hand[int(MG2Laser)-1])
                        del(hand[int(MG2Laser_2)-1])
                    elif MG2Laser < MG2Laser_2:
                        del(hand[int(MG2Laser_2)-1])
                        del(hand[int(MG2Laser)-1])
                    D += 4
                    ACTIONS -= 1
                else:
                    print("INPUT ERROR DETECTED. CANCELLING..")
            else:
                print("INPUT ERROR DETECTED. CANCELLING..")
                
                                                    # P.S2 is supposed to be startContract, but code demands it be special
        elif identity == 33 and "Projector S2" in species: # Projector S2
            if len(die) > 0:
                drawCards(draw_deck, len(die), hand)
                print("Projector S2 decoys deployed. +" + str(len(die)) + " cards.\n")

        elif identity == 34 and "manual" in species: # MG1 Kinetic
            printm(hand)
            MG1Kinetic = input("ENTER: NUMBER OF DAMAGE 1 CARD TO TRASH, OR [C]ancel \n")
            if "Cancel" in MG1Kinetic or "C" in MG1Kinetic or "c" in MG1Kinetic:
                print("Canceled using the MG1 Kinetic.\n\n")
            elif hand[ int(MG1Kinetic)-1][0] != "Damage 1":
                print("That is not a Damage 1. Cancelling...")
            elif int(MG1Kinetic) > 0 and int(MG1Kinetic) <= len(hand):
                print("The MG1 Kinetic supercharged a deadly blast! Damage requirements is 3 less.\n\n")
                del hand[ int(MG1Kinetic) - 1 ]
                mission[0][3][2] -= 3
            else:
                print("INPUT ERROR DETECTED. CANCELLING..")

        elif identity == 35 and "startContract" in species: # The Gatling Laser
            if mission[0][3][2] > 0:
                mission[0][3][2] -= 1
                print("The Gatling Laser automatically destroyed a by-standing target!")
                print("Damage requirements is 1 less.\n")

        elif identity == 36 and "playCardBasis" in species: # Emulator mk2
            limitedUses("Emulator mk2")
            if shipLimitedUses[ partIndex ] < 1:
                if (rememberCard[0] == "Shields"):
                    print("Passive shields holding. Emulator mk2 online. +1 Action.\n")
                    ACTIONS += 1
                    shipLimitedUses[ partIndex ] += 1

        elif identity == 37 and "manual" in species: # Dark Matter mk3
            if ACTIONS <= 0: # You must pay an action to use this part. 
                print("No actions available for this part. Cancelling...")
                break
            
            printm(hand)
            DarkMatter = input("ENTER: NUMBER OF A DAMAGE 1, OR DAMAGE 2, OR [C]ancel \n")
            if "Cancel" in DarkMatter or "C" in DarkMatter or "c" in DarkMatter:
                print("Canceled using the Dark Matter mk3.\n\n")
            elif hand[ int(DarkMatter)-1][0] != "Damage 1" and hand[ int(DarkMatter)-1][0] != "Damage 2":
                print("That is not a Damage card. Cancelling...")
            elif int(DarkMatter) > 0 and int(DarkMatter) <= len(hand):
                DarkMatter2 = input("ENTER: NUMBER OF THE OTHER DAMAGE CARD, OR [C]ancel \n")
                if "Cancel" in DarkMatter2 or "C" in DarkMatter2 or "c" in DarkMatter2:
                    print("Canceled using the  Dark Matter mk3.\n\n")
                elif hand[ int(DarkMatter2)-1][0] != "Damage 1" and hand[ int(DarkMatter2)-1][0] != "Damage 2":
                    print("That is not a Damage card. Cancelling...")
                    
                elif int(DarkMatter2) > 0 and int(DarkMatter2) <= len(hand):
                    if (hand[ int(DarkMatter)-1][0] == "Damage 1" and hand[ int(DarkMatter2)-1][0] == "Damage 2") or \
                       (hand[ int(DarkMatter)-1][0] == "Damage 2" and hand[ int(DarkMatter2)-1][0] == "Damage 1"):
                        print("Open the Dark Matter blasters. Stay clear of the blast radius!")
                        print("Played a Damage 1 and Damage 2 for 5 Damage and 1 action.\n")
                        cards_in_play.append(hand[int(DarkMatter)-1])
                        cards_in_play.append(hand[int(DarkMatter2)-1])
                        if DarkMatter > DarkMatter2:
                            del(hand[int(DarkMatter)-1])
                            del(hand[int(DarkMatter2)-1])
                        elif DarkMatter < DarkMatter2:
                            del(hand[int(DarkMatter2)-1])
                            del(hand[int(DarkMatter)-1])
                        D += 5
                        ACTIONS -= 1
                    else:
                        print("INPUT ERROR DETECTED. CANCELLING..")
                else:
                    print("INPUT ERROR DETECTED. CANCELLING..")
            else:
                print("INPUT ERROR DETECTED. CANCELLING..")

        elif identity == 38 and "startContract" in species: # Absorption K2
            if CARDS[4] not in hand:
                drawCards(draw_deck, 1, hand)
                print("Back-up battery activated. Absorption K2 has drawn you an extra card!\n") 

        elif identity == 39 and "startContract" in species: # Titan 3000
            if mission[0][3][3] > 0:
                mission[0][3][3] -= 1
                print("The Titan 3000 satisfies 1 of the Shield requirements!\n")

        elif identity == 40 and "playCardBasis" in species: # The Leech
        # This code is based on a single player game with the mercenary. It'll need an overhaul for multiplayer.
            limitedUses("The Leech")
            if shipLimitedUses[ partIndex ] < 1:
                if len(cards_in_play_MERC) > 0:
                    print("Covertly leeching power off the mercenary... +1 Action.\n")
                    ACTIONS += 1
                    shipLimitedUses[ partIndex ] += 1

        elif identity == 41 and "playCardBasis" in species: # MG Support Core
            limitedUses("MG Support Core")
            if shipLimitedUses[ partIndex ] < 1:
                if (rememberCard[0] == "Damage 1") or (rememberCard[0] == "Damage 2") or (rememberCard[0] == "Damage 3"):
                    print("Accessing auxiliarly power from the MG Support core. +1 Action.\n")
                    ACTIONS += 1
                    shipLimitedUses[ partIndex ] += 1
                    

        elif identity == 42 and "playCardBasis" in species: # Accelerator mk3
            limitedUses("Accelerator mk3")
            if shipLimitedUses[ partIndex ] < 1:
                if (rememberCard[0] == "Reactors"):
                    print("Accelerating reactor spin time. +1 Action.\n")
                    ACTIONS += 1
                    shipLimitedUses[ partIndex ] += 1
                    

        elif identity == 43 and "startContract" in species: # Escape Jets E1
            if CARDS[5] not in hand:
                drawCards(draw_deck, 1, hand)
                print("Escape Jets kicking in... E1 has drawn you an extra card!\n")

        elif identity == 44 and "manual" in species: # Replicator mk1
            if ACTIONS <= 0: # You must pay an action to use this part. 
                print("No actions available for this part. Cancelling...")
                break
            
            printm(hand)      
            print("DISCARD TWO MATCHING CARDS TO PLAY THE REPLICATOR.")
            copies1 = input("ENTER: NUMBER OF FIRST CARD, OR [C]ancel: \n")
            if "Cancel" in copies1 or "C" in copies1 or "c" in copies1:
                print("Cancelling using the Replicator mk1...\n")
            elif int(copies1) > 0 and int(copies1) <= len(hand):
                copies2 = input("ENTER: NUMBER OF SECOND MATCHING CARD, OR [C]ancel: \n")
                if "Cancel" in copies2 or "C" in copies2 or "c" in copies2:
                    print("Cancelling using the Replicator mk1...\n")
                elif int(copies2) > 0 and int(copies2) <= len(hand):
                    if hand[int(copies1) - 1][0] == hand[int(copies2) - 1][0]:

                        replicatormk1 = input("PLAY A RCTR, THRU, SHLD, OR DMG1, OR [C]ancel:\n")
                        while (replicatormk1 != "RCTR" and replicatormk1 != "THRU" and
                              replicatormk1 != "SHLD" and replicatormk1 != "DMG1" and
                              replicatormk1 != "Cancel" and replicatormk1 != "C" and replicatormk1 != "c"):
                            replicatormk1 = input("ERROR. INPUT INVALID. PLEASE RETRY.")

                        if "Cancel" in replicatormk1 or "C" in replicatormk1 or "c" in replicatormk1:
                            print("Cancelling using the Replicator mk1...\n")
                            break
                        elif "RCTR" in replicatormk1:
                            card_code(CARDS[4] , False, False)
                            message = "reactor"
                        elif "THRU" in replicatormk1:
                            card_code(CARDS[5] , False, False)
                            message = "thruster"
                        elif "SHLD" in replicatormk1:
                            card_code(CARDS[6] , False, False)
                            message = "shield"
                        elif "DMG1" in replicatormk1:
                            card_code(CARDS[1] , False, False)
                            message = "damage 1"

                        if copies1 > copies2: # Discard selected cards. Mindful of list shifting due to deletion.
                            discard.append(hand[int(copies1)-1])
                            discard.append(hand[int(copies2)-1])
                            del(hand[int(copies1)-1])
                            del(hand[int(copies2)-1])
                        elif copies1 < copies2:
                            discard.append(hand[int(copies1)-1])
                            discard.append(hand[int(copies2)-1])
                            del(hand[int(copies2)-1])
                            del(hand[int(copies1)-1])                                                    
                        print("The Replicator has created a" , message +"!\n")    
                        ACTIONS -= 1
      
                    else:
                        print("Those cards do not match. Cancelling...\n")

            else:
                print("INPUT ERROR DETECTED. CANCELLING...\n")

        elif identity == 45 and "playCardBasis" in species: # Duo 1000
            limitedUses("Duo 1000")
            if shipLimitedUses[ partIndex ] < 1:
                if (rememberCard[0] == "Shields"):
                    print("The Duo has synchronized our shields!\n")
                    card_code(CARDS[6] , False, False) # Activate an additional instance of "Shields" with played card.
                    shipLimitedUses[ partIndex ] += 1
                

        elif identity == 46 and "manual" in species: # Swarm mk1
            SwarmMk1 = input("ENTER: NUMBER OF A DAMAGE CARD, OR [C]ancel.\n")
            if "Cancel" in SwarmMk1 or "C" in SwarmMk1 or "c" in SwarmMk1:
                print("Canceled using the Swarm Mk1.\n\n")
            elif hand[ int(SwarmMk1)-1][0] != "Damage 1":
                print("That is not a Damage 1. Cancelling...")
            elif int(SwarmMk1) > 0 and int(SwarmMk1) <= len(hand):
                print("The Swarm hungers - your Damage 1 was discarded for +2 Actions.\n\n")
                discard.append( hand[ int(SwarmMk1) - 1 ] )
                del hand[ int(SwarmMk1) - 1 ]
                ACTIONS += 2
            else:
                print("INPUT ERROR DETECTED. CANCELLING..")

        # If you're using a MANUAL ship part, do not loop multiple times
        if "manual" in species:
            break



# Dictionary containing objectives
# FORMAT --- KEY : [ Name, Description, KEY number for code ]
OBJECTIVES = {
    0 : ["Megaton"          , "Acquire 3 Magnomi ship parts for your ship."         , 0 ],
    1 : ["Money Bags"       , "Have 8 Credits at the end of your turn."             , 1 ],
    2 : ["Speed Demon"      , "Acquire 3 Ventus ship parts for your ship."          , 2 ],
    3 : ["Santa Maria"      , "Complete an Explore contract alone."                 , 3 ],
    4 : ["Chain Reaction"   , "Play at least 4 Reactor cards on the same contract." , 4 ],
    5 : ["Efficiency"       , "Play no Thruster cards but complete a Delivery contract." , 5 ],
    6 : ["Over 9000"        , "Acquire 3 Komek ship parts for your ship."           , 6 ],
    7 : ["Saboteur"         , "Fail a contract as an ally."                         , 7 ],
    8 : ["Quick Strike"     , "Play at least 3 Thruster cards on the same contract.", 8 ],
    9 : ["Natural Leader"   , "Play at least 3 Crew Members on the same contract."  , 9 ],
    10: ["Barrage"          , "Play at least 5 Damage on the same contract."        , 10 ],
    11: ["Guns For Hire"    , "Complete a Kill contract alone."                     , 11 ],
    12: ["Specialist"       , "Acquire 2 Sorelia ship parts for your ship."         , 12 ],
    13: ["Generalist"       , "Have a Magnomi, Henko, Komek, and Ventus ship part attached to your ship." , 13 ],
    14: ["Ace"              , "Complete a contract with 2 or more Hazard Dice targetting you." , 14 ],
    15: ["Tank"             , "Acquire 3 Henko ship parts for your ship."           , 15 ],
    16: ["Fire Support"     , "Play no Damage cards, but complete a Kill Contract." , 16 ],
    17: ["Tinker"           , "After acquiring 4 ship parts, replace a part on your ship." , 17 ],
    18: ["Utopia"           , "Complete a contract with all other players as allies.", 18 ],
    19: ["Quick Run"        , "Complete a Delivery contract alone."                 , 19 ],
    20: ["You're My Hero"   , "Complete a Rescue contract alone."                   , 20 ],
    21: ["Shield Wall"      , "Play at least 3 Shield cards on the same contract."  , 21 ],
    22: ["Daredevil"        , "Play no Shield cards but complete a Rescue contract.", 22 ]
}

# Objectives will be checked every so often by the game. It will automatically check if any are fulfilled, and ask if you wish to score now or later. 
def objectives_code():      
    global ACTIONS, HAZARDS, PRESTIGE, ALLIES, COINS, R, T, D, S, C, MISSION_COMPLETE
    
    completableObjectivesID = [] # Remember all objectives that are scorable. This is how you score Prestige.

    for card in objectives:         
        identity = card[-1]         
    
        if identity == 0:       # Megaton - Acquire 3 Magnomi ship parts for your ship.
            progress = 0
            for part in ship_parts:
                if "MAGNOMI" in part[-2]:
                    progress += 1
            if progress >= 3:
                completableObjectivesID.append( card )  # This objective is added to an imaginary list, to be scored later.

        elif identity == 1:     # Money bags - Have 8 Credits at the end of your turn.
            if PHASE == 3 and COINS >= 8:
                completableObjectivesID.append( card )

        elif identity == 2:     # Speed Demon - Acquire 3 Ventus ship parts for your ship.
            progress = 0
            for part in ship_parts:
                if "VENTUS" in part[-2]:
                    progress += 1
            if progress >= 3:
                completableObjectivesID.append( card )

        elif identity == 3:         # Santa Maria - Complete an Explore contract alone.
            if len(mission) != 0:   # If you didn't go on a mission, you can't score it. Obviously.
                if (len(cards_in_play_MERC) == 0) and (MISSION_COMPLETE == True) and (mission[0][-1] == "Explore"):
                    completableObjectivesID.append( card )

        elif identity == 4:         # Chain Reaction - Play at least 4 Reactor cards on the same contract.
            progress = 0        
            for played_card in cards_in_play:
                if played_card[-1] == 4:
                    progress += 1
            if progress >= 4:
                completableObjectivesID.append( card )

        elif identity == 5:         # Efficiency - Play no Thruster cards but complete a Delivery contract.        
            efficiency = True
            for played_card in cards_in_play:
                if (played_card[-1] == 5):
                    efficiency = False
            if len(mission) != 0:
                if (efficiency == True) and (MISSION_COMPLETE == True) and (mission[0][-1] == "Delivery"):
                    completableObjectivesID.append( card )

        elif identity == 6:         # Over 9000 - Acquire 3 Komek ship parts for your ship.
            progress = 0
            for part in ship_parts:
                if "KOMEK" in part[-2]:
                    progress += 1
            if progress >= 3:
                completableObjectivesID.append( card )

        elif identity == 7:         # Saboteur - Fail a contract as an ally.
            if (len(cards_in_play_MERC) > len(cards_in_play) ) and (MISSION_COMPLETE == False): 
                completableObjectivesID.append( card )

        elif identity == 8:         # Quick Strike - Play at least 3 Thruster cards on the same contract.
            progress = 0            
            for played_card in cards_in_play:
                if played_card[-1] == 5:
                    progress += 1
            if progress >= 3:
                completableObjectivesID.append( card )

        elif identity == 9:         # Natural Leader - Play at least 3 Crew Members on the same contract.
            progress = 0            
            for played_card in cards_in_play:
                if played_card[-1] > 6:
                    progress += 1
            if progress >= 3:
                completableObjectivesID.append( card )

        elif identity == 10: # Barrage - Play at least 5 Damage on the same contract.
            progress = 0
            for played_card in cards_in_play:
                if played_card[-1] == 1:
                    progress += 1
                elif played_card[-1] == 2:
                    progress += 2
                elif played_card[-1] == 3:
                    progress += 3
            if progress >= 5:
                completableObjectivesID.append( card )

        elif identity == 11:   # Gun for Hire - Complete a Kill contract alone.
            if len(mission) != 0:
                if (len(cards_in_play_MERC) == 0) and (MISSION_COMPLETE == True) and (mission[0][-1] == "Kill"):
                    completableObjectivesID.append( card )
      
        elif identity == 12:  # Specialist - Acquire 2 Sorelia ship parts for your ship.        
            progress = 0
            for part in ship_parts:
                if "SORELIA" in part[-2]:
                    progress += 1
            if progress >= 2:
                completableObjectivesID.append( card )
      
        elif identity == 13:  # Generalist - Have a Magnomi, Henko, Komek, and Ventus ship part attached to your ship.       
            magnomi = False
            henko = False
            komek = False
            ventus = False
            for part in ship_parts:
                if ("MAGNOMI" in part[-2]) and (magnomi == False):
                    magnomi = True
                elif ("HENKO" in part[-2]) and (henko == False):
                    henko = True
                elif ("KOMEK" in part[-2]) and (komek == False):
                    komek = True
                elif ("VENTUS" in part[-2]) and (ventus == False):
                    ventus = True
            if (magnomi == True) and (henko == True) and (komek == True) and (ventus == True):
                completableObjectivesID.append( card )
   
        elif identity == 14:         # Ace - Complete a contract with 2 or more Hazard Dice targetting you.
            if len(mission) != 0:
                if (MISSION_COMPLETE == True) and (mission[0][2] >= 2):
                    completableObjectivesID.append( card )
          
        elif identity == 15:         # Tank - Acquire 3 Henko ship parts for your ship.
            progress = 0
            for part in ship_parts:
                if "HENKO" in part[-2]:
                    progress += 1
            if progress >= 3:
                completableObjectivesID.append( card )

        elif identity == 16:         # Fire Support - Play no Damage cards, but complete a Kill Contract.
            fireSupport = True
            for played_card in cards_in_play:
                if (played_card[-1] == 1) or (played_card[-1] == 2) or (played_card[-1] == 3):
                    fireSupport = False
            if len(mission) != 0:
                if (fireSupport == True) and (MISSION_COMPLETE == True) and (mission[0][-1] == "Kill"):
                    completableObjectivesID.append( card )

        elif identity == 17:         # Tinker - After acquiring 4 ship parts, replace a part on your ship.
            if tinkerObjTurn == TURN:   # The objective assumes you had replaced a part. Checks if it's the same turn when you did so.
                completableObjectivesID.append( card )

        elif identity == 18:         # Utopia - Complete a contract with all other players as allies.
            if (len(cards_in_play) > 0) and (len(cards_in_play_MERC) > 0) and (MISSION_COMPLETE == True):
                completableObjectivesID.append( card )
                
        elif identity == 19:         # Quick Run - Complete a Delivery contract alone.
            if len(mission) != 0:
                if (len(cards_in_play_MERC) == 0) and (MISSION_COMPLETE == True) and (mission[0][-1] == "Delivery"):
                    completableObjectivesID.append( card )
                
        elif identity == 20:         # You're My Hero - Complete a Rescue contract alone.
            if len(mission) != 0:
                if (len(cards_in_play_MERC) == 0) and (MISSION_COMPLETE == True) and (mission[0][-1] == "Rescue"):
                    completableObjectivesID.append( card )
                
        elif identity == 21:         # Shield Wall - Play at least 3 Shield cards on the same contract.
            progress = 0            
            for played_card in cards_in_play:
                if played_card[-1] == 6:
                    progress += 1
            if progress >= 3:
                completableObjectivesID.append( card )
                
        elif identity == 22:         # Daredevil - Play no Shield cards but complete a Rescue contract.
            dareDevil = True
            for played_card in cards_in_play:
                if (played_card[-1] == 6):
                    dareDevil = False
            if len(mission) != 0: 
                if (dareDevil == True) and (MISSION_COMPLETE == True) and (mission[0][-1] == "Rescue"):
                    completableObjectivesID.append( card )

    if len(completableObjectivesID) > 0: # If you found scorable objectives, ask if to score
        print("\nYou have" , str( len(completableObjectivesID) ) , "scorable objectives! Would you like to score them? ")
        decision = input("ENTER: [Y]/[N] \n")
        while ( decision != "Y" and decision != "y" and
                decision != "N" and decision != "n"):
            decision = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")

        if "Y" in decision or "y" in decision:
            for card in completableObjectivesID:
                print(card[0], "complete! +1 Prestige")
                PRESTIGE += 1
                for X in range( len(objectives) , 0, -1):   # Start from the back, and delete any until you reach 0
                    X -= 1                                  # This line is necessary - Python needs to count indexes from 1 less
                    if card[0] in objectives[X][0]:
                        del objectives[X]

    print("") # End this function with a new line
    
    
# Dictionary containing all the contracts
# Format - KEY : [ "Name" , [Prestige, credits, bonus cards] , # of Hazard dice, [RCT, THR, DMG, SHD, CREW] ],
#                                                                                  ^--- Requirements ---^
CONTRACTS = {
    0 : ["Asteroid Field"       , [2, 8, 0], 2 ,[4, 0, 0, 0, 3] , "Explore" ],
    1 : ["Escape Pods"          , [2, 7, 0], 2 ,[0, 0, 3, 3, 0] , "Rescue"  ],
    2 : ["Fuel Shortage"        , [1, 3, 0], 1 ,[0, 2, 2, 0, 0] , "Delivery"],
    3 : ["Core World Ace"       , [1, 5, 1], 1 ,[0, 0, 5, 0, 0] , "Kill"    ],
    4 : ["Envoy in Distress"    , [1, 2, 1], 2 ,[0, 0, 2, 2, 0] , "Rescue"  ],
    5 : ["Abandoned Vessel"     , [1, 4, 1], 2 ,[3, 0, 3, 0, 0] , "Explore" ],
    6 : ["Negotiation Insurance", [1, 2, 1], 2 ,[0, 3, 1, 0, 0] , "Delivery"],
    7 : ["Proof of Life"        , [3, 4, 0], 2 ,[4, 4, 0, 0, 0] , "Delivery"],
    8 : ["Nova Bloom"           , [3, 7, 0], 3 ,[5, 0, 0, 3, 0] , "Explore" ],
    9 : ["Distress Beacon"      , [1, 3, 0], 1 ,[3, 0, 0, 0, 1] , "Explore" ],
    10: ["Boarding Action"      , [4, 0, 2], 3 ,[0, 0, 5, 0, 4] , "Explore" ],
    11: ["Resistance Leader"    , [4, 6, 0], 3 ,[0, 2, 0, 4, 2] , "Rescue"  ],
    12: ["Decoy Target"         , [3, 0, 3], 3 ,[0, 4, 0, 4, 0] , "Rescue"  ],
    13: ["First Contact"        , [3, 0, 2], 2 ,[5, 0, 0, 3, 0] , "Explore" ],
    14: ["Royal Cargo"          , [5, 10,0], 4 ,[0, 5, 5, 0, 2] , "Delivery"],
    15: ["Derelict Planet"      , [3, 8, 0], 2 ,[5, 2, 0, 0, 3] , "Explore" ],
    16: ["Gauntlet Run"         , [3, 0, 2], 2 ,[0, 4, 4, 0, 0] , "Delivery"],
    17: ["Rival Pirate Gang"    , [1, 3, 0], 1 ,[0, 0, 2, 1, 0] , "Kill"    ],
    18: ["Elite Squadron"       , [4, 6, 1], 3 ,[4, 0, 8, 3, 0] , "Kill"    ],
    19: ["Space Anomaly"        , [0, 3, 0], 0 ,[1, 0, 1, 0, 0] , "Explore" ],
    20: ["Munitions Stockpile"  , [3, 7, 0], 2 ,[0, 4, 0, 3, 0] , "Delivery"],
    21: ["Prison Moon"          , [5, 10,0], 4 ,[0, 4, 2, 5, 0] , "Rescue"  ],
    22: ["Reactor Failure"      , [0, 3, 0], 0 ,[1, 0, 0, 1, 0] , "Rescue"  ],
    23: ["Escort Duty"          , [1, 2, 1], 1 ,[0, 3, 0, 0, 1] , "Delivery"],
    24: ["Emergency Meds"       , [3, 8, 0], 2 ,[3, 4, 4, 0, 0] , "Delivery"],
    25: ["Probe Recovery"       , [1, 2, 1], 1 ,[3, 2, 0, 0, 0] , "Explore" ],
    26: ["Bomber Screen"        , [3, 9, 0], 3 ,[0, 3, 6, 0, 0] , "Kill"    ],
    27: ["Stim Run"             , [1, 2, 0], 1 ,[1, 2, 0, 0, 0] , "Delivery"],
    28: ["Pirate Treasure"      , [1, 2, 0], 1 ,[2, 0, 0, 1, 0] , "Explore" ],
    29: ["Hunt the Hunter"      , [3, 7, 0], 2 ,[0, 0, 7, 0, 0] , "Kill"    ],
    30: ["Blockade Run"         , [0, 3, 0], 0 ,[0, 1, 0, 1, 0] , "Delivery"],
    31: ["Illegal Munitions"    , [2, 8, 0], 2 ,[0, 3, 4, 0, 0] , "Delivery"],
    32: ["Claim Bounty"         , [1, 3, 0], 1 ,[2, 0, 3, 0, 0] , "Kill"    ],
    33: ["Kill Slavers"         , [0, 4, 0], 0 ,[0, 1, 1, 0, 0] , "Kill"    ],
    34: ["Cryogenic Pods"       , [3, 7, 0], 3 ,[4, 0, 0, 4, 0] , "Kill"    ],
    35: ["Bounty Hunters"       , [3, 6, 0], 3 ,[0, 0, 6, 0, 2] , "Kill"    ],
    36: ["Ancient Ruins"        , [2, 7, 0], 2 ,[4, 4, 0, 0, 0] , "Explore" ],
    37: ["Martial Law"          , [1, 4, 1], 2 ,[0, 0, 0, 2, 2] , "Rescue"  ],
    38: ["Assault on Vilonia"   , [3, 5, 1], 2 ,[0, 0, 8, 0, 0] , "Kill"    ],
    39: ["Deep Space Scan"      , [2, 8, 0], 3 ,[4, 0, 0, 4, 0] , "Explore" ],
    40: ["Black Hole"           , [5, 12, 0],4 ,[4, 4, 0, 0, 5] , "Explore" ],
    41: ["Icarus Run"           , [2, 8, 0], 2 ,[0, 3, 0, 3, 0] , "Rescue"  ],
    42: ["Focused Fire"         , [3, 0, 3], 3 ,[4, 0, 6, 0, 0] , "Kill"    ],
    43: ["Decoy Convoy"         , [2, 6, 0], 2 ,[0, 0, 3, 3, 0] , "Rescue"  ],
    44: ["Admiral's Flagship"   , [5, 11, 1],4 ,[5, 0, 8, 5, 0] , "Kill"    ],
    45: ["Transport Rescue"     , [1, 3, 0], 1 ,[0, 0, 0, 2, 1] , "Rescue"  ],
    46: ["Refugee Crisis"       , [2, 7, 0], 2 ,[0, 3, 0, 0, 2] , "Delivery"],
    47: ["Supernova Escape"     , [1, 3, 0], 1 ,[0, 1, 0, 2, 0] , "Rescue"  ],
    48: ["Hostage Extraction"   , [3, 6, 0], 2 ,[0, 0, 0, 2, 3] , "Rescue"  ],
    49: ["Scout Cruiser"        , [3, 6, 0], 3 ,[0, 0, 5, 2, 0] , "Kill"    ]
                                   
}
    

# Simple tally of the amount of credits the player has
COINS = 3

# The amount of prestige the player has. The player will win when they earn 10 prestige.
PRESTIGE = 0

# All players start a contract off with 1 action. End the contract with 1.
ACTIONS = 1

# Initiate the variable with 0. End the contract with 0.
HAZARDS = 0

# This variable tracks the current phase.
PHASE = 1

# This variable tracks the current turn.
TURN = 1

# Game begins, you have not achieved victory (obviously).
VICTORY = False

# This variable tracks the number of allies helping the Mission Leader.
ALLIES = 0

# This variable is the size of a player's hand. Normally it is 5, and they will draw 5 upon turn start. 
HAND_LIMIT = 5

# Begin game as such. This will update appropriately
MISSION_COMPLETE = False
    
# These variables track the conditions of crewmembers and objectives. The game will check if they are true for additional effects.
KARY_POWALK = False
BAZ = False
tinkerObjTurn = 0

# End of game scoring. These variables are only used for end-game scoring.
prestigeScore = 0
unspentCredits = 0
partScore = 0
crewScore = 0

###########  Moonrakers is a deck building game. This section will track the decks in play currently, and describe some rules.
## DECKS ##
###########

###### DICTIONARY #######
# draw_deck             = Player 1's deck to draw action cards from into their hand.
# discard               = Player 1's discard deck for action cards. If the draw deck is empty, reshuffle discards to form a new draw deck.
# hand                  = Player 1's action cards in hand.
# cards_in_play         = Action cards that are played to fulfill a contract are put here.
# cards_in_play_MERC     = Action cards played by the Mercenary.
# contracts_deck        = The deck that holds undrawn contract cards.
# contracts_selection   = The 8 face-up contract cards available for selection.
# contracts_discard     = Discarded contracts go here. If the contracts deck is empty, reshuffle discards to form a new contracts deck.
# mission               = The active contract the players are attempting to complete.
# objectives_deck       = The deck that holds undrawn objective cards.
# objectives_selection  = When a player draws objective cards, they will view them here. Chosen goes into their collection, while discarded one goes back to the bottom of objective deck.
# objectives            = Player 1's uncompleted objectives.
# crew_deck             = The deck that holds undrawn crew members.
# crew_selection        = Crewmembers available for purchase are put here and are face up. If one is bought, immediately fill the vacant spot with a new crew.
# ship_parts_deck       = The deck that holds undrawn ship parts.
# ship_parts_selection  = Ship parts available for purchase are put here and are face up. If one is bought, immediately fill the vacant spot with a new ship part.
# ship_parts            = The ship parts that are installed on player 1's ship.
# mercenary_deck        = If playing with 1 or 2 players, set up the mercenary deck (MANDATORY IN THIS CODE).
# mercenary_hand        = The 5 faceup cards that were drawn from the mercenary deck. Discard after players' turn.
#                          NOTE that crew cards played from mercenary will be returned to the bottom of the crew deck.
# mercenary_discard     = The discard pile for the mercenary. It acts just like a player's discard pile, but for the merc.

draw_deck = [   CARDS[4], CARDS[4], CARDS[4],
                CARDS[5], CARDS[5], CARDS[6],
                CARDS[6], CARDS[1], CARDS[1],
                CARDS[0] ]

discard = [ ]

hand = [ ]

cards_in_play = []

cards_in_play_MERC = []

contracts_deck = [ CONTRACTS[0], CONTRACTS[1], CONTRACTS[2], CONTRACTS[3], CONTRACTS[4], CONTRACTS[5], CONTRACTS[6], CONTRACTS[7], CONTRACTS[8],
                   CONTRACTS[9], CONTRACTS[10], CONTRACTS[11], CONTRACTS[12], CONTRACTS[13], CONTRACTS[14], CONTRACTS[15], CONTRACTS[16], CONTRACTS[17],
                   CONTRACTS[18], CONTRACTS[19], CONTRACTS[20], CONTRACTS[21], CONTRACTS[22], CONTRACTS[23], CONTRACTS[24], CONTRACTS[25], CONTRACTS[26],
                   CONTRACTS[27], CONTRACTS[28], CONTRACTS[29], CONTRACTS[30], CONTRACTS[31], CONTRACTS[32], CONTRACTS[33], CONTRACTS[34], CONTRACTS[35],
                   CONTRACTS[36], CONTRACTS[37], CONTRACTS[38], CONTRACTS[39], CONTRACTS[40], CONTRACTS[41], CONTRACTS[42], CONTRACTS[43], CONTRACTS[44],
                   CONTRACTS[45], CONTRACTS[46], CONTRACTS[47], CONTRACTS[48], CONTRACTS[49]   ]
 
contracts_selection = []

contracts_discard = []

mission = [ ]

objectives_deck = [ OBJECTIVES[0] , OBJECTIVES[1], OBJECTIVES[2], OBJECTIVES[3], OBJECTIVES[4], OBJECTIVES[5] , OBJECTIVES[6], OBJECTIVES[7],
                    OBJECTIVES[8] , OBJECTIVES[9], OBJECTIVES[10], OBJECTIVES[11], OBJECTIVES[12], OBJECTIVES[13] , OBJECTIVES[14], OBJECTIVES[15],
                    OBJECTIVES[16] , OBJECTIVES[17], OBJECTIVES[18], OBJECTIVES[19], OBJECTIVES[20], OBJECTIVES[21] , OBJECTIVES[22]    ]

objectives_selection = [ ]

objectives = [] 

crew_deck = [ CARDS[7] , CARDS[8] , CARDS[9] , CARDS[10] , CARDS[11] , CARDS[12] , CARDS[13] , CARDS[14] , CARDS[15] , CARDS[16] , CARDS[17] , CARDS[18],
              CARDS[19] , CARDS[20] , CARDS[21] , CARDS[22] , CARDS[23] , CARDS[24] , CARDS[25] , CARDS[26] , CARDS[27] , CARDS[28] , CARDS[29] , CARDS[30],
                CARDS[31] , CARDS[32] , CARDS[33] , CARDS[34], CARDS[35] , CARDS[36] ]  

crew_selection = [ ] 

ship_parts_deck = [ SHIP_PARTS[0] , SHIP_PARTS[1] , SHIP_PARTS[2] , SHIP_PARTS[3], SHIP_PARTS[4], SHIP_PARTS[5], SHIP_PARTS[6],
                    SHIP_PARTS[7] , SHIP_PARTS[8] , SHIP_PARTS[9] , SHIP_PARTS[10], SHIP_PARTS[11], SHIP_PARTS[12], SHIP_PARTS[13],
                    SHIP_PARTS[14] , SHIP_PARTS[15] , SHIP_PARTS[16] , SHIP_PARTS[17], SHIP_PARTS[18], SHIP_PARTS[19], SHIP_PARTS[20],
                    SHIP_PARTS[21] , SHIP_PARTS[22] , SHIP_PARTS[23] , SHIP_PARTS[24], SHIP_PARTS[25], SHIP_PARTS[26], SHIP_PARTS[27],
                    SHIP_PARTS[28] , SHIP_PARTS[29] , SHIP_PARTS[30] , SHIP_PARTS[31], SHIP_PARTS[32], SHIP_PARTS[33], SHIP_PARTS[34],
                    SHIP_PARTS[35] , SHIP_PARTS[36] , SHIP_PARTS[37] , SHIP_PARTS[38], SHIP_PARTS[39], SHIP_PARTS[40], SHIP_PARTS[41],
                    SHIP_PARTS[42] , SHIP_PARTS[43] , SHIP_PARTS[44] , SHIP_PARTS[45], SHIP_PARTS[46]           ]

ship_parts_selection = [ ]

ship_parts = [ ] 

shipLimitedUses = [ 0, 0, 0, 0 ]

mercenary_deck = [ ]

mercenary_hand = [ ]

mercenary_discard = [ ]
            

###########################
## GAME PHASES AND STEPS ##
###########################

def phase_1():          # I need to include code under selecting "Base" prompting the user to return a contract or not.
    global COINS, PHASE, TURN, STAYED_AT_BASE, SP1, SP2, SP3, SP4, HAZARDS_BLOCKED, VICTORY
    HAZARDS_BLOCKED = 0      # Reset Flare Shard and Siphon
    for x in range(0,4): # Ship Part usage counter resets 
        shipLimitedUses[x] = 0
    PHASE = 1
    phase = True
    STAYED_AT_BASE = False
    returnedCard = False
    ship_parts_code("Flash", 0, 0) # If you own the Flash, increase Hand size to 6.
    
    print("\n===== Turn:" , TURN, " |  Phase: 1 -- Contract ===== " , "\n" )
    if len(hand) != HAND_LIMIT:
        drawCards(draw_deck, HAND_LIMIT, hand)           
    drawCards(mercenary_deck, 5, mercenary_hand)
    print("    You have $" + str(COINS) + " credits.")
    print("    You have " + str(PRESTIGE) + " prestige.")
    print("\n XXXX  The mercenary's hand is:  XXXX")
    printm(mercenary_hand)          
    print("\n    Your incomplete objectives are: ")
    printm(objectives)
    print("\n    Installed ship parts: ")
    printm(ship_parts)
    print("\n    Your hand is: ")
    printm(hand)
    print("\n    Available contracts: ")
    printm(contracts_selection)          
    print("\n\n INCOMING TRANSMISSION...\n" ,
          "Greetings, commander. Shall you select a contract to complete, or defend the base? ")
    while phase == True:
        choice = input("ENTER: [C]ontract, [B]ase, [R]eturn, [I]nspect \n")
        
        if "Base" in choice or "B" in choice or "b" in choice:
            ship_parts_code("DOOM", 0, 0)
            COINS += 1        # +1$ Credit for guarding the base
            print( "\n  You've received $1 for guarding the base. Total is now: $" + str(COINS) + " credits" )
            drawCards(objectives_deck, 2, objectives_selection)
            print("\n  Whilst defending the base, you come across a few ideas...")
            print("DRAW 2 NEW OBJECTIVES")
            printm(objectives_selection)
            flag = True
            while flag:                 # Draw 2 objectives. Keep 1. 
                obj = input("\nENTER: [1] OR [2] TO KEEP. DISCARD THE OTHER.\n")
                if obj == "1":
                    objectives.append( objectives_selection[0] )
                    objectives_deck.insert( len(objectives_deck), objectives_selection[1] )
                    print("\n  The first choice was obvious, you think to yourself. You have no regrets.\n" ,
                          " Your current objectives:")
                    printm(objectives)
                    del objectives_selection[1] 
                    del objectives_selection[0]
                    flag = False
                elif obj == "2":
                    objectives.append( objectives_selection[1] )
                    objectives_deck.insert( len(objectives_deck), objectives_selection[0] )
                    print("\n  After some deliberation, you changed your mind. The second choice is superior. \n" ,
                          " Your current objectives:")
                    printm(objectives)
                    del objectives_selection[1]
                    del objectives_selection[0]
                    flag = False
                elif obj == "Inspect" or obj == "I" or obj == "i":
                    inspect(objectives_selection)
                    
            if returnedCard == False: # Can return max 1 card per turn
                cycle = input("\nDo you want to return a contract to the bottom of the deck? \nENTER:[Y] / [N] \n")
                if cycle == "Y" or cycle == "y" or cycle == "Yes":
                    
                    inspecting = True
                    while inspecting == True:   
                        printm(contracts_selection)
                        entry = input("\nENTER: CARD NUMBER TO RETURN, OR [B]ack ' \n")
                        if "Back" in entry or "B" in entry or "b" in entry:
                            inspecting = False
                            break
                        elif entry.isdigit() and ( int(entry) >= 1 and int(entry) <= 8 ):
                            entry = int(entry) - 1
                            print_contract( contracts_selection[entry] )
                            cycle = input("\nDo you want to return this contract to the bottom of the deck? \nENTER:[Y] / [N] \n")
                            if cycle == "Y" or cycle == "y" or cycle == "Yes":
                                contracts_deck.insert( len(contracts_deck), contracts_selection[entry] )
                                print("Return complete. Contract {" , contracts_selection[entry][0] , "} has been returned. \n\n")
                                del contracts_selection[entry]
                                drawCards(contracts_deck, 1, contracts_selection)
                                inspecting = False
                                returnedCard = True
                                
                            elif cycle == "N" or cycle == "n":
                                pass
                            else:
                                print("INPUT ERROR DETECTED. GOING BACK")
                
            
            print("\n\n  You power down your ship upon finishing your shift." ,
                  "\nHAND IS DISCARDED")
            discardf()
            drawCards(draw_deck, HAND_LIMIT, hand)
            print("SKIPPING TO PHASE 3...")
            phase = False           # Break the phase 1 loop
            STAYED_AT_BASE = True  # This boolean value is necessary to skip phase 2
            
        elif "Return" in choice or "R" in choice or "r" in choice:      # Player may return 1 card from armory to the bottom of their deck
            if returnedCard == True: # Can return max 1 card per turn
                print("\nSorry, you can only return 1 card per turn. Backing...")
            else:   
                inspecting = True   # Identical code to the Base's return command (except for paying 1$ for it)
                while inspecting == True:       
                    printm(contracts_selection)
                    entry = input("\nENTER: CARD NUMBER TO RETURN, OR [B]ack ' \n")
                    if "Back" in entry or "B" in entry or "b" in entry:
                        inspecting = False
                        break
                    elif entry.isdigit() and ( int(entry) >= 1 and int(entry) <= 8 ):
                        entry = int(entry) - 1
                        print_contract( contracts_selection[entry] )
                        cycle = input("\nDo you want to return this contract to the bottom of the deck? \nENTER:[Y] / [N] \n")
                        if cycle == "Y" or cycle == "y" or cycle == "Yes":
                            contracts_deck.insert( len(contracts_deck), contracts_selection[entry] )
                            print("Return complete. Contract {" , contracts_selection[entry][0] , "} has been returned. \n\n")
                            del contracts_selection[entry]
                            drawCards(contracts_deck, 1, contracts_selection)
                            inspecting = False
                            COINS -= 1
                            returnedCard = True
                            printm(contracts_selection)
                            
                        elif cycle == "N" or cycle == "n":
                            pass
                        else:
                            print("INPUT ERROR DETECTED. GOING BACK")
            
            
            
            
        elif "Contract" in choice or "C" in choice or "c" in choice:
            print("\n A most cunning plan, sir. Which contract are you interested in?")
            planning = True
            while planning == True:
                print("")
                selection = True
                while selection == True:
                    print("    Your hand is: ")
                    printm(hand)
                    print("--------------------------------------------------------------------------")
                    printm(contracts_selection)
                    decision = input("\nENTER: THE NUMBER OF THE CONTRACT TO SELECT, OR [B]ack \n")
                    if "Back" in decision or "B" in decision or "b" in decision:
                            selection = False
                            planning = False
                            
                    elif decision.isdigit():
                        if int(decision) >= 1 and int(decision) < 9:    #If you don't have 8 contracts, it'll try pulling something out of range - makes error. Remove comment when contracts dictionary is complete.
                            print_contract( contracts_selection[int(decision) - 1] )
                            confirmation = input("ENTER COMMAND: [C]onfirm, [B]ack \n")
                            if confirmation == "Confirm" or confirmation == "C" or confirmation == "c":
                                mission.append( contracts_selection[ ( int(decision) - 1) ] )  
                                del contracts_selection[ ( int(decision) - 1) ]
                                print("\nCONTRACT {" , mission[0][0] , "} INITIATED. STANDBY FOR PHASE 2...")
                                selection = False   # Go directly to phase 2 by breaking all loops
                                planning = False
                                phase = False
                            elif confirmation == "Back" or confirmation == "B" or confirmation == "b":
                                pass
                            else:
                                print("TYPO DETECTED. PLEASE REENTER INFORMATION.")
                            
                    else: 
                        print("INPUT INVALID. PLEASE REENTER NUMBER.")
                    
        elif "Inspect" in choice or "I" in choice or "i" in choice:
            print(" Contract - Choose a contract from the selection to attempt. You may invite allies to aid you. \n"
                  " Base - Earn 1$ credit. Draw 2 objectives, keep 1. Discard your hand and skip directly to phase 3.\n"
                  " You may choose to return a contract to the bottom of the Contracts deck for free if you stay at base.")
        elif choice != "Base" or choice != "Contract" or choice != "Inspect":
            print("I'm sorry sir, could you repeat?")     
                    


def phase_2():
    global PRESTIGE, COINS, HAZARDS, diceHAZARDS, ACTIONS, R, T, D, S, C, tinkerObjTurn, die
    global PHASE, TURN, DEBT, PRESTIGE_DEBT, nMercCards, MISSION_COMPLETE
    PHASE = 2
    
    print("\n===== Turn:" , TURN, " |  Phase: 2 -- Execution ===== " , "\n" )
    print_contract( mission[0] )
    R, T, D, S, C = 0, 0, 0, 0, 0
    HAZARDS = 0
    DEBT = 0
    PRESTIGE_DEBT = 0
    nMercCards = 0
    ship_parts_code("startContract", 0, 0)
    print("\n")

    
# Phase 2 begins with rolling the indicated number of Hazard Dice.
    dieNumber = 1 # Tracks the dice being thrown
    die = [] # Remembers all dice results
    for dice in range( mission[0][2] ):
        time.sleep(1)
        
        dice = random.randint(1, 6)
        if dice == 1 or dice == 2:      # 2 Hazards on the dice
            die.append(2)
            print("Dice #" + str(dieNumber) + " - Extreme danger! - 2 Hazard")
        elif dice == 3 or dice == 4:    # 1 Hazard on the die
            die.append(1)
            print("Dice #" + str(dieNumber) + " - Risk detected - 1 Hazard")
        elif dice == 5 or dice == 6:     # 0 Hazard on the die
            die.append(0)
            print("Dice #" + str(dieNumber) + " - Smooth like butter - 0 Hazard")
        dieNumber += 1
        
    diceHAZARDS = sum(die)
    ship_parts_code("Projector S2", 0, 0)
    #print( "The total amount of hazards you are about to suffer == " , str(diceHAZARDS) , "\n" )
    time.sleep(1)


    progress = True
    while progress == True: # Player plays cards until they stop (''End'').
        print(" -------- INCOMING HAZARDS:" , (diceHAZARDS + HAZARDS), "--------\n" ) # Positive because HAZARDS is negative
        print(" ----------XX MERCENARY Cards played:" , len(cards_in_play_MERC) , "XX-------" )
        printm(cards_in_play_MERC)
        print("\n ------XX MERCENARY HAND: XX------")
        printm(mercenary_hand)
        print(" ------XX CREDIT DEBT:", DEBT, "| PRESTIGE OWED:", PRESTIGE_DEBT, "XX------")
        print("\n ---------- Ship Parts ---------")
        printm(ship_parts)
        print(" ------------ Player's Cards played:" , len(cards_in_play) , "--------- " )
        printm(cards_in_play)
        print("\n -------- Actions remaining:" , ACTIONS , "--------" )
        printm(hand)
        Card = input("\nENTER: NUMBER OF CARD TO PLAY, OR [M]ercenary, [P]art, [E]nd, [I]nspect ' \n")
        if "Inspect" in Card or "I" in Card or "i" in Card:
            inspect(hand)

        elif "Mercenary" in Card or "M" in Card or "m" in Card:
            merc_card = input("\nENTER: NUMBER OF CARD TO PLAY, OR [B]ack, [I]nspect \n")
            if merc_card.isdigit() and ( int(merc_card) >= 1 and int(merc_card) <= len(mercenary_hand) ):
                card_code( mercenary_hand[int(merc_card) - 1] , True , False)
                printRequirements()
                cards_in_play_MERC.append( mercenary_hand[int(merc_card) - 1] )
                if ( mercenary_hand[int(merc_card) - 1][-1] ) > 6:
                    PRESTIGE_DEBT += 1
                else:
                    DEBT = 1 + nMercCards + DEBT
                    nMercCards = 1 + nMercCards 
                del mercenary_hand[int(merc_card) - 1]

            elif "Inspect" in merc_card or "I" in merc_card or "i" in merc_card:
                inspect(mercenary_hand)
            
            elif "Back" in merc_card or "B" in merc_card or "b" in merc_card:
                pass
            
        elif "Part" in Card or "P" in Card or "p" in Card:
            printm(ship_parts)
            activate = input("ENTER: NUMBER OF SHIP PART TO PLAY \n")
            ship_part_index = int(activate) - 1
            if activate.isdigit():
                ship_parts_code("manual", ship_part_index, 0)
                printRequirements()
            else:
                print("INPUT ERROR DETECTED. GOING BACK...")

        elif "End" in Card or "E" in Card or "e" in Card:
            progress = False

        elif Card.isdigit() and ( int(Card) >= 1 and int(Card) <= len(hand) ):
            if ACTIONS > 0:
                rememberCardName = hand[ ( int(Card) - 1) ][0]
                card_code( hand[ ( int(Card) - 1) ] , False, False)
                if "Zardon the Enforcer" in rememberCardName: # If you chose Zardon, execute this SUPER SPECIFIC code   #
                    zardonIndex = 1                                                                                     #
                    for card in hand:                                                                                   #                                                                                #
                        if "Zardon the Enforcer" in card[0]:                                                            #
                            Card = zardonIndex                                                                          #
                        zardonIndex += 1                                                                                #
                    
                cards_in_play.append( hand[ ( int(Card) - 1) ] )
                ship_parts_code("playCardBasis", 0, hand[(int(Card)-1)] )
                printRequirements()
                del hand[ ( int(Card) - 1) ]
                ACTIONS -= 1
                
            else:
                print("NO ACTIONS REMAINING\n")

        else:
            print("\nINPUT ERROR DETECTED. RETRY.")

# Post contract debrief. Program checks if player fulfilled requirements. Distributes rewards, resets variables, etc.
    print("\n Concluding mission...")
    if (R >= mission[0][3][0]) and (T >= mission[0][3][1]) and (D >= mission[0][3][2]) and (S >= mission[0][3][3]) and (C >= mission[0][3][4]):
        MISSION_COMPLETE = True
        print("  Contract completed! Your patrons are impressed, and will now disburse the negotiated rewards.\n")
        
        if PRESTIGE_DEBT > 0:   # If you needed the mercenary's help, pay your fair share in Prestige
            if PRESTIGE_DEBT > mission[0][1][0]:
                PRESTIGE_DEBT = mission[0][1][0]
            print("The mercenary's loyal crew diverted" , PRESTIGE_DEBT , "prestige away from your public image!")
            earnedPRESTIGE = mission[0][1][0] - PRESTIGE_DEBT
            PRESTIGE += earnedPRESTIGE
            print( "+" + str(earnedPRESTIGE) , "Prestige" )
        else:                   # Otherwise, the profit is solely yours.
            PRESTIGE += mission[0][1][0]
            print( "+" + str(mission[0][1][0]) , "Prestige" )
            

        if DEBT > 0:            # Same thing as above, but for Credits
            if DEBT > mission[0][1][1]:
                DEBT = mission[0][1][1]
            print("The mercenary expects $" + str(DEBT), "for his efforts in helping you succeed.")
            earnedCOINS = mission[0][1][1] - DEBT
            COINS += earnedCOINS
            print( "+" + str(earnedCOINS) , "Credits" )
        else:
            COINS += mission[0][1][1]
            print( "+" + str(mission[0][1][1]) , "Credits" )
           
        
        
        bonuses = mission[0][1][2]
        if bonuses > 0:
            print("+" + str(mission[0][1][2]) , "Bonuses" )
        while bonuses > 0:      # If the reward included bonus cards, earn them.
            bonus_selection = input("ENTER: [C]rew, OR [P]art FOR A FREE BONUS.\n")
            if "Crew" in bonus_selection or "C" in bonus_selection or "c" in bonus_selection:
                drawCards(crew_deck, 1, discard)
                print("You have hired" , discard[0][0] + "!")
            elif "Part" in bonus_selection or "P" in bonus_selection or "p" in bonus_selection:
                if len(ship_parts) == 4: # Maximum ship parts allowed is 4. Replace a part to proceed.
                    print("WARNING: MAXIMUM CAPACITY OF 4 SHIP PARTS REACHED.")
                    printm(ship_parts)
                    validation = True
                    while validation == True:
                        replace = input("ENTER: NUMBER OF PART YOU WISH TO REPLACE:\n") 
                        if int(replace) >= 1 and int(replace) <= 4:
                            ship_parts.insert( (int(replace) - 1) , ship_parts_deck[0] )
                            print("Modification successful." , ship_parts[(int(replace) - 1)][0] , "has replaced " + ship_parts[int(replace)][0] + ".\n\n")
                            del ship_parts[ int(replace) ]
                            validation = False
                            tinkerObjTurn = TURN # Special code for the Tinker Objective to activate
                        else:
                            print("NUMBER INPUT INVALID. RETRY.")
                else:
                    drawCards(ship_parts_deck, 1, ship_parts)
                    print("You have installed" , ship_parts[0][0] + "!")
            bonuses -= 1
            
    else:
        print("  Attempt failed... You'll succeed next time.")
        

    # Before resolving hazard hits, resolve Baz's ability
    if BAZ == True and MISSION_COMPLETE == True:
        card_code(CARDS[6] , False, True)
        card_code(CARDS[6] , False, True)
        print("Baz: 'KABOOOOOM!' ")

    # Take an opportunity to score objectives
    objectives_code()

    
    HAZARDS = sum(die) + HAZARDS # HAZARDS is a negative number accumulated by shields and various things.      
    for x in range(HAZARDS): #This for loop guarantees that the player will not get negative Prestige.    
        if PRESTIGE <= 0:
            pass
        else:
            PRESTIGE -= 1
    if HAZARDS > 0:
        print("Your reputation is harmed due to", HAZARDS , "Hazards!")

    ship_parts_code("Flare Shard", 0, 0)
        
    ACTIONS = 1
    HAZARDS = 0


def phase_3():
    global R, T, D, S, C, PHASE, TURN, VICTORY, COINS
    returnedCard = False
    PHASE = 3
        
    print("\n===== Turn:" , TURN, " |  Phase: 3 -- Buying ===== " , "\n" )
    print("  Your Credits: $" + str(COINS) )
    print("  Your Prestige:" , PRESTIGE )
    print("\n ---------- Ship Parts: ----------")
    printm(ship_parts_selection)
    print("\n ---------- Crewmembers: ---------")
    printm(crew_selection)
    buying = True
    while buying == True:
        print("\n  You may browse and purchase any number of crew or ship parts. " )
        choice = input("ENTER: [C]rew, [P]arts, [R]eturn, [S]kip  \n")
        inspecting = True   
        if "Crew" in choice or "C" in choice or "c" in choice:                
            while inspecting == True:       # Code below is a manual, modified version of the inspect function.
                print("  Your Credits: $" + str(COINS) )
                printm(crew_selection)
                entry = input("\nENTER: CARD NUMBER TO INSPECT, OR [B]ack  \n")
                if "Back" in entry or "B" in entry or "b" in entry:
                    inspecting = False
                    break
                elif entry.isdigit() and ( int(entry) >= 1 and int(entry) <= 3 ):
                    entry = int(entry) - 1
                    print( " ID:" , crew_selection[entry][0] , "| Title:" , crew_selection[entry][-3], "| Class:" , crew_selection[entry][-2] , "\n" ,
                           "Ability:" , crew_selection[entry][1] , "\n" ,
                           "Price: $" + str( crew_selection[entry][2] )    )
                # IDEA - What if every crewmember had a unique dialogue for the print function below? A cheesy liner that gives them more personality.
                    cycle = input("\nDo you wish to hire this specialist, sir? \nENTER:[Y], [N] \n")
                    if cycle == "Y" or cycle == "y":        #
                        purchase( crew_selection[entry] , "crew", entry )     # Original - but bugged
                        
                    elif cycle == "N" or cycle == "n":
                        pass
                    else:
                        print("INPUT ERROR DETECTED. GOING BACK")
            
        elif "Parts" in choice or "P" in choice or "p" in choice:             
            while inspecting == True:
                print("  Your Credits: $" + str(COINS) )
                printm(ship_parts_selection)
                entry = input("\nENTER: CARD NUMBER TO INSPECT, OR [B]ack \n")
                if "Back" in entry or "B" in entry or "b" in entry:
                    inspecting = False
                    break
                elif entry.isdigit() and ( int(entry) >= 1 and int(entry) <= 6 ):
                    entry = int(entry) - 1
                    print( " ID:" , ship_parts_selection[entry][0] , "| Brand:" , ship_parts_selection[entry][-2] , "\n" ,
                           "Ability:" , ship_parts_selection[entry][1] , "\n" ,
                           "Additional parts:" , ship_parts_selection[entry][3], "\n" , 
                           "Price: $" + str( ship_parts_selection[entry][2] )    )
                    cycle = input("\nDo you wish to purchase this module, sir? \nENTER [Y], [N] \n")
                    if cycle == "Y" or cycle == "y":          
                        purchase( ship_parts_selection[entry] , "ship_parts" , entry )
                        
                    elif cycle == "N" or cycle == "n":
                        pass
                    else:
                        print("INPUT ERROR DETECTED. GOING BACK")

        elif "Return" in choice or "R" in choice or "r" in choice:      # Play may return 1 card from armory to the bottom of their deck
            if returnedCard == True: # Can return max 1 card per turn
                print("\nSorry, you can only return 1 card per turn. Backing...")
            else:   
                
                print("\nWould you like to return a crewmember or a ship part from the armory back to their deck?")
                returnChoice = input("ENTER: [C]rewmember, [S]hip Part, or [B]ack\n")
                while ( returnChoice != "Crewmember" and returnChoice != "C" and returnChoice != "c" and
                        returnChoice != "Ship Part" and returnChoice != "S" and returnChoice != "s" and
                        returnChoice != "Back" and returnChoice != "B" and returnChoice != "b"):
                    returnChoice = input("ERROR. RE-ENTER CHOICE:\n")

                if "Crewmember" in returnChoice or "C" in returnChoice or "c" in returnChoice:
                    inspecting = True
                    while inspecting == True:       # Code below is a manual, modified version of the inspect function.
                        printm(crew_selection)
                        entry = input("\nENTER: CARD NUMBER TO INSPECT, OR [B]ack ' \n")
                        if "Back" in entry or "B" in entry or "b" in entry:
                            inspecting = False
                            break
                        elif entry.isdigit() and ( int(entry) >= 1 and int(entry) <= 3 ):
                            entry = int(entry) - 1
                            print( " ID:" , crew_selection[entry][0] , "| Title:" , crew_selection[entry][-3], "| Class:" , crew_selection[entry][-2] , "\n" ,
                                   "Ability:" , crew_selection[entry][1] , "\n" ,
                                   "Price: $" + str( crew_selection[entry][2] )    )
                            cycle = input("\nDo you want to return this member to the bottom of the deck? \nENTER:[Y], [N] \n")
                            if cycle == "Y" or cycle == "y":
                                crew_deck.insert( len(crew_deck), crew_selection[entry] )
                                print("Return complete." , crew_selection[entry][0] , "has been returned. \n\n")
                                del crew_selection[entry]
                                drawCards(crew_deck, 1, crew_selection)
                                inspecting = False
                                COINS -= 1
                                returnedCard = True
                                
                            elif cycle == "N" or cycle == "n":
                                pass
                            else:
                                print("INPUT ERROR DETECTED. GOING BACK")
                    
                elif "Ship Part" in returnChoice or "S" in returnChoice or "s" in returnChoice:
                    inspecting = True
                    while inspecting == True:
                        print("  Your Credits: $" + str(COINS) )
                        printm(ship_parts_selection)
                        entry = input("\nENTER: CARD NUMBER TO INSPECT, OR [B]ack \n")
                        if "Back" in entry or "B" in entry or "b" in entry:
                            inspecting = False
                            break
                        elif entry.isdigit() and ( int(entry) >= 1 and int(entry) <= 6 ):
                            entry = int(entry) - 1
                            print( " ID:" , ship_parts_selection[entry][0] , "| Brand:" , ship_parts_selection[entry][-2] , "\n" ,
                                   "Ability:" , ship_parts_selection[entry][1] , "\n" ,
                                   "Additional parts:" , ship_parts_selection[entry][3], "\n" , 
                                   "Price: $" + str( ship_parts_selection[entry][2] )    )
                            cycle = input("\nDo you want to return this part to the bottom of the deck? \nENTER:[Y], [N] \n")
                            if cycle == "Y" or cycle == "y":          
                                ship_parts_deck.insert( len(ship_parts_deck), ship_parts_selection[entry] )
                                print("Return complete." , ship_parts_selection[entry][0] , "has been returned. \n\n")
                                del ship_parts_selection[entry]
                                drawCards(ship_parts_deck, 1, ship_parts_selection)
                                inspecting = False
                                COINS -= 1
                                returnedCard = True
                                
                            elif cycle == "N" or cycle == "n":
                                pass
                            else:
                                print("INPUT ERROR DETECTED. GOING BACK")
        
        elif "Skip" in choice or "S" in choice or "s" in choice:
              buying = False
        else:
              print("INPUT ERROR DETECTED. RETRY.")
    

    # Opportunity to score objectives       
    objectives_code()

    R, T, D, S, C = 0, 0, 0, 0, 0
    DEBT = 0
    PRESTIGE_DEBT = 0
    nMercCards = 0
    MISSION_COMPLETE = False
    KARY_POWALK = False
    BAZ = False
    discardf()
    discardM()
    if len(mission) > 0:
        drawCards(mission, 1, contracts_discard)
    if len(contracts_selection) < 8:
        drawCards(contracts_deck, 1, contracts_selection)
    x = input(" Phase 3 is about to conclude. Enter any key to begin the next turn.\n")
    TURN += 1
    ### PHASE CLEANUP COMPLETE. LOOP BACK TO PHASE 1 ###



##############  Let's get playing! Begin with setup, and create loops for the player to interact and play the game. 
## GAMEPLAY ##
##############
    
print(" Welcome to Moonrakers, commander. I am your adjutant A.I., and I will be accompanying you on your missions. \n" ,
      "Remember, if the program prompts you to enter an input, you can always type 'Inspect' to gain clarification.")
ready = input("ENTER ANY LETTER TO BEGIN PLAY. \n")
print("Would you like to play with 4-Hazard contracts? {NOT RECOMMENDED IF YOU ARE A BEGINNER}")
difficulty = input("ENTER: [Y] / [N]\n") # If yes, keep all 4 hazard contracts. If no, remove all contracts with 4 hazards.
while ( difficulty != "Y" and difficulty != "y" and
        difficulty != "N" and difficulty != "n"):
    difficulty = input("ERROR. INPUT INVALID. PLEASE RETRY.\n")

if "Y" in difficulty or "Yes" in difficulty or "y" in difficulty:
    for X in range( len(contracts_deck) , 0, -1):
        X -= 1                                  # This line is necessary - Python needs to count indexes from 1 less
        if contracts_deck[X][2] >= 4:
            del contracts_deck[X]
                        
random.shuffle(draw_deck)
random.shuffle(contracts_deck)
random.shuffle(objectives_deck)
random.shuffle(ship_parts_deck)
random.shuffle(crew_deck)
  
for X in range(8): 
    drawCards(contracts_deck, 1, contracts_selection)
    while contracts_selection[X][2] > 2: # Only for setup, return any 3 or 4 hazard contracts drawn back to the deck.
        contracts_deck.insert( len(contracts_deck) , X )
        del contracts_selection[X]
        drawCards(contracts_deck, 1, contracts_selection)
random.shuffle(contracts_deck) # The cards returned to the deck are shuffled.
        
drawCards(crew_deck, 3, crew_selection)                 
drawCards(ship_parts_deck, 6, ship_parts_selection)     

# Prepare the merc deck for single player / two players.
mercenary_deck = [ CARDS[1] , CARDS[1] , CARDS[2] , CARDS[4] , CARDS[4] , CARDS[4] , CARDS[5] ,
                   CARDS[5] , CARDS[5] , CARDS[6] , CARDS[6] , CARDS[6] ]
drawCards(crew_deck, 3, mercenary_deck)  
random.shuffle(mercenary_deck) # Generate the deck with basic cards and 3 from the crew deck.


setup_objectives()

# Game loops through the 3 phases until the game ends
while VICTORY == False:
    phase_1()
    if STAYED_AT_BASE == False:
        phase_2()
    phase_3()
    if TURN >= 11:
        VICTORY = True
        print("\n\n\n -------- TIME HAS RUN OUT, TURN 10 HAS ENDED. THE GAME IS OVER. -------- ")

        
print("Various Moonraker captains have gathered to judge your leadership.")
prestigeScore = 10 * PRESTIGE   # Each Prestige gets you 10 points
unspentCredits = COINS        # Each unspent credit goes to your net worth
for part in ship_parts:         # Count total value of all installed ship parts
    partScore += part[2]

drawCards(draw_deck, len(draw_deck), discard)    # All action and crew cards will be put into the discard pile
for crew in discard:            #   Count total value of all bought crewmembers
    crewScore = crewScore + crew[2]

netWorth = prestigeScore + unspentCredits + partScore + crewScore
rank = "None"

print("\n    <100 | Beginner \n 100-150 | Novice \n 150-200 | Advanced \n 200-250 | Mastery \n    >250 | Chosen one \n")
if netWorth > 250:
    rank = "Chosen one"
elif netWorth >= 200:
    rank = "Mastery"
elif netWorth >= 150:
    rank = "Advanced"
elif netWorth >= 100:
    rank = "Novice"
else:
    rank = "Beginner"

print("Unspent credits | Installed Ship Parts | Hired Crew | Prestige")
print("      ",unspentCredits,"       |         ",partScore,"          |     ",crewScore,"    |   ",prestigeScore)
print("\nYour total score:", netWorth, "| Your rank:" , rank)

print("\n\n\n\n\n#### Congratulations! You are recognized as the new leader of the Moonrakers. ####")
print("/////         \\\\\\\\\ \n""||||| VICTORY! |||||")
print("\\\\\\\\\          /////")
print("\n\n Thank you for playing. The game is now over, and you may quit.")
        
    
