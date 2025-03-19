from django.test import TestCase

from myapp.utility import CaseConversion

class TestSimpleResults(TestCase):
    def test_pascal_conversion(self):
        test_string = "thisShould_convert Correctly"
        expected = "ThisShouldConvertCorrectly"
        
        result = CaseConversion.to_pascal(test_string)
        
        self.assertEqual(result, expected)
        
    def test_snake_conversion(self):
        test_string = "thisShould_convert Correctly"
        expected = "this_should_convert_correctly"
        
        result = CaseConversion.to_snake(test_string)
        
        self.assertEqual(result, expected)
        