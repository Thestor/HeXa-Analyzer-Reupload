# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 08:06:46 2019

@author: Matthew
"""
import math

def InitiateBinarySearch(list_of_data, item_to_search, key_start = 0, key_end = 0):
    #key_start and key_end harmoniously limit the scope of which range of elements to sort

    list_of_data.sort()

    if key_end == 0:
        key_end = len(list_of_data)
        
    how_many_data = len(list_of_data)
    upper_limit = how_many_data - 1
    bottom_limit = 0
    middle_index = bottom_limit + round((upper_limit - bottom_limit) / 2)

    try:
        while True:
            getValue = eval(list_of_data[middle_index][key_start:key_end])
            if getValue == item_to_search:
                return True, True, middle_index
            elif upper_limit == bottom_limit or upper_limit - bottom_limit == -1 or upper_limit - bottom_limit == 1:
                return True, False, "Such a record cannot be found."
            elif getValue > item_to_search:
                upper_limit = middle_index
                middle_index = bottom_limit + math.floor((upper_limit - bottom_limit) / 2)
            else:
                bottom_limit = middle_index
                middle_index = bottom_limit + math.ceil((upper_limit - bottom_limit) / 2)
    except Exception as e:
        return False, False, None
        print(e)

        """Return statements = {if it is success}, {item in list}, {the_index_of_the_item}"""