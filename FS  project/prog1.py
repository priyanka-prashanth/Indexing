import time

class BTreeNode:
	def __init__(self, leaf = False):
		self.leaf = leaf
		self.keys = []
		self.child = []

class BTree:
	def __init__(self, t):
		self.root = BTreeNode(True)	
		self.t = t

	def print_tree(self, x, l = 0):
		print("Level ", l, " ", len(x.keys), end = ":")
		for i in x.keys:
			print("(", i[1], ",", i[2], ")", end=" ")
		print()
		l += 1
		if len(x.child) > 0:
			for i in x.child:
				self.print_tree(i, l)
	

	def search(self, k, x = None):
		
		
		if x != None:
			i = 0
			while i < len(x.keys) and k > x.keys[i][0]:
				i += 1
			if i < len(x.keys) and k == x.keys[i][0]:
				return (x, i)
			elif x.leaf:
				return None
			else:
				
				return self.search(k, x.child[i])
		else:
				return self.search(k, self.root)

	def insert(self, k):
		
		
		root = self.root
		
		if len(root.keys) == (2 * self.t) - 1:
			temp = BTreeNode()
			self.root = temp
			temp.child.insert(0, root)
			self._split_child(temp, 0)
			self._insert_nonfull(temp, k)
		else:
			self._insert_nonfull(root, k)

	def _insert_nonfull(self, x, k):
		
		i = len(x.keys) - 1
		if x.leaf:
			x.keys.append((None, None))
			while i >= 0 and k[0] < x.keys[i][0]:
				x.keys[i + 1] = x.keys[i]
				i -= 1
			x.keys[i + 1] = k
		else:
			while i >= 0 and k[0] < x.keys[i][0]:
				i -= 1
			i += 1
			if len(x.child[i].keys) == (2 * self.t) - 1:
				self._split_child(x, i)
				if k[0] > x.keys[i][0]:
					i += 1
			self._insert_nonfull(x.child[i], k)

	def _split_child(self, x, i):
		
		t = self.t
		y = x.child[i]
		z = BTreeNode(y.leaf)
		x.child.insert(i + 1, z)
		x.keys.insert(i, y.keys[t - 1])
		z.keys = y.keys[t : (2 * t) - 1]
		y.keys = y.keys[0 : t - 1]
		if not y.leaf:
			z.child = y.child[t : 2 * t]
			y.child = y.child[0 : t - 1]

	def delete(self, x, k):
		
		t = self.t
		i = 0
		while i < len(x.keys) and k > x.keys[i][0]:
			i += 1
		
		if x.leaf:
			if i < len(x.keys) and x.keys[i][0] == k:
				x.keys.pop(i)
				return
			return
		
		
		if i < len(x.keys) and x.keys[i][0] == k:
			return self._delete_internal_node(x, k, i)
		
		elif len(x.child[i].keys) >= t:
			self.delete(x.child[i], k)			
		
		else:
			if i != 0 and i+2 < len(x.child):
				if len(x.child[i-1].keys) >= t:
					self._delete_sibling(x, i, i-1)
				elif len(x.child[i+1].keys) >= t:
					self._delete_sibling(x, i, i+1)
				else:
					self._del_merge(x, i, i+1)
			elif i == 0: 
				if len(x.child[i+1].keys) >= t:
					self._delete_sibling(x, i, i+1)
				else:
					self._del_merge(x, i, i+1)
			elif i+1 == len(x.child):
				if len(x.child[i-1].keys) >= t:
					self._delete_sibling(x, i, i-1)
				else:
					self._del_merge(x, i, i-1)
			self.delete(x.child[i], k)
	
	def _delete_internal_node(self, x, k, i):
		
		t = self.t
		
		if x.leaf:
			if x.keys[i][0] == k[0]:
				x.keys.pop(i)
				return
			return

		
		if len(x.child[i].keys) >= t :
			x.keys[i] = self._delete_predecessor(x.child[i])
			return
		
		elif len(x.child[i+1].keys) >= t:
			x.keys[i] = self._delete_successor(x.child[i+1])
			return
		
		else:
			self._del_merge(x, i, i+1)
			self._delete_internal_node(x.child[i], k, self.t - 1)

	def _delete_predecessor(self, x):
		
		if x.leaf:
			return x.pop()
		n = len(x.keys) - 1
		if len(x.child[n].keys) >= self.t:
			self._delete_sibling(x, n+1, n)
		else:
			self._del_merge(x, n, n+1)
		self._delete_predecessor(x.child[n])

	def _delete_successor(self, x):
		
		if x.leaf:
			return x.keys.pop(0)
		if len(x.child[1].keys) >= self.t:
			self._delete_sibling(x, 0, 1)
		else:
			self._del_merge(x, 0, 1)
		self._delete_successor(x.child[0])

	def _del_merge(self, x, i, j):
		
		cnode = x.child[i]

		
		if j > i:			
			rsnode = x.child[j]
			cnode.keys.append(x.keys[i])
			#Assigning keys of right sibling node to child node
			for k in range(len(rsnode.keys)):
				cnode.keys.append(rsnode.keys[k])
				if len(rsnode.child) > 0:
					cnode.child.append(rsnode.child[k])
			if len(rsnode.child) > 0:
				cnode.child.append(rsnode.child.pop())
			new = cnode
			x.keys.pop(i)
			x.child.pop(j)
		else :
			lsnode = x.child[j]
			lsnode.keys.append(x.keys[j])
			for i in range(len(cnode.keys)):
				lsnode.keys.append(cnode.keys[i])
				if len(lsnode.child) > 0:
					lsnode.child.append(cnode.child[i])
			if len(lsnode.child) > 0:
				lsnode.child.append(cnode.child.pop())
			new = lsnode
			x.keys.pop(j)
			x.child.pop(i)
		
		if x == self.root and len(x.keys) == 0:
			self.root = new

	def _delete_sibling(self, x, i, j):
		
		cnode = x.child[i]
		if i < j:
			rsnode = x.child[j]
			cnode.keys.append(x.keys[i])
			x.keys[i] = rsnode.keys[0]
			if len(rsnode.child)>0:
				cnode.child.append(rsnode.child[0])
				rsnode.child.pop(0)
			rsnode.keys.pop(0)
		else :
			lsnode = x.child[j]
			cnode.keys.insert(0,x.keys[i-1])
			x.keys[i-1] = lsnode.keys.pop()
			if len(lsnode.child)>0:
				cnode.child.insert(0,lsnode.child.pop())

