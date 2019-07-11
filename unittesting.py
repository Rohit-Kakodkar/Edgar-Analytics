import sys
import unittest
sys.path.append('src')
from datetime import datetime
from sessionization import *

class unittesting(unittest.TestCase):

    def test_process_log_line(self):
        # Test four different kinds of records
        test_line0 = '101.81.133.jja,2017-06-30,00:00:00,0.0,1608552.0,0001047469-17-004337,-index.htm,200.0,80251.0,1.0,0.0,0.0,9.0,0.0,'
        corr_result0 = ('101.81.133.jja', datetime.strptime('2017-06-30 00:00:00', '%Y-%m-%d %H:%M:%S'))

        test_line1 = '101.81.133.jja,2017-06-51,00:00:00,0.0,1608552.0,0001047469-17-004337,-index.htm,200.0,80251.0,1.0,0.0,0.0,9.0,0.0,'
        corr_result1 = None

        test_line2 = '101.81.133.jja,2017-06-30,00:00:00,0.0,1608552.0,0001047469-17-004337,-index.htm,80251.0,1.0,0.0,0.0,9.0,0.0,'    #without " ".
        corr_result2 = None

        self.assertEqual(parse_log_line(test_line0),corr_result0)
        self.assertEqual(parse_log_line(test_line1),corr_result1)
        self.assertEqual(parse_log_line(test_line2),corr_result2)

if __name__ == '__main__':
    unittest.main()
