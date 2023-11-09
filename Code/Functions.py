import sympy
from sympy.solvers.solveset import linsolve

# Section 4
def outcome_prob(reachability_graph, desired_outcomes):
    if not desired_outcomes:
        raise ValueError("desired_outcomes can't be empty")
    symbols = {}
    equations = []

    # Create a symbol for each state
    for state in reachability_graph.states:
        # The replace is required since ':' is wrongly interpreted
        symbols[state] = sympy.symbols(state.identifier.replace(":", ";"))

    # Create a formula for each state
    for state in reachability_graph.states:
        # If the state is a deadlock the value depends if it desired or not
        if not state.outgoing_arcs:
            equations.append(sympy.Eq(symbols[state], 1 if state in desired_outcomes else 0))
            
        # If the state is not a deadlock the value depends on the outgoing arcss
        else:
            outgoing_probabilities = [sympy.Float(arc.odds)*symbols[arc.output] for arc in state.outgoing_arcs]
            equations.append(sympy.Eq(symbols[state], sum(outgoing_probabilities)))

    # Solve the linear equation
    solution = sympy.solve(equations, list(symbols.values()))

    # Update all indeterminate values to 0
    simplified_solution = {key: value if not isinstance(value, sympy.Expr) else value.subs({s: 0 for s in value.free_symbols}) for key, value in solution.items()}

    # Returns the result for the starting square
    return float(simplified_solution.get(symbols[reachability_graph.initial_state], 0.0))


# An alternative method for outcome prob that uses (supposedly) better solving
# Section 4
def alt_outcome_prob(reachability_graph, desired_outcomes):
    if not desired_outcomes:
        raise ValueError("desired_outcomes can't be empty")
    symbols = {}
    equations = []

    # Create a symbol for each state
    for state in reachability_graph.states:
        # The replace is required since ':' is wrongly interpreted
        symbols[state] = sympy.symbols(state.identifier.replace(":", ";"))

    # Create a formula for each state
    for state in reachability_graph.states:
        # If the state is a deadlock the value depends if it desired or not
        if not state.outgoing_arcs:
            if state in desired_outcomes:
                equations.append(symbols[state] - 1)
            
            else:
                equations.append(symbols[state])
            
        # If the state is not a deadlock the value depends on the outgoing arcss
        else:
            outgoing_probabilities = [sympy.Float(arc.odds)*symbols[arc.output] for arc in state.outgoing_arcs]
            equations.append(sum(outgoing_probabilities) - symbols[state])

    # Gets a list of the (strings of the) symbols
    symbols_list = list(symbols.values())
    symbols_string_list = list(symbols.keys())

    # Solve the linear equation
    solution = linsolve(equations, symbols_list)
    solution = list(solution)[0]

    # Update all indeterminate values to 0
    simplified_solution = {symbols_string_list[i]: solution[i].subs({s: 0 for s in solution[i].free_symbols}) for i in range(len(solution))}
    
    # Returns the result for the starting square
    return float(simplified_solution[reachability_graph.initial_state])


# Section 5.1
# Warning, this edits the dfa
def verify_prob(reachability_graph, dfa, alt = False):

    # Step 1, add self tau arcs to each state
    for state in dfa.states:
        DFA_Arc(state, state, "tau")
    
    combined_reachability_graph = ReachabilityGraph()

    # Step 2 combine automata
    # Create combined states (also initial and deadlock states)
    for dfa_state in dfa.states:
        for rg_state in reachability_graph.states:
            new_state = RG_State(f"{dfa_state.identifier}+{rg_state.identifier}", rg_state.tokens_per_place)
            
            if (dfa_state in dfa.final_states) and (rg_state in reachability_graph.deadlock_states):
                combined_reachability_graph.append_deadlock_state(new_state)

            elif (dfa_state == dfa.initial_state) and (rg_state == reachability_graph.initial_state):
                combined_reachability_graph.append_initial_state(new_state)

            else:
                combined_reachability_graph.append_state(new_state)
    
    # Create the combined arcs
    for rg_state in reachability_graph.states:
        for arc in rg_state.outgoing_arcs:
            for dfa_state in dfa.states:
                input = combined_reachability_graph.identifier_to_state[f"{dfa_state.identifier}+{rg_state.identifier}"]
                output = combined_reachability_graph.identifier_to_state[f"{dfa_state.label_to_outgoing_arc[arc.transition.label].output.identifier}+{arc.output.identifier}"]
                GraphArc(input, output, arc.odds, arc.transition)
    
    # Step 3 return outcome_prob result
    if alt:
        return alt_outcome_prob(combined_reachability_graph, combined_reachability_graph.deadlock_states)
    else:
        return outcome_prob(combined_reachability_graph, combined_reachability_graph.deadlock_states)


# Section 5.2
def trace_prob(reachability_graph, trace, alt = False):
    labels = {arc.transition.label for state in reachability_graph.states for arc in state.outgoing_arcs}
    dfa = DFA()

    initial_state = dfa.add_state("s0")
    dfa.initial_state = initial_state

    # The state you reach upon a mistake
    error_state = dfa.add_state("sr")
    for label in labels:
        DFA_Arc(error_state, error_state, label)

    last_state = initial_state
    number = 1
    for transition_label in trace:
        new_state = dfa.add_state(f"s{number}")
        number += 1

        # Add arc between current and next state
        DFA_Arc(last_state, new_state, transition_label)

        # Add an arc to the error state on all other labels
        for label in labels - {transition_label}:
            DFA_Arc(last_state, error_state, label)
        
        last_state = new_state
    
    # Setup the single final state
    dfa.final_states = [last_state]
    for label in labels:
        DFA_Arc(last_state, error_state, label)
    
    return verify_prob(reachability_graph, dfa, alt)


# Section 6
def s_conform(reachability_graph, prob_declare):

    # TODO filter for consistent scenarios
    scenarios = prob_declare.get_scenarios()

    for scenario in scenarios:
        characteristic_formula = scenario.get_characteristic_formula()
        scenario_dfa = DFA.read_formula(characteristic_formula) #TODO, this
        p = verify_prob(reachability_graph, scenario_dfa)

        # Check if this scenario is valid
        if not scenario.is_valid(p):
            return False

    return True



from Code.DFA import DFA
from Code.Element import RG_State
from Code.Arc import DFA_Arc, GraphArc
from Code.ReachabilityGraph import ReachabilityGraph