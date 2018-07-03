import angr

class CFGworker:
	
	def __init__(self, path):

		b = angr.Project(path, load_options={"auto_load_libs": False})
		cfg = b.analyses.CFGAccurate(show_progressbar=True)

		for addr, f in b.kb.functions.items():
			print hex(addr)
			print f.name
			print '----------------------------------'

		self.func_name = 'sub_413920'
		self.CFG = cfg.get_function_subgraph(self.func_name)

		self.func_addr = b.kb.functions[self.func_name].addr
		self.func_end = self.func_addr + b.kb.functions[self.func_name].size
		
		self.Branches = [i for i in self.CFG.get_branching_nodes() if i.addr <= self.func_end]
		self.N = [i for i in self.CFG.nodes()]
		self._sortNodes()

		print 'Nodes: %d' %len(self.N)
		
		self.PATHS = []
		self.PC = []		
		self.Loops = []

		self.curp = [] #for recursive alg

		print 'OK'


	def _isBranch(self, node):
		return node in self.Branches			

	def getNode(self, node_addr):
		for n in self.N:
			if n.addr == node_addr:
				return n			

	def _sortNodes(self):
		tmp_nodes = []
		nodes_addrs = [(i.addr, i) for i in self.N]
		nodes_addrs.sort()
		for i, j in nodes_addrs:
			tmp_nodes.append(j)
		self.N = tmp_nodes

	def nextNode(self, node):
		neighbors = [i for i in self.CFG.graph.neighbors(node)]
		l = len(neighbors)
		m = None
		if node.block != None:
			m = node.block.capstone.insns[-1].mnemonic
		if l == 2:
			#it's branch
			return neighbors
		elif l == 1:
			if m == 'call':
				indx = self.N.index(node)
				#uchitivat last node in list?
				return [self.N[indx+1]]
			else:
				return neighbors
		else:
			return []
				
	def getPath(self):
		path = []
		pc = []
		lf = 0
		cur_node = self.getNode(self.func_addr)
		while True:
			if not self._isLOOP(path):
				path.append(cur_node.addr)
				if self._isBranch(cur_node): #or cur_node.addr == self.func_addr:
					pc.append(cur_node.addr)

				nd = self.nextNode(cur_node)
				if len(nd) == 0: #or nd[0].addr > self.func_end:
					break
				cur_node = nd[0]
			else:
				print 'CATCH LOOP'
				break
		self.PATHS.append(path)
		self.PC.append(pc)

	def getNewPath(self, path, pc, node):
		indx = path.index(node.addr)
		path = path[:indx+1]
		indx = pc.index(node.addr)
		pc = pc[:indx+1]

		cur_node = self.nextNode(node)[1]
		while True:
			if not self._isLOOP(path):
				path.append(cur_node.addr)
				if self._isBranch(cur_node): #or cur_node.addr == self.func_addr:
					pc.append(cur_node.addr)
				nd = self.nextNode(cur_node)
				if len(nd) == 0 or nd[0].addr > self.func_end:
					break
				cur_node = nd[0]
			else:
				print 'CATCH LOOP'
				break
		self.PATHS.append(path)
		self.PC.append(pc)

	def getAllPaths(self): #iterative
		cur_node = self.getNode(self.func_addr)
		forward_stack = [cur_node]
		backward_stack = []
		path = []
		while True:
			cur_node = forward_stack.pop()
			path.append(cur_node.addr)

			s = self.nextNode(cur_node)
			if len(s) == 2:
				backward_stack.append(len(path)) #path = path[:i+1]

			if len(s) == 0 or self._isLOOP(path):
				self.PATHS.append(path)
				if len(backward_stack) != 0:
					indx = backward_stack.pop()
					path = [path[i] for i in range(indx)] 

			for n in s:
				forward_stack.append(n)
			
			if forward_stack == [] or len(self.PATHS) > 1000: #not enough memmory
				break 

	def RgetAllPaths(self, node): #recursive
		self.curp.append(node.addr)
		s = self.nextNode(node)

		if self._isLOOP(self.curp):
			p = self.curp
			self.PATHS.append(p)
			return

		if len(s) == 0:
			p = self.curp
			self.PATHS.append(p)

		for n in s:
			self.RgetAllPaths(n)
			self.curp.pop()

	def _isLOOP(self, path):
		l = len(path)
		if l < 2:
			return False
		a = path[-1]
		stack = [a]
		for i in range(l-2, -1, -1):
			if path[i] != a:
				stack.append(path[i])
			else:
				stack = stack[::-1]
				if stack == path[i-len(stack)+1:i+1]:
					self.Loops.append(path)
					return True
				else:
					return False
		return False

def main():
	path = '/home/angr/openssl'
	w = CFGworker(path)
	w.getAllPaths()
	print w.PATHS

if __name__ == '__main__':
	main()