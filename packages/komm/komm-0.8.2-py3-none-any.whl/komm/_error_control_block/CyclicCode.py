import functools
import itertools

import numpy as np

from .._algebra import BinaryPolynomial
from .._aux import tag
from .BlockCode import BlockCode


class CyclicCode(BlockCode):
    r"""
    General binary cyclic code. A cyclic code is a [linear block code](/ref/BlockCode) such that, if $c$ is a codeword, then every cyclic shift of $c$ is also a codeword. It is characterized by its *generator polynomial* $g(X)$, of degree $m$ (the redundancy of the code), and by its *parity-check polynomial* $h(X)$, of degree $k$ (the dimension of the code). Those polynomials are related by $g(X) h(X) = X^n + 1$, where $n = k + m$ is the length of the code.

    Examples of generator polynomials can be found in the table below.

    | Code $(n, k, d)$  | Generator polynomial $g(X)$              | Integer representation           |
    | ----------------- | ---------------------------------------- | -------------------------------- |
    | Hamming $(7,4,3)$ | $X^3 + X + 1$                            | `0b1011 = 0o13 = 11`             |
    | Simplex $(7,3,4)$ | $X^4 + X^2 + X +   1$                    | `0b10111 = 0o27 = 23`            |
    | BCH $(15,5,7)$    | $X^{10} + X^8 + X^5 + X^4 + X^2 + X + 1$ | `0b10100110111 = 0o2467 = 1335`  |
    | Golay $(23,12,7)$ | $X^{11} + X^9 + X^7 + X^6 + X^5 + X + 1$ | `0b101011100011 = 0o5343 = 2787` |

    For more details, see <cite>LC04, Ch. 5</cite>.
    """

    def __init__(self, length, systematic=True):
        super().__init__()
        self._length = length
        self._modulus = BinaryPolynomial.from_exponents([0, self._length])
        self._systematic = bool(systematic)

    def _init_from_generator_polynomial(self, generator_polynomial):
        self._generator_polynomial = BinaryPolynomial(generator_polynomial)
        self._parity_check_polynomial, remainder = divmod(self._modulus, self._generator_polynomial)
        if remainder != 0b0:
            raise ValueError("The generator polynomial must be a factor of X^n + 1")
        self._constructed_from = "generator_polynomial"
        self._post_init()

    def _init_from_parity_check_polynomial(self, parity_check_polynomial):
        self._parity_check_polynomial = BinaryPolynomial(parity_check_polynomial)
        self._generator_polynomial, remainder = divmod(self._modulus, self._parity_check_polynomial)
        if remainder != 0b0:
            raise ValueError("The parity-check polynomial must be a factor of X^n + 1")
        self._constructed_from = "parity_check_polynomial"
        self._post_init()

    def _post_init(self):
        self._dimension = self._parity_check_polynomial.degree
        self._redundancy = self._generator_polynomial.degree
        if self._systematic:
            self._information_set = np.arange(self._redundancy, self._length)

    @classmethod
    def from_generator_polynomial(cls, length, generator_polynomial, systematic=True):
        r"""
        Constructs a binary cyclic block code from its generator polynomial.

        Parameters:

            length (int): The length $n$ of the code.

            generator_polynomial (BinaryPolynomial | int): The generator polynomial $g(X)$ of the code, of degree $m$ (the redundancy of the code), specified either as a [binary polynomial](/ref/BinaryPolynomial) or as an integer to be converted to the former.

            systematic (Optional[bool]): Whether the encoder is systematic. Default is `True`.

        Examples:

            >>> code = komm.CyclicCode.from_generator_polynomial(23, 0b101011100011)  # Golay (23, 12)
            >>> (code.length, code.dimension, code.minimum_distance)
            (23, 12, 7)
        """
        obj = cls(length, systematic)
        obj._init_from_generator_polynomial(generator_polynomial)
        return obj

    @classmethod
    def from_parity_check_polynomial(cls, length, parity_check_polynomial, systematic=True):
        r"""
        Constructs a binary cyclic block code from its parity-check polynomial.

        Parameters:

            length (int): The length $n$ of the code.

            parity_check_polynomial (BinaryPolynomial | int): The parity-check polynomial $h(X)$ of the code, of degree $k$ (the dimension of the code), specified either as a [binary polynomial](/ref/BinaryPolynomial) or as an integer to be converted to the former.

            systematic (Optional[bool]): Whether the encoder is systematic. Default is `True`.

        Examples:

            >>> code = komm.CyclicCode.from_parity_check_polynomial(23, 0b1010010011111)  # Golay (23, 12)
            >>> (code.length, code.dimension, code.minimum_distance)
            (23, 12, 7)
        """
        obj = cls(length, systematic)
        obj._init_from_parity_check_polynomial(parity_check_polynomial)
        return obj

    def __repr__(self):
        if self._constructed_from == "generator_polynomial":
            args = "length={}, generator_polynomial={}, systematic={}".format(
                self._length, self._generator_polynomial, self._systematic
            )
        else:  # if self._constructed_from == "parity_check_polynomial":
            args = "length={}, parity_check_polynomial={}, systematic={}".format(
                self._length, self._parity_check_polynomial, self._systematic
            )
        return "{}({})".format(self.__class__.__name__, args)

    @property
    def generator_polynomial(self):
        r"""
        The generator polynomial $g(X)$ of the cyclic code. It is a [binary polynomial](/ref/BinaryPolynomial) of degree $m$, where $m$ is the redundancy of the code.
        """
        return self._generator_polynomial

    @property
    def parity_check_polynomial(self):
        r"""
        The parity-check polynomial $h(X)$ of the cyclic code. It is a [binary polynomial](/ref/BinaryPolynomial) of degree $k$, where $k$ is the dimension of the code.
        """
        return self._parity_check_polynomial

    @functools.cached_property
    def meggitt_table(self):
        r"""
        The Meggitt table for the cyclic code. It is a dictionary where the keys are syndromes and the values are error patterns. See <cite>XiD03, Sec. 3.4</cite>.
        """
        meggitt_table = {}
        for w in range(self.packing_radius + 1):
            for idx in itertools.combinations(range(self._length - 1), w):
                errorword_polynomial = BinaryPolynomial.from_exponents(list(idx) + [self._length - 1])
                syndrome_polynomial = errorword_polynomial % self._generator_polynomial
                meggitt_table[syndrome_polynomial] = errorword_polynomial
        return meggitt_table

    def _encode_cyclic_direct(self, message):
        r"""
        Encoder for cyclic codes. Direct, non-systematic method.
        """
        message_polynomial = BinaryPolynomial.from_coefficients(message)
        return (message_polynomial * self._generator_polynomial).coefficients(width=self._length)

    def _encode_cyclic_systematic(self, message):
        r"""
        Encoder for cyclic codes. Systematic method.
        """
        message_polynomial = BinaryPolynomial.from_coefficients(message)
        message_polynomial_shifted = message_polynomial << self._generator_polynomial.degree
        parity = message_polynomial_shifted % self._generator_polynomial
        return (message_polynomial_shifted + parity).coefficients(width=self._length)

    def _default_encoder(self):
        if self._systematic:
            return "cyclic_systematic"
        else:
            return "cyclic_direct"

    @functools.cached_property
    def generator_matrix(self):
        n, k = self.length, self.dimension
        generator_matrix = np.empty((k, n), dtype=int)
        row = self._generator_polynomial.coefficients(width=n)
        for i in range(k):
            generator_matrix[i] = np.roll(row, i)
        return generator_matrix

    @functools.cached_property
    def parity_check_matrix(self):
        n, m = self.length, self.redundancy
        parity_check_matrix = np.empty((m, n), dtype=int)
        row = self._parity_check_polynomial.coefficients(width=n)[::-1]
        for i in range(m):
            parity_check_matrix[m - i - 1] = np.roll(row, -i)
        return parity_check_matrix

    @tag(name="Meggitt decoder", input_type="hard", target="codeword")
    def _decode_meggitt(self, recvword):
        r"""
        Meggitt decoder. See <cite>XiD03, Sec. 3.4</cite> for more details.
        """
        meggitt_table = self.meggitt_table
        recvword_polynomial = BinaryPolynomial.from_coefficients(recvword)
        syndrome_polynomial = recvword_polynomial % self._generator_polynomial
        if syndrome_polynomial == 0:
            return recvword
        errorword_polynomial_hat = BinaryPolynomial(0)
        for j in range(self._length):
            if syndrome_polynomial in meggitt_table:
                errorword_polynomial_hat = meggitt_table[syndrome_polynomial] // (1 << j)
                break
            syndrome_polynomial = (syndrome_polynomial << 1) % self._generator_polynomial
        return (recvword_polynomial + errorword_polynomial_hat).coefficients(self._length)

    def _default_decoder(self, dtype):
        if dtype == int:
            return "meggitt"
        else:
            return super()._default_decoder(dtype)
