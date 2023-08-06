import unittest
from tests import create_test_suite

test_suite = create_test_suite()
text_runner = unittest.TextTestRunner().run(test_suite)