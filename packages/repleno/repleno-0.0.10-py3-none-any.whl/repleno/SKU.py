from __future__ import annotations

from enum import Enum
from typing import List
from repleno.utils import *
import warnings
from collections import deque
import pptree
import logging
import hashlib


class OutputFormatter:
    """
    Makes things easier to store in a standard dictionary
    """

    def __init__(self, max_stack_size=None):
        self.records = {}
        self._skus = set()
        self._highest_level = None
        self._max_stack_size = max_stack_size
        self._stack_size = 0

    def store(self, sku, parent_skus, child_skus, direction, level=0):
        if not isinstance(sku, SKU):
            raise TypeError(f"sku must be an instance of Links, not of {type(sku)}")

        if isinstance(parent_skus, SKU):
            parent_skus = [parent_skus]

        if isinstance(child_skus, SKU):
            child_skus = [child_skus]

        self._skus.add(sku)

        # check stack size
        self._stack_size += 1
        if self._max_stack_size and self._stack_size > self._max_stack_size:
            raise BufferError("Stack size exceeded maximum stack size.")

        # create key if does not exist
        self.records.setdefault(
            sku,
            {
                "sku_level": 0,
                "parent_skus": set(),
                "child_skus": set(),
                "_iterations": 0
            },
        )

        # store the values
        if parent_skus:
            self.records[sku]["parent_skus"] = self.records[sku]["parent_skus"].union(
                parent_skus
            )

        if child_skus:
            self.records[sku]["child_skus"] = self.records[sku]["child_skus"].union(
                child_skus
            )

        self.records[sku]["_iterations"] = self.records[sku]["_iterations"] + 1

        self.records[sku]["sku_level"] = level

        # check level
        if self._highest_level is None or self._highest_level < level:
            self._highest_level = level

        if direction not in ["children", "parents"]:
            raise TypeError(f"direction must be one either 'children' or 'parents'")

        if direction == "children":
            if level < self.records[sku]["sku_level"]:
                self.records[sku]["sku_level"] = level

        if direction == "parents":
            if level > self.records[sku]["sku_level"]:
                self.records[sku]["sku_level"] = level

    def get_output(self, skus_only=False, attributes=None, hash_keys=False):
        if skus_only:
            skus = self.records.keys()
            return [(sku.item, sku.location) for sku in skus]

        f_result = deque()
        sku_id_pairs = {}

        for sku, val in self.records.items():
            SKUing = str(sku.location) + str(sku.item)

            # Get or generate hash for all skus in this iteration
            # Why? Hash skus to avoid having special characters in ID
            sku_id_pairs.setdefault(
                sku, hashlib.sha256(SKUing.encode()).hexdigest()
            )
            sku_id = sku_id_pairs[sku]

            parent_ids = set()
            for p_sku in val["parent_skus"]:
                parent_SKUing = str(p_sku.location) + str(p_sku.item)
                p_id = sku_id_pairs.setdefault(
                    p_sku, hashlib.sha256(parent_SKUing.encode()).hexdigest()
                )
                parent_ids.add(p_id)

            id_prefix = "id_"  # so ID always starts with letters
            record = {
                "id": id_prefix + sku_id,
                "location": sku.location,
                "item": sku.item,
                "parents": list(sorted([id_prefix + i for i in parent_ids])),
                "level": ((-1) * (val["sku_level"] - self._highest_level)) + 1,
            }

            if attributes:
                for attr in attributes:
                    try:
                        record[attr] = getattr(sku, attr)
                    except Exception as e:
                        print(e)
                        raise


            # Add items without parents at the beginning of the list
            if len(val["parent_skus"]) == 0:
                f_result.appendleft(record)
            else:
                f_result.append(record)

        return list(f_result)



class SKUType(Enum):
    PARENT = "ultimate parent"
    INTERMEDIATE = "intermediate"
    CHILD = "ultimate child"
    UNDEFINED = "undefined"


class _SKULink:
    __slot__ = ["sku", "qty"]

    def __init__(self, sku: SKU, qty: float):
        if not isinstance(sku, SKU):
            raise TypeError(f"sku must be an SKU instance.")

        self.sku = sku
        self.qty = qty

    def __repr__(self):
        return f"{self.sku}"

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, value):
        if value is None:
            self._qty = 1
            return
        value = convert_to_float(value)

        if value <= 0:
            raise ValueError("Quantity must be a positive number.")

        self._qty = value


