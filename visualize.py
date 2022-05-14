from graphviz import Digraph
from random import randint


class Stack:
    def __init__(self, root=None):
        self.content = [root]

    def pop(self):
        return self.content.pop(0)

    def append(self, node):
        self.content.append(node)


class Viz:
    def __init__(self, root=None):
        self.dot = Digraph("ParseTree")
        if root:
            self.build(root)

    def build(self, root):
        count = 0
        stack = Stack((root, count))
        self.dot.node(str(count), root.type)
        count += 1
        while len(stack.content) > 0:
            current, last_id = stack.pop()
            # print(current)
            for child in current.children:
                stack.append((child, count))
                if child.name != "":
                    self.dot.node(str(count), "%s" % (child.name))
                else:
                    # print(child.type)
                    self.dot.node(str(count), child.type)
                self.dot.edge(str(last_id), str(count))
                count += 1

    def png(self):
        self.dot.format = 'png'
        self.dot.render('ParsingTree', view=False)
