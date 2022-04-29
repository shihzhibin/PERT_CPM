# Project_Management(PERT_CPM) 
### Theme: Use PERT to decide routes which one is critical path

### **Team Member**    

| 編輯者       |    暱稱         |                      LinkedIn                                                            |
| :-----------:|:-----------:   |:---------------------------------------------------------------------------------------: |
|  施智臏      | ZHI-BIN SHIH     | [https://www.linkedin.com/in/zhibin-shih-9a0a711a9/](https://www.linkedin.com/in/zhibin-shih-9a0a711a9/)     
|  Mr.Tsai    |  Louie Tsai       | 
### **Reference**
Author:PinoyStat  ,   Youtube: https://www.youtube.com/watch?v=UXPeO2d9nSs  
## Tutorial of the PERT_CPM
<details open="open">
  <summary><b>Table of Contents</b></summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
      <ul>
        <li><a href="#PERT_CPM">PERT_CPM</a></li>
    </li>
      </ul>
    <li>
      <a href="#the-model">python</a>
       <ul>
        <li><a href="#package">Input package</a></li>
        <li><a href="#Object">Define a class object named task</a></li>
        <li><a href="#Function">Define Function to input data or compute data </a></li>
        <li><a href="#Output result">Determine the critical path from the result</a></li>
         
# __Introduction__
If you are faced with many tasks at work, how to decide which tasks to perform first.Searching online resources suggest PERT(__Program Evaluation and Review Technique__) to schedule tasks.The program evaluation and review technique (PERT) is a statistical tool used in project management, which was designed to analyze and represent the tasks involved in completing a given project.
## __PERT_CPM__
> __PERT__ is a method of analyzing the tasks involved in completing a given project, especially the time needed to complete each task and to identify the minimum time needed to complete the total project. It incorporates uncertainty by making it possible to schedule a project while not knowing precisely the details and durations of all the activities.On the otherhand PERT and CPM are complementary tools, because __CPM__ employs one time estimation and one cost estimation for each activity; __PERT__ may utilize three time estimates (__optimistic, expected, and pessimistic__) and no costs for each activity.
 
# __The Model__
## __Package__
```python 
#Download package
import numpy as np
import pandas as pd  
import re
import os 
```         
## __Object__         
```python      
#Define a class object named task:
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
#Calculate the slack(Slack Time = LST – EST)
    def computeSlack(self):
        self.slack = self.lastfinish - self.earlyfinish
        if self.slack > 0 :
            self.critical = "NO"
        else:
            self.critical = "YES"
```
## __Function__   
