import signal, subprocess, sys

'''
The objective is to make easier the development and debugging for the Google Code Jam's interactive problems. 
To run it, the command is like the default interactive_runner.
I only know how to run programs with unbuffered stdout, stdin, stderr in Python.
1. python dev_interactive.py python3 -u testing_tool.py args -- python3 -u my_solution.py
Please try to open programs in unbuffered mode. Altough i tried with a C++ buffered program and worked fine
2. pythyon dev_interactive.py python3 -u testing_tool.py args -- ./my_solution
3. python dev_interactive.py python3 -u testing_tool.py args -- java solution
4. python dev_interactive.py python3 -u testing_tool.py args -- my_solution.exe

'''

class TimeoutExpired(Exception):
    pass

# signal will run this function when SIGALARM is raised
def alarm_handler(signum, frame):
    raise TimeoutExpired

def input_with_timeout(pipa, timeout):
    signal.signal(signal.SIGALRM, alarm_handler)
    # Produce SIGALARM in timeout seconds
    signal.setitimer(signal.ITIMER_REAL, timeout) 
    try:
        return pipa.readline().strip()
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0) # cancel alarm
        
# If you wanna kill the program, you also have to kill the children
def interrupt_handler(signum, frame):
    solution.kill()
    judge.kill()
    raise KeyboardInterrupt

def processpipe(piparead, pipawrite, timeout, printformat='{}', prefix='', sufix=''):
    answer = ''
    try:
        answer = input_with_timeout(piparead, timelimit)
    except TimeoutExpired:
        return False
    else:
        if answer == '': 
            return False
        #You can change this next condition to fit any debug flag you want
        if answer[0] == ':':
            answer = answer[1:] # Get rid of the flag
        else:
            print(answer, file=pipawrite)
            answer = prefix + answer + sufix
        print(printformat.format(answer))
        return True


signal.signal(signal.SIGINT, interrupt_handler)

if sys.argv.count("--") != 1:
    sys.exit("Expected one and only one '--'")
index2hyphen = sys.argv.index("--")
judgecomm = sys.argv[1:index2hyphen]
solutcomm = sys.argv[index2hyphen + 1:]

spstdout = subprocess.PIPE
spstdin = subprocess.PIPE
spstderr = subprocess.PIPE # Could also be an object file if you wanna keep track of
jpstdout = subprocess.PIPE
jpstdin = subprocess.PIPE
jpstderr = subprocess.PIPE # Also like spstderr, don't forget to add close file in 
                           # interrup_handler
timelimit = .002 # two miliseconds
maxnoinput = 5 # so 10 miliseconds for subprocess
maxchanges = 5 # If none of both have return anything, they might have paused for ever
# How the judge and solution output is going to be printed
# You can change this numbers to fit your console size
subprformat = ('{:<40}', '{:>40}')
# sufixes and prefixes for the console printing 
suprefixes = (
              ('J:', ''), 
              ('', ':S')
             )
solution = subprocess.Popen(
                            solutcomm,
                            stdout = spstdout, 
                            stdin = spstdin, 
                            stderr = spstderr, 
                            bufsize = 1,
                            universal_newlines = True
                            )

judge = subprocess.Popen(
                            judgecomm,
                            stdout = jpstdout, 
                            stdin = jpstdin, 
                            stderr = jpstderr, 
                            bufsize = 1,
                            universal_newlines = True
                            )

noinputloop = 0
anyinput = False
control = True
changes = 0
while solution.poll() == None and judge.poll() == None and changes < maxchanges:
    # Read solution output and connect it to the judge input
    if control:
        anyinput = processpipe(solution.stdout, judge.stdin, timelimit, subprformat[control], *suprefixes[control])
    else:
        anyinput = processpipe(judge.stdout, solution.stdin, timelimit, subprformat[control], *suprefixes[control])
    
    noinputloop += 1
    # If there's any input, reset everything            
    if anyinput:
        noinputloop = 0
        changes = 0
    elif noinputloop >= maxnoinput:
        print()
        noinputloop = 0
        changes += 1
        control =  not control
    anyinput = False
    
# There's no harm on being sure the subprocess died
solution.kill()
judge.kill()
