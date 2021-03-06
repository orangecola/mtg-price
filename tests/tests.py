import unittest
import config
import os
import boto3
import bigweb, tcgplayer, hareruya, cardkingdom

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

    def test_withCache(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(os.environ["cache_bucket"])
        bucket.objects.filter(Prefix="cache/").delete()
        self.assertEqual(sum(1 for _ in bucket.objects.filter(Prefix="cache/")), 0)
        os.environ["cache"] = "True"
        result = bigweb.bigweb("Avacyn, Angel of Hope")
        self.assertGreater(sum(1 for _ in bucket.objects.filter(Prefix="cache/")), 0)
    
    def test_nameTransformation_war(self):
        os.environ["cache"] = "False"
        result = bigweb.bigweb("Nissa, Who Shakes the World")
        print(result)
        names = [i[0] for i in result]
        self.assertTrue("Nissa, Who Shakes the World (JP Alternate Art)" in names)

    def test_setTransformation(self):
        os.environ["cache"] = "False"
        result = bigweb.bigweb("Yuriko, the Tiger's Shadow")
        print(result)
        set_codes = [i[4] for i in result]
        self.assertTrue("JDG" in set_codes)
        

class Test_tcgplayer(unittest.TestCase):
    def test_basicTest(self):
        result = tcgplayer.tcgplayer("Yuriko, the Tiger's Shadow")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 3)
        [self.assertEqual(len(i), 5) for i in result]
    def test_pagination(self):
        result = tcgplayer.tcgplayer("Cultivate")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 17)
        [self.assertEqual(len(i), 5) for i in result]

class Test_hareruya(unittest.TestCase):
    def test_basicTest(self):
        result = hareruya.hareruya("Yuriko, the Tiger's Shadow")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 3)
        [self.assertEqual(len(i), 5) for i in result]

class Test_cardkingdom(unittest.TestCase):
    def test_basicTest(self):
        os.environ["cache"] = "False"
        result = cardkingdom.cardkingdom("Yuriko, the Tiger's Shadow")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 3)
        [self.assertEqual(len(i), 5) for i in result]
    def test_foilTest(self):
        os.environ["cache"] = "False"
        result = cardkingdom.cardkingdom("Avacyn, Angel of Hope")
        print(result)
        #Check if all entries are returned
        self.assertEqual(len(result), 8)
        [self.assertEqual(len(i), 5) for i in result]
    def test_cacheTest(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(os.environ["cache_bucket"])
        bucket.objects.filter(Prefix="cache/").delete()
        self.assertEqual(sum(1 for _ in bucket.objects.filter(Prefix="cache/")), 0)
        os.environ["cache"] = "True"
        result = cardkingdom.cardkingdom("Avacyn, Angel of Hope")
        self.assertGreater(sum(1 for _ in bucket.objects.filter(Prefix="cache/")), 0)
        result = cardkingdom.cardkingdom("Avacyn, Angel of Hope")