# Description
This is the accompanying code for the report "Timing on Labelled Petri Net Functions in a Stochastic Setting".  
This code tests the running time of the methods described in the paper "Reasoning on Labelled Petri Nets and Their Dynamics in a Stochastic Setting".  

# Requirements
All code is using python. The results analysis (Results Analysis.ipynb) is in a jupyter notebook.  
The following libraries are used: time, datetime, collections pandas, numpy, matplotlib.pyplot, sympy.  
The 'S_CONFORM' function requires a manual step provided by the code from the paper 'Automata Linear Dynamic Logic on Finite Traces' that may be found at https://github.com/RiccardoDeMasellis/FLLOAT.  

# Description of the Files
The code folder contains all the code to create PNP's and run the methods we are testing. The files contained in here are as follows:
Arc: Contains classes for arcs used by PN, RG and DFA objects  
DFA: Contains a class for a DFA objects  
Element: Contains classes for states, places and transitions  
Functions: Contains the logic for the four functions that are being tested  
LTL: Contains some functionality for handling LTL statements  
PetriNet: Contains classes for PN and PNP  
ProbDeclare: Contains a class for ProbDeclare models  
ReachabilityGraph: contains a class for RG objects  

Furthermore there are the following files used for the experiments:  
Outcome-ProbExperiment: Contains code testing the running time of the OUTCOME-PROB function  
PNPCreator: Contains functions which generate the PNP's that are used by the experiments  
Results Analysis: Contains code to preprocess and create graphs from the experimental results  
Trace-ProbExperiment: Contains code testing the running time of the TRACE-PROB function  
TraceTester: Contains functions for acquiring knowledge from lists of all the traces in a PNP  
Verify-ProbExperiment: Contains code testing the running time of the VERIFY-PROB function  

Furthermore, the Paper Graphs folder stores the PNP's and DFA's used by the experiments,
the Results folder contains the experimental results and the Testing Graphs folder contains graphs used for testing.
