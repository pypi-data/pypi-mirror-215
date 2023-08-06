"""
Class to generate a non-normal field with known mean, var, skew & kurtosis

"""

import numpy as np


class Fleishman:
    """
    Generate a non-normal field with known mean, var, skew and excess kurtosis.

    This is based on a Fleishman method, which creates a cubic polynomial
    with a normal seed field, which is non-normal.

    Y = a + bX + cX^2 + dX^3

    The trick is to tune the four polynomial coefficient (a, b, c, d) such that
    the resulting non-normal field (Y) has the desired mean, var, skew & ekurt.

    Parameters
    ----------
    size: int
        size of output field
        default: 2**20

    mean: float
        mean
        default: 0

    var: float
        varience
        default: 1

    skew: float
        skewness
        default: 0

    ekurt: float
        excess kurtosis
        default: 0

    seed: int
        random number generator seed value
        default: 42

    max_iter: int
        maximum number of iterations to iterations for
        the newton method to converge

    converge: float
        newton method convergence threshold
        default: 1e-30

    References
    ----------
        - https://link.springer.com/article/10.1007/BF02293811
        - https://support.sas.com/content/dam/SAS/support/en/books/simulating-data-with-sas/65378_Appendix_D_Functions_for_Simulating_Data_by_Using_Fleishmans_Transformation.pdf
        - https://www.diva-portal.org/smash/get/diva2:407995/FULLTEXT01.pd
        - https://pubmed.ncbi.nlm.nih.gov/34779511/
        - https://gist.github.com/paddymccrudden/de5ab688b0d93e204098f03ccc211d88
        - https://link.springer.com/article/10.1007/BF02293687
    """

    def __init__(
        self,
        size=2**20,
        mean=0,
        var=1,
        skew=0,
        ekurt=0,
        seed=42,
        max_iter=128,
        converge=1e-30,
    ):
        self.size = size
        self.mean = mean
        self.var = var
        self.skew = skew
        self.ekurt = ekurt
        self.seed = seed
        self.max_iter = max_iter
        self.converge = converge

        # Seed random number generator
        self.rng = np.random.default_rng(self.seed)

    def fl_coeff_vsk(self, b, c, d):
        """Calculate the variance, skew and kurtois of a Fleishman Polynomial.

        F = -c + bX + cX^2 + dX^3, where X ~ N(0,1)

        Parameters
        ----------
        b, c, d: float
            Fleishman Polynomial Coefficients

        Returns
        -------
        var: float
            varience

        skew: float
            skewness

        ekurt: float
            excess kurtosis
        """

        var = (b**2) + 6 * (b * d) + 2 * (c**2) + 15 * (d**2)
        skew = 2 * c * ((b**2) + 24 * (b * d) + 105 * (d**2) + 2)
        ekurt = 24 * (
            (b * d)
            + (c**2) * (1 + (b**2) + 28 * (b * d))
            + (d**2) * (12 + 48 * (b * d) + 141 * (c**2) + 225 * (d**2))
        )

        return (var, skew, ekurt)

    def fl_func(self, b, c, d):
        """
        Define a function which will have roots.

        iff: the coeffs give the desired skew and ekurtosis

        Parameters
        ----------
        b, c, d: float
            Fleishman Polynomial Coefficients

        Returns
        -------
        function: tuple
        """

        x, y, z = self.fl_coeff_vsk(b, c, d)

        return (x - 1, y - self.skew, z - self.ekurt)

    def fl_deriv(self, b, c, d):
        """
        The deriviative of the fl_func above.


        Parameters
        ----------
        b, c, d: float
            Fleishman Polynomial Coefficients

        Returns
        -------
        matrix of partial derivatives
        """

        # Partial derivatives manually
        b2 = b * b
        c2 = c * c
        d2 = d * d
        bd = b * d
        df1db = 2 * b + 6 * d
        df1dc = 4 * c
        df1dd = 6 * b + 30 * d
        df2db = 4 * c * (b + 12 * d)
        df2dc = 2 * (b2 + 24 * bd + 105 * d2 + 2)
        df2dd = 4 * c * (12 * b + 105 * d)
        df3db = 24 * (d + c2 * (2 * b + 28 * d) + 48 * d**3)
        df3dc = 48 * c * (1 + b2 + 28 * bd + 141 * d2)
        df3dd = 24 * (
            b
            + 28 * b * c2
            + 2 * d * (12 + 48 * bd + 141 * c2 + 225 * d2)
            + d2 * (48 * b + 450 * d)
        )
        return np.array(
            [[df1db, df1dc, df1dd], [df2db, df2dc, df2dd], [df3db, df3dc, df3dd]]
        )

    def newton(self, b0, c0, d0):
        """Implements newtons method to find a root of fl_func."""

        # Loop counter
        i = 0

        # Initial conditions
        f = self.fl_func(b0, c0, d0)

        while np.abs(f).max() > self.converge or i < self.max_iter:
            J = self.fl_deriv(b0, c0, d0)
            delta = -1 * np.linalg.solve(J, f)
            (b0, c0, d0) = delta + (b0, c0, d0)
            f = self.fl_func(b0, c0, d0)
            i += 1

        return (b0, c0, d0)

    def fl_ic(self):
        """Initial condition estimate of the fleisman coefficients."""

        b0 = (
            0.95357
            - 0.05679 * self.ekurt
            + 0.03520 * self.skew**2
            + 0.00133 * self.ekurt**2
        )
        c0 = 0.10007 * self.skew + 0.00844 * self.skew**3
        d0 = 0.30978 - 0.31655 * b0

        return (b0, c0, d0)

    def gen_field(self):
        """Generate the non-normal fleishman field."""

        # Feasibility condition for solutions, or some such thing :/
        ekurt_thresh = -1.13168 + 1.58837 * self.skew**2

        try:
            if self.ekurt < ekurt_thresh:
                raise ValueError(
                    f"For the Fleishman method to function with:\n\tmean: {self.mean:.2f}\n\tvari: {self.var:.2f}\n\tskew: {self.skew:.2f}\nThe value of [ekurt] must be >= [{ekurt_thresh:.4f}]"
                )

            else:
                # Normal seed for fleishman method
                X = self.rng.normal(size=int(self.size))

                b0, c0, d0 = self.fl_ic()
                b, c, d = self.newton(b0, c0, d0)

                # Generate the field from the Fleishman polynomial
                # Then scale it by the std and mean
                self.field = (-1 * c + X * (b + X * (c + X * d))) * np.sqrt(
                    self.var
                ) + self.mean

                # Stats of the generated non-normal field,
                # as a sanity check
                mean = np.mean(self.field)

                # Moments of data
                mu_2 = np.mean((self.field - mean) ** 2)
                mu_3 = np.mean((self.field - mean) ** 3)
                mu_4 = np.mean((self.field - mean) ** 4)

                var = mu_2
                skew = mu_3 / (var**1.5)
                ekurt = mu_4 / (var**2) - 3

                self.field_stats = {
                    "mean": mean,
                    "var": var,
                    "skew": skew,
                    "ekurt": ekurt,
                }

        except ValueError as err:
            print(f"{type(err).__name__}: {err}\n")
