# AVL Tree — Self-Balancing BST in Python

Implementation of a self-balancing AVL tree as part of the Data Structures course (Project 1) at Tel Aviv University.

## Overview

An AVL tree is a self-balancing binary search tree where the height difference between the two subtrees of any node is at most 1. After every insert or delete, the tree automatically rebalances using rotations, guaranteeing O(log n) for all core operations.

This implementation includes both standard root-based operations and **finger operations** that start from the maximum node — making insertions and searches significantly faster for keys close to the maximum.

## Implemented Operations

| Operation | Description |
|---|---|
| `search(k)` | Search from root. Returns `(node, path_length+1)` |
| `finger_search(k)` | Search starting from the max node. Returns `(node, path_length+1)` |
| `insert(k, v)` | Insert from root. Returns `(node, edges, promote_count)` |
| `finger_insert(k, v)` | Insert starting from the max node. Returns `(node, edges, promote_count)` |
| `delete(node)` | Delete a given node (handles all cases: leaf, one child, two children) |
| `join(tree2, k, v)` | Merge two AVL trees with a separating key in O(log n) |
| `split(node)` | Split tree at a given node into two valid AVL trees |
| `avl_to_array()` | In-order traversal returning a sorted list of `(key, value)` pairs |
| `max_node()` | Returns the node with the maximum key in O(1) |
| `size()` | Returns the number of items in the tree |
| `get_root()` | Returns the root node |

## Implementation Details

- **Virtual nodes** (key=None) are used as sentinels at every leaf, simplifying rotation logic
- A **max pointer** is maintained for O(1) max access and efficient finger operations
- Rebalancing after **insert** stops at the first fix; after **delete** continues upward
- Supports **single and double rotations** (right, left, right-left, left-right)
- `join` walks the taller tree's spine to attach the shorter tree in O(|h1 - h2|)
- `split` walks upward from the split node, joining subtrees progressively

## Complexity

| Operation | Time Complexity |
|---|---|
| `search` / `finger_search` | O(log n) |
| `insert` / `finger_insert` | O(log n) |
| `delete` | O(log n) |
| `join` | O(log n) |
| `split` | O(log n) |
| `avl_to_array` | O(n) |
| `max_node` | O(1) |

## Usage

```python
tree = AVLTree()

node, edges, promotes = tree.insert(10, "ten")
tree.insert(5, "five")
tree.insert(15, "fifteen")

result, path_len = tree.search(5)
print(result.value)  # "five"

print(tree.avl_to_array())
# [(5, 'five'), (10, 'ten'), (15, 'fifteen')]

tree.delete(result)
print(tree.size())  # 2

left, right = tree.split(tree.get_root())
```

## Academic Context

Implemented as part of **Project 1 — Balanced Tree** in the Data Structures course at Tel Aviv University (Semester A, 2025–2026).
