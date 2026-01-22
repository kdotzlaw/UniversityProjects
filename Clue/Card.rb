#NAME: Katrina Dotzlaw
#STUDENT NUMBER: 7833061
#COURSE: COMP 2150 A02 Domaratzki
#CLASS: Card - creates cards objects that are dealt to players

class Card
  def initialize(t, v)
    @type = t
    @value = v
  end
  #getters
  attr_reader :type #use by calling type
  attr_reader :value #use by calling value
  def to_s
    "#{@value}"
  end
end