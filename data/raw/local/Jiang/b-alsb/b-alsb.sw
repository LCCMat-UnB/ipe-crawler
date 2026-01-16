# by Jin-Wu Jiang, jwjiang5918@hotmail.com; jiangjinwu@shu.edu.cn CITATION: Jiang, J. W., & Zhou, Y. P. (2017). Parameterization of Stillinger-Weber potential for two-dimensional atomic crystals. arXiv preprint arXiv:1704.03147

# SW parameters for b-AlSb    , used by LAMMPS
# these entries are in LAMMPS "metal" units:
#   epsilon = eV; sigma = Angstroms
#   other quantities are unitless

# format of a single entry (one or more lines):
#   element 1, element 2, element 3,
#   epsilon, sigma, a, lambda, gamma, costheta0, A, B, p, q,tol

# sw2 and sw3
Al  Sb  Sb     1.000   2.365   1.608  85.046   1.000  -0.419  20.580   0.697  4  0   0.000
Sb  Al  Al     1.000   2.365   1.608  85.046   1.000  -0.419  20.580   0.697  4  0   0.000

# zero terms
Al  Al  Al     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
Al  Al  Sb     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
Al  Sb  Al     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
Sb  Al  Sb     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
Sb  Sb  Al     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000
Sb  Sb  Sb     0.000   1.000   1.000   1.000   1.000   1.000   1.000   1.000  4  0   0.000