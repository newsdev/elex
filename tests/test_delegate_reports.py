try:
    set
except NameError:
    from sets import Set as set

import tests

class TestDelegateReports(tests.DelegateReportTestCase):

    def test_number_of_national_level_results(self):
        number_of_candidates = list(set([d.last for d in self.delegate_reports]))
        national_delegate_reports = [d for d in self.delegate_reports if d.level == 'nation']
        self.assertEqual(len(national_delegate_reports), len(number_of_candidates))

    def test_number_of_state_level_results(self):
        number_of_states = list(set([d.state for d in self.delegate_reports if d.level == 'state']))
        self.assertEqual(58, len(number_of_states))

    def test_state_us_to_national_transformation(self):
        number_of_national_results = list([d.level for d in self.delegate_reports if d.level == 'nation'])
        number_of_state_us_results = list([d.level for d in self.delegate_reports if d.state == 'US'])
        self.assertEqual(len(number_of_national_results), len(number_of_state_us_results))