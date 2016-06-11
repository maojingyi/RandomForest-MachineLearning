from math import log

#Example of data structure
my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]


# One of the more popular methods for consructing trees, CART (Classification And Regression Trees),
# was developed by Leo Breiman https://www.stat.berkeley.edu/~breiman/papers.html. CART is a recursive
# partitioning method that builds classification and regression trees for predicting continuous and
# categorical variables.
class DecisionNode:
    def __init__(self,column=-1,value=None,results=None,trueNodes=None,falseNodes=None):
        self.column=column # column index of criteria being tested
        self.value=value # vlaue necessary to get a true result
        self.results=results # dict of results for a branch, None for everything except endpoints
        self.trueNodes=trueNodes # true decision nodes
        self.falseNodes=falseNodes # false decision nodes


# Divides a set on a specific column. Can handle numeric or nominal values
def divideSet(rows,column,value):
    # Make a function that tells us if a row is in the first group
    # (true) or the second group (false)
    split_function=None
    # for numerical values
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    # for nominal values
    else:
        split_function=lambda row:row[column]==value

   # Divide the rows into two sets and return them
    set1=[row for row in rows if split_function(row)] # if split_function(row)
    set2=[row for row in rows if not split_function(row)]
    return (set1,set2)


# Create counts of possible results (last column of each row is the result)
def uniqueCounts(rows, classPosition = 0):
    results={}
    for row in rows: # The result is the last column
        if classPosition == 0: classPosition = len(row)
        lastRow=row[classPosition - 1]
        if lastRow not in results: results[lastRow]=0
        results[lastRow]+=1
    return results


# Information entropy tells how much information there is in an event. In general, the more uncertain or
# random the event is, the more information it will contain.
# The lower the entropy value is, the fewer questions we need to ask to predict certain outcome

# classPosition is the location of the class in the dataset(number of row)
def entropy(rows, classPosition = 0):
    log2=lambda x:log(x)/log(2)
    results=uniqueCounts(rows, classPosition)
    # Now calculate the entropy
    entropy=0.0
    for row in results.keys():
        probability=float(results[row])/len(rows) # current probability of class
        entropy=entropy-probability*log2(probability)
    return entropy


def buildTree(rows, scorefun=entropy):
    if len(rows) == 0: return DecisionNode()
    current_score = scorefun(rows)

    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1	# last column is result
    for col in range(0, column_count):
        # find different values in this column
        column_values = set([row[col] for row in rows])

        # for each possible value, try to divide on that value
        for value in column_values:
            set1, set2 = divideSet(rows, col, value)

            # Information gain
            p = float(len(set1)) / len(rows)
            gain = current_score - p*scorefun(set1) - (1-p)*scorefun(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    if best_gain > 0:
        trueBranch = buildTree(best_sets[0])
        falseBranch = buildTree(best_sets[1])
        return DecisionNode(column=best_criteria[0], value=best_criteria[1],
                trueNodes=trueBranch, falseNodes=falseBranch)
    else:
        return DecisionNode(results=uniqueCounts(rows))



def printTree(tree,indent=''):
    # Is this a leaf node?
    if tree.results!=None:
        print str(tree.results)
    else:
        # Print the criteria
        print 'Column ' + str(tree.column)+' : '+str(tree.value)+'? '

        # Print the branches
        print indent+'True->',
        printTree(tree.trueNodes,indent+'  ')
        print indent+'False->',
        printTree(tree.falseNodes,indent+'  ')


def printDataset(rows):
    for row in rows:
        print row


# Moves one column in the dataset to the last of the dataset
def postponeColumn(rows, columToPostpone):
    for row in rows:
        row.append(row[columToPostpone])
        del row[columToPostpone]


# When building the decision tree we want to first move the column we want to classify to the last
postponeColumn(my_data, 1)
printTree(buildTree(my_data))