# Coding interview patterns — study guide

A reference for the algorithm patterns worth mastering before an interview, split into two tiers by how often they actually show up. Work through Tier 1 fully before spending real time on Tier 2 — it covers the large majority of medium-difficulty problems.

For each pattern: what it is, the signal that should make you reach for it, a few classic problems to drill, and a template where one genuinely exists. Not every pattern has a reusable template (DP and backtracking vary too much problem to problem) — for those, the "how to derive it" notes matter more than any code snippet.

---

## Tier 1 — master first

### 1. Two pointers
**Concept:** Two indices moving through an array or string, either toward each other or in tandem, to avoid an O(n²) rescan.
**Signal:** Sorted input, looking for a pair/triplet, or partitioning in place.
**Classic problems:** Two Sum II (sorted), 3Sum, Container With Most Water, Valid Palindrome.

```python
def two_sum_sorted(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return []
```

### 2. Sliding window
**Concept:** A window over a contiguous range that expands and contracts to satisfy a constraint, maintaining running state instead of recomputing.
**Signal:** "Longest/shortest contiguous subarray or substring that ..."
**Classic problems:** Longest Substring Without Repeating Characters, Minimum Window Substring, Maximum Sum Subarray of Size K.

```python
def longest_unique_substring(s):
    seen = {}
    left = best = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

### 3. Fast & slow pointers
**Concept:** Two pointers moving through a linked list at different speeds to detect cycles or find midpoints without extra space.
**Signal:** Linked list, "detect a cycle," "find the middle," or a value sequence that loops back on itself.
**Classic problems:** Linked List Cycle, Find the Duplicate Number, Middle of the Linked List.

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False
```

### 4. Hash map / frequency counting
**Concept:** Track counts, positions, or "have I seen this before" state in a hashmap for O(1) lookups.
**Signal:** Anything about pairs summing to a target, duplicates, anagrams, or "how many times does X occur."
**Classic problems:** Two Sum, Group Anagrams, Top K Frequent Elements, Longest Consecutive Sequence.

This one usually doesn't need a template — the skill is recognizing when a hashmap turns an O(n²) nested-loop check into a single O(n) pass.

### 5. Binary search (incl. "search the answer")
**Concept:** Halve the search space each step. Works on sorted arrays, but also on any monotonic *feasibility* check, even with no array in sight.
**Signal:** Sorted lookup, or "minimize the maximum" / "maximize the minimum" where you can cheaply test "is X achievable?"
**Classic problems:** Search in Rotated Sorted Array, Koko Eating Bananas, Search Insert Position.

```python
def min_feasible(lo, hi, is_feasible):
    while lo < hi:
        mid = (lo + hi) // 2
        if is_feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

### 6. DFS / BFS (trees, graphs, grids)
**Concept:** Systematic exploration of nodes and edges. DFS goes deep (recursion/stack) — good for connectivity, path existence, tree recursion. BFS goes wide (queue) — guarantees shortest path on unweighted graphs and does level-by-level work.
**Signal:** "Shortest path" / "fewest steps" → BFS. "Does a path exist" / "connected components" → DFS. Grid problems are this pattern wearing a 2D array instead of an adjacency list.
**Classic problems:** Number of Islands, Rotting Oranges, Word Ladder, Clone Graph, Binary Tree Level Order Traversal.

### 7. Backtracking
**Concept:** Brute force with pruning: choose → recurse → undo the choice → try the next option. The runtime lives entirely in how early you cut dead branches.
**Signal:** "All subsets," "all permutations," "every valid arrangement."
**Classic problems:** Subsets, Permutations, N-Queens, Word Search.

```python
def backtrack(path, choices, results):
    if is_complete(path):
        results.append(path[:])
        return
    for choice in choices:
        if not is_valid(path, choice):
            continue
        path.append(choice)
        backtrack(path, remaining_choices(choices, choice), results)
        path.pop()
