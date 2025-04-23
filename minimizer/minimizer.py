# Imports
import re
from collections import defaultdict
import graphviz
from google.colab import files

# DFA class
class DFA:
    def __init__(self, alphabet, states, initial, finals, transitions):
        self.alphabet = alphabet
        self.states = states
        self.initial = initial
        self.finals = finals
        self.transitions = transitions

    @staticmethod
    def from_txt(file_path):
        # Read valid lines from the file (skip empty lines and comments)
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        alphabet = states = finals = transitions = None
        initial = None
        trans = []

        # Parse the automaton definition
        for line in lines:
            if line.startswith('alfabeto:'):
                alphabet = line.split(':')[1].split(',')
            elif line.startswith('estados:'):
                states = line.split(':')[1].split(',')
            elif line.startswith('inicial:'):
                initial = line.split(':')[1]
            elif line.startswith('finais:'):
                finals = line.split(':')[1].split(',')
            elif re.match(r'^\w+,\w+,\w+$', line):
                trans.append(tuple(line.split(',')))
            elif line.startswith('transicoes:'):
                transitions = line.split(':')[1].split(',')

        # Validate input structure
        if not all([alphabet, states, initial, finals, trans]):
            raise ValueError("Incomplete or malformed input file.")

        transitions = defaultdict(dict)
        for origin, dest, symbol in trans:
            if symbol in transitions[origin]:
                raise ValueError(f"Nondeterministic transition detected from {origin} with symbol {symbol}.")
            transitions[origin][symbol] = dest

        dfa = DFA(alphabet, states, initial, finals, transitions)
        dfa.validate()
        return dfa

    def validate(self):
        if self.initial not in self.states:
            raise ValueError("Invalid initial state.")
        for f in self.finals:
            if f not in self.states:
                raise ValueError(f"Invalid final state: {f}")
        for origin, trans in self.transitions.items():
            if origin not in self.states:
                raise ValueError(f"Invalid origin state: {origin}")
            for symbol, dest in trans.items():
                if symbol not in self.alphabet:
                    raise ValueError(f"Invalid symbol in transition: {symbol}")
                if dest not in self.states:
                    raise ValueError(f"Invalid destination state: {dest}")

    def remove_unreachable_states(self):
        reachable = set()

        def visit(state):
            if state in reachable:
                return
            reachable.add(state)
            for symbol in self.alphabet:
                dest = self.transitions.get(state, {}).get(symbol)
                if dest and dest not in reachable:
                    visit(dest)

        visit(self.initial)

        self.states = [s for s in self.states if s in reachable]
        self.finals = [f for f in self.finals if f in reachable]
        self.transitions = defaultdict(dict, {
            s: {sym: d for sym, d in trans.items() if d in reachable}
            for s, trans in self.transitions.items() if s in reachable
        })

    def minimize(self):
        print("\nStarting minimization using the Table Filling method...\n")
        print("Step 1: Removing unreachable states...")
        self.remove_unreachable_states()
        print(f"Reachable states: {self.states}\n")

        n = len(self.states)
        index = {state: i for i, state in enumerate(self.states)}
        rev_index = {i: state for i, state in enumerate(self.states)}
        table = [[False for _ in range(n)] for _ in range(n)]

        print("Step 2: Marking (final, non-final) pairs as distinguishable...")
        for i in range(n):
            for j in range(i):
                s1, s2 = rev_index[i], rev_index[j]
                if (s1 in self.finals) != (s2 in self.finals):
                    table[i][j] = True
                    print(f"  Marking as distinguishable: ({s1}, {s2})")
        print()

        print("Step 3: Propagating indirect distinctions...")
        changed = True
        while changed:
            changed = False
            for i in range(n):
                for j in range(i):
                    if table[i][j]:
                        continue
                    for symbol in self.alphabet:
                        t1 = self.transitions.get(rev_index[i], {}).get(symbol)
                        t2 = self.transitions.get(rev_index[j], {}).get(symbol)
                        if not t1 or not t2:
                            continue
                        i1, i2 = index[t1], index[t2]
                        if i1 == i2:
                            continue
                        if table[max(i1, i2)][min(i1, i2)]:
                            table[i][j] = True
                            changed = True
                            print(f"  ({rev_index[i]}, {rev_index[j]}) distinguished by {symbol} → ({t1}, {t2})")
                            break
        print()

        print("Step 4: Grouping equivalent states...")
        groups = []
        marked = set()
        for i in range(n):
            if self.states[i] in marked:
                continue
            group = [self.states[i]]
            for j in range(i):
                if not table[i][j]:
                    group.append(self.states[j])
                    marked.add(self.states[j])
            marked.add(self.states[i])
            groups.append(group)

        for idx, group in enumerate(groups, 1):
            print(f"  Group {idx}: {group}")
        print()

        print("Step 5: Creating new set of states...")
        group_names = {}
        new_states = []
        for group in groups:
            name = ', '.join(sorted(group))
            new_states.append(name)
            for state in group:
                group_names[state] = name

        print(f"  New states: {new_states}\n")
        new_initial = group_names[self.initial]
        new_finals = list(set(group_names[f] for f in self.finals))

        print(f"  New initial state: {new_initial}")
        print(f"  New final states: {new_finals}\n")

        print("Step 6: Creating new transitions...")
        new_transitions = defaultdict(dict)
        for group in groups:
            rep = group[0]
            new_state = group_names[rep]
            for symbol in self.alphabet:
                dest = self.transitions.get(rep, {}).get(symbol)
                if dest:
                    new_transitions[new_state][symbol] = group_names[dest]
                    print(f"  {new_state} --{symbol}--> {group_names[dest]}")
        print("\nMinimization complete!\n")

        return DFA(self.alphabet, new_states, new_initial, new_finals, new_transitions)

    def draw(self, filename='dfa_minimized'):
        dot = graphviz.Digraph()

        used = set(self.transitions.keys())
        for trans in self.transitions.values():
            used.update(trans.values())

        for state in used:
            shape = 'doublecircle' if state in self.finals else 'circle'
            dot.node(state, shape=shape)

        dot.node('', shape='none')
        dot.edge('', self.initial)

        grouped = defaultdict(list)
        for origin, trans in self.transitions.items():
            for symbol, dest in trans.items():
                grouped[(origin, dest)].append(symbol)

        for (origin, dest), symbols in grouped.items():
            label = '/'.join(sorted(symbols))
            dot.edge(origin, dest, label=label)

        dot.render(filename, format='png', cleanup=True)
        print(f"Diagram saved as {filename}.png")

# Colab main execution
if __name__ == '__main__':
    uploaded = files.upload()
    input_file = next(iter(uploaded))
    output_name = 'dfa_minimized'

    try:
        dfa = DFA.from_txt(input_file)
        print("DFA successfully loaded. Drawing original diagram...")
        dfa.draw('dfa_original')

        minimized_dfa = dfa.minimize()
        minimized_dfa.draw(output_name)

        print("Minimization completed successfully!")
    except Exception as e:
        print(f"Error: {e}")
