import numpy
from re import sub

# from beam_search import BeamSearch
from greedy import Greedy
from sys_anneal import SA
from a_star import AStar
from genetic import Genetic
# from aco import ACO, Graph


global tourString#12, 17,  21, 26, 42, 48, 58, 175, 180, 535
global cities_matrix
global tourlength


city_numbers = ["012", "017",  "021", "026", "042", "048", "058", "175", "180", "535"]
opt = [56, 1444, 2549, 1473, 1187, 12166, 25395, 21430, 1950, 48635]




def tour_length(tour):
    total_length = 0
    for i in range (len(tour)) :#for each city in the tour
        total_length += cities_matrix[tour[i-1] - 1, tour[i] - 1]#"tour[i]" is one city number in the tour, "tour[i-1]" the city before. Minusing 1 from each of those gives the index for the distance between those two cities in our matrix
    return total_length

def read_problem(problem_file_name):#converts txt city file into an array of ints called lines
    #random.seed(378939)  # This it to make sure we get the same answer each time.
    text_file = open(problem_file_name, mode='r')
    lines = text_file.read().split(',')
    #print(lines[0][-3:]) # tourString = lines[0]
    lines.pop(0)
    for i in range(1, len(lines)):
        lines[i] = lines[i].lstrip('\n')
    lines[0] = lines[0].lstrip('\nSIZE = ')
    lines = [x.replace(' ', '') for x in lines]
    for i in range(1, len(lines)):
        lines[i] = sub("[a-z]", '', sub("[A-Z]", '', lines[i]))
        lines[i] = sub('\n', '', lines[i])
    lines = list(map(int, lines))#lines = [int(float(i)) for i in lines]
    global tourlength
    tourlength = lines[0]
    lines.pop(0)

#    linescopy = lines[:]

    text_file.close()  #makes a symmetric matrix from lines with zeros on the leading diagonal
    global cities_matrix
    cities_matrix = numpy.zeros((tourlength, tourlength))
    for j in range(tourlength-1):
        for i in range(1+j,tourlength):
            cities_matrix[i][j] = cities_matrix[j][i] = lines.pop(0)

def run_algos():
    # print ('Computing my breadth-first-search path')
    # bs = BeamSearch(cities_matrix, tourlength, 2)
    # my_beam_sol = bs.beam_search()
    # writeTour('BeamSearch', my_beam_sol)
    # print(str(tour_length(my_beam_sol)))
#
   # print ('Computing my greedy path')
   # gr = Greedy(cities_matrix, tourlength)
   # my_greedy_sol = gr.greedy_algorithm()
   # writeTour('Greedy', my_greedy_sol)
   # print(str(tour_length(my_greedy_sol)))
#
   # print ('Computing my a star path')
   # ast = AStar(cities_matrix, tourlength)
   # my_a_star_sol = ast.a_star()
   # writeTour('A_Star', my_a_star_sol)
   # print(str(tour_length(my_a_star_sol)))
#
   # print ('Computing my genetic path')
   # gn = Genetic(cities_matrix, tourlength)
   # my_genetic_solution = gn.genetic()
   # print("my_genetic_solution")
   # print(my_genetic_solution)
   # writeTour('Genetic', my_genetic_solution)
   # print(str(tour_length(my_genetic_solution)))
#
    # print ('Computing my ant colony path')
    # aco = ACO(10, 100, 1.0, 20.0, 0.5, 10, 2)#ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
    # graph = Graph(cities_matrix, tourlength)
    # path, cost = aco.solve(graph)
    # writeTour('AntColony', path)
    # print(cost)

   # print("SA running...")
   # sa = SA(cities_matrix, tourlength)
   # system_annealing_solution = sa.sa_algorithm()
   # writeTour('SA', system_annealing_solution)
   # print("DONE SA TOUR!")
   # print("SA length =====" + str(tour_length(system_annealing_solution)))


def writeTour(algo, tour):
    cityOrder = []
    for city in tour:
        cityOrder.append(str(city))
    file = open('Solutions/' + algo + '/tour' + tourString + '.txt', 'w')
    file.write('NAME = AISearchfile' + tourString[-3:] + ',\n' + 'TOURSIZE = ' + str(int(tourString[-3:])) + ',\nLENGTH = ' + str(int(tour_length(tour))) + ',\n')
    for city in cityOrder:
        file.write(str(city) + ',')
    file.close()



if __name__ == '__main__':
    i=0
    for number in city_numbers:
        curr = "CITY: " + str(city_numbers[i])+", Optimal length: " + str(opt[i])
        print(curr)
        tourString = 'AISearchfile' + number
        read_problem('cityfiles/' + tourString + '.txt')
        run_algos()
        print('\n')
        i+=1
