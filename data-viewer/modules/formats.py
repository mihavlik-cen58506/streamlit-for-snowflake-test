import pandas as pd

indent = "  "


def getJson(df):
    """
    { "name": "KING",
      "children": [{
         "name": "BLAKE",
         "children": [
            { "name": "ALLEN" },
            { "name": "JAMES" },
            ...
        ]}]
    }
    """

    # collect all nodes
    nodes = {}
    for _, row in df.iterrows():
        name = row.iloc[0]
        nodes[name] = {"name": name}

    if df.empty:
        return {}

    # collect all nodes
    nodes = {}
    for _, row in df.iterrows():
        name = row.iloc[0]
        if pd.isna(name):
            continue
        nodes[name] = {"name": name}

    # move children under parents, and detect root
    root = None
    for _, row in df.iterrows():
        if pd.isna(row.iloc[0]):
            continue

        node = nodes.get(row.iloc[0])
        parent_name = row.iloc[1] if len(row) > 1 else None
        isRoot = pd.isna(parent_name)

        if isRoot:
            root = node
        else:
            parent = nodes.get(parent_name)
            if parent:
                if "children" not in parent:
                    parent["children"] = []
                parent["children"].append(node)
            else:
                print(
                    f"Warning: Parent '{parent_name}' not found for child '{row.iloc[0]}'"
                )

    return root or {}


def getXml(node, level=0):
    """
    <object>
      <name>KING</name>
      <children>
        <object>
          <name>BLAKE</name>
          <children>
              <object>
                <name>ALLEN</name>
              </object>
              <object>
                <name>JAMES</name>
              </object>
    ...
    """

    if not node:
        return ""  # Return empty string if node is None or empty

    # add <object> and <name>
    indent0 = indent * level
    indent1 = indent0 + indent

    s = '<?xml version="1.0" encoding="utf-8"?>\n' if level == 0 else ""
    s += f"{indent0}<object>\n"
    s += f"{indent1}<name>{node['name']}</name>\n"

    # recursively append the inner children
    if "children" in node and node["children"]:
        s += f"{indent1}<children>\n"
        for child in node["children"]:
            s += getXml(child, level + 2)
        s += f"{indent1}</children>\n"

    s += f"{indent0}</object>\n"
    return s


def getYaml(node, level=0, first=False):
    """
    KING
    - BLAKE
      - ALLEN
        JAMES
        MARTIN
    ...
    """

    if not node:
        return ""

    indent0 = indent * level
    indent1 = indent0 + "  "

    s = f"{node['name']}\n"
    if "children" in node and node["children"]:
        first = True
        for child in node["children"]:
            s += f"{indent0}- " if first else indent1
            s += getYaml(child, level + 1, first)
            first = False

    return s


def getPath(node, nodes, path=""):
    """
    [{ "id": "KING.JONES.SCOTT.ADAMS" },
    { "id": "KING.BLAKE.ALLEN" },
    { "id": "KING.BLAKE" },
    { "id": "KING.CLARK" },
    ...]
    """

    if nodes is None:
        nodes = []

    if not node:
        return nodes

    # append full path to the top of the current node
    path += node["name"] if not path else f'.{node["name"]}'
    nodes.append({"id": path})

    if "children" in node and node["children"]:
        for child in node["children"]:
            getPath(child, nodes, path)

    return nodes
