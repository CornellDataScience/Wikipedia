import makeGraph as mg
import randomwalk as rw

'''
Returns a value representing the average degree of loop occurence in a set of random walks.
Subvalues are calculated for each loop, calculated by subtracting the distance between the nodes from the length of the path.
This gives larger loops a smaller value and smaller loops a higher value.
Total value = (sum of subvalues)/(# of walks)/(max possible total value)
The sum is divided by the # of walks to get the average value per walk.
Then it is divided by the max possible value, which graph [a, a, a, ...].
This normalizes score such that a 1.0 indicates only self loops, and 0.0 indicates no self loops.

e.g.
list = (A) -> (B) -> (C) -> (C) -> (A) -> (D) -> (A)
1) loop from [2] to [3], value = (list length)-(distance between loop) = 7-1 = 6
2) loop from [0] to [4], value = 7-4 = 3
3) loop from [4] to [6], value = 7-2 = 5
4) loop from [0] to [6], value = 7-6 = 1
Total value = (sum of subvalues)/(# of walks)/(max possible total value)
            = 15/1/[(6)+(6+5)+(6+5+4)+...+(6+5+4+3+2+1)]
            = 0.0002996
'''
def loops(visited_paths):
    score = 0
    depth = len(visited_paths[0])
    for path in visited_paths:
        path = list(enumerate(path))
        for i,e in path[1:]:
            for i1,e1 in path[:i]:
                if e1 == e:
                    score += depth-(i-i1)
    try:
        return score/len(visited_paths)/sum([i**2 for i in range(depth-1, 0, -1)])
    except ZeroDivisionError:
        return 0

'''
Same as loops except outputted value is higher for larger loops. Do not use.
'''
def loops_old(visited_paths):
    score = 0
    for path in visited_paths:
        path = list(enumerate(path))
        for i,e in path[1:]:
            for i1,e1 in path[:i]:
                if e1 == e:
                    score += i-i1
    try:
        return score/len(visited_paths)/sum([i*(i+1)/2 for i in range(1, len(visited_paths[0]))])
    except ZeroDivisionError:
        return 0

if __name__ == '__main__':
    G = mg.make_prototype_graph("../data/Hevea_brasiliensis_2.json").to_directed()
    thresholds = [0, 0.1, 0.2, 0.3, 0.5, 1.0]
    start_tag = 'Hevea brasiliensis'
    for t in thresholds:
        path = rw.DiGraphRandomWalk(G, 10, 5, t, start_tag, True)
        print ("with threshold {}, self loop score is {}".format(t, loops(path)))
