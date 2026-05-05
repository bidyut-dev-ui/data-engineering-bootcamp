prompt - 

Always give complete, full answers. 
If the question is related to programming, include working code. 
If I ask about a topic or concept by name, give a one or two line definition first, then explain or give code.

From now on, whenever I say 'explain it' or 'what does it mean', always explain the last thing you just told me. Keep continuity with your previous answer.

1. Problem Statement: Given two strings s1 and s2, determine if they are anagrams of each other. Anagrams are words or phrases formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

    1. Constraints:

        Strings can contain lowercase English alphabets only.
        Strings can be of different lengths.
        Strings can be empty.

    2. Example Input/Output:

        Input: s1 = "listen", s2 = "silent" Output: True
        Input: s1 = "hello", s2 = "world" Output: False
        Input: s1 = "rat", s2 = "car" Output: False
        Input: s1 = "", s2 = "" Output: True
        Input: s1 = "aab", s2 = "aba" Output: True
        Input: s1 = "aabb", s2 = "abc" Output: False

    3. Thought Process & Approach:

        Initial Thoughts:

            3.1. If they are anagrams, they must have the same characters with the same frequencies.
            3.2. They must also have the same length. This is a quick early exit condition.

---------------------------------------------------------
def check_if_anagram(str1, str2):
  print(f"str1 is {str1} and str2 is {str2}")
  if len(str1) != len(str2):
    return False
  else:
    return sorted(str1.lower()) == sorted(str2.lower())

result = check_if_anagram("listen", "silent")
print(result)
----------------------------------------------------------

2. Reverse a Singly Linked List

    1. Problem Statement: Given the head of a singly linked list, reverse the list, and return the reversed list's new head.

    2. Node Definition: A ListNode object will have two attributes:

        val: The value of the node.
        next: A pointer to the next node in the list. It will be None if it's the last node.

    3. Constraints:

        The number of nodes in the list can be 0 to 5000.
        Node values are typically integers.

    4. Example Input/Output:

        Input: head = 1 -> 2 -> 3 -> 4 -> 5 -> None Output: 5 -> 4 -> 3 -> 2 -> 1 -> None
        Input: head = 1 -> 2 -> None Output: 2 -> 1 -> None
        Input: head = None Output: None
        Input: head = 1 -> None Output: 1 -> None
-------------------------------------------------------------
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    
    while curr:
        # 1. Save the next node (so we don't lose the rest of the list)
        next_node = curr.next
        
        # 2. Flip the pointer to face backward
        curr.next = prev
        
        # 3. Move the 'prev' and 'curr' pointers forward
        prev = curr
        curr = next_node
        
    # At the end, 'prev' will be pointing to the new head
    return prev
-------------------------------------------------------------

3. Find All Duplicate Elements in a List

    1. Problem Statement: Given an array of integers, find all the elements that appear more than once in the array. You can return the duplicates in any order.

    2. Constraints:

        The length of the list is between $0$ and $10^5$.
        The integers can be positive, negative, or zero.

    3. Example Input/Output:

        Input: nums = [4, 3, 2, 7, 8, 2, 3, 1] Output: [2, 3]
        Input: nums = [1, 1, 2] Output: [1]
        Input: nums = [1, 2, 3] Output: []

    4. Solution:

        The most efficient way to solve this is by using a Set (Hash Set). This allows us to track seen elements in $O(n)$ time complexity.


--------------------------------------------------
def find_duplicates(nums):
    seen = set()
    duplicates = set()
    
    for num in nums:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
            
    return list(duplicates)
--------------------------------------------------

