from Code.PetriNet import PNP
from Code.DFA import DFA

from Code.Functions import trace_prob

from TraceTester import label_in_trace
from PNPCreator import create_repeated_choice, create_massively_parallel

from math import factorial
import time
from datetime import datetime
import pandas as pd

# Run trace-prob experiment for the repeated choice petri nets
if True:
    times = pd.DataFrame(columns = ['options', "choices", "traces", "states", "multi_states", "method_time", "trace_time"])

    seed = 103349 
    for choices in [2, 3, 4, 5, 7, 10, 13, 15, 20]:
        for options in [2, 3, 4, 5, 7, 10, 13, 15, 20]:
            number_of_traces = int(options**choices)
            number_of_states = int(choices)
            number_of_multi_states = int(choices*(choices+1))

            create_repeated_choice(f"Paper Graphs\\repeated_choices{options}-{choices}.txt", options, choices, seed)
            seed += 1

            pnp = PNP.read_text(f"Paper Graphs\\repeated_choices{options}-{choices}.txt")

            try:
                # Use the provided method (alt_solver)
                st = time.time()
                reachability_graph = pnp.create_reachability_graph()
                result = trace_prob(reachability_graph, ["A"]*choices, True)
                mt = time.time() - st
            except:
                mt = -1

            tt = -1
            if number_of_traces <= 10000000: #10 million
                # Use the trace method
                st = time.time()
                traces = pnp.get_traces()
                result = label_in_trace(";A"*choices, traces)
                tt = time.time() - st

            times.loc[len(times)] = [int(options), int(choices), number_of_traces, number_of_states, number_of_multi_states, round(mt, 2), round(tt, 2)]

            times.to_csv("Results/TP-RC_save.csv", index=False)

            print(choices, options)
            print(datetime.now().strftime("%H:%M:%S"))


# Run verify-prob experiment for the massively parallel petri nets
if True:
    times = pd.DataFrame(columns = ['options', "choices", "parallel_size", "traces", "states", "multi_states", "method_time", "trace_time"])

    seed = 103349 
    for choices in [1, 2, 3, 4, 5]:
        for parallel_size in [2, 3, 4, 5]:
            number_of_traces = int((factorial(choices*parallel_size) / factorial(choices)**parallel_size) * 2**(choices*parallel_size))
            number_of_states = int(choices**parallel_size)
            number_of_multi_states = int((choices**parallel_size) * (choices*parallel_size))

            create_massively_parallel(f"Paper Graphs\\massively_parallel{2}-{choices}-{parallel_size}.txt", 2, choices, parallel_size, 103349)
            seed += 1

            pnp = PNP.read_text(f"Paper Graphs\\massively_parallel{2}-{choices}-{parallel_size}.txt")

            try:
                # Use the provided method (alt_solver)
                st = time.time()
                reachability_graph = pnp.create_reachability_graph()
                result = trace_prob(reachability_graph, ["A"]*choices*parallel_size, True)
                mt = time.time() - st
            except:
                mt = -1

            tt = -1
            if number_of_traces <= 10000000: #10 million
                # Use the trace method
                st = time.time()
                traces = pnp.get_traces()
                result = label_in_trace(";A"*choices*parallel_size, traces)
                tt = time.time() - st

            times.loc[len(times)] = [int(2), int(choices), int(parallel_size), number_of_traces, number_of_states, number_of_multi_states, round(mt, 2), round(tt, 2)]

            times.to_csv("Results/TP-MP_save.csv", index=False)

            print(choices, parallel_size)
            print(datetime.now().strftime("%H:%M:%S"))