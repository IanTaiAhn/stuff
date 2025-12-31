## Bitwise Help:

XOR (^)
Meaning: “exclusive OR” — returns 1 if the two bits are different, 0 if they’re the same.

AND (&)
Meaning: “bitwise AND” — returns 1 if both bits are 1.

NOT (~)
Meaning: “bitwise NOT” — flips every bit (0 → 1, 1 → 0).

Combined: & ~twos
First ~twos flips all bits of twos.

Then & keeps only the bits in ones ^ num that are not present in twos.

Effect: Ensures that if a bit has already been counted twice, it doesn’t stay in ones.

Think of ^ as a toggle switch, & as a filter, and ~ as a flip everything.

- ^ = toggle the switch
- & = check if the switch is on
- | = turn the switch on
- ~ = flip all switches

Common Problems Seen in medium-hard level problems:

## 🧭 Two Pointers (arrays, linked lists)
Concept: Use two indices/pointers moving at different speeds or directions to reduce complexity.

Classic problems:
- Find pairs in a sorted array that sum to a target
- Detect cycle in a linked list (Floyd’s cycle detection)
- Find middle of a linked list
- Valid palindrome check

Why interviews love it: It tests whether you can avoid brute force O(n²) by synchronizing two traversals.

## 🔄 Sliding Window (subarrays, substrings)
Concept: Maintain a “window” (range of indices) that expands/contracts to satisfy conditions.

Classic problems:
- Maximum sum subarray of size k
- Longest substring without repeating characters
- Minimum window substring (cover all characters)
- Why interviews love it: It’s a subtype of two pointers, but requires dynamic adjustment. Great for testing optimization intuition.

## 📉 Binary Search (sorted arrays, optimization)
Concept: Divide and conquer by halving the search space. Works on sorted data or monotonic functions.

Classic problems:
- Search insert position
- Find first/last occurrence of a target
- Search in rotated sorted array
- Binary search on “answer space” (e.g., minimize max load, find smallest feasible value)

Why interviews love it: It tests whether you can spot monotonicity and apply O(log n) instead of O(n).

## 🧮 Dynamic Programming (paths, subsequences, knapsack)
Concept: Break problems into overlapping subproblems, store results to avoid recomputation.

Classic problems:
- Longest common subsequence
- Longest increasing subsequence
- Edit distance
- 0/1 knapsack
- Coin change

Why interviews love it: It tests recursion-to-iteration thinking, memoization/tabulation, and optimization under constraints.

## ⚡ Greedy Algorithms (interval scheduling, coin problems)
Concept: Make the locally optimal choice at each step, hoping it leads to global optimum.

Classic problems:
- Activity selection / interval scheduling
- Minimum coins for change
- Huffman coding
- Minimum platforms (train scheduling)

Why interviews love it: It tests whether you can recognize when greedy works (greedy-choice property) vs when you need DP.

## 🧱 Prefix Sums & Difference Arrays
Concept: Precompute cumulative information so range queries or subarray constraints become O(1) or O(n).

Classic Problems:

- Subarray Sum Equals K
- Continuous Subarray Sum
- Range Sum Query (Immutable / 2D)
- Minimum Size Subarray Sum (prefix-sum variant)

## 🧩 Hash Map / Counting / Frequency Tables
Concept: Track counts, positions, or states to enforce constraints or detect patterns in O(n).

Classic Problems:

- Two Sum
- Group Anagrams
- Longest Substring Without Repeating Characters
- Top K Frequent Elements

## 🧵 Stack & Monotonic Stack
Concept: Use a stack to maintain structure (monotonicity, parentheses, operators) and solve O(n²) problems in O(n).

Classic Problems:

- Valid Parentheses
- Daily Temperatures
- Largest Rectangle in Histogram
- Next Greater Element I/II

## 🌳 Tree & Graph Traversal (DFS/BFS)
Concept: Systematically explore nodes/edges to compute connectivity, levels, paths, or detect cycles.

Classic Problems:

- Binary Tree Level Order Traversal
- Number of Islands
- Clone Graph
- Course Schedule (topological sort)

## 🧭 Backtracking / Search
Concept: Explore all possibilities via recursion with pruning using the “choose → explore → unchoose” pattern.

Classic Problems:

- Permutations
- Combinations
- Subsets
- Word Search
- N-Queens

## 🔗 Union-Find (Disjoint Set Union)
Concept: Efficiently track connected components with union and find operations.

Classic Problems:

- Number of Connected Components in an Undirected Graph
- Redundant Connection
- Accounts Merge
- Most Stones Removed with Same Row or Column

## 🧮 Heap / Priority Queue
Concept: Maintain a dynamic set where you repeatedly extract or track the min/max efficiently.

Classic Problems:

- Kth Largest Element in an Array
- Merge K Sorted Lists
- Task Scheduler
- Dijkstra’s Algorithm (network delay time)

## 🧊 Matrix / Grid Traversal
Concept: Treat the grid as a graph and use BFS/DFS or DP to explore or compute states.

Classic Problems:

- Rotting Oranges
- Walls and Gates
- Spiral Matrix
- Word Search (grid backtracking)

## 🧠 Bit Manipulation
Concept: Use bitwise operations to encode sets, states, or perform constant‑time arithmetic tricks.

Classic Problems:

- Single Number (XOR trick)
- Subsets (bitmask enumeration)
- Counting Bits
- Maximum XOR of Two Numbers

## ➗ Math & Number Theory
Concept: Use mathematical properties (GCD, modular arithmetic, primes) to simplify or optimize logic.

Classic Problems:

- Pow(x, n) (fast exponentiation)
- Greatest Common Divisor of Strings
- Count Primes (Sieve of Eratosthenes)
- Happy Number

## 🔤 Trie / Prefix Tree
Concept: Store strings in a prefix‑indexed tree for fast prefix/suffix queries.

Classic Problems:

- Implement Trie
- Word Search II
- Replace Words
- Design Add and Search Words Data Structure

## 📏 Intervals (Merge, Sweep Line)
Concept: Sort intervals and merge, sweep, or track active intervals to solve scheduling and overlap problems.

Classic Problems:

- Merge Intervals
- Insert Interval
- Meeting Rooms I/II
- Minimum Number of Arrows to Burst Balloons

## 🌲 Segment Tree / Fenwick Tree
Concept: Support fast range queries and updates using a tree‑structured index.

Classic Problems:

- Range Sum Query – Mutable
- Count of Smaller Numbers After Self (Fenwick)
- Kth Largest Element in a Stream (segment tree variant)
- Skyline Problem (advanced)


