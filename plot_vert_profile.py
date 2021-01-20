from plotting import *
from consts import lat_range

if __name__ == "__main__":
    letters = ['a', 'b', 'c']
    titles = ['15'+u'\N{DEGREE SIGN}'+'S - 7'+u'\N{DEGREE SIGN}'+'S', \
            '7'+u'\N{DEGREE SIGN}'+'S - 2'+u'\N{DEGREE SIGN}'+'S', \
                '2'+u'\N{DEGREE SIGN}'+'S - 1'+u'\N{DEGREE SIGN}'+'N']
    for i, r in enumerate(lat_range):
        plot_CO(letters[i], r, titles[i], "CombinedData", 100, 5)
        plot_BC(letters[i], r, titles[i], "CombinedData", 100, 5)
        plot_OA(letters[i], r, titles[i], "CombinedData", 100, 5)