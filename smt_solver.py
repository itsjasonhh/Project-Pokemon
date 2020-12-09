from z3 import *

# http://www.davar.net/MATH/PROBLEMS/EINSTEIN.HTM
# The author of this problem is Albert Einstein who said that 98% of the people in the world couldn't solve it.

#  	 Facts:
# 1.		There are 5 houses (along a street) in 5 different colors:
#       blue, green, red, white and yellow.
# 2.		In each house lives a person of a different nationality:
#       Brit, Dane, German, Norwegian and Swede.
# 3.		These 5 owners
# drink a certain beverage:
#       beer, coffee, milk, tea and water,
# smoke a certain brand of cigar:
#       Blue Master, Dunhill, Pall Mall, Prince, and blend,
# and keep a certain pet:
#       cat, bird, dog, fish and horse.
# 4.		No owners have the same pet, smoke the same brand of cigar, or drink the same beverage.
#  Hints:
# 1.		The Brit lives in a red house.
# 2.		The Swede keeps dogs as pets.
# 3.		The Dane drinks tea.
# 4.		The green house is on the left of the white house (next to it).
# 5.		The green house owner drinks coffee.
# 6.		The person who smokes Pall Mall rears birds.
# 7.		The owner of the yellow house smokes Dunhill.
# 8.		The man living in the house right in the center drinks milk.
# 9.		The Norwegian lives in the first house.
# 10.		The man who smokes blend lives next to the one who keeps cats.
# 11.		The man who keeps horses lives next to the man who smokes Dunhill.
# 12.		The owner who smokes Blue Master drinks beer.
# 13.		The German smokes Prince.
# 14.		The Norwegian lives next to the blue house.
# 15.		The man who smokes blend has a neighbor who drinks water.

#code loosely based from https://sat-smt.codes/SAT_SMT_by_example.pdf
def solve_puzzle():
    blue, green, red, white, yellow = Ints('blue green red white yellow')
    brit, dane, german, norwegian, swede = Ints('brit dane german norwegian swede')
    beer, coffee, milk, tea, water = Ints('beer coffee milk tea water')
    bluemaster, dunhill, pallmall, prince, blend = Ints('bluemaster dunhill pallmall prince blend')
    cat, bird, dog, fish, horse = Ints('cat bird dog fish horse')
    variables = []
    variables.append(blue)
    variables.append(green)
    variables.append(red)
    variables.append(white)
    variables.append(yellow)
    variables.append(brit)
    variables.append(dane)
    variables.append(german)
    variables.append(norwegian)
    variables.append(swede)
    variables.append(beer)
    variables.append(coffee)
    variables.append(milk)
    variables.append(tea)
    variables.append(water)
    variables.append(bluemaster)
    variables.append(dunhill)
    variables.append(pallmall)
    variables.append(prince)
    variables.append(blend)
    variables.append(cat)
    variables.append(bird)
    variables.append(dog)
    variables.append(fish)
    variables.append(horse)
    s = Solver()
    s.add(Distinct(blue, green, red, white, yellow))
    s.add(Distinct(brit, dane, german, norwegian, swede))
    s.add(Distinct(beer, coffee, milk, tea, water))
    s.add(Distinct(bluemaster, dunhill, pallmall, prince, blend))
    s.add(Distinct(cat, bird, dog, fish, horse))
    for i in variables:
        s.add(i >= 1, i <= 5)
    # 1.		The Brit lives in a red house.
    s.add(brit == red)
    # 2.		The Swede keeps dogs as pets.
    s.add(swede == dog)
    # 3.		The Dane drinks tea.
    s.add(dane == tea)
    # 4.		The green house is on the left of the white house (next to it).
    s.add(green == white - 1)
    # 5.		The green house owner drinks coffee.
    s.add(green == coffee)
    # 6.		The person who smokes Pall Mall rears birds.
    s.add(pallmall == bird)
    # 7.		The owner of the yellow house smokes Dunhill.
    s.add(yellow == dunhill)
    # 8.		The man living in the house right in the center drinks milk.
    s.add(milk == 3)
    # 9.		The Norwegian lives in the first house.
    s.add(norwegian == 1)
    # 10.		The man who smokes blend lives next to the one who keeps cats.
    s.add(Or(blend == cat + 1, blend == cat - 1))
    # 11.		The man who keeps horses lives next to the man who smokes Dunhill.
    s.add(Or(horse == dunhill + 1, horse == dunhill - 1))
    # 12.		The owner who smokes Blue Master drinks beer.
    s.add(bluemaster == beer)
    # 13.		The German smokes Prince.
    s.add(german == prince)
    # 14.		The Norwegian lives next to the blue house.
    s.add(Or(norwegian == blue + 1, norwegian == blue - 1))
    # 15.		The man who smokes blend has a neighbor who drinks water.
    s.add(Or(blend == water + 1, blend == water - 1))
    if s.check() == sat:
        house1 = []
        house2 = []
        house3 = []
        house4 = []
        house5 = []
        for var in variables:
            inp = int(str(s.model()[var]))
            if inp == 1:
                house1.append(str(var))
            elif inp == 2:
                house2.append(str(var))
            elif inp == 3:
                house3.append(str(var))
            elif inp == 4:
                house4.append(str(var))
            elif inp == 5:
                house5.append(str(var))
        print('House 1: ', house1)
        print('House 2: ', house2)
        print('House 3: ', house3)
        print('House 4: ', house4)
        print('House 5: ', house5)
    else:
        print('Cannot be solved!')
solve_puzzle()