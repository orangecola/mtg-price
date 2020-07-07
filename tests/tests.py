import unittest
import config
import os
import boto3
import bigweb, tcgplayer, hareruya

class Test_Bigweb(unittest.TestCase):
    def test_basicTest(self):
        result = bigweb.bigweb("Yuriko, the Tiger's Shadow")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 3)
        [self.assertEqual(len(i), 5) for i in result]

    def test_withoutCache(self):
        os.environ["cache"] = "False"
        result = bigweb.bigweb("Yuriko, the Tiger's Shadow")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 3)
        [self.assertEqual(len(i), 5) for i in result]
        pass

    def test_withCache(self):
        os.environ["cache"] = "True"
        result = bigweb.bigweb("Yuriko, the Tiger's Shadow")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 3)
        [self.assertEqual(len(i), 5) for i in result]
        pass
    
    def test_similarName(self):
        pass
    def test_nameTransformation(self):
        pass

class Test_tcgplayer(unittest.TestCase):
    def test_basicTest(self):
        result = tcgplayer.tcgplayer("Yuriko, the Tiger's Shadow")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 3)
        [self.assertEqual(len(i), 5) for i in result]

class Test_hareruya(unittest.TestCase):
    def test_basicTest(self):
        result = hareruya.hareruya("Yuriko, the Tiger's Shadow")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 3)
        [self.assertEqual(len(i), 5) for i in result]