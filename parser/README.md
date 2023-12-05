# Given Grammar
G: 
E → E + T | E – T | -E | T
T → T * F | T/F | F
F → int | (E)

# Rewritten Grammar
G1: 
E -> TE’ | -EE'
E’ -> +TE’ | -TE’ | ε
T -> FT’
T’ -> *FT’ | /FT’ | ε
F -> int | (E)

# Instruction:
1. Run the program

```python3 main.py```

2. Enter the input string
3. Press enter
4. The program will print the result