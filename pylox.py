import sys

from pylox.lox import Lox, LoxRepl

DEBUG = False

if __name__ == "__main__":
    args = sys.argv[1:]  # arg 0 is the name of this script
    lox = Lox(debug=DEBUG)
    if len(args) == 0:
        LoxRepl(lox).run()
    elif len(args) == 1:
        lox.run_file(args[0])
    else:
        print('nah')

# add one line
