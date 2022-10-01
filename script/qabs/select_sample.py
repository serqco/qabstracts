import json
import os.path
import random
import typing as tg

import qabs.base as base

def configure_argparser(p_select_sample):
    p_select_sample.add_argument('--size', metavar="N", type=int, required=True,
            help="Total number of abstracts in the sample")
    p_select_sample.add_argument('--blocksize', metavar="k", type=int, required=True,
            help="Size of subsamples that are stratified over volumes and randomized")
    p_select_sample.add_argument('--to', metavar="targetdir", type=str, required=True,
            help="target directory where to place result")
    p_select_sample.add_argument('volume', nargs='+',
            help="dirname of a retrievelit result (subpopulation)")


class Population:
    def __init__(self, volumes: tg.Sequence[str]):
        self.subpopulations = []  # type: tg.Sequence[tg.Sequence[str]]
        self.volumenames = []  # volume can have a multi-part path
        for volume in volumes:
            with open(f"{volume}.list", 'rt', encoding='utf-8') as lst:
                this_pop = lst.read().split()
            this_pop.pop()  # file ends with \n, so last item is empty
            random.shuffle(this_pop)
            self.subpopulations.append(this_pop)
            self.volumenames.append(os.path.basename(volume))
        self.next_subpopI = 0  # where to attempt to draw from next time

    def draw1(self) -> str:
        anything_left = sum(map(len, self.subpopulations)) > 0
        if not anything_left:
            raise ValueError("All subpopulations have run dry. Nothing left to draw from.")
        next = self.next_subpopI  # remember where we are and
        self.next_subpopI = (next + 1) % len(self.subpopulations)  # move on by 1
        if len(self.subpopulations[next]) > 0:
            return self.subpopulations[next].pop()  # return last element and remove it
        else:
            return self.draw1()  # return from next subpopulaation, because the current one is empty

class Sample:
    """
    A list that performs blockwise shuffling while built and 
    knows about its entries' structure a la 'EMSE-2021/AbuDab21.pdf' and can extract basenames from them.
    """
    def __init__(self, blocksize: int):
        self.blocksize = blocksize
        self._elems = []

    def add(self, elem: str):
        self._elems.append(elem)
        if len(self._elems) % self.blocksize == 0:
            self._shuffle_last(self.blocksize)

    def _shuffle_last(self, n: int):
        """randomize order of the last n elems"""
        N = len(self._elems)
        lastblock = self._elems[(N - n):N]
        lastblock = random.sample(lastblock, n)
        self._elems[(N - n):N] = lastblock

    @property
    def entries(self) -> tg.Generator[str, None, None]:
        for elem in self._elems:
            yield elem

    @property
    def citekeys(self):
        for elem in self._elems:
            yield base.citekey(elem)


def select_sample(size: int, blocksize: int, to: str, volumes: tg.Sequence[str]):
    pop = Population(volumes)
    sample = Sample(blocksize)
    for i in range(size):
        sample.add(pop.draw1())
    write_list(to, sample)
    write_who_what(to, sample, blocksize)
    write_titles(to, sample, volumes)


def write_list(to: str, sample: Sample):
    with open(f"{to}/sample.list", 'w', encoding='utf8') as lst:
        for elem in sample.entries:
            lst.write(f"{elem}\n")


def write_who_what(to: str, sample: Sample, blocksize: int):
    with open(f"{to}/sample-who-what.txt", 'w', encoding='utf8') as who:
        who.write("# what              who 1               who2\n")
        for i, citekey in enumerate(sample.citekeys):
            if i % blocksize == 0:
                who.write("#----- Block %d\n" % (int(i/blocksize)+1))
            who.write(f"{citekey}\t\t\n")


def write_titles(to: str, sample: Sample, volumes: tg.Sequence[str]):
    alltitles = dict()
    for volume in volumes:
        with open(f"{volume}-metadata.json", 'rt', encoding='utf8') as md:
            for entry in json.load(md):
                alltitles[entry['identifier']] = entry['title']  # make titles accessible by citekey
    titles = dict()
    for entry in sample.entries:
        volume, citekey = base.split_entry(entry)
        titles[citekey] = alltitles[citekey]
    with open(f"{to}/sample-titles.json", 'w', encoding='utf8') as j:
        json.dump(titles, j, indent=2)