4. Two Sum (Find Indices of Target)

    1. Problem Statement: Given an array of integers nums and an integer target, return the indices of the two numbers such that they add up to the target. You may assume that each input would have exactly one solution, and you may not use the same element twice.

    2. Constraints:

        $2 \leq nums.length \leq 10^4$
        Only one valid answer exists.

    3. Example Input/Output:

        Input: nums = [2, 7, 11, 15], target = 9 Output: [0, 1] (Because nums[0] + nums[1] == 9)
        Input: nums = [3, 2, 4], target = 6 Output: [1, 2]

    4. Solution:

        We use a Hash Map (Dictionary) to store the value and its index as we iterate. For each number, we check if its "complement" ($target - current\_number$) already exists in the map.

--------------------------------------------------
def two_sum(nums, target):
    hash_map = {} # val : index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
--------------------------------------------------

5. Maximum Subarray (Kadane’s Algorithm)

    1. Problem Statement: Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

    2. Constraints:

        $1 \leq nums.length \leq 10^5$
        nums[i] can be negative.

    3. Example Input/Output:

        Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4] Output: 6 (Subarray [4, -1, 2, 1] has the largest sum)
        Input: nums = [1] Output: 1

    4. Solution:

        Using Kadane's Algorithm, we iterate through the array once. At each step, we decide whether to "start over" with the current number or add it to the existing sum.

--------------------------------------------------
def max_sub_array(nums):
    current_sum = max_sum = nums[0]
    
    for num in nums[1:]:
        # Decide: Is it better to add the current number to the sum, 
        # or just start a new sum from the current number?
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
        
    return max_sum
--------------------------------------------------

6. Move Zeroes

    1. Problem Statement: Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements. You must do this in-place without making a copy of the array.

    2. Constraints:

        $1 \leq nums.length \leq 10^4$
        
    3. Example Input/Output:

        Input: nums = [0, 1, 0, 3, 12] Output: [1, 3, 12, 0, 0]
        Input: nums = [0] Output: [0]
        
    4. Solution:

        We use a Two-Pointer approach. One pointer tracks where the next non-zero element should go.

--------------------------------------------------
def move_zeroes(nums):
    last_non_zero = 0
    
    # 1. Move all non-zero elements to the front
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[last_non_zero] = nums[i]
            last_non_zero += 1
            
    # 2. Fill the rest of the array with zeroes
    for i in range(last_non_zero, len(nums)):
        nums[i] = 0
--------------------------------------------------

7. Sort a List in Ascending Order (Manual Sort)

    1. Problem Statement: Given a list of integers, sort the list in ascending order without using built-in methods like .sort() or sorted().

    2. Constraints:

        The list can contain up to $1,000$ elements.
        
    3. Example Input/Output:

        Input: nums = [64, 34, 25, 12, 22, 11, 90] Output: [11, 12, 22, 25, 34, 64, 90]
        
    4. Solution:

        We can use Bubble Sort. It works by repeatedly stepping through the list, comparing adjacent elements and swapping them if they are in the wrong order.

--------------------------------------------------

def manual_sort(nums):
    n = len(nums)
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if nums[j] > nums[j + 1]:
                # Swap the elements
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums
--------------------------------------------------

8. Find the Middle Element of a List

    1. Problem Statement: Given a list, find the middle element. If the list has an even number of elements, return the two middle elements.

    2. Example Input/Output:

        Input: nums = [10, 20, 30, 40, 50] Output: 30
        Input: nums = [1, 2, 3, 4] Output: [2, 3]

    3. Solution:

We calculate the index by dividing the length of the list by 2.

--------------------------------------------------

def find_middle_elements(nums):
    n = len(nums)
    mid = n // 2
    
    if n % 2 == 0:
        return [nums[mid - 1], nums[mid]]
    else:
        return nums[mid]
--------------------------------------------------

9. Implement Reverse String In-Place

    1. Problem Statement: Write a function that reverses a string in-place. The input is given as a list of characters.

    2. Constraints:

        The string length is between 0 and $10^4$.
        We must modify the list directly without creating a new one.

    3. Example Input/Output:

        Input: s = ["h", "e", "l", "l", "o"] Output: ["o", "l", "l", "e", "h"]
        Input: s = ["H", "a", "n", "n", "a"] Output: ["a", "n", "n", "a", "H"]

    4. Solution:

        We use the Two-Pointer technique. One pointer starts at the beginning (left), and the other starts at the end (right). We swap the characters and move the pointers toward the center until they meet.

