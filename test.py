import pstats
pstats.Stats("prof.out").strip_dirs().sort_stats("cumtime").print_stats(r"your_pkg|your_module")
