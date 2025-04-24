# 🧠 DFA Minimizer (Deterministic Finite Automaton)

This project implements a **DFA minimizer** using the **Table Filling method** in Python, designed to work smoothly in environments like **Google Colab**. It reads the DFA from a `.txt` file, validates and simplifies its structure, removes unreachable states, minimizes them, and generates visual diagrams using **Graphviz**.

---

## 🔍 Technologies
<div style="display: inline_block"><cbr> 
  <img align = "top" alt = "gabrielbribeiroo_GoogleColab" height = "50" width = "50" src="https://upload.wikimedia.org/wikipedia/commons/d/d0/Google_Colaboratory_SVG_Logo.svg" />
  <img align = "top" alt = "gabrielbribeiroo_Python" height = "50" width = "50" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" /> 
  <img align = "top" alt = "gabrielbribeiroo_JupyterNotebook" height = "50" width = "50" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jupyter/jupyter-original.svg" />
</div>
  
---

## 🚀 Features

✅ Read DFA definition from `.txt` files  
✅ Validate symbols, states, and transitions  
✅ Automatically remove **unreachable states**  
✅ Minimize DFA using the **Table Filling method**  
✅ Combine equivalent states with names like `"q0, q1"`  
✅ Merge duplicate transitions into one (`0/1` instead of two arrows)  
✅ Generate diagrams (`.png`) for original and minimized DFAs

---

## 📁 Input File Format (`.txt`)

Your input file should be formatted as follows:

alfabeto:0,1 
estados:q0,q1,q2 
inicial:q0 
finais:q2 
q0,q1,0 
q0,q0,1 
q1,q2,1
q1,q0,0 
q2,q2,0
q2,q2,1

---


### 💡 Explanation:
- `alfabeto:` lists the input symbols (comma-separated)
- `estados:` lists all state names
- `inicial:` is the start state
- `finais:` lists accepting (final) states
- Each transition is written as: `origin_state,destination_state,symbol`

---

## 🧪 Running on Google Colab

1. Upload your `afd.txt` using `files.upload()` or Colab's file pane
2. Run the Python script
3. The diagrams will be saved as `afd_original.png` and `afd_minimized.png`

---

## 📦 Requirements

- Python 3.x
- [Graphviz](https://graphviz.org/)
- Required libraries:
  - `graphviz`
  - `re`
  - `collections`
  - `google.colab` (for file upload in notebooks)

> Google Colab has all these libraries pre-installed.

---

## 📌 Example Usage (in code)

```python
afd = AFD.from_txt("afd.txt")         # Load DFA from file
afd.draw("afd_original")              # Draw the original DFA
minimized_afd = afd.minimize()        # Minimize the DFA
minimized_afd.draw("afd_minimized")   # Draw the minimized DFA
```
---

## 📊 Output Example
- afd_original.png: Graph of the DFA as initially described
- afd_minimized.png: Graph after minimization (with combined states and simplified transitions)

---

## 🛠️ Authors & License

- Developed for educational purposes as part of a project in Automata Theory, Formal Languages, or Logic.
- Feel free to use, fork, and adapt it for your class or personal studies.
- Distributed under the MIT License.

---

## 🙋 Contribute

- If you find any issues or want to propose improvements (e.g., regex support, NFA to DFA conversion, step-by-step minimization), feel free to open a pull request or issue.
- Happy automaton minimizing! 🎯
