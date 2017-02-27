#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def add_sat_tuple1(const,dom):
    '''
    This is for the binary constriants of not-equal
    '''
    
    sat_tuples = []
                            
    #All combinations of tuples
    for t in itertools.product(dom, dom):  
        
        #Check if the two values are not-equal
        if t[0] != t[1]:
            
            sat_tuples.append(t) 
            
    const.add_satisfying_tuples(sat_tuples)
    return const
    
def add_sat_tuple2(const, dom, n, summ):
    '''
    This is for the summantion constraint
    '''
    
    sat_tuples = []
    
    #10 possible numbers per variable, n variables in this constraint
    a = [[i for i in range(10)]for j in range(n)]
    
    #All combinations of tuples
    for t in itertools.product(*a):  
        
        #Check if the addition equals to the corresponding sum
        if sum(t) == summ:
            
            sat_tuples.append(t) 
            
    const.add_satisfying_tuples(sat_tuples)  
    
    return const
    
def cons_adjacent(cons, variable_array,i,j, dom):
    '''
    Return list of constraints for each BINARY CONSTRAINTS OF NOT-EQUAL
    The function also adds all the satisfying tuples
    
    '''
    #If the coordinates (i,j) is on the upper or bottom edge, build constraint with right of it
    if ((i == 0) or (i == len(variable_array)-1)) and (j < len(variable_array[0])-1):
        
        c = Constraint("C({},{})".format([i,j],[i,j+1]),[variable_array[i][j], variable_array[i][j+1]])
        
        c = add_sat_tuple1(c, dom)
        
        cons.append(c)
        
    
    #If the coordinates is on the left or right edge, build constraint with ones below
    if ((j == 0) or (j == len(variable_array[0])-1)) and (i < len(variable_array)-1):
        
        #Add this new constraint to the list of constraints
        c = Constraint("C({},{})".format([i,j],[i+1,j]),[variable_array[i][j], variable_array[i+1][j]])
        
        c = add_sat_tuple1(c, dom)
                
        cons.append(c)
        
    #For all the other cases, build constraint all around it (8 spots)
    else:
        if (i != 0) and (i != len(variable_array)-1):
            c = Constraint("C({},{})".format([i,j],[i-1,j-1]),[variable_array[i][j], variable_array[i-1][j-1]]) 
            c = add_sat_tuple1(c, dom)
            cons.append(c)      
            
            c = Constraint("C({},{})".format([i,j],[i-1,j]),[variable_array[i][j], variable_array[i-1][j]])
            c = add_sat_tuple1(c, dom)
            cons.append(c)      
            
            c = Constraint("C({},{})".format([i,j],[i-1,j+1]),[variable_array[i][j], variable_array[i-1][j+1]])
            c = add_sat_tuple1(c, dom)
            cons.append(c)             
            
            c = Constraint("C({},{})".format([i,j],[i,j-1]),[variable_array[i][j], variable_array[i][j-1]])
            c = add_sat_tuple1(c, dom)
            cons.append(c)  
            
            c = Constraint("C({},{})".format([i,j],[i,j+1]),[variable_array[i][j], variable_array[i][j+1]])
            c = add_sat_tuple1(c, dom)
            cons.append(c)         
            
            c = Constraint("C({},{})".format([i,j],[i+1,j-1]),[variable_array[i][j], variable_array[i+1][j-1]])
            c = add_sat_tuple1(c, dom)
            cons.append(c)         
            
            c = Constraint("C({},{})".format([i,j],[i+1,j]),[variable_array[i][j], variable_array[i+1][j]])
            c = add_sat_tuple1(c, dom)
            cons.append(c)       
            
            c = Constraint("C({},{})".format([i,j],[i+1,j+1]),[variable_array[i][j], variable_array[i+1][j+1]])
            c = add_sat_tuple1(c, dom)
            cons.append(c)             
            
    
    #Missed some cases...
    if ((i == 0) and (j == 1)) or ((i == len(variable_array)-2) and (j == len(variable_array[0])-1)):
        
        c = Constraint("C({},{})".format([i,j],[i+1,j-1]),[variable_array[i][j], variable_array[i+1][j-1]])
        c = add_sat_tuple1(c, dom)
        cons.append(c)   
        
    if ((i == 0) and (j == len(variable_array[0])-2)) or ((i == len(variable_array)-2) and (j == 0)):
        
        c = Constraint("C({},{})".format([i,j],[i+1,j+1]),[variable_array[i][j], variable_array[i+1][j+1]])
        c = add_sat_tuple1(c, dom)
        cons.append(c)           
        
    return cons

