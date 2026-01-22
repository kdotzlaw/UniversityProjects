#NAME: Katrina Dotzlaw
#COURSE: COMP 2150 A02 Domaratzki
#CLASS: Player - subclass of PlayerAbs, and it controls the computer players
class Player < PlayerAbs
  def initialize()
    super()
    @unknownCards = Array.new() #this will store all the cards that the computer can make guesses about
    @temp = Array.new() 
    @guessCall = false 
  end
  
  #Precondition: unknown if this player can answer the given guess
  #@param i: index of player guessing g
  #@param g: guess that this player might be able to answer
  #Postcondition: return nil if this player has none of the cards, or one of the cards in the guess if it has one
  def canAnswer(i, g)
    #if the computer has any of the cards in the guess in their hand, return a random one
    compCards = self.playerCards()
    howManyCards = Array.new()
    p = g.person()
    loc = g.place()
    we = g.weapon()
    compCards.size.times{|i|
      if compCards[i].to_s==p.to_s
        howManyCards<<p
    else if compCards[i].to_s==loc.to_s
      howManyCards<<loc
  else if compCards[i].to_s==we.to_s
      howManyCards<<we
end
end
end
#end of all ifs
} #end of loop
#now check how many cards of the guess this player has.
#if empty, return nil. If 1, return that one. Else, pick a random card and return it
if howManyCards.size==0
  return nil
else if howManyCards.size==1
  return howManyCards[0]
else if howManyCards.size>1
  r = rand(howManyCards.size)
  return howManyCards[r]
end
end
end
#end of ifs   
  end # end of canAnswer function
  
  #Precondition: no guesses have been made
  #Postcondition: a suggestion Guess is returned if this player has >3 cards in the unknownCards array. 
                # an accusation Guess is returned if this player has 3 cards in the unknownCards array
  def getGuess() 
    #on the first guess, add all cards available to be guessed to an array unknownCards
        if @guessCall==false
        @suspects.size.times{|i|@temp[i]=@suspects[i]}
        @unknownCards = (@temp<<@location).flatten!
        @unkownCards = (@unknownCards<<@weapon).flatten!
        #make sure to remove the cards we have in our hand
        playerCard = self.playerCards()
        playerCard.size.times{|i|
          @unknownCards.size.times{|j|
            if @unknownCards[j]==playerCard[i]
              @unknownCards.delete(playerCard[i])
              end
              }
              }
              end #end of if guessCall = false
              @guessCall = true #true because we dont need to remake the unknownCards array everytime we guess, just initially
    if @unknownCards.size==3
      p = nil
      loc = nil
      w = nil
     @unknownCards.size.times{|i|
       if @unknownCards[i].type==:person
         p = @unknownCards[i]
    else if @unknownCards[i].type==:place
      loc = @unknownCards[i]
      else if @unknownCards[i].type==:weapon
        w = @unknownCards[i]
        end
        end
        end
        }
    return Guess.new(p,loc,w,true)
    else
      
    #seperate the types of cards that we know
      peopleUnknown = Array.new()
      placeUnknown = Array.new()
      thingUnknown = Array.new()
      @unknownCards.size.times{|i|
        if @unknownCards[i].type==:person
          peopleUnknown<<@unkownCards[i]
          else if @unknownCards[i].type==:place
            placeUnknown<<@unkownCards[i]
            else if @unknownCards[i].type==:weapon
            thingUnknown<<@unknownCards[i]
            end
          end
      end
      }
      #shuffle all the cards we dont know (otherwise its really easy for the interactive player to figure out WHODUNNIT?)
      peopleUnknown.shuffle!
      #pick a person
      index = 0
      i = 0
      p = peopleUnknown[index]
      while peopleUnknown[i]!=p do
       index+=1
        p = peopleUnknown[index]
        i+=1
        end
        #pick a place
        index = 0
        i = 0
        placeUnknown.shuffle!
        loc = placeUnknown[index]
        while placeUnknown[i]!=loc do
          index+=1
          loc = placeUnknown[index]
          i+=1
        end
        #pick a weapon
          index = 0
          i = 0
          thingUnknown.shuffle!
          w = thingUnknown[index]
          
          while w!=thingUnknown[i] do
            
            index+=1
            w = thingUnknown[index]
            i+=1
          end
          return Guess.new(p,loc,w,false)
    end
 end # end of getGuess
 
 #Precondition: no one has showed this player a card
 #@param i: player index of player showing this player a card
 #@param c: card being showed to this player
 #Postcondition: this player has received info about a card. If c!=nil, then remove the card from the unknownCards[] as it is now known
  def receiveInfo(i,c)
    #receives a playerindex i and a card c and removes the card from the unknownCard array
    if c!=nil && i!=-1
     @unknownCards.delete(c)
    end
  end # end of receive info
end # end of Player class