from Code.PetriNet import PNP
from Code.DFA import DFA

from Code.Functions import verify_prob

from TraceTester import label_in_trace, multiple_label_in_trace
from PNPCreator import create_repeated_choice, create_massively_parallel, create_has_happened_DFA, create_multi_has_happened_DFA

from math import factorial
import time
from datetime import datetime
import pandas as pd


# Run verify-prob experiment for the repeated choice petri nets
if True:
    times = pd.DataFrame(columns = ['options', "choices", "times_happened", "traces", "states", "multi_states", "method_time", "trace_time"])

    seed = 103349 
    for choices in [2, 3, 5, 7, 10]:
        for options in [2, 3, 5, 7, 10]:
            for times_happened in [2, 3, 5, 7, 10]:
                number_of_traces = int(options**choices)
                number_of_states = int(choices)
                number_of_multi_states = int(choices*times_happened)

                create_repeated_choice(f"Paper Graphs\\repeated_choices{options}-{choices}.txt", options, choices, seed)
                seed += 1
                create_multi_has_happened_DFA(f"Paper Graphs\\A has happened {times_happened}X ({options} options).txt", "A", options, times_happened)

                pnp = PNP.read_text(f"Paper Graphs\\repeated_choices{options}-{choices}.txt")

                try:
                    # Use the provided method (alt_solver)
                    st = time.time()
                    reachability_graph = pnp.create_reachability_graph()
                    dfa = DFA.read_text(f"Paper Graphs\\A has happened {times_happened}X ({options} options).txt")
                    result = verify_prob(reachability_graph, dfa, True)
                    mt = time.time() - st
                except:
                    mt = -1

                tt = -1
                if number_of_traces <= 10000000: #10 million
                    # Use the trace method
                    st = time.time()
                    traces = pnp.get_traces()
                    result = multiple_label_in_trace("A", traces, times_happened)
                    tt = time.time() - st

                times.loc[len(times)] = [int(options), int(choices), int(times_happened), number_of_traces, number_of_states, number_of_multi_states, round(mt, 2), round(tt, 2)]

                times.to_csv("Results/VP-RC_save.csv", index=False)

                print(choices, options, times_happened)
                print(datetime.now().strftime("%H:%M:%S"))


# Run verify-prob experiment for the massively parallel petri nets
if True:
    times = pd.DataFrame(columns = ['options', "choices", "parallel_size", "times_happened,", "traces", "states", "multi_states", "method_time", "trace_time"])

    options = 2

    seed = 103349 
    for choices in [1, 2, 3, 4, 5]:
        for parallel_size in [2, 3, 4, 5]:
            for times_happened in [2, 3, 5, 7, 10]:
                number_of_traces = int((factorial(choices*parallel_size) / factorial(choices)**parallel_size) * options**(choices*parallel_size))
                number_of_states = int(choices**parallel_size)
                number_of_multi_states = int((choices**parallel_size) * times_happened)

                create_massively_parallel(f"Paper Graphs\\massively_parallel{options}-{choices}-{parallel_size}.txt", options, choices, parallel_size, 103349)
                seed += 1
                create_multi_has_happened_DFA(f"Paper Graphs\\A has happened {times_happened}X ({options*parallel_size} options).txt", "A", options*parallel_size, times_happened)

                pnp = PNP.read_text(f"Paper Graphs\\massively_parallel{options}-{choices}-{parallel_size}.txt")

                try:
                    # Use the provided method (alt_solver)
                    st = time.time()
                    reachability_graph = pnp.create_reachability_graph()
                    dfa = DFA.read_text(f"Paper Graphs\\A has happened {times_happened}X ({2*parallel_size} options).txt")
                    result = verify_prob(reachability_graph, dfa, True)
                    mt = time.time() - st
                except:
                    mt = -1

                tt = -1
                if number_of_traces <= 10000000: #10 million
                    # Use the trace method
                    st = time.time()
                    traces = pnp.get_traces()
                    result = multiple_label_in_trace("A", traces, times_happened)
                    tt = time.time() - st

                times.loc[len(times)] = [int(options), int(choices), int(parallel_size), int(times_happened), number_of_traces, number_of_states, number_of_multi_states, round(mt, 2), round(tt, 2)]

                times.to_csv("Results/VP-MP_save.csv", index=False)

                print(choices, parallel_size, times_happened)
                print(datetime.now().strftime("%H:%M:%S"))