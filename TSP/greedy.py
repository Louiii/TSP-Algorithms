class Greedy(object):
    def __init__(self, cost_matrix: list, rank: int):
        self.cities_matrix = cost_matrix
        self.tourlength = rank

    def greedy_algorithm(self):
        unvisited_cities = list(range(2, self.tourlength + 1))
        solution = [1]
        total_length = 0
        while len(unvisited_cities) > 0:
            min_length = self.cities_matrix.max()
            min_n = 0
            for city_index in range(len(unvisited_cities)):#this for-loop finds the nearest city
                current_length = self.cities_matrix[unvisited_cities[city_index] - 1, solution[-1] - 1]#free_cities[city_index] is the city index #print("Dist to next city: " + str(l) + ", min dist so far: " + str(min_l))
                if current_length == 0:
                    min_length = current_length
                    min_n = city_index
                if current_length < min_length:
                    min_length = current_length
                    min_n = city_index
            total_length += min_length
            solution.append(unvisited_cities[min_n])
            unvisited_cities.remove(unvisited_cities[min_n])#print("solution so far: " + str(solution))
        return solution
