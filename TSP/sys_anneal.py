import math
import random

from greedy import Greedy

class SA(object):
    def __init__(self, cost_matrix: list, rank: int):
        self.cities_matrix = cost_matrix
        self.number_of_cities = rank
    
    def sa_algorithm(self):
        ga = Greedy(self.cities_matrix, self.number_of_cities)
        solution = ga.greedy_algorithm()
        starting_temp = 100
        current_temperature = starting_temp
        min_length = self.tour_length(solution)
        best_solution = []
        i = 0
        coolingRate = 0.00015#this is the best I've found: 0.0002
        cool_count = 0
        
        lengths = []
        loop_count = []
        lo = 0
        average_distance = self.cities_matrix.sum()/self.number_of_cities**3
        print(average_distance)
        diff_frac = 0.01*average_distance**0.5
        print('Diff_frac' + str(diff_frac))
        while current_temperature>0.05:
            i+=1
            solution = self.optimise(self.cities_matrix, solution, self.number_of_cities, current_temperature, diff_frac)
            if i >= 150:
                i = 0#reset i
                cool_count+=1
                currentLength = self.tour_length(solution)
                #Exponential multiplicative cooling:
                current_temperature = starting_temp*(1 - coolingRate)**cool_count#t *= 1 - coolingRate
                
                
                #current_temperature = starting_temp*math.exp( -( 0.001*1.2*cool_count**1.15 ) )
    #            current_temperature = starting_temp/(1+1.8*math.log(1+0.001*cool_count))
                lo+=1
                loop_count.append(lo)
                lengths.append(currentLength)
                if currentLength < min_length:
                    min_length = currentLength
                    best_solution = solution[:]
    #    plt.plot(loop_count, lengths, 'b.')
    #    filename = 'city'+str(number_of_cities)
    #    plt.savefig(filename, format='svg', dpi=1200)
    #    plt.show()
        return best_solution
    
    #def sa_optimise(cities_matrix, tour, number_of_cities, temperature):
    def optimise(self, cities_matrix, tour, number_of_cities, temperature, diff_frac):
        c1_held = random.randint(0, number_of_cities-1)#c1_held+1 is now a random city index from our tour
        c1_swap = (c1_held+1) % number_of_cities#c1_swap is now the index of the city after c1 from our tour
        c2_swap = random.randint(0, number_of_cities-1)#same process as c1_held and c1_swap
        c2_held = (c2_swap + 1) % number_of_cities
        if c2_swap != c1_held and c2_swap != c1_swap:#we can only compare distinct cities...
            c1h, c1s, c2s, c2h = tour[c1_held], tour[c1_swap], tour[c2_swap], tour[c2_held]
            #return the city number from the tour list's index
            c1hs = cities_matrix[c1h - 1, c1s - 1]#find the distance between the cities from our matrix
            c2hs = cities_matrix[c2s - 1, c2h - 1]
            c1h2s = cities_matrix[c1h - 1, c2s - 1]
            c1s2h = cities_matrix[c1s - 1, c2h - 1]
            difference = (c1hs + c2hs) - (c1h2s + c1s2h)#compute the change in tour length after this swap
            random_swap = False
            if difference < 0:# if the swap is shorter, use it. if it is only a little shorter mutate
                if random.random() < math.exp( difference / temperature ):#math.exp( difference / t ) belongs to the set: (0,1)
                    random_swap = True
                    
            if random_swap or difference > diff_frac :
                new_tour = list(range(0, number_of_cities))# Make a new tour with both edges swapped.
                new_tour[0] = tour[c1_held]
                index = 1
                next_city = c2_swap
                while next_city != c1_swap:#loop through a section of the tour between c2_swap, up to - not including c1_swap
                    new_tour[index] = tour[next_city]#add each city to a new tour
                    index+=1
                    next_city = (next_city-1)%number_of_cities#
                    #
                new_tour[index] = tour[c1_swap]
                index+=1
                while c2_held != c1_held:
                    new_tour[index] = tour[c2_held]
                    index+=1
                    c2_held = (c2_held+1)%number_of_cities
                return new_tour
            else:
                return tour
        else:
            #print("c2_swap == c1_held or c2_swap == c1_swap <-- should be the rare case the random nodes are the same");
            return tour
    
    def tour_length(self, tour):
        total_length = 0
        for i in range (len(tour)) :#for each city in the tour
            total_length += self.cities_matrix[tour[i-1] - 1, tour[i] - 1]#"tour[i]" is one city number in the tour, "tour[i-1]" the city before. Minusing 1 from each of those gives the index for the distance between those two cities in our matrix
        return total_length
