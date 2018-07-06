import unittest
import pytz
from datetime import datetime, timedelta

utc = pytz.timezone("UTC")
bst = pytz.timezone("Europe/London")
oneHour = timedelta(hours = 1)

def isABstDay(dt):
    dayAt0 = datetime(dt.year, dt.month, dt.day, 0)
    dayAt5 = datetime(dt.year, dt.month, dt.day, 5)
    localizedAt0 = bst.localize(dayAt0)
    localizedAt5 = bst.localize(dayAt5)
    return bool(localizedAt0.dst()) or bool(localizedAt5.dst())

def clocksGoingForwards(dt):
    dayAt0 = datetime(dt.year, dt.month, dt.day, 0)
    dayAt5 = datetime(dt.year, dt.month, dt.day, 5)
    localizedAt0 = bst.localize(dayAt0)
    localizedAt5 = bst.localize(dayAt5)
    return not bool(localizedAt0.dst()) and bool(localizedAt5.dst())

def clocksGoingBackwards(dt):
    dayAt0 = datetime(dt.year, dt.month, dt.day, 0)
    dayAt5 = datetime(dt.year, dt.month, dt.day, 5)
    localizedAt0 = bst.localize(dayAt0)
    localizedAt5 = bst.localize(dayAt5)
    return bool(localizedAt0.dst()) and not bool(localizedAt5.dst())

def getDateTimeFromDayKeyAndMinutesFromMidnight(dayKey, minutesFromMidnight):
    baseDate = datetime(1980, 1, 1, 0, 0)
    translation = timedelta(days = dayKey, minutes=minutesFromMidnight)
    translatedDatetime = baseDate + translation
    adjustment = timedelta(0)
    if isABstDay(translatedDatetime): 
        adjustment = adjustment - oneHour
        if clocksGoingForwards(translatedDatetime):        
            adjustment = adjustment + oneHour
            if minutesFromMidnight < 24 * 60:
                adjustment = adjustment - oneHour
        if clocksGoingBackwards(translatedDatetime):          
            if minutesFromMidnight < 24 * 60:
                 adjustment = adjustment + oneHour
    return  translatedDatetime + adjustment

class TestsFor27thMarch2015(unittest.TestCase):
    def testBeforeMidnight(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(12869, 1439), datetime(2015, 3, 27, 23, 59))

class TestsFor28thTo29thMarch2015(unittest.TestCase):
    def testBeforeMidnight(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(12870, 1439), datetime(2015, 3, 28, 23, 59))
    def testMidnight(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(12870, 1440), datetime(2015, 3, 29, 0, 0))
    def testBeforeRealBST(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(12870, 1499), datetime(2015, 3, 29, 0, 59))
    def testRealBST(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(12870, 1500), datetime(2015, 3, 29, 1, 0))
    def testBeforeCubicNewDay(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(12870, 1709), datetime(2015, 3, 29, 4, 29))
    def testOnCubicNewDay(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(12871, 330), datetime(2015, 3, 29, 4, 30))

class TestsFor30thMarch2015(unittest.TestCase):
    def testAt5(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(12872, 360), datetime(2015, 3, 30, 5, 0))
    
class TestsFor24thTo25thOctober2015(unittest.TestCase):
    def testBeforeMidnight(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(13080, 1439), datetime(2015, 10, 24, 22, 59))
    def testBeforeUTCMidnight(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(13080, 1499), datetime(2015, 10, 24, 23, 59))
    def testMidnight(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(13080, 1500), datetime(2015, 10, 25, 0, 0))
    def testBeforeRealNotBST(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(13080, 1559), datetime(2015, 10, 25, 0, 59))
    def testAtRealNotBST(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(13080, 1560), datetime(2015, 10, 25, 1, 0))
    def testBeforeCubicNotBST(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(13080, 1709), datetime(2015, 10, 25, 3, 29))
    def testCubicNotBST(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(13081, 210), datetime(2015, 10, 25, 3, 30))
    def testCubicLateOn(self):
        self.assertEqual(getDateTimeFromDayKeyAndMinutesFromMidnight(13081, 270), datetime(2015, 10, 25, 4, 30))
        

        
        
        
        