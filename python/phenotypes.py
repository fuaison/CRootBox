#
# analyse the phenotypes of Leitner et al . 2014
#

import py_rootbox as rb
from rb_tools import *
import matplotlib.pyplot as plt


def simulate(name, simtime):
    rs = rb.RootSystem()
    rs.openFile(name, "params/")
    rs.initialize()
    rs.simulate(simtime, True)
    return rs


def analyse(rs, name, simtime, tv0):
    top = rb.SDF_PlantBox(1e6, 1e6, 42)
    bot = rb.SDF_Complement(top)
    ana = rb.SegmentAnalyser(rs)

    print()
    print(name, ", age", simtime, "days")
    print("======================================")
    print()
    print("Number of ----------------------------")
    na = len(rs.getBaseRoots());
    print("Axes      ", na)
    nr = rs.getNumberOfRoots();
    print("Roots     " , nr)
    ns = rs.getNumberOfSegments();
    print("Segments  " , ns)

    print("\nLength (cm) --------------------------")
    tl = ana.getSummed(rb.ScalarType.length)
    print("L0          ", round(tl))
    tl_top = ana.getSummed(rb.ScalarType.length, top)
    tl_bot = ana.getSummed(rb.ScalarType.length, bot)
    print("Lcomp (top) ", round(tl_top), "(", round(100 * (tl_top / tl)), "%)")
    print("Lcomp (bot) ", round(tl_bot), "(", round(100 * (tl_bot / tl)), "%)")
    a = rb.SegmentAnalyser(rs)  # copy
    a.filter(rb.ScalarType.order, 0)
    l0 = a.getSummed(rb.ScalarType.length)
    a = rb.SegmentAnalyser(rs)  # copy
    a.filter(rb.ScalarType.order, 1)
    l1 = a.getSummed(rb.ScalarType.length)
    print("Lord (zero) ", round(l0), "(", round(100 * (l0 / tl)), "%)")
    print("Lord (first)", round(l1), "(", round(100 * (l1 / tl)), "%)")

    print("\nVolume -------------------------------")
    tv = ana.getSummed(rb.ScalarType.volume)
    print("V0 (cm^3)   ", tv)
    print("rVol        ", tv / tv0)
    print()


def figure8d(rs, N):
    col = 'r', 'g', 'b'
    zz = 1  # mean layer thickness (cm)

    # root length distributions
    rld = np.zeros((3 * N, int(140 / zz)))
    for j in range(0, N):
        for i in range(0, 3):
            ana = rb.SegmentAnalyser(rs[i + j * 3])
            rld[i + j * 3, :] = np.transpose(v2a(ana.distribution(rb.ScalarType.length, 0, 140, int(140 / zz), True))) / (zz * 75.*15.)  # cm /cm^3
    # mean
    rld_mean = np.zeros((3, int(140 / zz)))
    for j in range(0, N):
        for i in range(0, 3):
            rld_mean[i, :] += rld[i + j * 3, :] / N

#     # error TDOO
#     rld_sd = np.zeros((3, int(140 / zz)))
#     for j in range(0, N):
#         for i in range(0, 3):
#             rld_sd[i, :] += np.square(rld[i + j * 3, :] - rld_mean[i, :])
#     for i in range(0, 3):
#         rld_sd[i, :] = np.sqrt(rld_sd[i, :] / N) / np.sqrt(N)

    z_ = np.linspace(-140, 0, int(140 / zz) + 1)
#     for i in range(0, 3):
#         plt.errorbar(rld_mean[i][::-1], 0.5 * (z_[:-1] + z_[1:]), xerr = rld_sd[i][::-1], color = col[i], ecolor = col[i])
    for i in range(0, 3):
        plt.plot(rld_mean[i][::-1], 0.5 * (z_[:-1] + z_[1:]), col[i])


names = ["maize_p1_zero_std", "maize_p2_zero_std", "maize_p3_zero_std"]
ages = [63.5, 55.5, 58.5 ]

N = 100
rs = []
for j in range(0, N):
    for i in range(0, 3):
        rs.append(simulate(names[i], ages[i]))

names = ["P1", "P2", "P3"]

tv0 = 1
for i in range(0, 3):
    if i == 0:  # reference volume (P1)
        ana = rb.SegmentAnalyser(rs[0])
        tv0 = ana.getSummed(rb.ScalarType.volume)
    analyse(rs[i], names[i], ages[i], tv0)

figure8d(rs, N)
plt.grid(True)
plt.xlabel("Root Length Density $[cm/cm^3]$")
plt.show()

