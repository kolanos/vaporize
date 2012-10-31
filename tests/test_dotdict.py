import unittest

from vaporize.servers import BackupSchedule


class TestBackupSchedule(unittest.TestCase):
    def test_to_dict(self):
        bs = BackupSchedule.create(daily='test')
        bs_dict = bs.to_dict()
        self.assertIn('daily', bs_dict['backupSchedule'])
        self.assertEqual('test', bs_dict['backupSchedule']['daily'])
