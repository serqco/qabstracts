"""qabstracts-specific concrete subclasses for classes in qscript.annotations"""
import re
import typing as tg

import qscript.annotations as qa


IUIUcount = tg.Tuple[int, int, int, int]


class CodebookAbstracts(qa.Codebook):
    IU_SUFFIX_REGEXP = r":[iu](\\d)+"

    def can_have_iu_suffix(self, code: str) -> bool:
        """Whether this code may be used with an iu suffix."""
        return re.search(self.IU_SUFFIX_REGEXP, self.codedefs[code].suffixdef) is not None

    @classmethod
    def _rawtopicdict(cls):
        return dict(
            background='background', gap='gap', need='gap',
            objective='objective',
            design='design', method='method', result='result', claim='result', summary='summary',
            conclusion='conclusion',
            fposs='Outlook', fneed='Outlook', fgap='Outlook', fwork='Outlook',
            limitation='_other', resourcepointer='_other', X='_other',
        )


class AnnotationsAbstracts(qa.Annotations):
    UCOUNT_REGEXP = r":u(\d+)"
    ICOUNT_REGEXP = r":i(\d+)"

    def codes_with_iucounts(self, annotation1: str, annotation2: str) -> tg.Mapping[str, IUIUcount]:
        """
        Map codes to tuples of (icount1, ucount1, icount2, ucount2) for 
        those codes in the annotations that can have IU suffixes.
        Counts are forced to 0 for codes that happen not to have a suffix.
        """
        result = dict()
        for code, cfullsuffix in re.findall(self.ANNOTATION_CONTENT_REGEXP, annotation1):
            if self.codebook.can_have_iu_suffix(code):
                result[code] = self.get_iu_counts(cfullsuffix)
        for code, cfullsuffix in re.findall(self.ANNOTATION_CONTENT_REGEXP, annotation2):
            if self.codebook.can_have_iu_suffix(code):
                icount1, ucount1 = result[code]
                icount2, ucount2 = self.get_iu_counts(cfullsuffix)
                result[code] = (icount1, ucount1, icount2, ucount2)
        # counts are never optional, so all values are pairs now
        return result

    def get_iu_counts(self, cfullsuffix: str) -> tg.Tuple[int, int]:
        """
        Return a pair (icount, ucount) from the given cfullsuffix.
        """
        if not cfullsuffix:
            return 0, 0
        mm = re.search(self.ICOUNT_REGEXP, cfullsuffix)
        icount = 0 if not mm else int(mm.group(1))
        mm = re.search(self.UCOUNT_REGEXP, cfullsuffix)
        ucount = 0 if not mm else int(mm.group(1))
        return icount, ucount

