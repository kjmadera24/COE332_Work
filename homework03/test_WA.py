from WaterAnalysis import CurrentTurb, MinTime
import pytest


def test_CurrentTurb():
    SampleData =  [{'a0': 2 , 'I90':2}, {'a0': 4 , 'I90':4}, {'a0': 24 , 'I90':24}, {'a0': 1.043 , 'I90':1.175}, {'a0': 1.018 , 'I90':1.151}, {'a0': 0.969 , 'I90':1.1920000000000002}, {'a0': 0.96 , 'I90':-1.187}, {'a0': 1.047 , 'I90':1.163}]
    assert CurrentTurb(SampleData, 'a0', 'I90') == 0.7261
def test_MinTime():
    assert MinTime(1.1246) == 5.81


