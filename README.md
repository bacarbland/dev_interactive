# dev_interactive
The objective is to make easier the development and debugging for the  Google Code Jam's interactive problems. 
If you have ever tried to solve an interactive problem, you should know that they are hard to debug. 

With these tool you can see the conversation between the two programs and output debug info without messing with the functionality of your solution


# Run
You need **python3** and a **Unix System** (Linux or Mac), Windows may function with a diferent timer and signal, but i haven't try it. Also maybe it could work with Python2 with the `future` alias of `print`

To run it, the command is `python3 dev_interactive.py ` followed by the commands for the judge and solution separated by a double hyphen.
The commands for the judge and solution are the same you would use normally, altough it would better to run them unbuffered.
I only know how to run programs with unbuffered stdout and stdin in Python. (`-u`)
### Unbuffered example:
- `python3 dev_interactive.py python3 -u testing_tool.py *args* -- python3 -u solution.py`


### Buffered examples:
Please try to open programs in unbuffered mode. Altough i tried with a C++ buffered program and worked just fine.
- `python3 dev_interactive.py python3 -u testing_tool.py *args* -- ./a.out`
- `python3 dev_interactive.py python3 -u testing_tool.py *args* -- java solution`
- `python3 dev_interactive.py python3 -u testing_tool.py *args* -- solution.exe`

# Printing debug info
Printing something in the solution without sending it to the judge is really easy, you just add ':' at the begining of each line:
`print(':', reallyImportantVariable)`
The same goes for the judge:
`print(':', variableFromJudgeProgram)`
