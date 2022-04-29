#packages
import numpy as np
import pandas as pd  
import re
import os
#define a class object named task:
class Task(object):
    def __init__(self,activity,predecessors,duration):
        self.activity = activity.upper()
        self.predecessors = predecessors
        self.duration = duration
        self.earlyStart = 0
        self.earlyfinish = 0
        self.successors = []
        self.lastStart = 0
        self.lastfinish = 0
        self.slack = 0
        self.critical = ""

    def computeSlack(self):
        self.slack = self.lastfinish - self.earlyfinish
        if self.slack > 0 :
            self.critical = "NO"
        else:
            self.critical = "YES"
        

#function to get data from excel and return a pandas data frame 
def readData(excelFile):
    global mydata
    mydata = pd.read_csv(excelFile)
    return mydata

#function to compute for duration the task or 
def computeDuration(mydata):
    mydata["DURATION"] = np.ceil((mydata["OPT"]+ mydata["MOST"]*4 + mydata["PESS"])/6)
    return mydata

#function to creat a task object:
def creatTask(mydata):
    taskObject = []
    
    for i in range(len(mydata)):
        taskObject.append(Task(mydata["ACTIVITY"][i],
        mydata["PREDECESSORS"][i],mydata["DURATION"][i]))
        
    return (taskObject)

def forwardPass(taskObject):
    for task in taskObject:
        if type(task.predecessors) is str: #type string
            #make the string uppercase
            task.predecessors = task.predecessors.upper()
            ef = [] #store the EF of all of the task's predecessors..
            #get the maximum latestfinish
            for j in task.predecessors:
                for t in taskObject:
                    if t.activity == j :
                        ef.append(t.earlyfinish)
                task.earlyStart = max(ef)
            del ef
        else:
            task.earlyStart = 0
            
        task.earlyfinish = task.earlyStart + task.duration

def backwardPass(taskObject):
    pred = []
    eF = []
    
    
    for task in taskObject:
        if type(task.predecessors) == str :
            for j in task.predecessors:
                pattern = re.compile(r'[A-Z]')
                match = pattern.finditer(j)
                for r in match:
                    pred.append(j)
                    for m in taskObject:
                        if m.activity == j:
                            m.successors.append(task.activity)
        eF.append(task.earlyfinish)
    
    for task in reversed(taskObject):
        if task.activity not in pred:
            task.lastfinish = max(eF)
        else:
            minLs = []
            for x in task.successors:
                for t in (taskObject):
                    if t.activity == x:
                        minLs.append(t.lastStart)
            task.lastfinish = min(minLs)
            del minLs
        task.lastStart = task.lastfinish - task.duration

def slack(taskObject):
    for task in taskObject:
        task.computeSlack()


def updateDataframe(df,TaskObject):
    df2 = pd.DataFrame({
        'ACTIVITY':df["ACTIVITY"],
        'PREDECESSORS': df ["PREDECESSORS"],
        'OPT':df["OPT"],
        'MOST':df["MOST"],
        'PESS':df["PESS"],
        'DURATION':df["DURATION"],
        "ES":pd.Series([task.earlyStart for task in TaskObject]),
        "EF":pd.Series([task.earlyfinish for task in TaskObject]),
        "LS":pd.Series([task.lastStart for task in TaskObject]),
        "LF":pd.Series([task.lastfinish for task in TaskObject]),
        "SLACK":pd.Series([task.slack for task in TaskObject]),
        "CRITICAL?":pd.Series([task.critical for task in TaskObject])})
    return (df2)


def main():
    pd.set_option('display.width',1000)
    os.system("clear")
    df = readData("network.csv")
    print("Loaded data:")
    print(df)
    
    df = computeDuration(df)
    taskObject = creatTask(df)
    
    forwardPass(taskObject)
    backwardPass(taskObject)
    slack(taskObject)
    
    finaldf =updateDataframe(df,taskObject)
    print("\nResults:")
    print(finaldf)
    
    print("\nResult saved to pertcpm.csv\n")
    finaldf.to_csv("pertcpm.csv",index = False)
#run the program:
    
main()









# visualization
import seaborn as sns
import matplotlib.pyplot as plt
#input data
project_data = pd.read_csv("network.csv" )
project_data = project_data.drop('Unnamed: 5', axis = 1)
project_data.index
project_data = project_data.drop([11,12,13,14,15])







#setup number of trials
num_of_trials = 1000
num_bins = 100
points = [0] * num_of_trials


data = pd.DataFrame(project_data, columns=["optimistic", "Most likely", 
                                  "pessimistic"])
data["activity"]=project_data["Activity"]
# Get the DataFrame column names as a list
clist = list(data.columns)
# Rearrange list the way you like 
clist_new = clist[-1:]+clist[:-1]   # brings the last column in the first place
# Pass the new list to the DataFrame - like a key list in a dict 
data =data[clist_new]
#creat NAN value
data["mean"] = np.nan
data["var"]= np.nan
#for i in num_of_trials:
for j in range(11):
    #caculate mu & std
    mu=(data['optimistic'][j]+(4*data["Most likely"][j])+data["pessimistic"][j])/6
    var=((data["pessimistic"][j]-data['optimistic'][j])/6)**2
    data["mean"][j] = mu
    data["var"][j]= var
    
    
    
    r = np.random.normal(mu,math.sqrt(var),num_of_trials)
    points += r



adjacency_matrix = get_adjacency_matrix(project_data,sep, nan_value)

#project networks
G = nx.DiGraph()

for index,activity in project_data.iterrows():
    
    G.add_node(activity[0],pos=(index,index+random.randint(0,14)))
    
    for immediate_predecessor in activity[1].split(sep):
        if(immediate_predecessor != nan_value):
            G.add_edge(immediate_predecessor, activity[0], weight=1)
            
#print('There are %d nodes in the graph with %d edges'%(G.number_of_edges(), G.number_of_nodes()))

pos=nx.get_node_attributes(G,'pos')
nx.draw(G, pos, node_color='gold', edge_color='grey',with_labels=True, font_weight='bold')



























# fig=plt.figure(figsize=(16,10))
# ax = fig.add_subplot(111)
# ax2 = ax.twinx()
# ax.set_xlabel("Duration",fontsize=12)

# ax.set_ylabel("Probability",labelpad=3) 
# ax2.set_ylabel("Frequency",labelpad=3) 
# ax.set_ylim(0,35)
# ax.yaxis.tick_right()
# ax2.yaxis.tick_left()
# plt.subplots_adjust(top=0.9)
# fig.suptitle("Forecast : Project completion time")
# ax.set_title("Frequency chart")
# n, bins, patches = plt.hist(points, num_bins, 
#                             range = (points.min(), points.max()),
#                             color = "skyblue", lw=1, 
#                             edgecolor="steelblue", 
#                             weights=[1/num_of_trials]*
#                             num_of_trials)
# plt.show()



#建構path(建構path全部家一起)

  


