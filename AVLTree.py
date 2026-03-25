#id1:213712698
#name1:Omer Konkol
#username1:omerkonkol



"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
  	
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None
		self.countNodes = 0
		self.max = None
  
	# Creates a virtual node (key=None)
	def make_virtual(self):
		return AVLNode(None, None)

	# Creates a real node and attaches virtual children
	def make_real(self, key, val):
		node = AVLNode(key, val)
		node.left = self.make_virtual()
		node.right = self.make_virtual()
		node.left.parent = node
		node.right.parent = node
		node.height = 0
		return node


	# Updates height of a node based on its children
	def update_height(self, node):
		if not node.is_real_node():
			return -1
		node.height = 1 + max(node.left.height, node.right.height)
		return node.height


	# Computes balance factor = height(left) - height(right)
	def bf(self, node):
		return node.left.height - node.right.height


	# Performs a right rotation around y
	def rotate_right(self, y):
		x = y.left
		B = x.right

		x.right = y
		y.left = B

		x.parent = y.parent
		y.parent = x
		if B.is_real_node():
			B.parent = y

		if x.parent is None:
			self.root = x
		else:
			if x.parent.left == y:
				x.parent.left = x
			else:
				x.parent.right = x

		self.update_height(y)
		self.update_height(x)

		return x


	# Performs a left rotation around x
	def rotate_left(self, x):
		y = x.right
		B = y.left

		y.left = x
		x.right = B

		y.parent = x.parent
		x.parent = y
		if B.is_real_node():
			B.parent = x

		if y.parent is None:
			self.root = y
		else:
			if y.parent.left == x:
				y.parent.left = y
			else:
				y.parent.right = y

		self.update_height(x)
		self.update_height(y)

		return y


	# Rebalances the AVL tree upwards from a given node
	def rebalance(self, node, is_delete=False):
		promotes = 0

		while node is not None and node.is_real_node():

			height_before = node.height
			self.update_height(node)
			bf = self.bf(node)

			# Balanced and height did not change
			if abs(bf) < 2 and node.height == height_before:
				# INSERT: can stop
				if not is_delete:
					break
				# DELETE: must continue upward
				node = node.parent
				continue

			# Balanced but height changed → promote
			if abs(bf) < 2:
				promotes += 1
				node = node.parent
				continue

			# Unbalanced → rotations
			if bf == 2:
				if self.bf(node.left) < 0:
					self.rotate_left(node.left)
				node = self.rotate_right(node)

			elif bf == -2:
				if self.bf(node.right) > 0:
					self.rotate_right(node.right)
				node = self.rotate_left(node)

			# INSERT: stop after first rotation
			if not is_delete:
				break

			# DELETE: continue upward
			node = node.parent

		return promotes




	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		node = self.get_root()
		if node is None:
			return None, 1  # empty tree: defined as path length 1

		edges = 0

		while node.is_real_node():

			if key == node.key:
				return node, edges + 1  # path edges + 1 as required

			# choose direction
			if key < node.key:
				next_node = node.left
			else:
				next_node = node.right

			# search fails here: key would be located as a child of this node
			# path length = edges so far + edge to this node + 1
			if not next_node.is_real_node():
				return None, edges + 2

			node = next_node
			edges += 1





	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	
	def finger_search(self, key):

		if self.get_root() is None:
			return None, 1  # empty tree

		node = self.max_node()
		edges = 1  # starting node counts by definition

		# move upward to a node that may contain the key
		while node.parent is not None and node.key > key:
			node = node.parent
			edges += 1

		# regular BST search downward
		while node.is_real_node():

			if key == node.key:
				return node, edges  # already includes +1

			if key < node.key:
				next_node = node.left
			else:
				next_node = node.right

			# search fails here: key would be a child of this node
			# add one edge to reach this node + final +1
			if not next_node.is_real_node():
				return None, edges + 1

			node = next_node
			edges += 1

		


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		# Empty tree
		if self.get_root() is None:
			new = self.make_real(key, val)
			self.root = new
			self.max = new
			self.countNodes = 1
			return new, 1, 0

		curr = self.root
		edges = 0

		# Single BST descent to insertion point
		while True:
			edges += 1
			if key < curr.key:
				if not curr.left.is_real_node():
					break
				curr = curr.left
			else:
				if not curr.right.is_real_node():
					break
				curr = curr.right

		# Attach new node
		new = self.make_real(key, val)
		if key < curr.key:
			curr.left = new
		else:
			curr.right = new
		new.parent = curr

		# Update max if needed
		if key > self.max.key:
			self.max = new

		# Rebalance upwards
		promotes = self.rebalance(curr, is_delete=False)

		self.countNodes += 1
		return new, edges, promotes




	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		# Empty tree
		if self.get_root() is None:
			new = self.make_real(key, val)
			self.root = new
			self.max = new
			self.countNodes = 1
			return new, 1, 0

		curr = self.max
		edges = 0

		# Move up until subtree may contain key
		while curr.parent is not None and key < curr.key:
			curr = curr.parent
			edges += 1

		# BST descent from that point
		while True:
			edges += 1
			if key < curr.key:
				if not curr.left.is_real_node():
					break
				curr = curr.left
			else:
				if not curr.right.is_real_node():
					break
				curr = curr.right

		# Attach new node
		new = self.make_real(key, val)
		if key < curr.key:
			curr.left = new
		else:
			curr.right = new
		new.parent = curr

		# Update max if needed
		if key > self.max.key:
			self.max = new

		# Rebalance upwards
		promotes = self.rebalance(curr, is_delete=False)

		self.countNodes += 1
		return new, edges, promotes


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):

		# If we're deleting the current max, update max AFTER structural changes
		deleting_max = (self.max is not None and node == self.max)

		# Case 1: leaf (no real children)
		if (not node.left.is_real_node()) and (not node.right.is_real_node()):
			parent = node.parent

			# Tree becomes empty
			if parent is None:
				self.root = None
				self.max = None
				self.countNodes = 0
				return

			# Replace node with a fresh virtual child
			if parent.left == node:
				parent.left = self.make_virtual()
				parent.left.parent = parent
			else:
				parent.right = self.make_virtual()
				parent.right.parent = parent

			self.countNodes -= 1

			# Rebalance from the first node whose subtree height may shrink
			self.rebalance(parent, is_delete=True)

		# Case 2: exactly one real child
		elif node.left.is_real_node() != node.right.is_real_node():
			child = node.left if node.left.is_real_node() else node.right
			parent = node.parent

			# Node is root
			if parent is None:
				self.root = child
				child.parent = None
				self.countNodes -= 1

				# Rebalance from new root (it may shrink after deletion)
				self.rebalance(child, is_delete=True)

			else:
				# Bypass node
				if parent.left == node:
					parent.left = child
				else:
					parent.right = child
				child.parent = parent

				self.countNodes -= 1

				# Rebalance from parent (first possible shrink point)
				self.rebalance(parent, is_delete=True)

		# Case 3: two real children (physical successor replace)
		else:
			succ = self.successor(node)  # leftmost in right subtree

			# We'll rebalance from where the successor was physically removed
			if succ.parent == node:
				# Special case: successor is node.right
				start = succ  # succ's right link changes, so start here

				# Detach successor from its old spot: node.right becomes succ.right
				node.right = succ.right
				node.right.parent = node  # works for virtual too

			else:
				# General case: successor deeper in right subtree
				succ_parent = succ.parent
				start = succ_parent  # succ_parent loses a child -> height may shrink here

				# Detach successor: succ_parent.left becomes succ.right
				succ_parent.left = succ.right
				succ_parent.left.parent = succ_parent  # works for virtual too

			# Now transplant succ into node's position (physical swap, no copying)
			parent = node.parent
			succ.parent = parent

			if parent is None:
				self.root = succ
			else:
				if parent.left == node:
					parent.left = succ
				else:
					parent.right = succ

			# Attach node's original children under succ
			succ.left = node.left
			succ.left.parent = succ

			succ.right = node.right
			succ.right.parent = succ

			self.countNodes -= 1

			# Rebalance from the first place where a node was physically removed
			self.rebalance(start, is_delete=True)

		# Update max if needed
		if deleting_max:
			curr = self.get_root()
			if curr is None:
				self.max = None
			else:
				while curr.right.is_real_node():
					curr = curr.right
				self.max = curr




	def successor(self, node):
		# Successor is leftmost in right subtree
		curr = node.right
		while curr.left.is_real_node():
			curr = curr.left
		return curr



	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		# Case 0: both trees are empty
		if self.get_root() is None and tree2.get_root() is None:
			self.root = self.make_real(key, val)
			self.countNodes = 1
			self.max = self.root
			return

		# Case 1: self is empty -> insert (key, val) into tree2 and take its root
		if self.get_root() is None:

			# Ensure tree2 has a valid max pointer before insertion
			if tree2.max is None and tree2.get_root() is not None:
				curr = tree2.root
				while curr.right.is_real_node():
					curr = curr.right
				tree2.max = curr

			tree2.insert(key, val)
			self.root = tree2.root
			self.countNodes = tree2.countNodes
			self.max = tree2.max
			return

		# Case 2: tree2 is empty -> insert (key, val) into self
		if tree2.get_root() is None:
			self.insert(key, val)
			# self.max is updated inside insert
			return

		# Create the separating node
		x = self.make_real(key, val)

		# Decide which tree is on the left and which is on the right
		# (based on the precondition)
		if self.get_root().key < key:
			TL, TR = self.root, tree2.root
			left_count, right_count = self.countNodes, tree2.countNodes
			new_max = tree2.max          # larger keys are on the right
		else:
			TL, TR = tree2.root, self.root
			left_count, right_count = tree2.countNodes, self.countNodes
			new_max = self.max           # larger keys are on the right

		hL, hR = TL.height, TR.height

		# Heights differ by at most 1 -> x becomes the new root
		if abs(hL - hR) <= 1:
			x.left = TL
			x.right = TR
			TL.parent = x
			TR.parent = x
			self.root = x
			self.countNodes = left_count + right_count + 1
			self.update_height(x)
			self.max = new_max
			return

		# TL is taller: walk down its right spine
		if hL > hR:
			curr = TL
			while curr.right.is_real_node() and curr.right.height > hR:
				curr = curr.right

			# Attach x between curr and curr.right
			B = curr.right
			x.left = B
			if B.is_real_node():
				B.parent = x

			x.right = TR
			TR.parent = x

			curr.right = x
			x.parent = curr

			self.root = TL
			self.countNodes = left_count + right_count + 1

			self.update_height(x)
			self.rebalance(x.parent, is_delete=True)
			self.max = new_max
			return

		# TR is taller: walk down its left spine
		curr = TR
		while curr.left.is_real_node() and curr.left.height > hL:
			curr = curr.left

		# Attach x between curr and curr.left
		B = curr.left
		x.right = B
		if B.is_real_node():
			B.parent = x

		x.left = TL
		TL.parent = x

		curr.left = x
		x.parent = curr

		self.root = TR
		self.countNodes = left_count + right_count + 1

		self.update_height(x)
		self.rebalance(x.parent, is_delete=True)
		self.max = new_max
		return



	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		T_left = AVLTree()
		T_right = AVLTree()

		# Initialize left tree from node.left (without computing max)
		if node.left.is_real_node():
			T_left.root = node.left
			T_left.root.parent = None

		# Initialize right tree from node.right (without computing max)
		if node.right.is_real_node():
			T_right.root = node.right
			T_right.root.parent = None

		curr = node
		parent = node.parent

		# Walk upward toward the original root
		while parent is not None:

			if curr == parent.left:
				# parent.key and parent.right belong to the RIGHT result
				temp = AVLTree()

				if parent.right.is_real_node():
					temp.root = parent.right
					temp.root.parent = None

				T_right.join(temp, parent.key, parent.value)

			else:
				# parent.key and parent.left belong to the LEFT result
				temp = AVLTree()

				if parent.left.is_real_node():
					temp.root = parent.left
					temp.root.parent = None

				T_left.join(temp, parent.key, parent.value)

			curr = parent
			parent = parent.parent

		# Compute max for each resulting tree

		if T_left.root is not None:
			curr = T_left.root
			while curr.right.is_real_node(): 
				curr = curr.right
			T_left.max = curr
		else:
			T_left.max = None

		if T_right.root is not None:
			curr = T_right.root
			while curr.right.is_real_node():
				curr = curr.right
			T_right.max = curr
		else:
			T_right.max = None

		return T_left, T_right



	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		# Result list that will store (key, value) pairs in sorted order
		result = []

		def inorder(node):
			# Stop recursion on virtual (non-real) nodes
			if not node.is_real_node():
				return

			# Visit left subtree
			inorder(node.left)

			# Visit current node
			result.append((node.key, node.value))

			# Visit right subtree
			inorder(node.right)

		# Empty tree case
		if self.root is None or not self.root.is_real_node():
			return []

		# In-order traversal from the root
		inorder(self.root)

		# Return sorted array representation
		return result




	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return self.max


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self.countNodes	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		if self.root is None or not self.root.is_real_node():
			return None

		return self.root


    


