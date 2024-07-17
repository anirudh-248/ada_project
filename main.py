import streamlit as st
from graphviz import Digraph

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

def height(node):
    if node is None:
        return 0
    return node.height

def max(a, b):
    return a if a > b else b

def newNode(data):
    return Node(data)

def getBalance(node):
    if node is None:
        return 0
    return height(node.left) - height(node.right)

def rightRotate(y):
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    y.height = max(height(y.left), height(y.right)) + 1
    x.height = max(height(x.left), height(x.right)) + 1

    return x

def leftRotate(x):
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    x.height = max(height(x.left), height(x.right)) + 1
    y.height = max(height(y.left), height(y.right)) + 1

    return y

def insert(node, data, step=None):
    if node is None:
        return newNode(data), step

    step += 1
    if data < node.data:
        node.left, step = insert(node.left, data, step)
    elif data > node.data:
        node.right, step = insert(node.right, data, step)
    else:
        return node, step

    node.height = 1 + max(height(node.left), height(node.right))

    balance = getBalance(node)

    if balance > 1 and data < node.left.data:
        return rightRotate(node), step

    if balance < -1 and data > node.right.data:
        return leftRotate(node), step

    if balance > 1 and data > node.left.data:
        node.left = leftRotate(node.left)
        return rightRotate(node), step

    if balance < -1 and data < node.right.data:
        node.right = rightRotate(node.right)
        return leftRotate(node), step

    return node, step

def inOrder(root, ls):
    if root is not None:
        inOrder(root.left, ls)
        ls.append(root.data)
        inOrder(root.right, ls)

def preOrder(root, ls):
    if root is not None:
        ls.append(root.data)
        preOrder(root.left, ls)
        preOrder(root.right, ls)

def visualize_tree(node, graph=None):
    if graph is None:
        graph = Digraph()
        graph.attr('node', shape='circle')

    if node is not None:
        if node.left:
            graph.edge(str(node.data), str(node.left.data))
            visualize_tree(node.left, graph)
        if node.right:
            graph.edge(str(node.data), str(node.right.data))
            visualize_tree(node.right, graph)
    return graph

def custom_write(ls):
    return ', '.join(f'{item}' for item in ls)

st.title("ADA Project - AVL Tree")

uploaded_file = st.file_uploader("Upload the input file", type="txt")
if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    numbers = [int(num) for num in content.strip().split() if num.isdigit()]
    
    root = None
    steps = []
    step = 0
    graph = Digraph()
    graph.attr('node', shape='circle')

    for key in numbers:
        root, step = insert(root, key, step)
        current_graph = visualize_tree(root, Digraph())
        steps.append(current_graph.source)

    ino = []
    pre = []

    inOrder(root, ino)
    preOrder(root, pre)

    st.subheader("Construction of AVL tree:")
    if steps:
        step_index = st.slider('Step', 0, len(steps)-1, 0)
        st.graphviz_chart(steps[step_index])

    st.subheader("Inorder Traversal of the AVL tree:")
    st.write(custom_write(ino))

    st.subheader("Preorder Traversal of the AVL tree:")
    st.write(custom_write(pre))

    st.subheader("Final AVL Tree Structure:")
    final_graph = visualize_tree(root, Digraph())
    st.graphviz_chart(final_graph.source)
