import functools
import itertools

import numpy as np

from .._algebra.util import null_matrix, right_inverse
from .._aux import tag
from .._util import binlist2int, int2binlist


class BlockCode:
    r"""
    General binary linear block code. It is characterized by its *generator matrix* $G$, a binary $k \times n$ matrix, and by its *parity-check matrix* $H$, a binary $m \times n$ matrix. Those matrix are related by $G H^\top = 0$. The parameters $k$, $m$, and $n$ are called the code *dimension*, *redundancy*, and *length*, respectively, and are related by $k + m = n$. For more details, see <cite>LC04, Ch. 3</cite>.
    """

    def __init__(self):
        self._generator_matrix = None
        self._parity_check_matrix = None
        self._parity_submatrix = None
        self._information_set = None
        self._parity_set = None
        self._length = None
        self._dimension = None
        self._redundancy = None
        self._constructed_from = None
        self._minimum_distance = None
        self._codeword_weight_distribution = None
        self._coset_leader_weight_distribution = None

    def _init_from_generator_matrix(self, generator_matrix):
        self._generator_matrix = np.array(generator_matrix, dtype=int) % 2
        self._dimension, self._length = self._generator_matrix.shape
        self._redundancy = self._length - self._dimension
        self._constructed_from = "generator_matrix"

    def _init_from_parity_check_matrix(self, parity_check_matrix):
        self._parity_check_matrix = np.array(parity_check_matrix, dtype=int) % 2
        self._redundancy, self._length = self._parity_check_matrix.shape
        self._dimension = self._length - self._redundancy
        self._constructed_from = "parity_check_matrix"

    def _init_from_parity_submatrix(self, parity_submatrix, information_set="left"):
        self._parity_submatrix = np.array(parity_submatrix, dtype=int) % 2
        self._dimension, self._redundancy = self._parity_submatrix.shape
        self._length = self._dimension + self._redundancy
        if information_set == "left":
            self._information_set = np.arange(self._dimension)
        elif information_set == "right":
            self._information_set = np.arange(self._redundancy, self._length)
        else:
            self._information_set = np.array(information_set, dtype=int)
        if (
            self._information_set.size != self._dimension
            or self._information_set.min() < 0
            or self._information_set.max() > self._length
        ):
            raise ValueError("Parameter 'information_set' must be a 'k'-subset of 'range(n)'")
        self._parity_set = np.setdiff1d(np.arange(self._length), self._information_set)
        self._generator_matrix = np.empty((self._dimension, self._length), dtype=int)
        self._generator_matrix[:, self._information_set] = np.eye(self._dimension, dtype=int)
        self._generator_matrix[:, self._parity_set] = self._parity_submatrix
        self._parity_check_matrix = np.empty((self._redundancy, self._length), dtype=int)
        self._parity_check_matrix[:, self._information_set] = self._parity_submatrix.T
        self._parity_check_matrix[:, self._parity_set] = np.eye(self._redundancy, dtype=int)
        self._constructed_from = "parity_submatrix"

    @classmethod
    def from_generator_matrix(cls, generator_matrix):
        r"""
        Constructs a binary linear block code from its generator matrix.

        Parameters:

            generator_matrix (Array2D[int]): Generator matrix $G$ for the code, which is a $k \times n$ binary matrix.

        Examples:

            >>> komm.BlockCode().from_generator_matrix([[1, 0, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 1, 0]])
            BlockCode.from_generator_matrix([[1, 0, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 1, 0]])
        """
        obj = cls()
        obj._init_from_generator_matrix(generator_matrix)
        return obj

    @classmethod
    def from_parity_check_matrix(cls, parity_check_matrix):
        r"""
        Constructs a binary linear block code from its parity-check matrix.

        Parameters:

            parity_check_matrix (Array2D[int]): Parity-check matrix $H$ for the code, which is an $m \times n$ binary matrix.

        Examples:

            >>> komm.BlockCode().from_parity_check_matrix([[0, 1, 1, 1, 0, 0], [1, 0, 1, 0, 1, 0], [1, 1, 0, 0, 0, 1]])
            BlockCode.from_parity_check_matrix([[0, 1, 1, 1, 0, 0], [1, 0, 1, 0, 1, 0], [1, 1, 0, 0, 0, 1]])
        """
        obj = cls()
        obj._init_from_parity_check_matrix(parity_check_matrix)
        return obj

    @classmethod
    def from_parity_submatrix(cls, parity_submatrix, information_set="left"):
        r"""
        Constructs a binary linear block code from its parity submatrix and information set.

        Parameters:

            parity_submatrix (Array2D[int]): Parity submatrix $P$ for the code, which is a $k \times m$ binary matrix.

            information_set (Optional[Array1D[int] | str]): Either an array containing the indices of the information positions, which must be a $k$-sublist of $[0 : n)$, or one of the strings `'left'` or `'right'`. The default value is `'left'`.

        Examples:

            >>> komm.BlockCode().from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]], information_set=[0, 1, 2])
        """
        obj = cls()
        obj._init_from_parity_submatrix(parity_submatrix, information_set)
        return obj

    def __repr__(self):
        if self._constructed_from == "generator_matrix":
            args = f"{self._generator_matrix.tolist()}"
        elif self._constructed_from == "parity_check_matrix":
            args = f"{self._parity_check_matrix.tolist()}"
        elif self._constructed_from == "parity_submatrix":
            args = f"{self._parity_submatrix.tolist()}, information_set={self._information_set.tolist()}"
        return f"{self.__class__.__name__}.from_{self._constructed_from}({args})"

    @property
    def length(self):
        r"""
        The length $n$ of the code.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.length
            6
        """
        return self._length

    @property
    def dimension(self):
        r"""
        The dimension $k$ of the code.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.dimension
            3
        """
        return self._dimension

    @property
    def redundancy(self):
        r"""
        The redundancy $m$ of the code.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.redundancy
            3
        """
        return self._redundancy

    @property
    def rate(self):
        r"""
        The rate $R = k/n$ of the code.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.rate
            0.5
        """
        return self._dimension / self._length

    @functools.cached_property
    def minimum_distance(self):
        r"""
        The minimum distance $d$ of the code. This is equal to the minimum Hamming weight of the non-zero codewords.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.minimum_distance
            3
        """
        if self._minimum_distance is None:
            return np.flatnonzero(self.codeword_weight_distribution)[1]
        return self._minimum_distance

    @functools.cached_property
    def packing_radius(self):
        r"""
        The packing radius of the code. This is also called the *error-correcting capability* of the code, and is equal to $\lfloor (d - 1) / 2 \rfloor$.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.packing_radius
            1
        """
        return (self.minimum_distance - 1) // 2

    @functools.cached_property
    def covering_radius(self):
        r"""
        The covering radius of the code. This is equal to the maximum Hamming weight of the coset leaders.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.covering_radius
            2
        """
        return np.flatnonzero(self.coset_leader_weight_distribution)[-1]

    @functools.cached_property
    def generator_matrix(self):
        r"""
        The generator matrix $G$ of the code. It as a $k \times n$ binary matrix, where $k$ is the code dimension, and $n$ is the code length.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.generator_matrix
            array([[1, 0, 0, 0, 1, 1],
                   [0, 1, 0, 1, 0, 1],
                   [0, 0, 1, 1, 1, 0]])
        """
        if self._generator_matrix is None:
            return null_matrix(self._parity_check_matrix)
        return self._generator_matrix

    @functools.cached_property
    def parity_check_matrix(self):
        r"""
        The parity-check matrix $H$ of the code. It as an $m \times n$ binary matrix, where $m$ is the code redundancy, and $n$ is the code length.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.parity_check_matrix
            array([[0, 1, 1, 1, 0, 0],
                   [1, 0, 1, 0, 1, 0],
                   [1, 1, 0, 0, 0, 1]])
        """
        if self._parity_check_matrix is None:
            return null_matrix(self._generator_matrix)
        return self._parity_check_matrix

    @functools.cached_property
    def codeword_table(self):
        r"""
        The codeword table of the code. This is a $2^k \times n$ matrix whose rows are all the codewords. The codeword in row $i$ corresponds to the message whose binary representation (MSB in the right) is $i$.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.codeword_table
            array([[0, 0, 0, 0, 0, 0],
                   [1, 0, 0, 0, 1, 1],
                   [0, 1, 0, 1, 0, 1],
                   [1, 1, 0, 1, 1, 0],
                   [0, 0, 1, 1, 1, 0],
                   [1, 0, 1, 1, 0, 1],
                   [0, 1, 1, 0, 1, 1],
                   [1, 1, 1, 0, 0, 0]])
        """
        codeword_table = np.empty([2**self._dimension, self._length], dtype=int)
        for i in range(2**self._dimension):
            message = int2binlist(i, width=self._dimension)
            codeword_table[i] = self.encode(message)
        return codeword_table

    @functools.cached_property
    def codeword_weight_distribution(self):
        r"""
        The codeword weight distribution of the code. This is an array of shape $(n + 1)$ in which element in position $w$ is equal to the number of codewords of Hamming weight $w$, for $w \in [0 : n]$.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.codeword_weight_distribution
            array([1, 0, 0, 4, 3, 0, 0])
        """
        if self._codeword_weight_distribution is None:
            return np.bincount(np.sum(self.codeword_table, axis=1), minlength=self._length + 1)
        return self._codeword_weight_distribution

    @functools.cached_property
    def coset_leader_table(self):
        r"""
        The coset leader table of the code. This is a $2^m \times n$ matrix whose rows are all the coset leaders. The coset leader in row $i$ corresponds to the syndrome whose binary representation (MSB in the right) is $i$. This may be used as a LUT for syndrome-based decoding.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.coset_leader_table
            array([[0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0],
                   [0, 0, 0, 0, 1, 0],
                   [0, 0, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 1],
                   [0, 1, 0, 0, 0, 0],
                   [1, 0, 0, 0, 0, 0],
                   [1, 0, 0, 1, 0, 0]])
        """
        coset_leader_table = np.empty([2**self._redundancy, self._length], dtype=int)
        taken = []
        for w in range(self._length + 1):
            for idx in itertools.combinations(range(self._length), w):
                errorword = np.zeros(self._length, dtype=int)
                errorword[list(idx)] = 1
                syndrome = np.dot(errorword, self.parity_check_matrix.T) % 2
                syndrome_int = binlist2int(syndrome)
                if syndrome_int not in taken:
                    coset_leader_table[syndrome_int] = np.array(errorword)
                    taken.append(syndrome_int)
                if len(taken) == 2**self.redundancy:
                    break
        return coset_leader_table

    @functools.cached_property
    def coset_leader_weight_distribution(self):
        r"""
        The coset leader weight distribution of the code. This is an array of shape $(n + 1)$ in which element in position $w$ is equal to the number of coset leaders of weight $w$, for $w \in [0 : n]$.

        Examples:

            >>> code = komm.BlockCode.from_parity_submatrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
            >>> code.coset_leader_weight_distribution
            array([1, 6, 1, 0, 0, 0, 0])
        """
        if self._coset_leader_weight_distribution is None:
            return np.bincount(np.sum(self.coset_leader_table, axis=1), minlength=self._length + 1)
        return self._coset_leader_weight_distribution

    @functools.cached_property
    def _generator_matrix_right_inverse(self):
        return right_inverse(self.generator_matrix)

    def encode(self, message, method=None):
        r"""
        Encodes a given message to its corresponding codeword.

        Parameters:

            message (Array1D[int]): The message to be encoded. Its length must be $k$.

            method (Optional[str]): The encoding method to be used.

        Returns:

            codeword (Array1D[int]): The codeword corresponding to `message`. Its length is equal to $n$.
        """
        message = np.array(message)

        if message.size != self._dimension:
            raise ValueError("Length of 'message' must be equal to the code dimension")

        if method is None:
            method = self._default_encoder()

        encoder = getattr(self, "_encode_" + method)
        codeword = encoder(message)

        return codeword

    def _encode_generator_matrix(self, message):
        codeword = np.dot(message, self.generator_matrix) % 2
        return codeword

    def _encode_systematic_generator_matrix(self, message):
        codeword = np.empty(self._length, dtype=int)
        codeword[self._information_set] = message
        codeword[self._parity_set] = np.dot(message, self._parity_submatrix) % 2
        return codeword

    def _default_encoder(self):
        if self._constructed_from == "parity_submatrix":
            return "systematic_generator_matrix"
        else:
            return "generator_matrix"

    def message_from_codeword(self, codeword):
        r"""
        Returns the message corresponding to a given codeword. In other words, applies the inverse encoding map.

        Parameters:

            codeword (Array1D[int]): A codeword from the code. Its length must be $n$.

        Returns:

            message (Array1D[int]): The message corresponding to `codeword`. Its length is equal to $k$.
        """
        if self._constructed_from == "parity_submatrix":
            return codeword[self._information_set]
        else:
            return np.dot(codeword, self._generator_matrix_right_inverse) % 2

    def decode(self, recvword, method=None, **kwargs):
        r"""
        Decodes a received word to a message.

        Parameters:

            recvword (Array1D[int] | Array1D[float]): The word to be decoded. If using a hard-decision decoding method, then the elements of the array must be bits (integers in $\\{ 0, 1 \\}$). If using a soft-decision decoding method, then the elements of the array must be soft-bits (floats standing for log-probability ratios, in which positive values represent bit $0$ and negative values represent bit $1$). Its length must be $n$.

            method (Optional[str]): The decoding method to be used.

            kwargs (): Keyword arguments to be passed to the decoding method.

        Returns:

            message_hat (Array1D[int]): The message decoded from `recvword`. Its length is equal to $k$.
        """
        recvword = np.array(recvword)

        if recvword.size != self._length:
            raise ValueError("Length of 'recvword' must be equal to the code length")

        if method is None:
            method = self._default_decoder(recvword.dtype)

        decoder = getattr(self, "_decode_" + method)

        if decoder.target == "codeword":
            message_hat = self.message_from_codeword(decoder(recvword, **kwargs))
        elif decoder.target == "message":
            message_hat = decoder(recvword, **kwargs)

        return message_hat

    @tag(name="Exhaustive search (hard-decision)", input_type="hard", target="codeword")
    def _decode_exhaustive_search_hard(self, recvword):
        r"""
        Exhaustive search minimum distance hard decoder. Hamming distance.
        """
        codewords = self.codeword_table
        metrics = np.count_nonzero(recvword != codewords, axis=1)
        codeword_hat = codewords[np.argmin(metrics)]
        return codeword_hat

    @tag(name="Exhaustive search (soft-decision)", input_type="soft", target="codeword")
    def _decode_exhaustive_search_soft(self, recvword):
        r"""
        Exhaustive search minimum distance soft decoder. Euclidean distance.
        """
        codewords = self.codeword_table
        metrics = np.dot(recvword, codewords.T)
        codeword_hat = codewords[np.argmin(metrics)]
        return codeword_hat

    @tag(name="Syndrome table", input_type="hard", target="codeword")
    def _decode_syndrome_table(self, recvword):
        r"""
        Syndrome table decoder.
        """
        coset_leader_table = self.coset_leader_table
        syndrome = np.dot(recvword, self.parity_check_matrix.T) % 2
        syndrome_int = binlist2int(syndrome)
        errorword_hat = coset_leader_table[syndrome_int]
        codeword_hat = np.bitwise_xor(recvword, errorword_hat)
        return codeword_hat

    def _default_decoder(self, dtype):
        if dtype == int:
            if self._dimension >= self._redundancy:
                return "syndrome_table"
            else:
                return "exhaustive_search_hard"
        elif dtype == float:
            return "exhaustive_search_soft"

    @staticmethod
    def _extended_parity_submatrix(parity_submatrix):
        last_column = (1 + np.sum(parity_submatrix, axis=1)) % 2
        extended_parity_submatrix = np.hstack([parity_submatrix, last_column[np.newaxis].T])
        return extended_parity_submatrix

    @classmethod
    def _available_decoding_methods(cls):
        table = []
        for name in dir(cls):
            if name.startswith("_decode_"):
                identifier = name[8:]
                method = getattr(cls, name)
                table.append([method.name, "`{}`".format(identifier), method.input_type])
        return table
