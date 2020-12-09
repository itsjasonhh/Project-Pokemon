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
#       Blue Master, Dunhill, Pall Mall, Prince and blend,
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

# code from https://github.com/0vercl0k/z3-playground/blob/master/einstein_riddle_z3.py

def solve_puzzle():
    #returns the column i of the matrix
    def column(matrix, i):
        return [matrix[j][i] for j in range(5)]

    def instanciate_int_constrained(name, s):
        x = Int(name)
        #Each int represents an index in p[name]
        s.add(x >= 0, x <= 4)
        return x
    
    p = {
        'color': ('Yellow','Green','Blue','Red','White'),
        'nationality': ('Brit','Dane','German','Norwegian','Swede'),
        'beverage': ('Beer','Coffee','Milk','Tea','Water'),
        'smoke': ('Blue Master','Dunhill','Pall Mall', 'Prince', 'Blend'),
        'pet': ('Cat', 'Bird', 'Dog', 'Fish', 'Horse')
    }

    s = Solver()
    color, nationality, beverage, smoke, pet = range(5)

    #creates [[color0, nationality0, ...],...,[color4,nationality4,...]]
    houses = [[instanciate_int_constrained('%s%d' % (prop, n), s) for prop in p.keys()] for n in range(5)]

    for i in range(5):
        s.add(Distinct(column(houses, i)))
    
    #hints
    
    #The Brit lives in a red house
    s.add(Or([And(houses[i][nationality] == p['nationality'].index('Brit'), houses[i][color] == p['color'].index('Red')) for i in range(5)]))

    #The Swede keeps dogs as pets
    s.add(Or([And(houses[i][nationality] == p['nationality'].index('Swede'), houses[i][pet] == p['pet'].index('Dog')) for i in range(5)]))

    #The Dane drinks tea
    s.add(Or([And(houses[i][nationality] == p['nationality'].index('Dane'), houses[i][beverage] == p['beverage'].index('Tea')) for i in range(5)]))

    #The green house is on the left of the white house
    s.add(Or([And(houses[i][color] == p['color'].index('Green'), houses[i+1][color] == p['color'].index('White')) for i in range(4)]))

    #The green house owner drinks coffee
    s.add(Or([And(houses[i][color] == p['color'].index('Green'), houses[i][beverage] == p['beverage'].index('Coffee')) for i in range(5)]))

    #The person who smokes Pall Mall rears birds
    s.add(Or([And(houses[i][smoke] == p['smoke'].index('Pall Mall'), houses[i][pet] == p['pet'].index('Bird')) for i in range(5)]))

    #The owner of the yellow house smokes Dunhill
    s.add(Or([And(houses[i][color] == p['color'].index('Yellow'), houses[i][smoke] == p['smoke'].index('Dunhill')) for i in range(5)]))

    #The man living in the house right in the center drinks milk
    s.add(houses[2][beverage] == p['beverage'].index('Milk'))

    #The Norwegian lives in the first house
    s.add(houses[0][nationality] == p['nationality'].index('Norwegian'))

    #The man who smokes Blend lives in next to the one who keeps cats
    s.add(Or(
        And(houses[0][smoke] == p['smoke'].index('Blend'), houses[1][pet] == p['pet'].index('Cat')),
        And(houses[1][smoke] == p['smoke'].index('Blend'), Or(houses[0][pet] == p['pet'].index('Cat'), houses[2][pet] == p['pet'].index('Cat'))),
        And(houses[2][smoke] == p['smoke'].index('Blend'), Or(houses[1][pet] == p['pet'].index('Cat'), houses[3][pet] == p['pet'].index('Cat'))),
        And(houses[3][smoke] == p['smoke'].index('Blend'), Or(houses[2][pet] == p['pet'].index('Cat'), houses[4][pet] == p['pet'].index('Cat'))),
        And(houses[4][smoke] == p['smoke'].index('Blend'), houses[3][pet] == p['pet'].index('Cat')),
    ))

    #The man who keeps horses lives next to the man who smokes Dunhill
    s.add(Or(
            And(houses[0][pet] == p['pet'].index('Horse'), houses[1][smoke] == p['smoke'].index('Dunhill')),
            And(houses[1][pet] == p['pet'].index('Horse'), Or(houses[0][smoke] == p['smoke'].index('Dunhill'), houses[2][smoke] == p['smoke'].index('Dunhill'))),
            And(houses[2][pet] == p['pet'].index('Horse'), Or(houses[1][smoke] == p['smoke'].index('Dunhill'), houses[3][smoke] == p['smoke'].index('Dunhill'))),
            And(houses[3][pet] == p['pet'].index('Horse'), Or(houses[2][smoke] == p['smoke'].index('Dunhill'), houses[4][smoke] == p['smoke'].index('Dunhill'))),
            And(houses[4][pet] == p['pet'].index('Horse'), houses[3][smoke] == p['smoke'].index('Dunhill'))
    )) 

    #The owner who smokes Blue Master drinks beer
    s.add(Or([And(houses[i][smoke] == p['smoke'].index('Blue Master'), houses[i][beverage] == p['beverage'].index('Beer')) for i in range(5)]))

    #The German smokes Prince
    s.add(Or([And(houses[i][nationality] == p['nationality'].index('German'), houses[i][smoke] == p['smoke'].index('Prince')) for i in range(5)]))

    #The Norwegian lives next to the blue house
    s.add(Or(
            And(houses[0][nationality] == p['nationality'].index('Norwegian'), houses[1][color] == p['color'].index('Blue')),
            And(houses[1][nationality] == p['nationality'].index('Norwegian'), Or(houses[0][color] == p['color'].index('Blue'), houses[2][color] == p['color'].index('Blue'))),
            And(houses[2][nationality] == p['nationality'].index('Norwegian'), Or(houses[1][color] == p['color'].index('Blue'), houses[3][color] == p['color'].index('Blue'))),
            And(houses[3][nationality] == p['nationality'].index('Norwegian'), Or(houses[2][color] == p['color'].index('Blue'), houses[4][color] == p['color'].index('Blue'))),
            And(houses[4][nationality] == p['nationality'].index('Norwegian'), houses[3][color] == p['color'].index('Blue'))
    ))

    #The man who smokes Blend has a neighbor who drinks water
    s.add(Or
        (   And(houses[0][smoke] == p['smoke'].index('Blend'), houses[1][beverage] == p['beverage'].index('Water')),
            And(houses[1][smoke] == p['smoke'].index('Blend'), Or(houses[0][beverage] == p['beverage'].index('Water'), houses[2][beverage] == p['beverage'].index('Water'))),
            And(houses[2][smoke] == p['smoke'].index('Blend'), Or(houses[1][beverage] == p['beverage'].index('Water'), houses[3][beverage] == p['beverage'].index('Water'))),
            And(houses[3][smoke] == p['smoke'].index('Blend'), Or(houses[2][beverage] == p['beverage'].index('Water'), houses[4][beverage] == p['beverage'].index('Water'))),
            And(houses[4][smoke] == p['smoke'].index('Blend'), houses[3][beverage] == p['beverage'].index('Water'))
    ))    

    if s.check() == unsat:
        raise Exception('The system is not solvable!')
    m = s.model()
    solution = [[m[case].as_long() for case in line] for line in houses]
    for i in range(5):
        print('House %s = Color: %s, Nationality: %s, Beverage: %s, Smoke: %s, Pet: %s' % (
            i + 1,
            p['color'][solution[i][color]],
            p['nationality'][solution[i][nationality]],
            p['beverage'][solution[i][beverage]],
            p['smoke'][solution[i][smoke]],
            p['pet'][solution[i][pet]]
        ))
        
solve_puzzle()