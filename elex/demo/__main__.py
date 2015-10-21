from elex import ap

if __name__ == "__main__":
    races = ap.Election.get_races('2014-11-04', national=True)

    for race in races:
        print race

        for candidate in race.candidates:
            print "  %s" % candidate