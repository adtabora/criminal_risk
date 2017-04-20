import sys, getopt, os

def main(argv):

    step = argv[0]

    if step == "links":
        import tribunaLinks 
        tribunaLinks.getLinks()


#run main
if __name__ == "__main__":
   main(sys.argv[1:])