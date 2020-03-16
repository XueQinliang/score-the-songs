# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 08:51:52 2019

@author: Nicole~
"""
import numpy as np

def dtw_distance(ts_a, ts_b, d=lambda x,y: abs(x-y)%12, mww=10000):
    """Computes dtw distance between two time series
    
    Args:
        ts_a: time series a
        ts_b: time series b
        d: distance function
        mww: max warping window, int, optional (default = infinity)
        
    Returns:
        dtw distance
    """
    
    # Create cost matrix via broadcasting with large int
    ts_a, ts_b = np.array(ts_a), np.array(ts_b)
    M, N = len(ts_a), len(ts_b)
    cost = np.ones((M, N))

    # Initialize the first row and column
    cost[0, 0] = d(ts_a[0], ts_b[0])
    for i in range(1, M):
#        cost[i, 0] = cost[i-1, 0] + d(ts_a[i], ts_b[0])
        cost[i, 0] = cost[i-1, 0] + 100

    for j in range(1, N):
#        cost[0, j] = cost[0, j-1] + d(ts_a[0], ts_b[j])
        cost[0, j] = cost[0, j-1] + 100

    # Populate rest of cost matrix within window
    for i in range(1, M):
        for j in range(max(1, i - mww), min(N, i + mww)):
            choices = cost[i-1, j-1], cost[i, j-1], cost[i-1, j]
            cost[i, j] = min(choices) + d(ts_a[i], ts_b[j])


    # Return DTW distance given window 
    return cost[-1, -1]