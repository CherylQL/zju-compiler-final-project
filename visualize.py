from graphviz import Digraph

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
            for child in current.children:
                stack.append((child, count))
                if child.name != "":
                    if child.name == "<>":  # <>会干扰显示（底层用的是html标签）
                        self.dot.node(str(count), "!=")
                    else:
                        self.dot.node(str(count), "%s" % (child.name))
                else:
                    self.dot.node(str(count), child.type)
                self.dot.edge(str(last_id), str(count))
                count += 1

    def png(self):
        self.dot.format = 'png'
        self.dot.render('ParsingTree', view=False)
