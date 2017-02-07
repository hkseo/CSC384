#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Sokoban warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
import os
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS, sokoban_goal_state #for Sokoban specific classes and problems

#SOKOBAN HEURISTICS
def heur_displaced(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''       
  count = 0
  for box in state.boxes:
    if box not in state.storage:
      count += 1
  return count

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''      
    #We want an admissible heuristic, which is an optimistic heuristic. 
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum Manhattan distance of the boxes to their closest storage spaces is such a heuristic.  
    #When calculating distances, assume there are no obstacles on the grid and that several boxes can fit in one storage bin.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    #the location of the boxes
    d = state.boxes
    
    #sum of all Manhattan distance of the boxes
    m_dist = 0
    
    #reference for finding the lowest distance
    reference = 100000
    
    #coordinates and the restriction of the boxes
    for key,value in d.items():
      
      if state.restrictions:
        #find the drop locations with the particular restrictions
        for j in state.restrictions[value]:
          
          #manhattan distance
          dist = abs(key[0]-j[0]) + abs(key[1]-j[1])
          
          #find the nearest droping point
          if dist < reference:
            reference = dist
      #For the case where there are no restrictions
      else:
        for k in state.storage:
          dist = abs(key[0]-k[0]) + abs(key[1]-k[1])
        
          if dist < reference:
            reference = dist
            
      #sum them all up
      m_dist += reference
      

    return m_dist

def heur_alternate(state):
#IMPLEMENT
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
    #heur_manhattan_distance has flaws.   
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    #1) More boxes in the open position, less h_val
    #Add up all the walls around each boxes * 5
    
    #First find manhattan
    f_dist = heur_manhattan_distance(state)
    const = 3
    
    
    width = state.width
    height = state.height
    #2) Favour moving boxes to the corner
    '''
    if state.restrictions:
      for key, value in state.storage:
    '''
  
    for key,value in state.boxes.items():
      
      #Higher h_val for boxes that are close to the wall
      if key[0] + 1 == width:
        f_dist += const*2
      if key[0] - 1 == 0:
        f_dist += const*2
      if key[1] + 1 == height:
        f_dist += const*2
      if key[1] - 1 == 0:
        f_dist += const*2
      
      for key2 in state.obstacles:
        
        #Higher h_val for boxes that are close to the obstacles
        if key[0] + 1 == key2[0]:
          f_dist += const*2
        if key[0] - 1 == key2[0]:
          f_dist += const*2
        if key[1] + 1 == key2[1]:
          f_dist += const*2
        if key[1] - 1 == key2[1]:
          f_dist += const *2     
        
        for key3,value in state.boxes.items():
          
          #Higher h_val for boxes that are close to other boxes
          if key[0] + 1 == key3[0]:
            f_dist += const
          if key[0] - 1 == key3[0]:
            f_dist += const
          if key[1] + 1 == key3[1]:
            f_dist += const
          if key[1] - 1 == key3[1]:
            f_dist += const             
            
          if key[0] + 1 == width or key[0] + 1 == key2[0] or key[0] + 1 == key3[0]:
            
    return f_dist

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    
    fval = sN.gval + (weight * sN.hval)
    
    return fval

def anytime_gbfs(initial_state, heur_fn, timebound):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 
    #Will be searching using the best first search
    se = SearchEngine('best_first', 'full')
    
    #Initialize the search
    se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn)    
    
    #Starting time
    time1 = os.times()[0]
    
    #Search without a costbound to start
    path = se.search(timebound)
    
    #Ending time
    time = os.times()[0]
    
    #Duration
    dur = time - time1
    
    #Update the timebound
    timebound -= dur
    
    if path:
      #Implement a costbound: h_bound and c_bound + h_bound should be infinite
      costbound = (path.gval,1E100,1E200)
    else:
      return path    
    
    #Iterate the best-first search until the open is empty
    while se.open.empty() == False:
      
      
      time1 = os.times()[0]
      path2 = se.search(timebound,costbound)
      time = os.times()[0]
      dur = time - time1
      timebound -= dur
      
      if path2:
        costbound = (path2.gval,1E100,1E200)
        path = path2
      else:
        break
        
      
    return path

#def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
def anytime_weighted_astar(initial_state, weight, heur_fn, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 
    
    #Will be searching using the Astar search
    se = SearchEngine('custom', 'full')
    
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    #Initialize the search
    se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function = wrapped_fval_function)  
    
    #Starting time
    time1 = os.times()[0]
    
    #Search without a costbound to start
    path = se.search(timebound)
    
    #Ending time
    time = os.times()[0]
    
    #Duration
    dur = time - time1
    
    #Update the timebound
    timebound -= dur
    
    if path:
      #Implement a costbound: h_bound and c_bound should be infinite
      costbound = (1E100,1E100,path.gval)
    else:
      return path    
    
    #Iterate the best-first search until the open is empty
    while se.open.empty() == False:
      
      
      time1 = os.times()[0]
      path2 = se.search(timebound,costbound)
      time = os.times()[0]
      dur = time - time1
      timebound -= dur
      
      if path2:
        costbound = (1E100,1E100,path.gval)
        path = path2
      else:
        break
        
      
    return path    
    
   

if __name__ == "__main__":
    
    #TEST CODE
    solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
    print("*************************************")  
    print("Running A-star")     
  
    for i in range(0, 10): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.
  
      print("*************************************")  
      print("PROBLEM {}".format(i))
      
      s0 = PROBLEMS[i] #Problems will get harder as i gets bigger
  
      final = anytime_gbfs(s0,heur_fn=heur_manhattan_distance,timebound = 4)
  
      if final:
        final.print_path()
        solved += 1
      else:
        unsolved.append(i)    
      counter += 1
  
    if counter > 0:  
      percent = (solved/counter)*100
  
    print("*************************************")  
    print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
    print("*************************************") 
    '''
    solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit 
    print("Running Anytime Weighted A-star")   
  
    for i in range(0, 10):
      print("*************************************")  
      print("PROBLEM {}".format(i))
  
      s0 = PROBLEMS[i] #Problems get harder as i gets bigger
      weight = 10
      final = anytime_weighted_astar(s0, weight, heur_fn= heur_manhattan_distance,timebound = 4)
      #final = anytime_weighted_astar(s0, heur_fn=heur_displaced, weight=weight, timebound=timebound)
  
      if final:
        final.print_path()   
        solved += 1 
      else:
        unsolved.append(i)
      counter += 1      
  
    if counter > 0:  
      percent = (solved/counter)*100   
        
    print("*************************************")  
    print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
    print("*************************************") 
    '''

    