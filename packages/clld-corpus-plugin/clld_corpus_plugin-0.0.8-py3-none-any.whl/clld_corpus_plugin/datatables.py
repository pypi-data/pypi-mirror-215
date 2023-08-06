from clld.db.models.common import Contribution
from clld.db.models.common import Language
from clld.db.models.common import Parameter
from clld.db.models.common import Sentence_files
from clld.db.models.common import Value
from clld.db.models.common import ValueSentence
from clld.db.models.common import ValueSet
from clld.web.datatables.base import Col
from clld.web.datatables.base import DataTable
from clld.web.datatables.base import LinkCol
from clld.web.datatables.sentence import AudioCol
from clld.web.datatables.sentence import Sentences as orig_Sentences
from clld_corpus_plugin import models


class CountCol(Col):
    def __init__(self, dt, name, **kw):
        Col.__init__(self, dt, name, **kw)

    def format(self, item):
        return item.part_count


class Texts(DataTable):
    def col_defs(self):
        return [
            Col(self, "id"),
            LinkCol(self, "name"),
            CountCol(self, "Parts", bSortable=False, bSearchable=False),
        ]


class Speakers(DataTable):
    def col_defs(self):
        return [Col(self, "id"), LinkCol(self, "name")]


class Sentences(orig_Sentences):
    __constraints__ = [Parameter, Contribution, Language]

    def base_query(self, query):
        query = super().base_query(query)
        if self.contribution:
            query = query.filter(models.Record.contribution == self.contribution)
        return query


class SentencesWithAudio(Sentences):
    def col_defs(self):
        return super().col_defs() + [AudioCol(self, "audio")]
