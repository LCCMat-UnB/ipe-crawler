# by Jin-Wu Jiang, jwjiang5918@hotmail.com; jiangjinwu@shu.edu.cn CITATION: Jiang, J. W., & Zhou, Y. P. (2017). Parameterization of Stillinger-Weber potential for two-dimensional atomic crystals. arXiv preprint arXiv:1704.03147

# SW parameters for b-GaAs    , used by LAMMPS
# these entries are in LAMMPS "metal" units:
#   epsilon = eV; sigma = Angstroms
#   other quantities are unitless

# format of a single entry (one or more lines):
#   element 1, element 2, element 3,
#   epsilon, sigma, a, lambda, gamma, costheta0, A, B, p, q,tol

# sw2 and sw3
Ga  As  As     1.000   2.161   1.614  91.177   1.000  -0.415  18.485   0.711  4  0   0.000
As  Ga  Ga     1.000   2.161   1.614  91.177   1.000  -0.415  18.485   0.711  4  0   0.000

# zero terms
Ga  Ga  Ga     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
Ga  Ga  As     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
Ga  As  Ga     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
As  Ga  As     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
As  As  Ga     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
As  As  As     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000