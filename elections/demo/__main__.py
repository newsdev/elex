from elections import ap

if __name__ == "__main__":
    e = ap.Election.get_next_election()
    print "The next election will be on %s." % e.electiondate