def main():

	B = BTree(10000)
	start = time.time()
	print("B-Tree is being constructed")
	#print("The time before the construction of btree\n")
	#print(datetime.datetime.time(datetime.datetime.now()))
	with open('US.txt', 'r') as f:
		
		for line in f:
			word = line.split("\t")
			B.insert((hash(word[2]), int(word[1]), word[2]))
	#print("The time after the construction of btree\n")
	#print(datetime.datetime.time(datetime.datetime.now()))
	print("Time for B-Tree to be built")
	print("--- %s seconds ---" % (time.time() - start))
	c = 5
	while c > 0 :
		print("Enter your choice")
		print("1) Insert new place and pin")
		print("2) Delete")
		print("3) Search by place")
		print("4) Print the B-Tree")
		print("0) Exit")
		c = int(input())

		if c == 1:
			pin = int(input("Enter the pin: "))
			place = input("Enter the place name : ")
			startI = time.time()
			B.insert((hash(place), pin, place))
			print("Time for the place to be inserted :   %s seconds " % (time.time() - startI))
			print("Your data has been entered")
		elif c == 2:
			place = input("Enter the place name: ")
			startD = time.time()
			B.delete(B.root, hash(place))
			print("Time for the place to be deleted :   %s seconds " % (time.time() - startD))

			
		elif c == 3:
			place = input("Enter the place name to be searched: ")
			startS = time.time()
			K = B.search(hash(place))
			if K != None:
				(x, i) = K
				print("The place ", x.keys[i][2], " has following pin codes")
				for j in range(i,len(x.keys)):
					if x.keys[j][2] == place:
						print('Pin:', x.keys[j][1])
						print("Time taken for the place to be searched :   %s seconds " % (time.time() - startS))

						
			else:	
				print("Place doesn't exist on this planet!")
		elif c == 4:
			#f = open("Tree.txt","w+")
			#tree = str(B.root)
			#f.write(tree)
			#print("Check tree ")
			B.print_tree(B.root)
			#f.write(x)
			#f.close()		
		else :
			break


if __name__ == '__main__':
	main()
