import numpy as np

from .Modulation import Modulation


class APSKModulation(Modulation):
    r"""
    Amplitude- and phase-shift keying (APSK) modulation. It is a complex [modulation scheme](/ref/Modulation) in which the constellation is the union of component [PSK](/ref/PSKModulation) constellations, called *rings*. More precisely,
    $$
        \mathcal{S} = \bigcup_{k \in [0 : K)} \mathcal{S}_k,
    $$
    where $K$ is the number of rings and
    $$
        \mathcal{S}_k = \left\\{ A_k \exp \left( \mathrm{j} \frac{2 \pi i}{M_k} \right) \exp(\mathrm{j} \phi_k) : i \in [0 : M_k) \right\\},
    $$
    where $M_k$ is the *order*, $A_k$ is the *amplitude*, and $\phi_k$ is the *phase offset* of the $k$-th ring, for $k \in [0 : K)$. The size of the resulting complex-valued constellation is $M = M_0 + M_1 + \cdots + M\_{K-1}$. The order $M_k$ of each ring need not be a power of $2$; however, the order $M$ of the constructed APSK modulation must be. The APSK constellation is depicted below for $(M_0, M_1) = (8, 8)$ with $(A_0, A_1) = (A, 2A)$ and $(\phi_0, \phi_1) = (0, \pi/8)$.

    <figure markdown>
      ![16-APSK constellation.](/figures/apsk_16.svg)
    </figure>
    """

    def __init__(self, orders, amplitudes, phase_offsets=0.0, labeling="natural"):
        r"""
        Constructor for the class.

        Parameters:

            orders (Tuple[int, ...]): A $K$-tuple with the orders $M_k$ of each ring, for $k \in [0 : K)$. The sum $M_0 + M_1 + \cdots + M_{K-1}$ must be a power of $2$.

            amplitudes (Tuple[float, ...]): A $K$-tuple with the amplitudes $A_k$ of each ring, for $k \in [0 : K)$.

            phase_offsets (Optional[Tuple[float, ...] | float]): A $K$-tuple with the phase offsets $\phi_k$ of each ring, for $k \in [0 : K)$. If specified as a single float $\phi$, then it is assumed that $\phi_k = \phi$ for all $k \in [0 : K)$. The default value is `0.0`.

            labeling (Optional[Array1D[int] | str]): The binary labeling $\mathcal{Q}$ of the modulation. Can be specified either as a 1D-array of integers, in which case must be permutation of $[0 : M)$, or as a string, in which case must be equal to `'natural'`. The default value is `'natural'`.

        Examples:

            >>> apsk = komm.APSKModulation(orders=(8, 8), amplitudes=(1.0, 2.0), phase_offsets=(0.0, np.pi/8))
            >>> np.around(apsk.constellation, decimals=4)
            array([ 1.    +0.j    ,  0.7071+0.7071j,  0.    +1.j    , -0.7071+0.7071j,
                   -1.    +0.j    , -0.7071-0.7071j, -0.    -1.j    ,  0.7071-0.7071j,
                    1.8478+0.7654j,  0.7654+1.8478j, -0.7654+1.8478j, -1.8478+0.7654j,
                   -1.8478-0.7654j, -0.7654-1.8478j,  0.7654-1.8478j,  1.8478-0.7654j])
        """
        if isinstance(phase_offsets, (tuple, list)):
            phase_offsets = tuple(float(phi_k) for phi_k in phase_offsets)
            self._phase_offsets = phase_offsets
        else:
            self._phase_offsets = float(phase_offsets)
            phase_offsets = (float(phase_offsets),) * len(orders)

        constellation = []
        for M_k, A_k, phi_k in zip(orders, amplitudes, phase_offsets):
            ring_constellation = A_k * np.exp(2j * np.pi * np.arange(M_k) / M_k) * np.exp(1j * phi_k)
            constellation = np.append(constellation, ring_constellation)

        order = int(np.sum(orders))
        if isinstance(labeling, str):
            if labeling in ["natural", "reflected"]:
                labeling = getattr(Modulation, "_labeling_" + labeling)(order)
            else:
                raise ValueError("Only 'natural' or 'reflected' are supported for {}".format(self.__class__.__name__))

        super().__init__(constellation, labeling)

        self._orders = tuple(int(M_k) for M_k in orders)
        self._amplitudes = tuple(float(A_k) for A_k in amplitudes)

    def __repr__(self):
        args = "{}, amplitudes={}, phase_offsets={}".format(self._orders, self._amplitudes, self._phase_offsets)
        return "{}({})".format(self.__class__.__name__, args)
