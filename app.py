import streamlit as st
import math
import random

st.set_page_config(page_title="Data Structure Visualizer", layout="wide")

VIBRANT_COLORS = [
    "#FF6F61", "#6B5B95", "#88B04B", "#F7CAC9", "#92A8D1", "#955251", "#B565A7", "#009B77", "#DD4124", "#45B8AC",
    "#EFC050", "#5B5EA6", "#9B2335", "#DFCFBE", "#55B4B0", "#E15D44", "#7FCDCD", "#BC243C", "#C3447A", "#98B4D4"
]

st.title("📊 Data Structure Visualizer")
tabs = st.tabs(["Array", "Tree", "BST", "DFS"])

# --- Array Visualization ---
with tabs[0]:
    st.header("Array Traversal")
    arr_input = st.text_input("Enter array elements (comma separated):", "1,2,3,4,5")
    arr = [x.strip() for x in arr_input.split(",") if x.strip()]
    if 'array_step' not in st.session_state or st.session_state.get('array_input_last') != arr_input:
        st.session_state.array_step = 0
        st.session_state.array_input_last = arr_input
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Next Step", key="array_next") and arr:
            st.session_state.array_step = (st.session_state.array_step + 1) % len(arr)
    with col2:
        if st.button("Reset", key="array_reset"):
            st.session_state.array_step = 0
    if arr:
        i = st.session_state.array_step
        st.write(f"**Traversing array:** Highlighting element at index {i} (value: {arr[i]})")
        cols = st.columns(len(arr))
        for j, v in enumerate(arr):
            color = "#ffd700" if j == i else VIBRANT_COLORS[j % len(VIBRANT_COLORS)]
            with cols[j]:
                st.markdown(f"""
                    <div style='background:{color};border-radius:15px;padding:20px 0;margin:5px;text-align:center;font-size:2em;font-weight:bold;color:#222;'>{v}</div>
                """, unsafe_allow_html=True)

# --- Tree Visualization ---
def draw_tree(nodes, highlight_index=None):
    import matplotlib.pyplot as plt
    n = len(nodes)
    if n == 0:
        return
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.axis('off')
    levels = math.floor(math.log2(n)) + 1
    node_radius = 0.2
    v_spacing = 1.2
    h_margin = 0.5
    positions = {}
    for i in range(n):
        level = math.floor(math.log2(i+1))
        max_nodes = 2 ** level
        index_in_level = i - (2 ** level - 1)
        y = -level * v_spacing
        total_width = max_nodes * (node_radius * 2 + h_margin)
        if max_nodes == 1:
            x = 0
        else:
            x = -total_width/2 + index_in_level * (total_width / (max_nodes - 1))
        positions[i] = (x, y)
    # Draw lines
    for i in range(n):
        parent = (i - 1) // 2
        if i != 0 and parent >= 0:
            x1, y1 = positions[parent]
            x2, y2 = positions[i]
            ax.plot([x1, x2], [y1, y2], color="#7b8fa1", linewidth=2)
    # Draw nodes
    for i, val in enumerate(nodes):
        x, y = positions[i]
        color = "#ffd700" if i == highlight_index else VIBRANT_COLORS[i % len(VIBRANT_COLORS)]
        circle = plt.Circle((x, y), node_radius, color=color, ec="#2d3a4b", lw=2, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(val), fontsize=16, ha='center', va='center', color="#222", zorder=3)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-levels*v_spacing, 1)
    st.pyplot(fig)

with tabs[1]:
    st.header("Binary Tree (Level Order)")
    tree_input = st.text_input("Enter tree nodes (comma separated):", "A,B,C,D,E,F,G")
    tree_nodes = [x.strip() for x in tree_input.split(",") if x.strip()]
    if 'tree_step' not in st.session_state or st.session_state.get('tree_input_last') != tree_input:
        st.session_state.tree_step = 0
        st.session_state.tree_input_last = tree_input
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Next Step", key="tree_next") and tree_nodes:
            st.session_state.tree_step = (st.session_state.tree_step + 1) % len(tree_nodes)
    with col2:
        if st.button("Reset", key="tree_reset"):
            st.session_state.tree_step = 0
    if tree_nodes:
        i = st.session_state.tree_step
        parent = (i - 1) // 2 if i != 0 else None
        if i == 0:
            reasoning = f"Placing root node with value {tree_nodes[0]}."
        else:
            if parent is not None and parent >= 0:
                side = "left" if i == 2 * parent + 1 else "right"
                reasoning = f"Placing node with value {tree_nodes[i]} as {side} child of node {tree_nodes[parent]}."
            else:
                reasoning = f"Placing node with value {tree_nodes[i]}."
        st.write(reasoning)
        draw_tree(tree_nodes, highlight_index=i)

