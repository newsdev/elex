from elex.parser import ap

if __name__ == "__main__":
    races = ap.Election.get_races('2012-03-13', omitResults=True)

    for race in races:
        print race

        for candidate in race.candidates:
            print "  %s" % candidate