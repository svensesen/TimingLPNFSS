from Code.PetriNet import PNP

from TraceTester import last_label
from PNPCreator import create_multi_line

from Code.Functions import alt_outcome_prob

import time
from datetime import datetime
import pandas as pd

# Run outcome-prob experiment for the multi line petri nets
if True:
    times = pd.DataFrame(columns = ['lines', "choices", "traces", "states", "multi_states", "method_time", "trace_time"])

    seed = 103349 
    for choices in [2, 3, 4, 5, 7, 10, 13, 15, 20]:
        for lines in [2, 3, 4, 5, 7, 10, 13, 15, 20]:
            number_of_traces = int(lines**choices)
            number_of_states = int(choices*lines + 1)
            number_of_multi_states = int(choices*lines + 1)

            create_multi_line(f"Paper Graphs\\multi_line{lines}-{choices}.txt", lines, choices, seed)
            seed += 1

            pnp = PNP.read_text(f"Paper Graphs\\multi_line{lines}-{choices}.txt")
            
            try:
                # Use the provided method (alt_solver)
                st = time.time()
                reachability_graph = pnp.create_reachability_graph()
                result = alt_outcome_prob(reachability_graph, [reachability_graph.identifier_to_state["P)qend0:1"]])
                mt = time.time() - st
            except:
                mt = -1

            tt = -1
            if number_of_traces <= 10000000: #10 million
                # Use the trace method
                st = time.time()
                traces = pnp.get_traces()
                result = last_label("A", traces)
                tt = time.time() - st

            times.loc[len(times)] = [int(lines), int(choices), number_of_traces, number_of_states, number_of_multi_states, round(mt, 2), round(tt, 2)]

            times.to_csv("Results/OP-ML_save.csv", index=False)

            print(choices, lines)
            print(datetime.now().strftime("%H:%M:%S"))