# --- BST Visualization ---
class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def bst_insert(root, value, highlight=False, path=None):
    if path is None:
        path = []
    if root is None:
        node = BSTNode(value)
        path.append(node)
        return node, node if highlight else node, path
    path.append(root)
    if value < root.value:
        root.left, node, path = bst_insert(root.left, value, highlight, path)
        return root, node, path
    else:
        root.right, node, path = bst_insert(root.right, value, highlight, path)
        return root, node, path

def build_bst(values, highlight_index):
    root = None
    highlight_node = None
    path = []
    for i, v in enumerate(values):
        highlight = (i == highlight_index)
        root, node, node_path = bst_insert(root, v, highlight)
        if highlight:
            highlight_node = node
            path = node_path
    return root, highlight_node, path

def draw_bst(root, highlight_node=None, path=None):
    import matplotlib.pyplot as plt
    def get_levels(node):
        if not node:
            return 0
        return 1 + max(get_levels(node.left), get_levels(node.right))
    def assign_positions(node, x0, x1, y, v_spacing, positions):
        if not node:
            return
        x = (x0 + x1) / 2
        positions[node] = (x, y)
        assign_positions(node.left, x0, x, y - v_spacing, v_spacing, positions)
        assign_positions(node.right, x, x1, y - v_spacing, v_spacing, positions)
    if not root:
        return
    levels = get_levels(root)
    node_radius = 0.2
    v_spacing = 1.2
    width = 2 ** levels
    positions = {}
    assign_positions(root, 0, width, 0, v_spacing, positions)
    fig, ax = plt.subplots(figsize=(8, 3 + levels))
    ax.axis('off')
    # Draw lines
    def draw_lines(node):
        if not node:
            return
        if node.left:
            x1, y1 = positions[node]
            x2, y2 = positions[node.left]
            color = "#ffb347" if path and node in path and node.left in path else "#7b8fa1"
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=4 if color == "#ffb347" else 2)
            draw_lines(node.left)
        if node.right:
            x1, y1 = positions[node]
            x2, y2 = positions[node.right]
            color = "#ffb347" if path and node in path and node.right in path else "#7b8fa1"
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=4 if color == "#ffb347" else 2)
            draw_lines(node.right)
    draw_lines(root)
    # Draw nodes
    def draw_nodes(node):
        if not node:
            return
        x, y = positions[node]
        color = "#ffd700" if node == highlight_node else random.choice(VIBRANT_COLORS)
        if path and node in path:
            color = "#ffb347"
        circle = plt.Circle((x, y), node_radius, color=color, ec="#2d3a4b", lw=2, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, str(node.value), fontsize=16, ha='center', va='center', color="#222", zorder=3)
        draw_nodes(node.left)
        draw_nodes(node.right)
    draw_nodes(root)
    ax.set_xlim(-1, width + 1)
    ax.set_ylim(-levels * v_spacing, 1)
    st.pyplot(fig)

with tabs[2]:
    st.header("Binary Search Tree (BST)")
    bst_input = st.text_input("Enter BST values (comma separated):", "7,3,10,1,5,8,12")
    bst_values = []
    try:
        bst_values = [int(x.strip()) for x in bst_input.split(",") if x.strip()]
    except:
        st.warning("Please enter only integer values for BST.")
    if 'bst_step' not in st.session_state or st.session_state.get('bst_input_last') != bst_input:
        st.session_state.bst_step = 0
        st.session_state.bst_input_last = bst_input
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Next Step", key="bst_next") and bst_values:
            st.session_state.bst_step = (st.session_state.bst_step + 1) % len(bst_values)
    with col2:
        if st.button("Reset", key="bst_reset"):
            st.session_state.bst_step = 0
    if bst_values:
        i = st.session_state.bst_step
        root, highlight_node, path = build_bst(bst_values, i)
        val = bst_values[i]
        if i == 0:
            reasoning = f"Inserting {val}: Tree is empty, insert as root."
        else:
            path_str = []
            for j in range(len(path)-1):
                if val < path[j].value:
                    path_str.append(f"{val} < {path[j].value}, go left.")
                else:
                    path_str.append(f"{val} >= {path[j].value}, go right.")
            path_str.append("Insert here.")
            reasoning = f"Inserting {val}: " + ' '.join(path_str)
        st.write(reasoning)
        draw_bst(root, highlight_node, path)

