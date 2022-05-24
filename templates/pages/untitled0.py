# -*- coding: utf-8 -*-
"""
Created on Sun May 22 11:38:23 2022

@author: Hoang Anh
"""
l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
n = 20
 
def search(s, n):
    low = 0
    high = len(l) - 1
    
    
    while high >= low:
        mid = (high+low)//2
        if l[mid] == n:
            return mid
            
        elif l[mid] < n:
                low = mid+1 
        elif l[mid] > n:
                high = mid-1
        
    return -1

print(search(l, n))