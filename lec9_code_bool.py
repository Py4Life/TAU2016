#########################################
## Boolean model for regulatory networks
#########################################

def update_node(G, states, i):
    ''' Return new state of node i given states vector '''
    n = len(states)

    #FILL THIS FUNCTION
    
    return new #new state of node i

def update(G, states):
    ''' Return the next states vector - apply transition function to all nodes '''
    n = len(states)
    next_states = [-1]*n

    for i in range(n):
        next_states[i] = update_node(G, states,i)
    return next_states


def run(G, init, track = False):
    ''' start with init vector, and run until steady state/loop '''
    trajectory = set() #for loop detection
    c = 1 #if you want to count steps
    
    if track:
        print(init)
        
    states = init
    next_states = update(G, states)

    trajectory.add(tuple(states))
    #print(trajectory)

    while states != next_states \
          and tuple(next_states) not in trajectory:

        if track:
            print(states)

        states = next_states
        next_states = update(G, states)

        c += 1
        trajectory.add(tuple(states))
        #print(trajectories)

    if states == next_states:
        return states #steady state (attractor) reached
    else:
        print("LOOP!!!")

    

import itertools

def attractor_size(G, attractor):
    ''' count how many initial vectors end up in the attractor vector '''
    n = len(G)
    cnt = 0
    total = 0

    all_vectors = itertools.product([0,1], repeat=n)#cartesian product of (0,1)^n
    for states in all_vectors:
        states = list(states) #convert tuple-->list, to make mutable
        final = run(G, states)
        if final == attractor:
            cnt+=1
        total+=1
    return cnt/total*100

#############################################
### check input correctness
def validate(G, init):
    """ verify that the input is valid """
    n = len(G)
    assert n == len(init)
    assert all([len(G[i]) == n for i in range(n)])


#############################################
### Input network - example for infinite loop

nodes = ['A','B'] 

init = [1, 0]

G = [
     [-1,1],
     [1,-1]
    ]

##validate(G, init)
##run(G, init, True)


#############################################
### Input network - toy example from lecture

nodes = ['A','B','C','D','E','F'] 

init = [1, 0, 1, 0, 0, 0]

G = [
    [ 0, 0, 0, 1, 0, 0],
    [-1, 0, 0,-1,-1, 0],
    [-1, 0, 0, 0, 0, 0],
    [ 1, 0, 0, 0, 1, 0],
    [ 0, 0, 0, 0, 0, 1],
    [ 0, 0, 0,-1, 1,-1]
    ]

##print("A single simulation of the toy network")
##validate(G, init)
##print(nodes)
##run(G, init, True)

#############################################
### Input network - yeast cell-cycle
### "The Yeast Cell-Cycle Network is Robustly Designed", Li et.al, PNAS, 2004

nodes = ['Cln3','MBF','SBF','Cln1,2','Cdh1','Swi5','Cdc20/Cdc14','Clb5,6','Sic1','Clb1,2','Mcm1/SFF'] 

init = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0] #simulation of this is in the paper
                                         #stationary G1 with Cln3=1 (signal to start a cycle)

G = [
    [-1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [ 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0,-1,-1, 0, 0, 0,-1, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0],
    [ 0, 0, 0, 0, 0,-1, 0, 0, 1, 0, 0],
    [ 0, 0, 0, 0, 1, 1,-1,-1, 1,-1, 0],
    [ 0, 0, 0, 0,-1, 0, 0, 0,-1, 1, 1],
    [ 0, 0, 0, 0, 0, 0, 0,-1, 0,-1, 0],
    [ 0,-1,-1, 0,-1,-1, 1, 0,-1, 0, 1],
    [ 0, 0, 0, 0, 0, 1, 1, 0, 0, 1,-1]
    ]

print("A single simulation of the Yeast cell cycle:")
validate(G, init)
print(nodes)
run(G, init, True)

#main attractor size count
final = [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0] #according to paper, 1764 initial vectors end here
print(round(attractor_size(G, final)), "% of initial vectors end at", final)


