# by Jin-Wu Jiang, jwjiang5918@hotmail.com; jiangjinwu@shu.edu.cn CITATION: Jiang, J. W., & Zhou, Y. P. (2017). Parameterization of Stillinger-Weber potential for two-dimensional atomic crystals. arXiv preprint arXiv:1704.03147

# SW parameters for b-GeO     , used by LAMMPS
# these entries are in LAMMPS "metal" units:
#   epsilon = eV; sigma = Angstroms
#   other quantities are unitless

# format of a single entry (one or more lines):
#   element 1, element 2, element 3,
#   epsilon, sigma, a, lambda, gamma, costheta0, A, B, p, q,tol

# sw2 and sw3
Ge  O   O      1.000   1.413   2.037  47.962   1.000  -0.182   7.390   2.136  4  0   0.000
O   Ge  Ge     1.000   1.413   2.037  47.962   1.000  -0.182   7.390   2.136  4  0   0.000

# zero terms
Ge  Ge  Ge     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
Ge  Ge  O      0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
Ge  O   Ge     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
O   Ge  O      0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
O   O   Ge     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
O   O   O      0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000