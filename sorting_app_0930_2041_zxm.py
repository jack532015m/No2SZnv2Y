# 代码生成时间: 2025-09-30 20:41:52
# -*- coding: utf-8 -*-
# NOTE: 重要实现细节

"""
Sorting App using Python and Celery framework.
This program implements a sorting algorithm using Celery tasks.
"""
# NOTE: 重要实现细节

import celery
# FIXME: 处理边界情况
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded

# Configure Celery with Redis as the message broker
app = Celery(
    "sorting_app",
    broker="redis://localhost:6379/0",  # Update with your Redis configuration
    backend="redis://localhost:6379/0",  # Update with your Redis configuration
)

@app.task(bind=True, soft_time_limit=10)  # 10 seconds soft time limit
def sort_numbers(self, numbers, algorithm):
    """
    A Celery task to sort numbers using different algorithms.
    
    Args:
# NOTE: 重要实现细节
        self: The Celery task instance.
        numbers (list): A list of numbers to sort.
        algorithm (str): The name of the sorting algorithm to use.
            Currently supported algorithms are 'bubble' and 'quick'.
    
    Returns:
        list: The sorted list of numbers.
    
    Raises:
        ValueError: If the algorithm is not supported.
        SoftTimeLimitExceeded: If the sorting task exceeds the soft time limit.
    """
    
    try:
        if algorithm not in ['bubble', 'quick']:
            raise ValueError("Unsupported sorting algorithm")

        if algorithm == 'bubble':
            return bubble_sort(numbers)
        elif algorithm == 'quick':
            return quick_sort(numbers)
        
    except SoftTimeLimitExceeded as e:
        self.retry(exc=e)
        raise


def bubble_sort(arr):
    """
# TODO: 优化性能
    Perform a bubble sort on the given list of numbers.
    
    Args:
        arr (list): A list of numbers to sort.
    
    Returns:
        list: The sorted list of numbers.
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def quick_sort(arr):
    """
    Perform a quick sort on the given list of numbers.
    
    Args:
# 改进用户体验
        arr (list): A list of numbers to sort.
# 扩展功能模块
    
    Returns:
        list: The sorted list of numbers.
    """
    if len(arr) <= 1:
        return arr
# 优化算法效率
    else:
        pivot = arr.pop()
        less_than_pivot = [x for x in arr if x <= pivot]
        greater_than_pivot = [x for x in arr if x > pivot]
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)

# Example usage:
# sorted_numbers = sort_numbers.delay([3, 6, 8, 10, 1, 2, 1], 'bubble')
# print(sorted_numbers.get())