--------------------------------------------------

def reverse_string_inplace(s):
    left = 0
    right = len(s) - 1
    
    while left < right:
        # Swap the characters
        s[left], s[right] = s[right], s[left]
        
        # Move pointers inward
        left += 1
        right -= 1
--------------------------------------------------
10. Palindrome Check (String or Number)

    1. Problem Statement: Determine if a given string or number is a palindrome (reads the same forward and backward). Ignore casing for strings.

    2. Example Input/Output:

        Input: s = "Radar" Output: True
        Input: x = 12321 Output: True
        Input: s = "Python" Output: False

    3. Solution:

        We can use Python's slicing technique or a two-pointer approach to check for symmetry.

--------------------------------------------------

def is_palindrome(data):
    # Convert to string and lowercase to handle numbers and casing
    s = str(data).lower()
    return s == s[::-1]
--------------------------------------------------
11. Convert a String to an Array

    1. Problem Statement: Convert a given string into an array (list) of characters.

    2. Example Input/Output:

        Input: s = "hello"
        Output: ["h", "e", "l", "l", "o"]

    3. Solution:

        In Python, strings are iterable, so we can convert them to a list using the list() constructor.

--------------------------------------------------

def string_to_array(s):
    return list(s)
--------------------------------------------------
12. Find the Missing Number in a Sequence

    1. Problem Statement: You are given a list of n-1 distinct integers in the range 1 to n. Find the missing integer.

    2. Constraints:

        The list contains distinct integers.
        The numbers are in the range 1 to n.

    3. Example Input/Output:

        Input: nums = [1, 2, 4, 5, 6]
        Output: 3

        Input: nums = [1, 3, 4, 5]
        Output: 2

    4. Solution:

        We can use the mathematical property that the sum of the first n natural numbers is n*(n+1)/2. By subtracting the sum of the given list from the expected sum, we can find the missing number.

--------------------------------------------------

def find_missing_number(nums):
    n = len(nums) + 1
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum
--------------------------------------------------
13. Remove Duplicates from a Sorted List

    1. Problem Statement: Given a sorted list, remove duplicates in-place such that each element appears only once. Return the new length of the list.

    2. Constraints:

        The list is sorted in non-decreasing order.
        We must modify the list in-place.

    3. Example Input/Output:

        Input: nums = [1, 1, 2, 3, 3, 3, 4, 5, 5]
        Output: 5 (The list becomes [1, 2, 3, 4, 5, _, _, _, _])

        Input: nums = [1, 1, 1, 1]
        Output: 1 (The list becomes [1, _, _, _])

    4. Solution:

        We use a two-pointer approach. One pointer (`write_index`) tracks where the next unique element should be placed, and the other pointer (`i`) iterates through the list.

--------------------------------------------------

def remove_duplicates(nums):
    if not nums:
        return 0
    
    write_index = 1 # Start from the second position
    
    for i in range(1, len(nums)):
        # If the current element is different from the previous one
        if nums[i] != nums[i - 1]:
            # Place it at the write_index
            nums[write_index] = nums[i]
            # Move the write_index forward
            write_index += 1
            
    return write_index
--------------------------------------------------
14. Group Anagrams

    1. Problem Statement: Given a list of strings, group the anagrams together. Anagrams are words formed by rearranging the letters of another word.

    2. Example Input/Output:

        Input: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
        Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]

    3. Solution:

        We can use a Hash Map (Dictionary) where the key is the sorted version of the string (which is the same for all anagrams), and the value is a list of the original strings.

--------------------------------------------------

