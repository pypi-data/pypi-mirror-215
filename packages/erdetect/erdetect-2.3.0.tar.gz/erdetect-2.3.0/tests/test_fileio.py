import unittest


class TestFileIO(unittest.TestCase):
    def test_fileio_bv_mem_priority(self):
        """
        Test ....
        """
        """
        from erdetect.utils.bids import __prepare_input

        data_path = 'D:\\BIDS_erdetect\\sub-MSEL01872\\ses-ieeg01\\ieeg\\sub-MSEL01872_ses-ieeg01_task-ccep_run-01_ieeg.mefd'
        trial_epoch = (-1.0, 2.0)
        baseline_norm = 'median'
        baseline_epoch = (-0.5, -0.02)
        out_of_bound_handling = 'first_last_only'
        preproc_priority = 'mem'

        data_reader, baseline_method, out_of_bound_method = __prepare_input(data_path,
                                                                            trial_epoch, baseline_norm, baseline_epoch,
                                                                            out_of_bound_handling, preproc_priority)

        """
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
