import matplotlib.pyplot as plt
import numpy as np
import math
from random import seed
from random import random
import pandas as pd

def data_generator():
	"""
	creates a set of random points
	"""
	return [(random()*20, random()*20) for i in range(50)]

def find_side(p1, p2, p):
	"""
	Helper function that finds on which side of a line point lies
	params:
	p1: tuple, x and y coordinate of first point on the line
	p2: tuple, x and y coordinate of second point on the line
	p: tuple, x and y coordinate of the point whose orientation we need to find
	"""
	val = (p2[0]*p[1] - p[0]*p2[1]) - (p1[0]*p[1] - p[0]*p1[1]) + (p1[0]*p2[1] - p2[0]*p1[1])
	if val <= 0:
		return -1
	if val > 0:
		return 1
	return 0

def set_generator(data):
	"""
	helper function
	params:
	data: list: input data
	This function will help us create the lower and the upper part of the data
	"""
	min_x = 10
	max_x = 0
	for pt in data: 
		if pt[0] < min_x:
			min_x = pt[0]
			pt1 = pt
		if pt[0] > max_x:
			max_x = pt[0]
			pt2 = pt
	upper = [pt for pt in data if pt != pt1 and pt != pt2 and find_side(pt1, pt2, pt) > 0]
	lower = [pt for pt in data if pt != pt1 and pt != pt2 and find_side(pt1, pt2, pt) < 0]
	return pt1, pt2, upper, lower

def quickhull(set_, pt1, pt2, side):
    """
    The main algorithm
    params:
    set_: list of tuples of points that we need to explore
    pt1: tuple, x and y coordinate of first point on the line
    pt2: tuple, x and y coordinate of second point on the line
    side: whether we are exploring upper part or the lower part
    """
    if len(set_) == 0:
      global hull
      hull.append(pt1)
      hull.append(pt2)
      return 
    pt0 = [-1]
    sum_dist = -1
    for pt in set_:
      left_ = math.sqrt((pt[0]-pt1[0])**2 + (pt[1]-pt1[1])**2)
      right_ = math.sqrt((pt[0]-pt2[0])**2 + (pt[1]-pt2[1])**2)
      side_ = find_side(pt1,pt2,pt)
      if sum_dist < left_ + right_:
        sum_dist = left_ + right_
        pt0[0] = pt
    set1 = [pt for pt in set_ if pt != pt0[0] and find_side(pt1, pt0[0], pt) == side]
    set2 = [pt for pt in set_ if pt != pt0[0] and find_side(pt0[0], pt2, pt) == side]
    quickhull(set1, pt1, pt0[0], find_side(pt1, pt2, pt0[0]))
    quickhull(set2, pt2, pt0[0], find_side(pt2, pt1, pt0[0]))

def main():
	data = data_generator()
	p1, p2, upper, lower = set_generator(data)
	hull = []
	points = []
	if len(upper) > 0:
		quickhull(upper, p1, p2, find_side(p1, p2, upper[0]))
	if len(lower) > 0:
		quickhull(lower, p1, p2, find_side(p1, p2, lower[0]))
	return hull, points

if __name__ == '__main__':
	hull, points = main()
	
