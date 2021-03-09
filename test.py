#!/usr/bin/env python3
import pytest

def three():
    return 3

def two():
    return 2

def test_two():
    assert two() == 2

def test_three():
    assert three() == 3
