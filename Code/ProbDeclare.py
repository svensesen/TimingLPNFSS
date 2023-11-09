class ProbDeclare():
    def __init__(self):
        self.symbols = []
        self.crisp_constraints = []
        self.probability_constraints = []
    
    def get_scenarios(self):
        def get_scenario_recursive(current, remaining, positive):
            if not remaining:
                positive.append(set(sorted(current)))
            else:
                get_scenario_recursive(current + [remaining[0]], remaining[1:], positive)
                get_scenario_recursive(current, remaining[1:], positive)

        scenarios = []
        get_scenario_recursive([], self.probability_constraints.copy(), positive)
        return [Scenario(positive, set(input)-positive, set(crisp_constraints)) for positive in scenarios]


class PC():
    def __init__(self, _LTL_formula, _operator, _probability):
        self.LTL_formula = _LTL_formula
        self.operator = _operator
        self.probability = _probability

class Scenario():
    def __init__(self, _true_constraints, _false_constraints, _crisp_constraints):
        self.true_constraints = _true_constraints
        self.false_constraints = _false_constraints
        self.crisp_constraints = _crisp_constraints
    
    def characteristic_formula(self):
        true_formulas = [constraint.LTL_formula for constraint in self.true_constraints]
        false_formulas = ["¬"+constraint.LTL_formula for constraint in self.false_constraints]

        all_formulas = true_formulas + false_formulas + self.crisp_constraints

        return "∧".join([f"({formula})" for formula in all_formulas])
    
    # Check if this scenario is valid for a given probability p
    def is_valid(self, p):
        for constraint in self.true_constraints:
            match constraint.condition:
                case "=": if not value1 == value2: return False
                case "!=": if not value1 != value2: return False
                case ">": if not return value1 > value2: return False
                case "<": if not return value1 < value2: return False
                case ">=": if not return value1 >= value2: return False
                case "=>": if not return value1 >= value2: return False
                case "<=": if not return value1 <= value2: return False
                case "=<": if not return value1 <= value2: return False
        
        return True



