class AStar(object):
    def __init__(self, cost_matrix: list, rank: int):
        self.cities_matrix = cost_matrix
        self.tourlength = rank

    def p_ga(self, tour_so_far, unvisited):#return all new tours after the first split and their corresponding unvisited
        tour = tour_so_far[:]
        unv = unvisited[:]
        while(True):
            next_cities = []
            lengths = []

            #lengths is a list of the distances to all unvisited cities in the correct order
            for u in unv:
                lengths.append(self.cities_matrix[u - 1, tour[-1] - 1])
    #        print('lengths',lengths)
            min_length = min(lengths)
    #        print('min_length', min_length)
            for city_index in range(len(lengths)):
                if lengths[city_index]==min_length:
                    next_cities.append(unv[city_index])
            #next_cities is a list of all the closest unvisited cities
            if len(next_cities) != 1: break
            #remove the closest city from unvisited and add it to tour, repeat
            tour += next_cities
            unv.remove(next_cities[0])
            if len(unv) == 0: break
        if len(unv) == 0: return [(tour, [])]
    #    print('TOUR:',tour, 'unvisited',unv)
        #fix do - while
        options = []
        for n in next_cities:
            u = unv[:]
            u.remove(n)
            options.append(  (tour + [n], u)  )
        #options includes tuples of the tour and the unvisited cities in that tour
        return options

    def p_greedy(self, tour, unv):#complete the partial greedy tour, use p_ga to calc all routes, return the min length
        if len(unv) == 0:
            return tour
        elif len(unv) == 1:
            return tour + unv
    #    print('PGREEDY:completed_so_far : ' + str(tour) + 'unvisited : ' + str(unv))
        options = self.p_ga(tour, unv)
    #    print('PGREEDY:options : ' + str(options))
        if len(options) == 1:
    #        print(options[0][0])
            return self.tour_length(options[0][0])
        uncomp = options[:]
        complete = []
        while len(uncomp) > 0:
            curr = uncomp[0]
            uncomp.pop(0)
            new_opts = self.p_ga(curr[0], curr[1])
    #        print('PGREEDY:new_opts : ' + str(new_opts))
            for o in new_opts:
                if len(o[1])==0:
                    complete.append(o[0])
                else:
                    uncomp.append(o)
        lengths=[]
        for c in complete:
            lengths.append(self.tour_length(c))
        return min(lengths)

    def fn(self, completed_so_far, unvisited ):
    #    print('fn')
    #    print('completed_so_far : ' + str(completed_so_far) + 'unvisited : ' + str(unvisited))
        current_tour = completed_so_far[:]
        unvis = unvisited[:]
        while len(current_tour) < self.tourlength:
            fringe_tours = []
            lengths = []
            fringe = unvis[:]
            for fringe_city in fringe:
                unv = unvis[:]
                unv.remove( fringe_city )
                fringe_tours.append(  (current_tour + [fringe_city], unv )  )#partial_tour_length( partial_greedy( [fringe_city]+unv ) ) )  )
                lengths.append( self.p_greedy( current_tour + [fringe_city], unv) )
    #        print('lengths:',str(lengths))
            #fringe_tours is a list of all the tours through the fringe city
            #make a list of all the tours of min length from fringe cities
            joint_min_tours = []
            min_length = min(lengths)
            for i in range(len(lengths)):
                if lengths[i] == min_length:
                    joint_min_tours.append(fringe_tours[i])
            if len(joint_min_tours) > 1:
                # print('joint min:',str(min_length))
                # print('joint tours:',str(joint_min_tours))
                return joint_min_tours
            current_tour = joint_min_tours[0][0]
            unvis.remove(joint_min_tours[0][0][-1])
        return joint_min_tours


    def a_star(self):
        options = []
        for i in range(self.tourlength):
            s = list(range(1, self.tourlength + 1))
        #    shuffle(s)
            s = [s[i]] + s[:i] + s[i + 1:]
            joint_min_cities = self.fn( [s[0]], s[1:] )
        #    joint_min_cities = self.fn( [1], list(range(2, self.tourlength + 1)) )
    #        print('a_star:', joint_min_cities)
            if len(joint_min_cities)==1:
                options.append( (joint_min_cities[0][0], self.tour_length(joint_min_cities[0][0])) )
            else:
                uncomplete = joint_min_cities[:]
                completed = []
                while len(uncomplete)>0:
                    curr = uncomplete[0]
                    uncomplete.pop(0)
                    joint_min_tour = self.fn(curr[0], curr[1])
                    if len(joint_min_tour)==1:
                        completed.append( joint_min_tour[0][0] )
                    else:
                        uncomplete += joint_min_tour
                lengths = []
                for c in completed:
                    lengths.append( self.tour_length(c) )
                m = min(lengths)
                options.append( (completed[lengths.index(m)], m) )
                #print('COMPLETED!!',completed)
        lens=([x[1] for x in options])
        return options[lens.index(min(lens))][0]

    def tour_length(self, tour):
        total_length = 0
        for i in range (len(tour)) :#for each city in the tour
            total_length += self.cities_matrix[tour[i-1] - 1, tour[i] - 1]#"tour[i]" is one city number in the tour, "tour[i-1]" the city before. Minusing 1 from each of those gives the index for the distance between those two cities in our matrix
        return total_length
