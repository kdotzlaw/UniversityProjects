require "test/unit"
require_relative "PlayerAbs" 
require_relative "InteractivePlayer"
require_relative "Player"
require_relative "Card"
require_relative "Guess"

class TestPlayer < Test::Unit::TestCase
  
  def setup()
    @ppl = Array.new(0)
    10.times do |i| 
     c = Card.new(:person, "Suspect #{i}" )
     @ppl << c
    end
    
    @places = Array.new(0)
    10.times do |i| 
      c = Card.new(:place, "Place #{i}")
      @places << c
    end
        
    @weapons = Array.new(0)
    10.times do |i| 
      c = Card.new(:weapon, "Weapon #{i}")
      @weapons << c
    end
  
  end
  def test_player_no_cards()
     # test if a player answers nil if no cards.
     p = Player.new()
     
     p.setup(2,0,@ppl,@places,@weapons) # updated -> proper name (setup)
     p.setCard(@ppl[1])
     p.setCard(@places[1])
     p.setCard(@weapons[1])
     g = Guess.new(@ppl[0],@places[0],@weapons[0],false)
 
     ans = p.canAnswer(1,g) # updated -> proper order of parameters
     assert(ans.nil?)
   end
  

     
  def test_player_one_card()
    # test if a player can answer if it has one card
    p = Player.new()
    
    p.setup(2,0,@ppl,@places,@weapons) # updated -> proper name (setup)
    p.setCard(@ppl[0])
    g = Guess.new(@ppl[0],@places[0],@weapons[0],false)
    ans = p.canAnswer(1,g) # updated -> proper order of parameters
    assert(!ans.nil? && ans==@ppl[0])
  end
  
  def test_player_three_cards()
  # test if a player can answer if it has all three cards
    p = Player.new()
  
    g = Guess.new(@ppl[0],@places[0],@weapons[0],false)
    p.setup(2,0,@ppl,@places,@weapons) # updated -> proper name (setup)
    p.setCard(@ppl[0])
    p.setCard(@places[0])
    p.setCard(@weapons[0])
    ans = p.canAnswer(1,g) # updated --> proper order of parameters
    assert(!ans.nil? && (ans==@ppl[0] || ans==@places[0] || ans==@weapons[0]))
  end

  def test_answer() # guess should be the cards that the player doesn't have, can accuse. 
   p = Player.new
   p.setup(2,0,@ppl,@places,@weapons)  # updated --> proper name (setup)
       
   @ppl[1..9].each {|x| p.setCard(x) }
   @places[1..9].each {|x| p.setCard(x) }
   @weapons[1..9].each {|x| p.setCard(x) }

   g = p.getGuess()
      assert (g.person == @ppl[0]&& g.place == @places[0]&& g.weapon == @weapons[0]&& g.accusation)
  
  end
  
  def test_answer2() # after a player gets some new info, it should deduce who has been murdered.
    p = Player.new
    p.setup(2,0,@ppl,@places,@weapons) # updated -> proper name (setup)
      
  @ppl[1..8].each {|x| p.setCard(x) }
  @places[1..9].each {|x| p.setCard(x) }
  @weapons[1..9].each {|x| p.setCard(x) }

  g = p.getGuess()
  assert ((g.person == @ppl[0]|| g.person == @ppl[9]) && g.place == @places[0] && g.weapon == @weapons[0] && !g.accusation)
  p.receiveInfo(1,@ppl[0])
  g = p.getGuess()
  #issue is this assert
  assert ((g.person == @ppl[9]) && g.place == @places[0] && g.weapon == @weapons[0] && g.accusation)

 end
#  
end
