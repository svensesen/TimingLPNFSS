def label_in_trace(label, traces):
    return sum([trace[1] for trace in traces if label in trace[0].split(";")])

def multiple_label_in_trace(label, traces, times):
    return sum([trace[1] for trace in traces if trace[0].split(";").count(label) >= times])

def last_label(label, traces):
    return sum([trace[1] for trace in traces if label == trace[0].split(";")[-1]])

def trace_checker(trace, traces):
    return sum([sub_trace[1] for sub_trace in traces if trace == sub_trace])