def cons_row(cons, variable_array,i,j, dom):
    k = 1
    
    #As long as the index is within the bound
    while j+k < 10:
        
        #Check all the combinations within the row for variable [i,j]
        c = Constraint("C({},{})".format([i,j],[i,j+k]),[variable_array[i][j], variable_array[i][j+k]])
        c = add_sat_tuple1(c, dom)
        cons.append(c)        
        
        k += 1
        
    
    return cons

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    board_length = len(initial_tenner_board[0])
    variable_array = [[] for i in range(board_length)]
    vars = []
    cons = []
    
    #n by 10 board
    board = initial_tenner_board[0]
    
    #last row
    lastrow = initial_tenner_board[1]
    
    #Domain 
    dom = []
    for i in range(10):
        dom.append(i)    
    
    #Build variables
    for i in range(len(board)):
        
        for j in range(len(board[i])):
            
            #If no number is assigned
            if board[i][j] == -1:
                
                #Name is the coordinate of the variable
                #Domain 0-9 is assigned
                v = Variable('{}'.format([i,j]),[a+1 for a in range(-1,9)])
                vars.append(v)
                variable_array[i].append(v)
            else:
                
                #Domain of the assigned number is assigned
                v = Variable('{}'.format([i,j]),[board[i][j]])
                v.assign(board[i][j])
                
                #Need to have array of variables input into CSP class
                vars.append(v)
                
                #Need to have the grid for the output of the function
                variable_array[i].append(v)
                
    #Build constraints 
    for i in range(len(variable_array)):
        
        for j in range(len(variable_array[i])):
            
            #For the contiguous cells
            #Get list of constraints for each variable
            cons = cons_adjacent(cons, variable_array,i,j,dom) 
            
            #For the row constraint
            cons = cons_row(cons,variable_array,i,j,dom)
    
    #For the sum constraint
    for j in range(len(variable_array[0])):
        
        lis = []
        
        for i in range(len(variable_array)):
            
            #List of all the variables in a column
            lis.append(variable_array[i][j])
            
            
        c = Constraint("C(c{})".format(j),[l for l in lis])
        c = add_sat_tuple2(c,dom, len(variable_array), lastrow[j])
        cons.append(c)               
    
    tenner_csp = CSP("{}--tenner".format(len(variable_array)), vars)
    
    for c in cons:
        
        tenner_csp.add_constraint(c)
        
    return (tenner_csp,variable_array)
                   
                
    
#IMPLEMENT

##############################

def cons_row2(cons, v_arrayi,i,dom):
    '''
    Returns Constraints list with the newly built all-diff row constraint
    '''
    c = Constraint("C(r{})".format(i), v_arrayi)
    
    sat_tuples = []
        
    #10 possible numbers per variable (For unassigned), 10 variables in this constraint
    a = [[i for i in range(10)]for j in range(10)]
    
    #Can reduce the domain of each variables if they are assigned
    for i in range(10):
        
        if v_arrayi[i].is_assigned():
            
            a[i] = [v_arrayi[i].assignedValue]
    
    #All combinations of tuples
    for t in itertools.product(*a):  
        
        #Check if all the components are different in the tuple
        if len(t) > len(set(t)):
            
            #There are repeats in the tuple
            continue
        
        else:
            
            #The combination is satisfying
            sat_tuples.append(t) 
            
    c.add_satisfying_tuples(sat_tuples)      
    
    
    cons.append(c)
    
        
    
    return cons

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular,
       model_2 has a combination of n-nary 
       all-different constraints and binary not-equal constraints: all-different 
       constraints for the variables in each row, binary constraints for  
       contiguous cells (including diagonally contiguous cells), and n-nary sum 
       constraints for each column. 
       Each n-ary all-different constraint has more than two variables (some of 
       these variables will have a single value in their domain). 
       model_2 should create these all-different constraints between the relevant 
       variables.
    '''
    
    board_length = len(initial_tenner_board[0])
    variable_array = [[] for i in range(board_length)]
    vars = []
    cons = []
    
    #n by 10 board
    board = initial_tenner_board[0]
    
    #last row
    lastrow = initial_tenner_board[1]
    
    #Domain 
    dom = []
    for i in range(10):
        dom.append(i)    
    
    #Build variables
    for i in range(len(board)):
        
        for j in range(len(board[i])):
            
            #If no number is assigned
            if board[i][j] == -1:
                
                #Name is the coordinate of the variable
                #Domain 0-9 is assigned
                v = Variable('{}'.format([i,j]),[a+1 for a in range(-1,9)])
                vars.append(v)
                variable_array[i].append(v)
            else:
                
                #Domain of the assigned number is assigned
                v = Variable('{}'.format([i,j]),[board[i][j]])
                v.assign(board[i][j])
                
                #Need to have array of variables input into CSP class
                vars.append(v)
                
                #Need to have the grid for the output of the function
                variable_array[i].append(v)
                
    #Build constraints 
    for i in range(len(variable_array)):
        
        for j in range(len(variable_array[i])):
            
            #For the contiguous cells
            #Get list of constraints for each variable
            cons = cons_adjacent(cons, variable_array,i,j,dom) 
            
        #For the all-diff row constraint
        cons = cons_row2(cons,variable_array[i],i,dom)
    
    #For the sum constraint
    for j in range(len(variable_array[0])):
        
        lis = []
        
        for i in range(len(variable_array)):
            
            #List of all the variables in a column
            lis.append(variable_array[i][j])
            
            
        c = Constraint("C(c{})".format(j),[l for l in lis])
        c = add_sat_tuple2(c,dom, len(variable_array), lastrow[j])
        cons.append(c)               
    
    tenner_csp = CSP("{}--tenner".format(len(variable_array)), vars)
    
    for c in cons:
        
        tenner_csp.add_constraint(c)
        
    return (tenner_csp,variable_array)    

#IMPLEMENT