```

### 8. Dynamic programming
**Concept:** Recursion where subproblems repeat, so you cache them. Write the brute-force recursion first, notice repeated calls, add memoization — that's top-down DP.
**Signal:** "Count the ways," "minimum cost," "best/longest ___" where choices build on smaller versions of the same problem.
**Classic problems:** Coin Change, Longest Increasing Subsequence, Edit Distance, 0/1 Knapsack.
**How to derive it (no universal template exists):**
1. Write the brute-force recursive solution first, in plain terms.
2. Name the *state* — the minimal set of variables that fully describes a subproblem.
3. Write the recurrence: how does this state's answer depend on smaller states?
4. Identify the base case(s).
5. Memoize (top-down) or convert to a table (bottom-up).

### 9. Heap / priority queue / top-K
**Concept:** Maintain a structure where you can repeatedly extract the min or max in O(log n), without sorting everything.
**Signal:** "k largest/smallest," "streaming median," "merge k sorted ___."
**Classic problems:** Kth Largest Element in an Array, Merge k Sorted Lists, Task Scheduler.

### 10. Merge intervals
**Concept:** Sort by start time, then sweep left to right merging anything that overlaps.
**Signal:** Overlapping ranges, scheduling, room/resource booking.
**Classic problems:** Merge Intervals, Insert Interval, Meeting Rooms II.

### 11. Monotonic stack
**Concept:** A stack kept in strictly increasing or decreasing order; pop anything that breaks the order before pushing. Turns O(n²) "next greater/smaller element" scans into O(n).
**Signal:** "Next greater/smaller element," spans, histogram-style rectangle problems.
**Classic problems:** Daily Temperatures, Next Greater Element I/II, Largest Rectangle in Histogram, Valid Parentheses.

### 12. Prefix sums
**Concept:** Precompute a running total so any range sum becomes one subtraction. Paired with a hashmap, this also counts subarrays that sum to a target.
**Signal:** Repeated range-sum queries, or "subarray that sums to K."
**Classic problems:** Subarray Sum Equals K, Range Sum Query (Immutable), Continuous Subarray Sum.

---

## Tier 2 — learn next

### 13. Topological sort
**Concept:** BFS or DFS with a dependency twist — order nodes so every edge points forward. If you can't, there's a cycle.
**Signal:** Ordering tasks with dependencies, detecting a cycle in a DAG.
**Classic problems:** Course Schedule, Course Schedule II, Alien Dictionary.

### 14. Union-Find (Disjoint Set Union)
**Concept:** Efficiently track connected components as edges arrive, using `union` and `find` with path compression.
**Signal:** Dynamic connectivity — "are these two things in the same group," counting groups as connections form.
**Classic problems:** Number of Connected Components, Redundant Connection, Accounts Merge.

### 15. Greedy
**Concept:** Make the locally optimal choice at each step. Works only when the problem has the greedy-choice property — otherwise you need DP instead.
**Signal:** Interval scheduling, "minimum number of ___ to cover ___," coin/resource problems where a simple rule provably works.
**Classic problems:** Activity Selection, Jump Game, Minimum Number of Arrows to Burst Balloons.

### 16. Cyclic sort
**Concept:** When an array holds values 1..n (or a known range), place each value at its matching index in one pass. Whatever's left out of place reveals the missing or duplicated value — no extra space needed.
**Signal:** Array of 1..n, asked for the missing or duplicate value in O(1) space.
**Classic problems:** Missing Number, Find All Duplicates in an Array, First Missing Positive.

### 17. Trie (prefix tree)
**Concept:** A tree where each path from the root spells out a string, enabling fast prefix/word lookups.
**Signal:** "Starts with," prefix search, autocomplete, dictionary/word-list problems.
**Classic problems:** Implement Trie, Word Search II, Design Add and Search Words Data Structure.

---

## Quick-scan table

| # | Pattern | Tier | One-line signal |
|---|---|---|---|
| 1 | Two pointers | 1 | Sorted array/string, need a pair |
| 2 | Sliding window | 1 | Longest/shortest contiguous run under a constraint |
| 3 | Fast & slow pointers | 1 | Linked list cycle or midpoint |
| 4 | Hash map / frequency | 1 | Pairs, duplicates, counts |
| 5 | Binary search | 1 | Sorted lookup, or minimize-the-max |
| 6 | DFS / BFS | 1 | Traversal, shortest path, connectivity |
| 7 | Backtracking | 1 | All subsets/permutations/arrangements |
| 8 | Dynamic programming | 1 | Overlapping subproblems, optimal count/cost |
| 9 | Heap / top-K | 1 | k largest/smallest, streaming extremes |
| 10 | Merge intervals | 1 | Overlapping ranges, scheduling |
| 11 | Monotonic stack | 1 | Next greater/smaller element |
| 12 | Prefix sums | 1 | Repeated range-sum queries |
| 13 | Topological sort | 2 | Task dependencies, DAG cycle check |
| 14 | Union-Find | 2 | Dynamic connectivity, group counting |
| 15 | Greedy | 2 | Locally optimal choice works globally |
| 16 | Cyclic sort | 2 | Array of 1..n, find missing/duplicate |
| 17 | Trie | 2 | Prefix search, autocomplete |

---

## How to study this

For each pattern: solve the "template" problem cold, no notes. If you get stuck, look at just the part where you stalled — not the whole solution. Once you can rebuild the template from the one-line concept alone, move to the next pattern in the tier. Tier 1 fully solid is worth more than Tier 1 + Tier 2 both half-learned.