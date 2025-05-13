from collections import deque

def epsilon_closure(state_set, transitions):
    closure = set(state_set)
    stack = list(state_set)
    while stack:
        state = stack.pop()
        for next_state in transitions.get(state, {}).get('ε', set()):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def move(state_set, symbol, transitions):
    result = set()
    for state in state_set:
        result |= transitions.get(state, {}).get(symbol, set())
    return result

def nfa_to_dfa(nfa):
    dfa_states = []
    dfa_transitions = {}
    state_map = {}
    dfa_accept_states = set()

    start_closure = frozenset(epsilon_closure({nfa['start_state']}, nfa['transitions']))
    queue = deque([start_closure])
    state_map[start_closure] = 'S0'
    dfa_states.append('S0')
    state_count = 1

    while queue:
        current = queue.popleft()
        current_name = state_map[current]
        dfa_transitions[current_name] = {}

        for symbol in nfa['alphabet']:
            move_result = move(current, symbol, nfa['transitions'])
            closure_result = frozenset(epsilon_closure(move_result, nfa['transitions']))

            if not closure_result:
                continue

            if closure_result not in state_map:
                state_map[closure_result] = f'S{state_count}'
                dfa_states.append(f'S{state_count}')
                queue.append(closure_result)
                state_count += 1

            dfa_transitions[current_name][symbol] = state_map[closure_result]

    for nfa_set, name in state_map.items():
        if nfa['accept_states'] & nfa_set:
            dfa_accept_states.add(name)

    return {
        'states': set(dfa_states),
        'alphabet': nfa['alphabet'],
        'transitions': dfa_transitions,
        'start_state': 'S0',
        'accept_states': dfa_accept_states
    }

nfa = {
    'states': {'q0', 'q1', 'q2'},
    'alphabet': {'a', 'b'},
    'transitions': {
        'q0': {'ε': {'q1'}, 'a': {'q0'}},
        'q1': {'b': {'q2'}},
        'q2': {}
    },
    'start_state': 'q0',
    'accept_states': {'q2'}
}

dfa = nfa_to_dfa(nfa)
from pprint import pprint
pprint(dfa)
