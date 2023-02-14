from WaterAnalysis import CurrentTurb, MinTime
import pytest


def test_CurrentTurb():
    SampleData =  {'a0': [2, 4, 24, 1.16, 1.16, 1.24, 1.23, 1.16], 'I90': [2, 4, 24, 1.106, 1.1720000000000002, 1.1820000000000002, 1.145, 1.1380000000000001]}
    assert CurrentTurb(SampleData, 'a0', 'I90') == 1.1246

def test_MinTime():
    assert MinTime(1.1246) == 5.81


