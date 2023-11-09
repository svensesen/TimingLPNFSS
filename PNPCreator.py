import os
import random


# Lines are the number of lines that can be traversed and switched between 
# has this many end states
# Choices are the number of choices in a row
def create_multi_line(file_name, lines, choices, seed):
    random.seed = seed
    alphabet = list(map(chr, range(65, 91)))

    if os.path.isfile(file_name):
        os.remove(file_name)
    f = open(file_name, "x")

    f.write("i q0 1\n") #initial state
    f.write("p q0\n") #starting place

    for i in range(lines): #deadlock states
        f.write(f"d qend{i} 1\n") 

    for i in range(choices):
        for j in range(lines):
            #next place on same line
            if i == (choices - 1): f.write(f"p qend{j}\n") 
            else: f.write(f"p q{i+1}{j}\n")

            if (i == 0) and (j != 0):
                continue

            probabilities = [round(random.random(),2) for _ in range(lines)]
            probabilities = [i/sum(probabilities) for i in probabilities]
            
            for k in range(len(probabilities)):
                f.write(f"t {alphabet[k]}({i*lines + j}) {probabilities[k]}\n") #transition

                #place to transition
                if i == 0: f.write(f"a q0 {alphabet[k]}({i*lines + j})\n") 
                else: f.write(f"a q{i}{j} {alphabet[k]}({i*lines + j})\n") 
                #transition to place
                if i == (choices - 1): f.write(f"a {alphabet[k]}({i*lines + j}) qend{k}\n")
                else: f.write(f"a {alphabet[k]}({i*lines + j}) q{i+1}{k}\n") 


# Options are the number of options per choice
# Choices are the number of choices in a row
def create_repeated_choice(file_name, options, choices, seed):
    random.seed = seed
    alphabet = list(map(chr, range(65, 91)))

    if os.path.isfile(file_name):
        os.remove(file_name)
    f = open(file_name, "x")

    f.write("i q0 1\n") #initial state
    f.write(f"d q{choices} 1\n") #deadlock state
    f.write("p q0\n") #starting place

    for i in range(choices):
        f.write(f"p q{i+1}\n") #next place

        probabilities = [round(random.random(),2) for _ in range(options)]
        probabilities = [i/sum(probabilities) for i in probabilities]

        for j in range(options):
            f.write(f"t {alphabet[j]}({i}) {probabilities[j]}\n") #transition
            f.write(f"a q{i} {alphabet[j]}({i})\n") #place to transition
            f.write(f"a {alphabet[j]}({i}) q{i+1}\n") #transition to place


# Options are the number of options per choice
# Choices are the number of choices in a row
# Parallel_size is the amount of patterns going in parallel
def create_massively_parallel(file_name, options, choices, parallel_size, seed):
    random.seed = seed
    alphabet = list(map(chr, range(65, 91)))

    if os.path.isfile(file_name):
        os.remove(file_name)
    f = open(file_name, "x")

    f.write("i q0 1\n") #initial state
    f.write(f"d q{choices+2} 1\n") #deadlock state
    f.write("p q0\n") #starting place
    f.write(f"p q{choices+2}\n") #ending place

    f.write("t tau(0) 1\n") #tau startoff
    f.write("a q0 tau(0)\n") #starting tau connection

    f.write("t tau(1) 1\n") #tau endoff
    f.write(f"a tau(1) q{choices+2}\n") #ending tau connection
    
    for i in range(1, parallel_size+1):
        f.write(f"p q1{i}\n") # starting place for parallel
        f.write(f"a tau(0) q1{i}\n") #tau to parallel starting
        f.write(f"a q{choices+1}{i} tau(1)\n") #parallel ending to tau
        
        for j in range(1, choices+1):
            f.write(f"p q{j+1}{i}\n") #next place

            probabilities = [round(random.random(),2) for _ in range(options)]
            probabilities = [i/sum(probabilities) for i in probabilities]

            for k in range(options):
                f.write(f"t {alphabet[k+(i-1)*options]}({j}{i}) {probabilities[k]}\n") #transition
                f.write(f"a q{j}{i} {alphabet[k+(i-1)*options]}({j}{i})\n") #place to transition
                f.write(f"a {alphabet[k+(i-1)*options]}({j}{i}) q{j+1}{i}\n") #transition to place


def create_has_happened_DFA(file_name, happened, number_of_labels):
    alphabet = list(map(chr, range(65, 91)))

    if os.path.isfile(file_name):
        os.remove(file_name)
    f = open(file_name, "x")

    f.write(f"l {' '.join(alphabet[0:number_of_labels])}\n") #labels
    f.write("s q0\ns q1\n") #states
    f.write(f"a q0 q1 {happened}\na q0 q0 -{happened}\na q1 q1 +\n") #arcs
    f.write("f q1\n") #final state
    f.write("i q0\n") #initial state


def create_multi_has_happened_DFA(file_name, happened, number_of_labels, number_of_times):
    alphabet = list(map(chr, range(65, 91)))

    if os.path.isfile(file_name):
        os.remove(file_name)
    f = open(file_name, "x")

    f.write(f"l {' '.join(alphabet[0:number_of_labels])}\n") #labels
    f.write("i q0\n") #initial state

    for i in range(number_of_times):
        f.write(f"s q{i}\n") # Create state
        f.write(f"a q{i} q{i+1} {happened}\n") # Create arc to next state
        f.write(f"a q{i} q{i} -{happened}\n") # Create looping arc
    
    f.write(f"s q{i+1}\n") #last state
    f.write(f"a q{i+1} q{i+1} +\n") #last state loop
    f.write(f"f q{i+1}\n") #final state
    