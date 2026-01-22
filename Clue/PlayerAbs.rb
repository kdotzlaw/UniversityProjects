#NAME: Katrina Dotzlaw
#STUDENT NUMBER: 7833061
#COURSE: COMP 2150 A02 Domaratzki
#CLASS: PlayerAbs - in charge of setting up players 
  #this is an abstract class

class PlayerAbs
 
  def initalize()
    @numPlayers = nil
    @currPlayer = nil
    @suspects = nil
    @location = nil
    @weapon = nil
   @canStillGuess = true # true as long as the player doesnt make an incorrect accusation 
  end
  def setup(nPlayers,i,people,loc,weap) # will be the same for all players
    @numPlayers = nPlayers
    @currPlayer = i
    @suspects = people #array - only contains people
    @location = loc #array
    @weapon = weap #array
   @playerCards = Array.new() #keep track of which cards the player has
   @canStillGuess = true
  end
 
  #getters 
  attr_reader :currPlayer #use by calling currPlayer
  attr_reader :playerCards #use by calling playerCards
  attr_reader :canStillGuess
  #setter
  def canStillGuess=(canStillGuess)
    @canStillGuess = canStillGuess
  end
  
  #Precondition: player hasnt received a card
  #@param c: card that player receives
  #Postcondition: player has now received a card, and it has been added to their hand
  def setCard(c) # indicates that the current player has received a card
   #add a card to the players hand'
    @playerCards<<(c)
  end # end of setCards
  
  #This is used to print the cards of the given player (mainly used in InteractivePlayer)
  def printCards(currPlayer)
 @playerCards.size.times{|i| 
   #if i==currPlayer
  puts("#{@playerCards[i].to_s}")
    #end 
  }
  end #end of print cards
  
  #Abstract methods that are implemented in subclasses
  def getGuess()
    #abstract method
    raise "Must make either a InteractivePlayer or a Player to use this"
  end
def receiveInfo(playerIndex, c)
  raise "Must make either a InteractivePlayer or a Player to use this"
  #this is a method implemented in subclasses, not here (abs)
end

#this is an abstract class
def PlayerAbs.new(*args)
  if self == PlayerAbs
        raise "this is an abstract class, cant create object"
      else
        super
  end 
  end #end of PlayerAbs
  
end #EOF