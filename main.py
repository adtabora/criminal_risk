import sys, getopt, os

def main(argv):

    step = argv[0]

    if step == "links":
        import tribunaLinks 
        tribunaLinks.getLinks()

    if step == "pos.train":
        from pos_tagger import pos_tagger
        pos_tagger.train_tagger()

    if step == "pos.tag":
        from pos_tagger import pos_tagger
        pos_tagger.tag_articles()


    


#run main
if __name__ == "__main__":
   main(sys.argv[1:])