def group_anagrams(strs):
    anagram_map = {}
    
    for word in strs:
        # Sort the letters of the word to create a canonical key
        sorted_word = "".join(sorted(word))
        
        # If the key is not in the map, initialize it with an empty list
        if sorted_word not in anagram_map:
            anagram_map[sorted_word] = []
        
        # Append the original word to the list
        anagram_map[sorted_word].append(word)
        
    # Return the values (the groups of anagrams)
    return list(anagram_map.values())
--------------------------------------------------
15. Validate Parentheses

    1. Problem Statement: Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets. Open brackets must be closed in the correct order.

    2. Constraints:

        $1 \leq s.length \leq 10^4$
        $s$ consists of parentheses only '()[]{}'.

    3. Example Input/Output:

        Input: s = "()[]{}"
        Output: True

        Input: s = "(]"
        Output: False

        Input: s = "([)]"
        Output: False

    4. Solution:

        We use a Stack. When we encounter an opening bracket, we push it onto the stack. When we encounter a closing bracket, we check if the stack is empty or if the top element is the corresponding opening bracket. If it matches, we pop it; otherwise, the string is invalid.

--------------------------------------------------

def is_valid_parentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            # If it's a closing bracket
            # Pop the top element if the stack is not empty, else assign a dummy value
            top_element = stack.pop() if stack else '#'
            
            # Check if the popped element is the corresponding opening bracket
            if mapping[char] != top_element:
                return False
        else:
            # If it's an opening bracket, push it onto the stack
            stack.append(char)
            
    # If the stack is empty, all brackets were matched correctly
    return not stack
--------------------------------------------------
16. Binary Search

    1. Problem Statement: Given a sorted list of integers `nums` and a target value, find the index of the target in the list. If the target is not found, return -1.

    2. Constraints:

        - `nums` is sorted in non-decreasing order.
        - $1 \leq nums.length \leq 10^4$
        - $-10^4 \leq nums[i], target \leq 10^4$
        - All integers in `nums` are unique.

    3. Example Input/Output:

        Input: nums = [-1, 0, 3, 5, 9, 12], target = 9
        Output: 4
        Explanation: 9 exists in nums and its index is 4.

        Input: nums = [-1, 0, 3, 5, 9, 12], target = 2
        Output: -1
        Explanation: 2 does not exist in nums so return -1.

    4. Solution:

        We use the Binary Search algorithm, which works on sorted arrays. We maintain two pointers, `left` and `right`, representing the search space. In each step, we calculate the middle index `mid`. We compare `nums[mid]` with the `target`.
        - If `nums[mid] == target`, we found the element and return `mid`.
        - If `nums[mid] < target`, the target must be in the right half, so we update `left = mid + 1`.
        - If `nums[mid] > target`, the target must be in the left half, so we update `right = mid - 1`.
        We continue this process until `left > right`, which means the target is not in the array.

--------------------------------------------------

def binary_search(nums, target):
    """
    Performs binary search on a sorted list to find the index of the target.
    
    Args:
        nums: A list of integers sorted in non-decreasing order.
        target: The integer value to search for.
        
    Returns:
        The index of the target if found, otherwise -1.
    """
    left = 0
    right = len(nums) - 1
    
    while left <= right:
        # Calculate the middle index
        # Using (left + right) // 2 can cause overflow for very large lists, 
        # so (left + (right - left) // 2) is safer, though for typical 
        # interview constraints, either is usually fine.
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            # Target found
            return mid
        elif nums[mid] < target:
            # Target is in the right half
            left = mid + 1
        else:
            # Target is in the left half
            right = mid - 1
            
    # Target not found
    return -1
--------------------------------------------------
17. Merge Two Sorted Lists

    1. Problem Statement: Merge two sorted lists into a single sorted list.

    2. Example Input/Output:

        Input: list1 = [1, 2, 4], list2 = [1, 3, 4]
        Output: [1, 1, 2, 3, 4, 4]

        Input: list1 = [], list2 = [0]
        Output: [0]

    3. Solution:

        We use a two-pointer approach. We maintain a new list `merged` and two pointers, `i` for `list1` and `j` for `list2`. We compare the elements at the current pointers and append the smaller one to the `merged` list, then increment the corresponding pointer. We continue until one of the lists is exhausted, after which we append the remaining elements of the other list.

