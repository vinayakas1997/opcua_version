import os
import json
from opcua import Client, ua
import numpy as np
class OpcuaAutoNodeMapper:
    def __init__(self, client: Client, json_path="nodes.json",reload=False):
        self.client = client
        self.json_path = json_path
        self.node_map = {}
        self._initialize_node_map(reload)

    
        
        if os.path.exists(json_path):
            self._load_nodes_from_json()
        else:
            print("[INFO] JSON not found. Browsing server...")
            self._browse_and_save_nodes()

    def _initialize_node_map(self, reload=False):
        if reload:
            print("[INFO] Reloading node map to JSON")
            self.node_map = {}
            self._browse_and_save_nodes()
            print("[INFO] Node map reloaded")
            return
    
    def _load_nodes_from_json(self):
        with open(self.json_path) as f:
            self.node_map = json.load(f)
        print(f"[INFO] Loaded {len(self.node_map)} nodes from JSON")

    def _browse_and_save_nodes(self):
        # print("[INFO] JSON not found. Browsing server...")
        objects_node = self.client.get_objects_node()
        self.node_map = {}
        self._recursive_browse(objects_node)
        with open(self.json_path, "w") as f:
            json.dump(self.node_map, f, indent=4)
        print(f"[INFO] Saved {len(self.node_map)} nodes to {self.json_path}")

    def _recursive_browse(self, node):
        try:
            for child in node.get_children():
                try:
                    browse_name = child.get_browse_name().Name
                    # node_id_str = str(child.nodeid)
                    node_id_str = child.nodeid.to_string()
                    node_class = child.get_node_class()

                    if node_class == ua.NodeClass.Variable:
                        self.node_map[browse_name] = node_id_str

                    self._recursive_browse(child)

                except Exception as e:
                    print(f"[WARN] Skipping node: {e}")
        except Exception as e:
            print(f"[ERROR] Cannot browse: {e}")

    def _cast_to_type(self, value, variant_type):
        if variant_type == ua.VariantType.Int16:
            return np.int16(value)
        elif variant_type == ua.VariantType.Int32:
            return np.int32(value)
        elif variant_type == ua.VariantType.Int64:
            return np.int64(value)
        elif variant_type == ua.VariantType.UInt16:
            return np.uint16(value)
        elif variant_type == ua.VariantType.UInt32:
            return np.uint32(value)
        elif variant_type == ua.VariantType.UInt64:
            return np.uint64(value)
        elif variant_type == ua.VariantType.Float:
            return float(value)
        elif variant_type == ua.VariantType.Double:
            return float(value)
        elif variant_type == ua.VariantType.Boolean:
            return bool(value)
        elif variant_type == ua.VariantType.String:
            return str(value)
        else:
            print(f"[WARN] No cast rule for {variant_type.name}, using raw value")
            return value
    
    def read(self, name):
        return self.client.get_node(self.node_map[name]).get_value()

    def write(self, name, value):
        node = self.client.get_node(self.node_map[name])

        # Get expected VariantType from the node
        expected_type = node.get_data_type_as_variant_type()

        # Auto-cast Python value based on VariantType
        typed_value = self._cast_to_type(value, expected_type)

        # Wrap in Variant with correct type
        variant = ua.Variant(typed_value, expected_type)

        # Write to server
        node.set_value(variant)
        print(f"[INFO] Wrote value '{typed_value}' to '{name}' as {expected_type.name}")
    
    def get_node_map(self,name):
        return self.node_map[name]