#NAME: Katrina Dotzlaw
#COURSE: COMP 2150 A02 Domaratzki
#CLASS: InteractivePlayer - subclass of Abstract Player class (PlayerAbs)

class InteractivePlayer < PlayerAbs
  def initialize()
    super()
   #shares all properties in PlayerAbs
  end
  #Precondition: unknown if i have any of the cards in the Guess g
  #@param playerIndex: index of the player making the guess that i might be able to answer
  #@param g: guess made by Player[playerIndex]
  #Postcondition: return a Card (Cases: if i only have 1 card, return it. If i have >1 card, i choose which to show)
    #Or return nil, if i dont have any of the cards
  def canAnswer(playerIndex, g) 
   #which cards do i have?
    myCards = self.playerCards()
      #keep track of how many of the cards in Guess i have
      count = 0
      #stores result of comparison with cards in Guess g
      p = nil
      pl = nil
      w = nil
      #loop through my cards and check if i have any of the cards in Guess g
      myCards.size.times{|i|
        if myCards[i].to_s==g.person().to_s
          p = myCards[i]
          count+=1
       else if myCards[i].to_s==g.place().to_s
         pl = myCards[i]
         count+=1
         else if myCards[i].to_s==g.weapon().to_s
           w = myCards[i]
           count+=1
           end #else if weapon
           end #else if place
        end #end if person
        } #end loop
#if i only have 1 of the cards in the guess, show it
        if count==1 
          if p!=nil
           puts("Player #{playerIndex+1} asked you about #{g.person()} in #{g.place()} with #{g.weapon()}, you only have 1 card #{p.to_s}, showed it to them.")
            return p
          else if pl!=nil
            puts ("Player #{playerIndex+1} asked you about #{g.person()} in #{g.place()} with #{g.weapon()}, you only have 1 card #{pl.to_s}, showed it to them.") 
            return pl
          else if w!=nil
            puts ("Player #{playerIndex+1} asked you about #{g.person()} in #{g.place()} with #{g.weapon()}, you only have 1 card #{w.to_s}, showed it to them. ") 
            return w
          end 
        end 
        end
     
else  if count>1
      #if i have more than 1 of the cards in the guess, i choose which one to show
      puts("Player #{playerIndex+1} asked you about #{g.person()} in #{g.place()} with #{g.weapon()}. Which do you show?")
      c = 1
      #make an array of cards that contain the cards in the Gues g that i have
      cardsToShow = Array.new()
      k=0
      myCards.size.times{|j|
        if myCards[j]==p||myCards[j]==pl||myCards[j]==w
          #display all cards
          puts("#{c}: #{myCards[j].to_s} ")
          cardsToShow[k]=myCards[j]
          k+=1
          c+=1
          end
          }
          #still inside count>1
          #choose which card to show player[playerIndex]
          s = gets.chomp
          if s == "1"
            #display card at spot 0
            puts ("You showed player #{playerIndex+1} the card #{cardsToShow[0].to_s}")
            return cardsToShow[0]
            else if s=="2"
              #display card at spot 1
             puts ("You showed player #{playerIndex+1} the card #{cardsToShow[1].to_s} ")
             #cardsToShow[1].to_s
             return cardsToShow[1]
              else if s =="3"
              puts ("You showed player #{playerIndex+1} the card #{cardsToShow[2].to_s} ")
              #cardsToShow[2].to_s
              return cardsToShow[2]
               end
               end
               end 
       #out of count>1     
else #count==0
   puts("Player #{playerIndex+1} asked about #{g.person()} in #{g.place()} with #{g.weapon()} but you couldn't answer")
   
end #end of count==1
  end 
 
end # end of function canAnswer
  #Precondition: i have not made a guess
  #Postcondition: user input is used to generate a guess and return it
  def getGuess()
      puts("Displaying all cards in the game: ")
       @suspects.size.times{|i| puts("#{@suspects[i].to_s}")}
       @location.size.times{|i| puts("#{@location[i].to_s}")}
       @weapon.size.times{|i| puts("#{@weapon[i].to_s}")}
    #@suspects.size.times{|i|puts("Suspects in interactive player: #{@suspects[i].to_s}")}
    puts("It is your turn")
    puts("\nDisplaying your cards: ")
    printCards(self.currPlayer())
    puts()
    puts("Which person do you want to suggest?")
    person = gets.chomp
    puts("Which location do you want to suggest?")
    place = gets.chomp
    puts("Which weapon do you want to suggest?")
    weapon = gets.chomp
    puts("Is this an accusation (Y/N)?")
    acc = gets.chomp
    #if the guess is an accusation
    if acc == "Y" ||acc == "y"
      return Guess.new(person,place,weapon,true)
     #return g
    else if acc == "N"|| acc == "n" 
      return Guess.new(person,place,weapon,false)
     # return g
    else if acc==""
     return Guess.new(person,place,weapon,false)
    end
    end #else if
    end #if
  end #end of getGuess
  
  #Precondition: i have not been shown a card
  #@param playerIndex: index of player that i am asking to show me a card
  #@param c: the card that player[playerIndex] is showing me
  #Postcondition: if c==nil, player[playerIndex] does not have any cards in the guess i made
                # if c!=nil, player[playerIndex] has one of the cards and has shown it to me
  def receiveInfo(playerIndex, c)
   if c==nil 
     puts("Player #{playerIndex} could not refute your suggestion")
   else
     puts("Player #{playerIndex+1} refuted your suggestion by showing you #{c.to_s}")
     #c.to_s
   end #ends if
end #end of receive info
end #end of InteractivePlayer