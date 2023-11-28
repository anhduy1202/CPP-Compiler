from dataclasses import dataclass

@dataclass
class IntNode:
	value: any

	def __repr__(self):
		return f"{self.value}"

@dataclass
class AddNode:
	left: any
	right: any

	def __repr__(self):
		return f"({self.left}+{self.right})"

@dataclass
class SubtractNode:
	left: any
	right: any

	def __repr__(self):
		return f"({self.left}-{self.right})"

@dataclass
class MultiplyNode:
	left: any
	right: any

	def __repr__(self):
		return f"({self.left}*{self.right})"

@dataclass
class DivideNode:
	left: any
	right: any

	def __repr__(self):
		return f"({self.left}/{self.right})"

@dataclass
class PositiveNode:
	node: any

	def __repr__(self):
		return f"(+{self.node})"
	
@dataclass
class NegativeNode:
	node: any

	def __repr__(self):
		return f"(-{self.node})"
