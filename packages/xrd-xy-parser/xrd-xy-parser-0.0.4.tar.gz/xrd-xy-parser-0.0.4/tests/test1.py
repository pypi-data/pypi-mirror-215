import pathlib
import unittest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
import numpy as np

from xrd_xy_parser import xy
from tests.success_cases import inouts


# success_in = "success_in"
# success_out = "success_out"
failpath = "tests/fail"


class simpletest(unittest.TestCase):
    def test_success(self):
        for case in inouts:
            # mock = MagicMock(spec=pathlib.Path.open)
            # mock.return_value = mock_open(read_data=case.in_)
            # mockfile = mock_open(read_data=case.in_)
            # mockfile.return_value
            # with patch("", mockfile):
            # with patch("pathlib.Path") as mock:
            #     mock.return_value
            # filepath.open.return_value = mock_open()
            # mocko = mock_open(mock, case.in_)
            mock = mock_open(read_data=case.in_)
            with patch("pathlib.Path.open", mock):

                got0, got1, got2 = xy.readstr("")

                self.assertEqual(got0, case.out_[0])
                self.assertTrue((got1 == case.out_[1]).all())
                self.assertEqual(got2, case.out_[2])

    def test_fail(self):
        cnt = 0

        for f in Path(failpath).glob("*"):
            cnt += 1
            self.assertRaises(xy.ParseError, xy.read, f.resolve())
        self.assertTrue(cnt > 0, "fail file not found")

    def test_read2xy_success(self):
        for case in inouts:

            mock = mock_open(read_data=case.in_)
            with patch("pathlib.Path.open", mock):

                got = xy.read2xy("")

                dummydata = np.array(case.out_[1])
                xs = dummydata[:, 0]
                ys = dummydata[:, 1]
                self.assertTrue((got.x == xs).all())
                self.assertTrue((got.y == ys).all())