--------------------------------------------------

def merge_sorted_lists(list1, list2):
    """
    Merges two sorted lists into a single sorted list.
    
    Args:
        list1: The first sorted list of integers.
        list2: The second sorted list of integers.
        
    Returns:
        A new list containing all elements from list1 and list2 in sorted order.
    """
    merged = []
    i = 0  # Pointer for list1
    j = 0  # Pointer for list2
    
    # Traverse both lists while both have elements
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
            
    # Append remaining elements from list1, if any
    while i < len(list1):
        merged.append(list1[i])
        i += 1
        
    # Append remaining elements from list2, if any
    while j < len(list2):
        merged.append(list2[j])
        j += 1
        
    return merged
--------------------------------------------------
18. Find the Intersection of Two Arrays

    1. Problem Statement: Given two arrays of integers, find their intersection (the common elements). Each element in the result should be unique.

    2. Constraints:

        - Each element in the result must be unique.
        - The result can be in any order.

    3. Example Input/Output:

        Input: nums1 = [1, 2, 2, 1], nums2 = [2, 2]
        Output: [2]

        Input: nums1 = [4, 9, 5], nums2 = [9, 4, 9, 8, 4]
        Output: [9, 4] (or [4, 9])

    4. Solution:

        We can convert both lists to sets to automatically handle duplicates. Then, we find the intersection of the two sets using the `&` operator or the `intersection()` method. Finally, we convert the resulting set back to a list.

--------------------------------------------------

def intersection(nums1, nums2):
    """
    Finds the intersection of two arrays (unique common elements).
    
    Args:
        nums1: The first list of integers.
        nums2: The second list of integers.
        
    Returns:
        A list containing the unique common elements.
    """
    # Convert lists to sets to automatically remove duplicates
    set1 = set(nums1)
    set2 = set(nums2)
    
    # Find the intersection of the two sets
    intersection_set = set1.intersection(set2)
    
    # Convert the result back to a list
    return list(intersection_set)

# Alternative concise solution:
def intersection_concise(nums1, nums2):
    return list(set(nums1) & set(nums2))
--------------------------------------------------
19. Frequency Map (Dictionary Problem)

    1. Problem Statement: Given a list of words, return a dictionary where the keys are the unique words and the values are the number of times each word appears.

    2. Constraints:
        - The function should be case-insensitive.

    3. Example Input/Output:

        Input: words = ["Apple", "banana", "apple", "CHERRY", "apple"]
        Output: {"apple": 3, "banana": 1, "cherry": 1}

    4. Solution:

        We iterate through the list, normalizing the strings to lowercase and updating a count in a dictionary.

-----------------------------------------------

    def count_word_frequency(words):
        frequency = {}
        for word in words:
            word = word.lower()
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1
        return frequency

--------------------------------------------------
20. Group Anagrams (Dictionary Problem)

    1. Problem Statement: Given a list of strings, group the anagrams together in a dictionary where the key is the sorted version of the word.

    2. Example Input/Output:

        Input: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
        Output: {"aet": ["eat", "tea", "ate"], "ant": ["tan", "nat"], "abt": ["bat"]}
    
    3. Solution:

        By sorting the characters of each word, all anagrams will result in the same string, which we can use as a dictionary key.

-----------------------------------------------
    def group_anagrams(strs):
    anagram_map = {}
    
    for s in strs:
        # Sort the word to create a key (e.g., "eat" -> "aet")
        sorted_key = "".join(sorted(s))
        
        if sorted_key not in anagram_map:
            anagram_map[sorted_key] = []
        
        anagram_map[sorted_key].append(s)
        
    return anagram_map
------------------------------------------------
21. 