"""
# Merkle Tree model
"""
from merkly.utils.crypto import keccak, half, slice_in_pairs
from merkly.utils.math import is_power_2
from typing import List, Optional
from pydantic import BaseModel
from functools import reduce


class Node(BaseModel):
    """
    # 🍃 Leaf of Tree
    """

    left: Optional[str]
    right: Optional[str]

    def __repr__(self) -> str:
        if self.left is None:
            return f"Node(right: {self.right[:4]}...)"
        elif self.right is None:
            return f"Node(left: {self.left[:4]}...)"
        else:
            return ""


class MerkleTree:
    """
    # 🌳 Merkle Tree
    - You can pass a list of raw data
    - They will hashed by `keccak-256`
    """

    def __init__(self, leafs: List[str]) -> None:
        is_power_2(leafs.__len__())
        self.leafs: List[str] = self.__hash_leafs(leafs)
        self.raw_leafs = leafs
        self.short_leafs = self.short(self.leafs)

    def __hash_leafs(self, leafs: List[str]) -> List[str]:
        return list(map(keccak, leafs))

    def __repr__(self) -> str:
        return f"""MerkleTree(
            raw_leafs: {self.raw_leafs}
            leafs: {self.leafs}
            short_leafs: {self.short(self.leafs)}
        )"""

    def short(self, data: List[str]) -> List[str]:
        return [f"{x[:4]}..." for x in data]

    @property
    def root(self) -> str:
        return MerkleTree.merkle_root(self.leafs)[0]

    def proof(self, raw_leaf: str) -> List[Node]:
        proof = MerkleTree.merkle_proof(self.leafs, [], keccak(raw_leaf))
        proof.reverse()
        return proof

    def verify(self, proof: List[str], raw_leaf: str) -> bool:
        full_proof = [keccak(raw_leaf)]
        full_proof.extend(proof)

        def _f(_x: Node, _y: Node) -> Node:
            """
            # f(x,y) -> Node
            """
            if not isinstance(_x, Node):
                if _y.left is not None:
                    return Node(left=keccak(_y.left + _x))
                else:
                    return Node(left=keccak(_x + _y.right))
            if _x.left is not None and _y.left is not None:
                return Node(left=keccak(_y.left + _x.left))
            if _x.right is not None and _y.right is not None:
                return Node(right=keccak(_x.right + _y.right))

            if _x.right is not None:
                return Node(right=keccak(_y.left + _x.right))
            if _x.left is not None:
                return Node(left=keccak(_x.left + _y.right))

        return reduce(_f, full_proof).left == self.root

    @staticmethod
    def merkle_root(leafs: list):
        """
        # Merkle Root of `x: list[str]` using keccak256
        - params `x: list[str]`
        - return `hexadecimal: list[str]`

        ```python
        >>> merkle_root(["a", "b", "c", "d"])
        ["159b0d5005a27c97537ff0e6d1d0d619be408a5e3f2570816b02dc5a18b74f47"]

        >>> merkle_root(["a", "b"])
        ["414e3a845393ef6d68973ddbf5bd85ff524443cf0e06a361624f3d51b879ec1c"]
        ```
        """
        if len(leafs) == 1:
            return leafs

        return MerkleTree.merkle_root([keccak(i + j) for i, j in slice_in_pairs(leafs)])

    @staticmethod
    def merkle_proof(leafs: List[str], proof: List[str], leaf: str) -> list:
        """
        # Make a proof
        - if the `leaf` index is less than half the size of the `leafs`
        list then the right side must reach root and vice versa
        """

        try:
            index = leafs.index(leaf)
        except ValueError as err:
            msg = f"leaf: {leaf} does not exist in the tree: {leafs}"
            raise ValueError(msg) from err

        if len(leafs) == 2:
            if index == 1:
                proof.append(Node(left=leafs[0]))
            else:
                proof.append(Node(right=leafs[1]))
            return proof

        left, right = half(leafs)

        if index < len(leafs) / 2:
            proof.append(Node(right=MerkleTree.merkle_root(right)[0]))
            return MerkleTree.merkle_proof(left, proof, leaf)
        else:
            proof.append(Node(left=MerkleTree.merkle_root(left)[0]))
            return MerkleTree.merkle_proof(right, proof, leaf)
