import random
import numpy
import matplotlib
import itertools
from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')
matplotlib.rcParams.update({'axes.labelsize': 12, 'axes.titlesize': 20})


class EnergyGame(object):

    def __init__(self, throws, start):
        self.throws = throws
        self.start = start

    def playGame(self):
        """
        Plays the energy game on a 6x6 grid, with 36 energy quanta

        Parameters
        ----------
        throws: int
            The number of throws to play for
        start: str, 'uniform' (default) or 'skewed'
            If 'uniform', start with one quanta of energy on every atom.
            If 'skewed', place all 36 quanta on the first atom of the array

        Returns
        -------
        number_list, count_list: tuple of lists
            number_list is a list with all the levels that are occupied
            count_list is a list with the corresponding occupance of each level
        """
        # Create table
        if self.start == 'uniform':
            table = numpy.ones(shape=(6, 6), dtype='int')
        elif self.start == 'skewed':
            table = numpy.zeros(shape=(6, 6), dtype='int')
            table[0, 0] = 36
        else:
            raise ValueError('start must be uniform or skewed')
        initial_counters = table.sum()
        succesful_throws = 0
        # Start game
        while succesful_throws < self.throws:
            # First throw
            coords = (random.randint(0, 5), random.randint(0, 5))
            if table[coords[0], coords[1]] > 0:
                succesful_throws += 1
                table[coords[0], coords[1]] -= 1
                # Second throw
                coords2 = (random.randint(0, 5), random.randint(0, 5))
                table[coords2[0], coords2[1]] += 1
        final_counters = table.sum()
        # Do the counting
        number_list = []
        count_list = []
        for number in range(0, int(table.max() + 1)):
            number_list.append(number)
            count_list.append(len(table[table == number]))
        # Conservation of energy checks
        assert sum([st * cnt for st, cnt
                    in zip(number_list, count_list)]) == initial_counters
        assert initial_counters == final_counters
        return number_list, count_list

    def visualize(self, ax=None):
        """
        Visualize the final distribution after playing the game
        """
        if ax is None:
            f, ax = plt.subplots(1, 1, figsize=(7, 7))
        n, c = self.playGame()
        ax.bar(n, c, width=0.5)
        if self.throws < 5000:
            ax.set_title('%d throws' % self.throws)
        else:
            ax.set_title('{:.0E} throws'.format(self.throws))
        plt.setp(ax.get_xticklabels(), visible=True)
        ax.set(xlabel='Count', ylabel='Energy level')
        return ax


def plot_plays(start):
    f, axarr = plt.subplots(2, 2, figsize=(6, 6), sharey=True, sharex=False)
    for throws, coord in zip([5, 25, 100, int(1e4)], itertools.product([0, 1], [0, 1])):
        board = EnergyGame(throws, start)
        ax = axarr[coord[0], coord[1]]
        board.visualize(ax=ax)
    axarr[0, 0].set_ylabel('Count')
    axarr[1, 0].set_ylabel('Count')
    axarr[1, 0].set_xlabel('Energy level')
    axarr[1, 1].set_xlabel('Energy level')
    plt.tight_layout()
    return f


if __name__ == '__main__':
    # plot_plays('uniform').savefig('energy_game_uniform.png', dpi=300)
    # plot_plays('skewed').savefig('energy_game_skewed.png', dpi=300)
    board = EnergyGame(100, 'uniform')
    board.visualize()
    plt.show()
