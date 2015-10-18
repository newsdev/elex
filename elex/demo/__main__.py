from elex import ap

if __name__ == "__main__":
    election = ap.Election.get_next_election()
    races = election.get_races()

    for race in races:
        print race

        for candidate in race.candidates:
            print candidate