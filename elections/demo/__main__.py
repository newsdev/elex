from elections import ap

if __name__ == "__main__":
    e = ap.Election.get_next_election()
    races = e.get_races()

    for r in races:
        print r
        for c in r.candidates:
            print "  %s %s" % (c, c.ballotorder)