#NAME: Katrina Dotzlaw
#STUDENT NUMBER: 7833061
#COURSE: COMP 2150 A02 Domaratzki
#CLASS: Guess - create Guess objects that are used by players to make suggestions or accusations about WHODUNNIT

class Guess
  def initialize(c1,c2,c3,a)
    @person = c1 
    @place = c2
    @weapon = c3
    @accusation = a #true if guess is an accusation, false if suggestion
  end
  #getters
  attr_reader :person
  attr_reader :place
  attr_reader :weapon
  attr_reader :accusation
  def to_s
    if @accusation==true
      "Accusation: #{@person} in #{@place} with the #{@weapon}"
    else
      "Suggestion: #{@person} in #{@place} with the #{@weapon}"
    end
  end
end
