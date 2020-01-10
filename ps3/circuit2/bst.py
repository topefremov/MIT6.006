class BST(object):
    """
Simple binary search tree implementation.
This BST supports insert, find, and delete-min operations.
Each tree contains some (possibly 0) BSTnode objects, representing nodes,
and a pointer to the root.
"""

    def __init__(self):
        self.root = None

    def insert(self, t):
        """Insert key t into this BST, modifying it in-place."""
        new = BSTnode(t)
        if self.root is None:
            self.root = new
        else:
            node = self.root
            while True:
                if t < node.key:
                    # Go left
                    if node.left is None:
                        node.left = new
                        new.parent = node
                        break
                    node = node.left
                else:
                    # Go right
                    if node.right is None:
                        node.right = new
                        new.parent = node
                        break
                    node = node.right
        
        new.update_sizes_rec()            
        return new
    
    def delete(self, t):
        """Delete key t from this BST, modifying it in-place"""
        node = self.find(t)
        if node is None:
            return None
    
        if node.left == None:
            self._transplant(node, node.right)
        elif node.right == None:
            self._transplant(node, node.left)
        else:
            _node = node.right.min()
            if (_node.parent != node):
                self._transplant(_node, _node.right)
                _node.right = node.right
                _node.right.parent = _node
            
            self._transplant(node, _node)
            _node.left = node.left
            _node.left.parent = _node
        
        parent = node.parent
        node.disconnect()
        
        if parent is not None:
            parent.update_sizes_rec()
        
        return node, parent

    def rank(self, t):
        """Return the number of keys <= t in the subtree rooted at root."""
        if self.root is not None:
            return self.root.rank(t)
        else:
            return 0

    def find(self, t):
        """Return the node for key t if is in the tree, or None otherwise."""
        node = self.root
        while node is not None:
            if t == node.key:
                return node
            elif t < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def delete_min(self):
        """Delete the minimum key (and return the old node containing it)."""
        if self.root is None:
            return None, None
        else:
            # Walk to leftmost node.
            node = self.root
            while node.left is not None:
                node = node.left
            # Remove that node and promote its right subtree.
            if node.parent is not None:
                node.parent.left = node.right
            else: # The root was smallest.
                self.root = node.right
            if node.right is not None:
                node.right.parent = node.parent
                    
            parent = node.parent
            node.disconnect()
            
            if parent is not None:
                parent.update_sizes_rec()
            
            return node, parent

    def _transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else: 
            u.parent.right = v
        if v != None:
            v.parent = u.parent


    def __str__(self):
        if self.root is None: return '<empty tree>'
        def recurse(node):
            if node is None: return [], 0, 0
            label = str(node.key) + "(" + str(node.size) + ")"
            left_lines, left_pos, left_width = recurse(node.left)
            right_lines, right_pos, right_width = recurse(node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and node.parent is not None and \
               node is node.parent.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.': label = ' ' + label[1:]
            if label[-1] == '.': label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle-2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
              [left_line + ' ' * (width - left_width - right_width) +
               right_line
               for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width
        return '\n'.join(recurse(self.root) [0])

class BSTnode(object):
    """
Representation of a node in a binary search tree.
Has a left child, right child, and key value.
"""
    def __init__(self, t):
        """Create a new leaf with key t."""
        self.key = t
        self.size = 1
        self.disconnect()
    
    def update_sizes_rec(self):
        node = self
        while node is not None:
            node.update_sizes()
            node = node.parent
    
    def update_sizes(self):
       """Updates this node's size based on its children's sizes."""
       if (self.left is None and self.right is None):
           self.size = 1
       else:
        self.size = (1 if self.left is None else self.left.size) + (1 if self.right is None else self.right.size) 
    
    def rank(self, t):
       """Return the number of keys <= t in the subtree rooted at this node."""
       left_size = 0 if self.left is None else self.left.size
       if t == self.key:
            return left_size + 1
       elif t < self.key:
           if self.left is None:
                return 0
           else:
                return self.left.rank(t)
       else:
            if self.right is None:
                return left_size + 1
            else:
                return self.right.rank(t) + left_size + 1
    
    def min(self):
        """Find the minimum element rooted by this node"""
        node = self
        while node.left is not None:
            node = node.left
        return node

    
    def disconnect(self):
        self.left = None
        self.right = None
        self.parent = None

def test(args=None, BSTtype=BST):
    import random, sys
    if not args:
        args = sys.argv[1:]
    if not args:
        print 'usage: %s <number-of-random-items | item item item ...>' % \
              sys.argv[0]
        sys.exit()
    elif len(args) == 1:
        items = (random.randrange(100) for i in xrange(int(args[0])))
    else:
        items = [int(i) for i in args]

    tree = BSTtype()
    print tree
    for item in items:
        tree.insert(item)
        print
        print tree

if __name__ == '__main__': test()
