import matplotlib.pyplot as plt


class SimpleGraph:
    def __init__(
            self, x, y, xerr=None, yerr=None, title='', xlabel='', ylabel='', xticks=None, yticks=None,
            grid=True, linestyle='-', marker='', show=True, save=True
    ):
        self.plt = plt
        plt.errorbar(x, y, xerr=xerr, yerr=yerr, capsize=3, linestyle=linestyle, marker=marker)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        ax = plt.gca()
        if xticks is not None:
            plt.xticks(xticks)
        if yticks is not None:
            plt.yticks(yticks)
        if grid:
            ax.grid()
        if save:
            plt.savefig(f'{title}', dpi=300)
        if show:
            plt.show()

        pass

    def savefig(self, title=None, dpi=300):
        if title is None:
            pass
        self.plt.savefig(f'{title}', dpi=dpi)


class ManyLinesGraph:
    def __init__(self):
        pass


class BinsGraph:
    def __init__(self):
        pass


class S0MatrixGraph:
    def __init__(self):
        pass


if __name__ == '__main__':
    x = [0, 1, 2, 3, 4, 5]
    y = [5, 3, 7, 3, 5, 1]
    xerr = [0.1, 0.1, 0.1, 0.1, 0.3, 0.3]
    yerr = [0.1, 0.1, 0.1, 0.1, 0.3, 0.3]
    xticks = list(range(0, 10, 1))
    yticks = list(range(0, 10, 1))
    s = SimpleGraph(x, y, xerr=xerr, yerr=yerr, xticks=xticks, yticks=yticks, title='test', save=True)
