import sys
from echo_lite.agent import run

def main():
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        task = "what is 12*7 and the time in UTC?"
    
    result = run(task)
    print(result)

if __name__ == "__main__":
    main()

