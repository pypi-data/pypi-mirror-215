from collections import deque

class Node:
    """tree element"""
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

def search(root, key):
    """search tree by key"""
    if not root:
        return None
    if key < root.key:
        return search(root.left, key)
    if key > root.key:
        return search(root.right, key)
    return root.val

def insert(root, key, val):
    """insert a node"""
    # Return a new node if the tree is empty
    if not root:
        return Node(key, val)

    # Traverse to the right place and insert the node
    if key < root.key:
        root.left = insert(root.left, key, val)
    else:
        root.right = insert(root.right, key, val)

    return root

def inorder_successor(root):
    """find inorder successor"""
    current = root

    while current.left:
        current = current.left

    return current

def delete(root, key):
    """delete node"""
    if not root:
        # Key is not in tree
        return root

    # Find the node to be deleted
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        # If the node is with only one child or no child
        if root.left is None:
            temp = root.right
            root = None
            return temp

        if root.right is None:
            temp = root.left
            root = None
            return temp

        # If the node has two children,
        # place the inorder successor in position of the node to be deleted
        temp = inorder_successor(root.right)

        root.key = temp.key

        # Delete the inorder successor
        root.right = delete(root.right, temp.key)

    return root

def serialize(root):
    """serialize tree to string"""
    if not root:
        return ""

    result = ""
    q = deque()
    q.append(root)
    while len(q) > 0:
        cur = q.popleft()
        if cur:
            result += str(cur.key) + ":" + str(cur.val)
            if cur.left:
                q.append(cur.left)
            else:
                q.append(None)
            if cur.right:
                q.append(cur.right)
            else:
                q.append(None)
        else:
            result += "NULL:NULL"
        result += ","

    return result

def deserialize(string):
    """deserialize tree from string"""
    # Parse string into array of strings
    tmp = string.split(",")
    data = []

    for i in range(len(tmp)-1):
        # Separate strings into key-value pairs
        data.append(tmp[i].split(":"))

    return make(data)

def make(elements):
    """make tree from array of key-value pairs"""
    root = None

    for element in elements:
        key = element[0]
        val = element[1]

        # Skip over null nodes
        if key != "NULL":
            root = insert(root, key, val)

    return root
