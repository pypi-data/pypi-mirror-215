import numpy as np
from scipy import special

from .._aux import tag
from .BlockCode import BlockCode


class RepetitionCode(BlockCode):
    r"""
    Repetition code. For a given length $n$, it is the [linear block code](/ref/BlockCode) whose only two codewords are $00 \cdots 0$ and $11 \cdots 1$. The repetition code has the following parameters:

    - Length: $n$
    - Dimension: $k = 1$
    - Minimum distance: $d = n$

    Notes:

        - Its dual is the [single parity check code](/ref/SingleParityCheckCode).
    """

    def __init__(self, n):
        r"""
        Constructor for the class.

        Parameters:

            n (int): The length $n$ of the code. Must be a positive integer.

        Examples:

            >>> code = komm.RepetitionCode(5)
            >>> (code.length, code.dimension, code.minimum_distance)
            (5, 1, 5)
            >>> code.generator_matrix
            array([[1, 1, 1, 1, 1]])
            >>> code.parity_check_matrix
            array([[1, 1, 0, 0, 0],
                   [1, 0, 1, 0, 0],
                   [1, 0, 0, 1, 0],
                   [1, 0, 0, 0, 1]])
            >>> code.encode([1])
            array([1, 1, 1, 1, 1])
            >>> code.decode([1, 0, 1, 0, 0])
            array([0])
        """
        parity_submatrix = np.ones((1, n - 1), dtype=int)
        super().__init__()
        super()._init_from_parity_submatrix(parity_submatrix)
        self._minimum_distance = n
        self._coset_leader_weight_distribution = np.zeros(n + 1, dtype=int)
        for w in range((n + 1) // 2):
            self._coset_leader_weight_distribution[w] = special.comb(n, w, exact=True)
        if n % 2 == 0:
            self._coset_leader_weight_distribution[n // 2] = special.comb(n, n // 2, exact=True) // 2

    def __repr__(self):
        args = "{}".format(self._length)
        return "{}({})".format(self.__class__.__name__, args)

    @tag(name="Majority-logic", input_type="hard", target="codeword")
    def _decode_majority_logic(self, recvword):
        r"""
        Majority-logic decoder. A hard-decision decoder for Repetition codes only.
        """
        majority = np.argmax(np.bincount(recvword))
        codeword_hat = majority * np.ones_like(recvword)
        return codeword_hat

    def _default_decoder(self, dtype):
        if dtype == int:
            return "majority_logic"
        else:
            return super()._default_decoder(dtype)