class SKU:
    """Any single article held in stock inside of the factory. It can be any
    item finished good (FG), semi-assemblies or raw-materials.
    """

    __slot__ = ["item", "location", "sellable", "phantom", "obsolete", "_type", "status", "_abc_classifications", "abc_classification", "safety_stock_qty", "lead_time", "inventory_qty", "minimum_order_qty", "batch_qty", "_child_links", "_parent_links", "_pptree_parents", "_pptree_children"]

    classification_rank = {
        "AX": 90,
        "AY": 80,
        "AZ": 70,
        "BX": 60,
        "BY": 50,
        "BZ": 40,
        "CX": 30,
        "CY": 20,
        "CZ": 10,
        "NA": 00,
    }

    def __init__(
        self,
        item,
        location,
        inventory_qty: float = 0,
        minimum_order_qty: float = 1,
        batch_qty: float = 0,
        safety_stock_qty: float = 0,
        lead_time: int = 0,
        abc_classification="NA",
        sellable=False,
        phantom=False,
        obsolete=False,
        status=None,
    ):
        # Keys
        self.item = item
        self.location = location

        # Qualitative fields
        self.sellable = sellable
        self.phantom = phantom
        self.obsolete = obsolete
        self._type = SKUType.UNDEFINED
        self.status = status 
        # Classification: necessary if setter gets classification before assigning a classification
        self._abc_classification = "NA"
        self.abc_classification = abc_classification

        # Numerical fields
        self.safety_stock_qty = safety_stock_qty
        self.lead_time = lead_time
        self.inventory_qty = inventory_qty
        self.minimum_order_qty = minimum_order_qty
        self.batch_qty = batch_qty

        # Links between the items
        self._child_links: List[_SKULink] = []
        self._parent_links: List[_SKULink] = []

        # Links between the items (only for pptree library)
        self._pptree_parents: List[SKU] = []
        self._pptree_children: List[SKU] = []

    def __repr__(self):
        return f"SKU(location={self.location}, item={self.item})"

    def __str__(self):
        return f"{self.item}"

    def __eq__(self, other):
        if isinstance(other, SKU):
            return (self.location, self.item) == (other.location, other.item)
        return False

    def __hash__(self):
        return hash((self.location, self.item))

    # Children
    # ========================

    @property
    def children(self):
        """Returns all the immediate child items."""
        output = set()
        for child_link in self._child_links:
            output.add(child_link.sku)

        return output
    
    @property
    def active_children(self):
        """Returns all the child items that are not obsoleted."""
        output = set()
        for child_link in self._child_links:
            if not child_link.sku.obsolete:
                output.add(child_link.sku)

        return output

    @property
    def child_links(self):
        """Returns all the immediate child items along with the quantities."""
        return self._child_links
    
    @property
    def child_skus(self):
        return {links.sku for links in self._child_links}

    @property
    def ultimate_children(self):
        """Return all the lowermost/lowest child items in this bill of materials.
        
        Note: list may contain duplicate parent items.
        """
        return self._get_leaf_nodes("children")

    @property
    def all_children(self):
        """Return all the child items in the bill of materials (from immediate to ultimate items)"""
        return self._level_order_traverse("children")

    # Parents
    # =======================

    @property
    def parents(self):
        """Returns all the immediate parent items."""
        output = set()
        for parent_link in self._parent_links:
            output.add(parent_link.sku)

        return output

    @property
    def active_parents(self):
        """Returns all the child items that are not obsoleted."""
        output = set()
        for parent_link in self._parent_links:
            if not parent_link.sku.obsolete:
                output.add(parent_link.sku)

        return output

    @property
    def parent_links(self):
        """Returns all the immediate parent items along with the quantities."""
        return self._parent_links

    @property
    def ultimate_parents(self):
        """Return all the topmost/highest parent items in this bill of materials.
        
        Note: list may contain duplicate parent items.
        """
        return self._get_leaf_nodes("parents")

    @property
    def all_parents(self):
        """Return all the parent items in the bill of materials (from immediate to ultimate items)"""
        return self._level_order_traverse("parents")

    # Others
    # =========================

    @property
    def inventory_qty(self):
        """Get the value of inventory_qty qty."""
        return self._inventory_qty

    @inventory_qty.setter
    def inventory_qty(self, value):
        try:
            value = float(value)
        except TypeError:
            print("minimum order qty must be an integer or a float.")
            raise
        self._inventory_qty = float(value)

    @property
    def minimum_order_qty(self):
        """Get the value of minimum order qty."""
        return self._minimum_order_qty

    @minimum_order_qty.setter
    def minimum_order_qty(self, value):
        """Set the value of minimum order qty."""
        try:
            value = float(value)
        except TypeError:
            print("minimum order qty must be an integer or a float.")
            raise

        if value <= 0:
            raise ValueError(f"minimum order qty must be a positive number.")

        self._minimum_order_qty = float(value)

    @property
    def batch_qty(self):
        """Get the value of rounding value qty."""
        return self._batch_qty

    @batch_qty.setter
    def batch_qty(self, value):
        """Set the value of rounding value qty."""
        try:
            value = float(value)
        except TypeError:
            print("rounding value qty must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"rounding value qty must be a positive number.")

        self._batch_qty = float(value)

    @property
    def safety_stock_qty(self):
        """Get the value of safety stock qty."""
        return self._safety_stock_qty

    @safety_stock_qty.setter
    def safety_stock_qty(self, value):
        """Set the value of safety stock qty."""
        try:
            value = float(value)
        except TypeError:
            print("safety stock qty must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"safety stock qty must be a positive number.")

        self._safety_stock_qty = float(value)

    @property
    def lead_time(self):
        """Get the value of lead time."""
        return self._lead_time

    @lead_time.setter
    def lead_time(self, value):
        """Set the value of lead time."""
        try:
            value = float(value)
        except TypeError:
            print("lead time must be an integer or a float.")
            raise

        if value < 0:
            raise ValueError(f"lead time must be a positive number.")

        self._lead_time = int(value)

    @property
    def type(self):
        return self._type.value

    @type.setter
    def type(self, value):
        if not isinstance(value, SKUType):
            raise TypeError(
                f"Argument must be of type NodeType.\nYour value is:{value} and type: {type(value)}"
            )

        if value == SKUType.INTERMEDIATE:
            raise ValueError(
                f"You can only assign the values: PARENT and CHILD.\nYour value is: {value.name}"
            )

        # current   new     result
        # ===========================
        # None      parent  parent
        # None      child   child
        # child     parent  intermediate
        # child     child   child
        # parent    parent  parent
        # parent    child   intermediate

        if value != self._type:
            if self._type == SKUType.UNDEFINED:
                self._type = value
            else:
                self._type = SKUType.INTERMEDIATE


    def _level_order_traverse(self, direction):
        # try to get the attribute
        if getattr(self, direction) is None:
            raise AttributeError(
                f"Attribute {direction} not found in class {self.__class__.__name__}"
            )

        stack = list(getattr(self, direction))  # self should not be in the output
        result = []

        while stack:
            node = stack.pop()
            result.append(node)

            for nodes in getattr(node, direction):
                stack.append(nodes)

        return result

    def _get_leaf_nodes(self, direction):
        if getattr(self, direction) is None:
            raise AttributeError(
                f"Attribute {direction} not found in class {self.__class__.__name__}"
            )

        stack = getattr(self, direction)
        root_nodes = []

        while stack:
            node = stack.pop()
            if len(getattr(node, direction)) == 0:
                root_nodes.append(node)
            else:
                stack += getattr(node, direction)

        return root_nodes


    @property
    def abc_classification(self):
        return self._abc_classification

    @abc_classification.setter
    def abc_classification(self, value):
        """
        Sets the value of classification

        Args:
            value (str): the length must be two and the first letter must be
            either A, B, or C and the second letter must be X, Y, or Z.

            e.g.:
                AX
                AY
                BZ
                CZ
        """

        new_classification = self.classification_rank.get(value)
        if new_classification is None:
            raise ValueError(
                f"Value '{new_classification}' not found in classifications."
            )

        if self._is_classification_higher(self.abc_classification, value):
            self._abc_classification = value
            self._propagate_classifications_down(value)

    @property
    def sellable(self):
        return self._sellable

    @sellable.setter
    def sellable(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"Bad Type: input must be a boolean, not a '{type(value)}'.")
        self._sellable = value

    def _propagate_classifications_down(self, new_value):
        """
        Push this item classification down to their children and update the
        childrens classification if needed.

        Classification is updated only when the new classification has a higher
        score than the current classification.

        Args:
            new_classification (str): new classification for this item.
        """
        queue = [self]

        while queue:
            for _ in range(len(queue)):
                node = queue.pop()

                if self._is_classification_higher(node.abc_classification, new_value):
                    node.abc_classification = new_value

                for child_link in node._child_links:
                    queue.append(child_link.sku)

    def _is_classification_higher(self, current, new):
        return self.classification_rank[current] < self.classification_rank[new]

    def get_missing_safety_stock_qty(self):
        if self.inventory_qty < 0:
            return self.safety_stock_qty

        if self.inventory_qty < self.safety_stock_qty:
            return self.safety_stock_qty - self.inventory_qty
        else:
            return 0

    def lot_size(self, order_qty):
        """Rounds the order quantity to the nearest multiple of the minimum order quantity.

        If a rounding order quantity is specified, the rounded value will be a multiple
        of the rounding value that is higher than the minimum order quantity.

        Args:
            order_qty (float): The order quantity to round.

        Returns:
            float: The rounded order quantity.

        """
        if order_qty == 0:
            return 0

        if self.batch_qty:
            min_qty = self.minimum_order_qty or 0
            order_qty = max(order_qty, min_qty)
            return get_next_multiple(order_qty, self.batch_qty)

        if self.minimum_order_qty:
            return max(order_qty, self.minimum_order_qty)

    def _link_both_skus(self, child_sku, qty):
        """
        Note: this is an internal method that can be used externally only by the
        Factory class. This is because the Factory needs to register it to keep
        track of all the items.

        """
        if not isinstance(child_sku, SKU):
            raise TypeError("child_node argument must be of type Item.")

        if self.item == child_sku.item and self.location == child_sku.location:
            warnings.warn(
                f"parent and child skus cannot be the same.\n{child_sku.item} is parent and child at the same time"
            )
        
        self._check_for_recursion(child_sku)
        self._update_types(child_sku)
        self._update_sellable_flag(child_sku)
        self._add_child_for_pptree_visualisation(child_sku)

        # Link both ways: parent > child and child > parent
        if not isinstance(qty, (float, int)):
            raise TypeError(f"qty must be a float number.")

        self._child_links.append(_SKULink(child_sku, qty))
        child_sku._parent_links.append(_SKULink(self, 0 if qty == 0 else 1 / qty))


    def _check_for_recursion(self, child_node):
        if child_node in self.all_parents:
            raise ValueError(
                f"Linking the parent-child relationship ('{self.item}'>>'{child_node.code}') resulted in recursion."
            )

    def _update_types(self, child_node):
        self.type = SKUType.PARENT
        child_node.type = SKUType.CHILD

    def _update_sellable_flag(self, child_node):
        if self.type == SKUType.PARENT:
            self.sellable = True

        if child_node.type == SKUType.PARENT:
            self.sellable = True

    def _add_child_for_pptree_visualisation(self, child_node):
        child_node._pptree_parents.append(self)
        self._pptree_children.append(child_node)

    def show(self, direction="children"):
        if direction not in ["children", "parents"]:
            raise ValueError('direction arg must be "children" or "parents"')
        else:
            # second argument is property name of Node that holds next node
            pptree.print_tree(self, childattr="_pptree_" + direction)

    def get_phaseout_collaterals(self, tree=False):
        """
        Returns all items that should be phased out together

        Args:
            tree (bool, optional): If true, it returns the same item with the
            prefix "po_" and linked to this item are the item collaterals.
            Defaults to False and returns only a list of item codes that are
            collaterals.

        Returns:
            list or Item: returns a list if tree is False, otherwise it returns
            an Item.
        """
        logging.debug(f"Getting collaterals for {self.item}")

        po_self = SKU(self.item)

        parent_collat, po_self = self._link_parents_to_po_item(po_self)
        child_collat, po_self = self._link_child_to_po_item(parent_collat, po_self)

        all_collaterals = set()
        all_collaterals.update(parent_collat)
        all_collaterals.update(child_collat)
        all_collaterals.discard(self.item)

        if tree:
            return po_self
        else:
            return all_collaterals

    def _link_parents_to_po_item(self, po_self):
        """
        Check if parent items should be part of collaterals when self is being
        obsoleted
        """
        if po_self is not None and not isinstance(po_self, SKU):
            raise TypeError(
                f"input is an instance of {type(po_self)}, it must be of type Item."
            )

        logging.debug(f"traversing {len(self.parents)} parents for item {self.item}")

        # Insert None so the new tree can be linked to po_self
        stack = [(parent, None) for parent in self.parents]
        collat_list = set()

        while stack:
            parent, child = stack.pop()

            # === for tree ===
            if child is None:
                po_child = po_self
            else:
                po_child = SKU(child.code)

            po_parent = SKU(parent.code)
            po_parent._link_both_skus(po_child)

            # === for list ===
            collat_list.add(parent.code)
            collaterals, po_parent = parent._link_child_to_po_item(
                collat_list, po_parent
            )
            collat_list.update(collaterals)

            # === traversal ===
            child = parent
            for p in child.parents[::-1]:
                if p.code is not collaterals:
                    stack.append((p, child))

        return collat_list, po_self

    def _link_child_to_po_item(self, collaterals, po_self):
        """
        Check if child items should be part of collaterals when self is being
        obsoleted
        """
        if po_self is not None and not isinstance(po_self, SKU):
            raise TypeError(
                f"input is an instance of {type(po_self)}, it must be of type Item."
            )

        stack = [(None, child) for child in self.children]
        result = set()

        while stack:
            parent, child = stack.pop()

            po_child = SKU(child.code)
            if parent is None:
                po_parent = po_self
            else:
                po_parent = SKU(parent.code)

            not_sellable_single_parent = len(child.parents) <= 1 and not child.sellable

            parents_code = [i.code for i in child.parents]
            all_parents_in_collaterals = not bool(set(parents_code) - collaterals)
            not_sellable_all_parents_in_collaterals = (
                len(child.parents) > 1
                and all_parents_in_collaterals
                and not child.sellable
            )

            if not_sellable_single_parent or not_sellable_all_parents_in_collaterals:
                # for tree
                child_codes = [i.code for i in po_parent.children]
                if po_child.item not in child_codes:
                    po_parent._link_both_skus(po_child)

                # for list
                result.add(child.code)

                parent = child
                for c in parent.children[::-1]:
                    if c.code is not collaterals:
                        stack.append((parent, c))

        return result, po_self

    def _are_levels_equal(self, node, direction, past_node=None):
        anti_direction = "parents" if direction == "children" else "children"

        if not self and not node:
            # both nodes are empty, so they're equal
            return True
        elif not self or not node:
            # one node is empty and the other is not, so they're not equal
            return False
        elif self.item != node.code:
            # the nodes have different values, so the trees are not equal
            return False
        elif len(getattr(self, direction)) != len(getattr(node, direction)):
            # the nodes have different numbers of children, so the trees are not equal
            return False
        elif past_node is not None and len(getattr(self, anti_direction)) > 1:
            # recursively check the children of the parents or the parents of the children
            # perform the check in the other direction
            # get nodes in the other direction but remove the previous one
            # (where it's coming from) to avoid infine recursion
            # (bouncing back and forth between child-parent)
            next_nodes = getattr(self, anti_direction)
            next_nodes.remove(past_node)

            other_next_nodes = getattr(node, anti_direction)
            return self._move_to_next_level(
                next_nodes, other_next_nodes, anti_direction
            )

        else:
            # recursively check if each parent/child of node1 is equal to any
            # parent/child of node2
            next_nodes = getattr(self, direction)
            other_next_nodes = getattr(node, direction)
            return self._move_to_next_level(next_nodes, other_next_nodes, direction)

    def _move_to_next_level(self, next_nodes, other_next_nodes, direction):
        for next_node in next_nodes:
            found_match = False
            for other_next_node in other_next_nodes:
                if next_node._are_levels_equal(other_next_node, direction, self):
                    found_match = True
                    break
            if not found_match:
                return False
        return True

    def is_tree_equal(self, node):
        """
        Recursively checks all children and parents to see if self and node
        parameter belong to a tree with the same item codes.

        Args:
            node (Item): Second that self is compared to.

        Returns:
            bool: True if all tree is equal, False otherwise.

        """
        upwards = self._are_levels_equal(node, "parents")
        downwards = self._are_levels_equal(node, "children")

        return upwards and downwards



    def get_lineage(
        self,
        include_obsoletes=True,
        attributes=None,
        max_stack_size=None,
    ):
        """
        It gets all the parents and children of a location + item code.

        It returns a list of dictionaries containing the following keys:
        {
            "id": the hashed string of location + item,
            "location": the location code,
            "item": the item code,
            "parents": the ID's of the immediate parents,
            "children": the ID's of the immediate children,
            "stocking_type": the stocking type,
            "level": starts at 0 with root items and increases by +1,
        }

        The parents list contains only items that have id's
        """

        output = OutputFormatter(max_stack_size=max_stack_size)

        # add current items and iterate over the children
        # ===============================================
        if not include_obsoletes and self.obsolete:
            return []

        parent_skus = self.parents if include_obsoletes else self.active_parents
        queue = [(parent_skus, self, 0)]  # (previous_sku, current_sku, level)
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, sku, level = queue.pop(0)

                child_skus = sku.child_skus if include_obsoletes else sku.active_children

                output.store(
                    sku=sku,
                    parent_skus=sku_ancestor,
                    child_skus=child_skus,
                    level=level,
                    direction="children",
                )

                for child_sku in sku.child_skus:
                    queue.append((sku, child_sku, level - 1))

        # iterate over the parents
        # ==========================
        # get parent nodes from node

        child_skus = self.child_skus if include_obsoletes else self.active_children
        queue = [(child_skus, self, 0)]
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, sku, level = queue.pop(0)

                parent_skus = sku.parents if include_obsoletes else sku.active_parents

                output.store(
                    sku=sku,
                    parent_skus=parent_skus,
                    child_skus=sku_ancestor,
                    level=level,
                    direction="parents",
                )

                for parent_sku in sku.parents:
                    queue.append((sku, parent_sku, level + 1))

        return output.get_output(attributes=attributes)


    def get_collaterals(
        self,
        include_obsoletes=False,
        max_stack_size=None,
        attributes=None,
        skus_only=False,
    ):
        """
        It generates a list of all items that meet the following criteria:
            1. Items that use item_code as input material for their produciton;
            2. Items that are used as input material for item_code's production;
            3. Any indirect items that satisfy the point 1 or 2.

        It returns a list of dictionaries with the following keys:

            TODO: complete doscstring

        """
        if not include_obsoletes and self.obsolete:
            return []

        output = OutputFormatter(max_stack_size=max_stack_size)

        output = self._scan_this_and_parents(
            collaterals=output,
            include_obsoletes=include_obsoletes,
        )
        output = self._scan_children(
            collaterals=output,
            level=0,
            include_obsoletes=include_obsoletes,
        )

        return output.get_output(skus_only, attributes, skus_only)

    def _scan_this_and_parents(self, collaterals, include_obsoletes):
        p_collaterals = collaterals

        child_skus = self.children if include_obsoletes else self.active_children
        queue = [(child_skus, self, 0)]  # (previous_sku, current_sku, level)
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, sku, level = queue.pop(0)

                # Scan the children and add the result to p_collaterals
                p_collaterals = sku._scan_children(collaterals=p_collaterals, level=level, include_obsoletes=include_obsoletes)

                # Filter out obsoletes if needed
                parent_skus = sku.parents if include_obsoletes else sku.active_parents

                # Add parent to collaterals
                p_collaterals.store(
                    sku=sku,
                    parent_skus=parent_skus,
                    child_skus=sku_ancestor,
                    level=level,
                    direction="parents",
                )

                for parent_node in sku.parents:
                    queue.append((sku, parent_node, level + 1))

        return p_collaterals

    def _scan_children(self, collaterals, level, include_obsoletes):
        """
        Check if child items should be part of collaterals when self is being
        obsoleted
        """

        # Start from the children
        mod_children = self.children if include_obsoletes else self.active_children
        # Remove any SKU that is already in collaterals
        mod_children = mod_children - collaterals._skus        

        queue = [(self, sku, level - 1) for sku in mod_children]
        while queue:
            for _ in range(len(queue)):
                sku_ancestor, sku, level = queue.pop(0)

                # Logic to see if child should be added
                unique_parent = len(sku.parents) <= 1
                all_parents_in_collaterals = not bool(set(sku.parents) - collaterals._skus)

                add_children = unique_parent and not sku.sellable or all_parents_in_collaterals

                if add_children:
                    # Filter out obsoletes if needed
                    mod_children = sku.children if include_obsoletes else sku.active_children
                    mod_children = mod_children - collaterals._skus

                    # Add child to collaterals
                    collaterals.store(
                        sku=sku,
                        parent_skus=sku_ancestor,
                        child_skus=mod_children,
                        level=level,
                        direction="children",
                    )

                    # Move to next children
                    for child_node in mod_children:
                        if not collaterals.records.get(child_node):
                            queue.append((sku, child_node, level - 1))
        
        return collaterals