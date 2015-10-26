from elex.parser import ap

if __name__ == "__main__":
    races = ap.Election.get_races('2015-10-24', omitResults=False, level="reportingUnit")

    for race in races:
        print race

        for reporting_unit in race.reportingunits:
            print "  %s" % reporting_unit

            for candidate in reporting_unit.candidates:
                print "    %s" % candidate