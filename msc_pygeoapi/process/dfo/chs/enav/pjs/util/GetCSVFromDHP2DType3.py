import sys

from dhp.sfmt.ISFMT import ISFMT
from dhp.util.DHPToCSV import DHPToCSV

dhpInputFilesDir=sys.argv[1]
csvOutpuFilesDir=sys.argv[2]

DHPToCSV().convert(dhpInputFilesDir, csvOutpuFilesDir, ISFMT.ALLOWED_DATA_CODING_FMT.three)
