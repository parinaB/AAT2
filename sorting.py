import copy

def selection_sort(patients_list):
    """
    Selection Sort: O(n^2) complexity. 
    Processes small batches sequentially.
    """
    arr = copy.deepcopy(patients_list)
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            # Sort primarily by lower priority score (higher urgency)
            # Secondary check: Tie-break using earliest arrival time
            if (arr[j]['current_priority'] < arr[min_idx]['current_priority']) or \
               (arr[j]['current_priority'] == arr[min_idx]['current_priority'] and arr[j]['arrival_time'] < arr[min_idx]['arrival_time']):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def merge_sort(patients_list):
    """
    Merge Sort: O(n log n) stable complexity. 
    Handles large incoming queues under heavy traffic pressure.
    """
    if len(patients_list) <= 1:
        return patients_list
        
    mid = len(patients_list) // 2
    left = merge_sort(patients_list[:mid])
    right = merge_sort(patients_list[mid:])
    
    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if (left[i]['current_priority'] < right[j]['current_priority']) or \
           (left[i]['current_priority'] == right[j]['current_priority'] and left[i]['arrival_time'] <= right[j]['arrival_time']):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result