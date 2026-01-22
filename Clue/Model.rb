#NAME: Katrina Dotzlaw
#STUDENT NUMBER: 7833061
#COURSE: COMP 2150 A02 Domaratzki
#CLASS: Model - sets up players, sets up cards, deals cards, and runs the game

class Model
  #class variables to store answer
  @aPerson 
  @aPlace 
  @aWeapon 
  
  # initialize
  def initialize(people, loc, w)
    @person = people
    @place = loc
    @weapon = w
    @gameOver = false
    @winner = nil
    @cards = Array.new()
  end
  attr_reader :cards
  
  #Precondtion: none of the players have been setup
  #@param aPlayers: the array of players we want Model to setup
  #Postcondition: all players have been setup correctly
  def setPlayers(aPlayers)
    #@players = Array.new(aPlayers.size())
    @players = aPlayers
  @players.size.times{|i| @players[i].setup(@players.size-1,i,@person,@place,@weapon)}
  end #end of setPlayers
  
  #Precondition:WHODUNNIT? has not been chosen, cards have not been dealt
  #Postcondition: WHODUNNIT? has been chosen, cards have been dealt to all players
  def setupCards()
    #pick which cards are the answer randomly
    @aPerson = @person[rand(@person.size)]
    @aPlace = @place[rand(@place.size)]
    @aWeapon = @weapon[rand(@weapon.size)]
    #make a new array of all cards distributable to players (doesnt include answers!)
    #DONT REMOVE THE ANSWERS FROM THE ORIGINAL 3 LISTS - WE CAN STILL GUESS THEM
    temp =  Array.new()
    #make a temporary array to add to cards
    @person.size.times{|i|temp[i]=@person[i]}
    #add all the cards to the cards[]
    @cards = (temp<<@place).flatten!
    @cards = (@cards << @weapon).flatten!
    #cards now has all possible cards
    #remove the answer cards from cards[]
    @cards.delete(@aPerson)
    @cards.delete(@aPlace)
    @cards.delete(@aWeapon)
    #shuffle cards
    @cards.shuffle!
    #loop through cards and players and deal a card to each player until there are no more cards
    index = 0
    while (index!=@cards.size()) do
      @players.size().times {|i| 
      if index!=(@cards.size())
        @players[i].setCard(@cards[index])
        #InteractivePlayer's cards should print so that i can see them
        if @players[i].instance_of? InteractivePlayer
              puts("You received the card: #{@cards[index].to_s} ")
              end
                 index+=1
                 end #closes if
        }#end for loop
    end # ends while loop
  
    #put the answer cards back in after cards are dealt
    @cards<<@aPerson
    @cards<<@aPlace
    @cards<<@aWeapon
  end #end of setupCards
  #Precondition: the game is not over, and no one has one
  #Postcondition: game is over, one of the players has won the game.
  def play()
    #generate a random playerIndex to choose which player goes first
   activePlayer = rand(@players.size)
   #keep track of the current size (the game should end if someone guesses wrong and theres only 1 other actively guessing player)
   currSize = @players.size
   # puts("WHODUNNIT? #{@aPerson.to_s}, #{@aPlace.to_s}, #{@aWeapon.to_s}")
    while !@gameOver do
      #while the game is not over,
      #ask the active player for their guess
      if @players[activePlayer].instance_of? InteractivePlayer
        #since the computerPlayers only make an accusation when they are sure theyre correct,
        #only the InteractivePlayer can guess wrong
        if @players[activePlayer].canStillGuess==true
        g = @players[activePlayer].getGuess()
    else
      # if the interactive player is out of the game, they cant guess so move to the next player
      activePlayer = (activePlayer+1)%(@players.size)
    end #end of if InteractivePlayer.canStillGuess==true
  else
    #get the computer's guess
    g = @players[activePlayer].getGuess()
  end # if its a comp player, just guess
      #if guess is an accusation, test if its correct 
      if g.accusation==true
        if g.person.to_s==@aPerson.to_s && g.place.to_s==@aPlace.to_s&&g.weapon.to_s==@aWeapon.to_s
          @winner = @players[activePlayer]
          #print different messages for comp players and InteractivePlayers
          if @players[activePlayer].instance_of? InteractivePlayer
            puts("You solved the crime!")
            puts("It was #{@aPerson} in the #{@aPlace} with the #{@aWeapon}!")
            @gameOver = true
                 break;
          else
          puts("Player #{activePlayer+1} has solved the crime!")
          puts("It was #{@aPerson} in the #{@aPlace} with the #{@aWeapon}!")
          @gameOver = true
           break;
        end #end of if accusation is correct 
      else
        #if the accusation is not correct, activePlayer is removed from the game(can still show cards though, no more guesses)
        #test how many players are left in the game. Game is over if there is only one player left in the game
       if currSize==2
         @gameOver = true
         @winner = @players[0] # the last player standing wins
         puts("Player 1 has won the game by default!")
      else
        puts("You guessed wrong! You have lost the game, and can only show cards")
        currSize-=1
        if @players[activePlayer].instance_of? InteractivePlayer
            @players[activePlayer].canStillGuess=false
           
          end
       end #end if currSize==2
      end # end of accusation == true
    else #if not an accusation
      #ask players if they can respond to the guess - start with next player after active player
      nextPlayer = (activePlayer+1)%(@players.size)
      while nextPlayer!=activePlayer do
      c = @players[nextPlayer].canAnswer(activePlayer,g)
      #if another player can answer, provide the answer to the active player
      @players[activePlayer].receiveInfo(nextPlayer,c)
      nextPlayer = (nextPlayer+1)%(@players.size)
      end  #end while
      #else, report that to the active player
      end #end if not accusation
      if !@gameOver
       activePlayer = (activePlayer+1)%(@players.size)
     end #if game is not over
    end #end of while game not over
  end #end of play()
end #end of module class