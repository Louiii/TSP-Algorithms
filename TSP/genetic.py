#import math
import random
#import numpy
#from re import sub
#from random import shuffle
from greedy import Greedy

class Genetic(object):
    def __init__(self, cost_matrix: list, rank: int):
        self.cities_matrix = cost_matrix
        self.tourlength = rank

    def rnd_swap(self, list_):
        i = random.randint(2, self.tourlength-2)
        index_1 = random.randint(0, i-1)
        index_2 = random.randint(i, self.tourlength-1)
        return list_[:index_1] + [ list_[index_2] ] + list_[index_1+1:index_2] + [ list_[index_1] ] + list_[index_2+1:]

    def genetic(self):
        #init
        ga = Greedy(self.cities_matrix, self.tourlength)
        initial = ga.greedy_algorithm()
        current_pop = []
        for i in range(100) :
            baby = initial[:]
            #swap a few in initial
            if random.random() < 0.95:
                baby = self.rnd_swap(baby)
                if random.random() < 0.7:
                    baby = self.rnd_swap(baby)
                    if random.random() < 0.4:
                        baby = self.rnd_swap(baby)
            #current.shuffle()#shuffle to a certain degree
    #        current = random.sample(range(1, tourlength + 1), tourlength)

            current_pop.append(  (baby, self.tour_length(baby))  )

    #    print("currentpopppppp"+str(len(current_pop)))


        min_length = min(list(map(lambda x: x[1], current_pop)))
        curr_best = list(filter(lambda x: x[1] == min_length, current_pop))[0]
    #    print(curr_best)
        ########################

        new_best = curr_best[:]
        checker = 0
        new_pop = []
        while checker < 20 :  #while not(max fitness hasn't improved in x generations)
            for i in range(100) :
                parents = self.select_parents(current_pop)
                dad, mum = parents[0], parents[1]
                #SPLICE
                rand_index = random.randint(0, self.tourlength-1)
                #take the prefix of dad and add the suffix of mum
                child_with_duplicates = dad[0][:rand_index] + mum[0][rand_index:]

                #MUTATE
                for j in range(len(child_with_duplicates)) :
                    #for city in child_with_duplicates:
                    if random.random() < 0.01:#with a 1% chance randomly mutate each city
                        #city = random.sample(range(1, tourlength + 1), tourlength)[0]
                        child_with_duplicates[j] = random.randint(1, self.tourlength)
                #make a set of all the cities not included
                not_included = [x for x in range(1, self.tourlength+1)]
                for c in child_with_duplicates:
                    if c in not_included:
                        not_included.remove(c)

                random.shuffle(not_included)
                #check over for repetitions, if there is: add the first from the set
                child = []
                for c in child_with_duplicates:
                    if c in child:
                        child.append(not_included[0])
                        not_included.pop(0)
                    else :
                        child.append(c)
                #add child to current_pop[i]
                new_pop.append(  (child, self.tour_length(child))  )
            current_pop = new_pop
            new_pop = []

            min_length = min(list(map(lambda x: x[1], current_pop)))
            new_best = list(filter(lambda x: x[1] == min_length, current_pop))[0]

    #        print("new_best: " + str(new_best[1]) + "curr_best: " + str(curr_best[1]))
    #        print("curr_best[1] > new_best[1] : " + str(curr_best[1] > new_best[1]))
            ########################

            if curr_best[1] > new_best[1] :
                curr_best = new_best
                checker == 0
            elif curr_best[1] == new_best[1] :
                checker += 1
    #            else :
    #                checker == 0
    #        print("new_best: " + str(new_best[1]))
    #        print("Fittest in generation: " + str(curr_best[0]))
    #        print("Length: " + str(curr_best[1]))
    #        print("checker:" + str(checker))

        return curr_best[0]

    def select_parents(self, current_pop):
        lengths = list(map(lambda x: x[1], current_pop))
        ranks = list(map(lambda x: (1/x)**4, lengths))#**4 put the lower ranked ones lower
        tot = sum(ranks)
        probs = list(map(lambda x: x/tot, ranks))#normalised ranks of pop
        parents = []
        for i in range(2):
            random_num = random.random()
            accum = 0
            index = 0
            while accum < random_num:
                accum += probs[index]
                index += 1
            parents.append(current_pop[index-1])
        return parents


    def tour_length(self, tour):
        total_length = 0
        for i in range (len(tour)) :#for each city in the tour
            total_length += self.cities_matrix[tour[i-1] - 1, tour[i] - 1]#"tour[i]" is one city number in the tour, "tour[i-1]" the city before. Minusing 1 from each of those gives the index for the distance between those two cities in our matrix
        return total_length
