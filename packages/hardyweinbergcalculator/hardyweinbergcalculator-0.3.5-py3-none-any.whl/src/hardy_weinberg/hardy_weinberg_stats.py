import json
import traceback

from ..genetics import Gene
from ..config import get_logger
from sympy import symbols
import numpy as np
from typing import List

log = get_logger(__name__)

# --------------------------------------------------------------------------- #
# Define symbols for Hardy-Weinberg equations
_p, _q, _p2, _2pq, _q2 = symbols("p, q, p**2, 2*pq, q**2")


# --------------------------------------------------------------------------- #
class HardyWeinbergStats:
    """Hardy-Weinberg Statistics class:
    defines a single Hardy-Weinberg Statistics object.
    """

    p: float
    q: float
    p_expected: float
    q_expected: float
    two_pq_expected: float
    total_population: float
    p_plus_q: float
    p_squared: float
    q_squared: float
    two_pq: float
    homozygous_dominant_population: float = None
    homozygous_recessive_population: float = None
    heterozygous_population: float = None
    p_squared_plus_two_pq_plus_q_squared: float = None
    chi_square_test: float = None
    genes: List[Gene] = None
    data_structure: np.array = None

    def __init__(
        self,
        p: float = None,
        q: float = None,
        homozygous_dominant_population: float = None,
        homozygous_recessive_population: float = None,
        heterozygous_population: float = None,
        total_population: float = None,
        genes: List[Gene] = None,
        *args,
        **kwargs,
    ):
        try:
            self.p = None
            self.q = None
            if (
                homozygous_dominant_population is not None
                and homozygous_recessive_population is not None
                and heterozygous_population is not None
            ):
                self.homozygous_dominant_population = homozygous_dominant_population
                self.homozygous_recessive_population = homozygous_recessive_population
                self.heterozygous_population = heterozygous_population
                self.total_population = round(
                    sum(
                        [
                            self.homozygous_dominant_population,
                            self.homozygous_recessive_population,
                            self.heterozygous_population,
                        ]
                    ),
                    1,
                )
                self.p = (
                    2 * self.homozygous_dominant_population
                    + self.heterozygous_population
                ) / (2 * self.total_population)
                self.q = (
                    2 * self.homozygous_recessive_population
                    + self.heterozygous_population
                ) / (2 * self.total_population)
                self._calculate_expected_values()
                self.chi_square_test, self.data_structure = self._run_chi_square_tests()
                self.genes = genes
            elif total_population is not None and p is not None or q is not None:
                self.total_population = round(total_population, 1)
                self.p = p if p is not None else 1.0 - q  # p = 1 - q
                self.q = q if q is not None else 1.0 - p  # q = 1 - p
                self._calculate_expected_values()
                self.chi_square_test, self.data_structure = self._run_chi_square_tests()
                self.genes = genes
            elif genes is not None and isinstance(genes, list) and len(genes) > 0:
                self.genes = genes
                # get the population count from genes
                (
                    self.homozygous_dominant_population,
                    self.homozygous_recessive_population,
                    self.heterozygous_population,
                ) = HardyWeinbergStats.get_population_count_from_genes(self.genes)
                # set the total population
                self.total_population = round(len(genes), 1)

                self.p = (
                    2 * self.homozygous_dominant_population
                    + self.heterozygous_population
                ) / (2 * self.total_population)

                self.q = (
                    2 * self.homozygous_recessive_population
                    + self.heterozygous_population
                ) / (2 * self.total_population)
                self._calculate_expected_values()
                self.chi_square_test, self.data_structure = self._run_chi_square_tests()
            else:
                raise ValueError(
                    "\n\nInvalid parameters passed to HardyWeinbergStats constructor. Please \n"
                    "pass either p and total_population or homozygous_dominant_population, \n"
                    "homozygous_recessive_population, heterozygous_population, and total_population.\n"
                    "Please see documentation for more details."
                )
            self.genes = genes if genes is not None else []
        except Exception as e:
            log.error(f"Error: {e}")

    @staticmethod
    def get_population_count_from_genes(genes: List[Gene], *args, **kwargs):
        """
        Get the population count from a list of genes
        :param genes:
        :param args:
        :param kwargs:
        :return:
        """
        homozygous_dominant_population = 0
        homozygous_recessive_population = 0
        heterozygous_population = 0
        if genes is not None and isinstance(genes, list) and len(genes) > 0:
            for g in genes:
                for zygous, trait in zip(g.metadata["zygous"], g.metadata["traits"]):
                    if zygous[0] == "homozgous":
                        if trait[0] == "dominant":
                            homozygous_dominant_population += 1
                        elif trait[0] == "recessive":
                            homozygous_recessive_population += 1
                    elif zygous[0] == "heterozygous":
                        heterozygous_population += 1

        return (
            homozygous_dominant_population,
            homozygous_recessive_population,
            heterozygous_population,
        )

    def _calculate_expected_values(self):
        """
        Calculates the expected values for the Hardy-Weinberg equation
        :return: expected values
        """
        self.p_expected = (self.p**2) * self.total_population
        self.q_expected = (self.q**2) * self.total_population
        self.two_pq_expected = (2 * self.p * self.q) * self.total_population
        self.p_plus_q = self.p + self.q
        self.p_squared = self.p**2
        self.q_squared = self.q**2
        self.two_pq = 2 * self.p * self.q
        self.p_squared_plus_two_pq_plus_q_squared = (
            self.p_squared + self.two_pq + self.q_squared
        )

    def _run_chi_square_tests(self, *args, **kwargs):
        """
        Performs the chi-square test on the observed and expected values
        :return: chi-square test results
        """
        try:
            matrix = np.array(
                object=[
                    [
                        [
                            self.homozygous_dominant_population,
                            self.homozygous_recessive_population,
                            self.heterozygous_population,
                        ]
                    ],
                    [[self.p_expected, self.q_expected, self.two_pq_expected]],
                    [[self.p_squared, self.q_squared, self.two_pq]],
                    [[0, 0, 0]],
                ],
                dtype=np.float64,
            )

            log.info(f"\nStats Matrices: \n{matrix}")
            log.info(
                f"""\n
                {matrix[0:1][0][0]},\n
                {matrix[1:2][0][0]},\n
                {matrix[2:3][0][0]},\n
                {matrix[3:4][0][0]}
                """
            )
            i = 0
            chi_square_test = 0.0
            chi_square_values = []
            while i < len(matrix[0:1][0][0]):
                # select the observed, expected, and frequency values based
                # on the shape of the matrix (3, 1, 3) or data structure
                observed, expected, frequencies = (
                    matrix[0:1][0][0][i],
                    matrix[1:2][0][0][i],
                    matrix[2:3][0][0][i],
                )
                log.info(
                    f"\nObserved: {observed} \nExpected: {expected} \nFrequency: {frequencies}"
                )
                chi_square_value = ((observed - expected) ** 2) / expected
                # add the chi-square value to the matrix
                chi_square_values.append(chi_square_value)
                log.info(f"\nMatrix: \n{matrix}")
                # add the chi-square value to the chi-square test
                chi_square_test += chi_square_value
                matrix[3:4][0][0][i] = chi_square_value
                i += 1
            log.info(
                f"\nMatrix shape: {matrix.shape}"
                f"\nChi-Square Test Results: {chi_square_test}"
                f"\nSize of matrix: {matrix.size}"
            )
            return chi_square_test, matrix.tolist()
        except Exception as e:
            log.error(f"Error: {e}")
            log.error(traceback.format_exc())

    def __dict__(self):
        return {
            f"{_p}": self.p,
            f"{_q}": self.q,
            "expected_homozygous_dominant_population": self.p_expected,
            "expected_homozygous_recessive_population": self.q_expected,
            "expected_heterozygous_population": self.two_pq_expected,
            f"{_p} + {_q}": self.p_plus_q,
            f"{_p2}": self.p_squared,
            f"{_q2}": self.q_squared,
            f"{_2pq}": self.two_pq,
            f"{_p2} + {_2pq} + {_q2}": self.p_squared_plus_two_pq_plus_q_squared,
            "chi_square_test": self.chi_square_test,
            "homozygous_dominant_population": self.homozygous_dominant_population,
            "homozygous_recessive_population": self.homozygous_recessive_population,
            "heterozygous_population": self.heterozygous_population,
            "total_population": self.total_population,
            "genes": len([a.__dict__() for a in self.genes])
            if isinstance(self.genes, list)
            else [],
            "data_structure": self.data_structure,
        }

    def to_json(self):
        return json.dumps(self.__dict__(), indent=4, sort_keys=True)

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.__dict__()

    def __iter__(self):
        return iter(self.__dict__())