# --- DFS Visualization ---
def draw_graph(nodes, edges, visited, stack, highlight, highlight_edge):
    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for edge in edges:
        if '-' in edge:
            a, b = edge.split('-')
            a, b = a.strip(), b.strip()
            G.add_edge(a, b)
    pos = nx.circular_layout(G)
    fig, ax = plt.subplots(figsize=(7, 4))
    nx.draw_networkx_edges(G, pos, ax=ax, width=2, edge_color="#7b8fa1")
    if highlight_edge:
        nx.draw_networkx_edges(G, pos, edgelist=[highlight_edge], ax=ax, width=4, edge_color="#ffb347")
    node_colors = []
    for n in G.nodes:
        if n == highlight:
            node_colors.append("#ffd700")
        elif n in visited:
            node_colors.append(VIBRANT_COLORS[nodes.index(n) % len(VIBRANT_COLORS)])
        else:
            node_colors.append("#eaf0fa")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, edgecolors="#2d3a4b", linewidths=2, node_size=900)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=16, font_color="#222")
    ax.axis('off')
    st.pyplot(fig)

with tabs[3]:
    st.header("DFS on Graph")
    dfs_nodes_input = st.text_input("Nodes (comma separated):", "A,B,C,D,E")
    dfs_edges_input = st.text_input("Edges (A-B,B-C,...):", "A-B,B-C,C-D,D-E,A-E")
    nodes = [x.strip() for x in dfs_nodes_input.split(",") if x.strip()]
    edges = [x.strip() for x in dfs_edges_input.split(",") if x.strip()]
    if 'dfs_step' not in st.session_state or st.session_state.get('dfs_input_last') != (dfs_nodes_input, dfs_edges_input):
        st.session_state.dfs_step = 0
        st.session_state.dfs_input_last = (dfs_nodes_input, dfs_edges_input)
        st.session_state.dfs_steps = []
        if nodes and edges:
            adj = {n: [] for n in nodes}
            for edge in edges:
                if '-' in edge:
                    a, b = edge.split('-')
                    a, b = a.strip(), b.strip()
                    if a in adj and b in adj:
                        adj[a].append(b)
                        adj[b].append(a)
            steps = []
            stack_history = []
            def dfs(node, parent, visited, stack):
                steps.append(("visit", node, set(visited), list(stack), parent))
                visited.add(node)
                stack.append(node)
                stack_history.append(list(stack))
                for neighbor in sorted(adj[node]):
                    if neighbor not in visited:
                        steps.append(("recurse", node, set(visited), list(stack), neighbor))
                        dfs(neighbor, node, visited, stack)
                steps.append(("backtrack", node, set(visited), list(stack), parent))
                stack.pop()
                stack_history.append(list(stack))
            dfs(nodes[0], None, set(), [])
            st.session_state.dfs_steps = steps
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Next Step", key="dfs_next") and nodes and edges:
            st.session_state.dfs_step = (st.session_state.dfs_step + 1) % len(st.session_state.dfs_steps)
    with col2:
        if st.button("Reset", key="dfs_reset"):
            st.session_state.dfs_step = 0
    if nodes and edges and st.session_state.get('dfs_steps'):
        steps = st.session_state.dfs_steps
        i = st.session_state.dfs_step
        action, node, visited, stack, arg = steps[i]
        highlight = node
        highlight_edge = None
        if action == "recurse":
            highlight_edge = (node, arg)
        if action == "visit":
            reasoning = f"DFS visiting node {node}. Stack: {stack}"
        elif action == "recurse":
            reasoning = f"DFS at node {node}, recursing to {arg}. Stack: {stack}"
        elif action == "backtrack":
            reasoning = f"DFS backtracking from node {node}. Stack after pop: {stack}"
        else:
            reasoning = ""
        st.write(reasoning)
        draw_graph(nodes, edges, visited, stack, highlight, highlight_edge)
        st.markdown(f"**Stack:** {' → '.join(stack)}") 