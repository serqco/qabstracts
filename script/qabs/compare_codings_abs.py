import qscript.cmd.compare_codings as qccc

class CodingsComparatorAbstracts(qccc.CodingsComparator):
    def check_suffixes(self, annots, as1, as2, ctx, maxcountdiff):
        for code, counts in annots.codes_with_iucounts(as1.annotation, as2.annotation).items():
            icount1, ucount1, icount2, ucount2 = counts
            idiff = abs(icount1 - icount2) > maxcountdiff
            udiff = abs(ucount1 - ucount2) > maxcountdiff
            if idiff and udiff:
                self._printmsg(ctx, f"{code}: Very different numbers of i&u gaps, please reconsider:",
                               self._numbered_sentence(as1),
                               self._of_1(ctx, as1.annotation), self._of_2(ctx, as2.annotation))
            elif idiff:
                self._printmsg(ctx, f"{code}: Very different numbers of informativeness gaps, please reconsider:",
                               self._numbered_sentence(as1),
                               self._of_1(ctx, as1.annotation), self._of_2(ctx, as2.annotation))
            elif udiff:
                self._printmsg(ctx, f"{code}: Very different numbers of understandability gaps, please reconsider:",
                               self._numbered_sentence(as1),
                               self._of_1(ctx, as1.annotation), self._of_2(ctx, as2.annotation))
