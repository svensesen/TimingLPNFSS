from collections import defaultdict


# This is a labelled transitions system
class ReachabilityGraph:
    def __init__(self):
        self.states = []
        self.identifier_to_state = defaultdict(lambda: None)
        self.initial_state = None
        self.deadlock_states = [] # Also called accepting states

    def add_initial_state(self, _initial_tokens_per_place):
        self.initial_state = self.add_state(_initial_tokens_per_place)
        return self.initial_state

    def add_state(self, _tokens_per_place,):
        state = RG_State(RG_State.tpp_to_id(_tokens_per_place), _tokens_per_place)
        self.states.append(state)
        self.identifier_to_state[state.identifier] = state
        return state

    def ttp_to_state(self, tokens_per_place):
        return self.identifier_to_state[RG_State.tpp_to_id(tokens_per_place)]
    
    def append_initial_state(self, state):
        self.initial_state = state
        self.append_state(state)

    def append_deadlock_state(self, state):
        self.deadlock_states.append(state)
        self.append_state(state)

    def append_state(self, state):
        self.states.append(state)
        self.identifier_to_state[state.identifier] = state
    
    
    

from Code.Element import RG_State