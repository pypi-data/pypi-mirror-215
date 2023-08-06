from clld import interfaces
from clld.db.meta import Base
from clld.db.meta import CustomModelMixin
from clld.db.meta import PolymorphicBaseMixin
from clld.db.models import IdNameDescriptionMixin
from clld.db.models import Sentence
from clld.db.models.common import Contribution
from clld.db.models.common import HasSourceMixin
from clld.db.models.common import Language
from clld.interfaces import ISentence
from sqlalchemy import JSON
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint
from sqlalchemy import text
from sqlalchemy.orm import relationship
from zope.interface import implementer
from clld_corpus_plugin.interfaces import IMeaning
from clld_corpus_plugin.interfaces import ISpeaker
from clld_corpus_plugin.interfaces import ITag
from clld_corpus_plugin.interfaces import IText
from clld_corpus_plugin.interfaces import IWordform


@implementer(ITag)
class Tag(Base, IdNameDescriptionMixin):
    pass


@implementer(ISpeaker)
class Speaker(Base, IdNameDescriptionMixin):
    pass


@implementer(interfaces.ISentence)
class Record(CustomModelMixin, Sentence):
    pk = Column(Integer, ForeignKey("sentence.pk"), primary_key=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="sentences")


class SpeakerSentence(Base, PolymorphicBaseMixin):
    __table_args__ = (UniqueConstraint("speaker_pk", "sentence_pk"),)

    sentence_pk = Column(Integer, ForeignKey("sentence.pk"), nullable=False)
    speaker_pk = Column(Integer, ForeignKey("speaker.pk"), nullable=False)
    speaker = relationship(Speaker, innerjoin=True, backref="sentences")
    sentence = relationship(Record, innerjoin=True, backref="speaker")


@implementer(IText)
class Text(Base, IdNameDescriptionMixin, HasSourceMixin):
    text_type = Column(Unicode())
    text_metadata = Column(JSON)

    @property
    def part_count(self):
        return len(self.sentences)


class TextTag(Base, PolymorphicBaseMixin):
    __table_args__ = (UniqueConstraint("text_pk", "tag_pk"),)

    text_pk = Column(Integer, ForeignKey("text.pk"), nullable=False)
    tag_pk = Column(Integer, ForeignKey("tag.pk"), nullable=False)
    text = relationship(Text, innerjoin=True, backref="tags")
    tag = relationship(Tag, innerjoin=True, backref="texts")


class SentenceTag(Base, PolymorphicBaseMixin):
    __table_args__ = (UniqueConstraint("sentence_pk", "tag_pk"),)

    sentence_pk = Column(Integer, ForeignKey("sentence.pk"), nullable=False)
    tag_pk = Column(Integer, ForeignKey("tag.pk"), nullable=False)
    sentence = relationship(Record, innerjoin=True, backref="tags")
    tag = relationship(Tag, innerjoin=True, backref="sentences")


try:
    from clld_morphology_plugin.models import Wordform
except ImportError:

    @implementer(IWordform)
    class Wordform(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
        __table_args__ = (UniqueConstraint("language_pk", "id"),)

        language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
        language = relationship(Language, innerjoin=True)

        contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
        contribution = relationship(Contribution, backref="wordforms")

    @implementer(IMeaning)
    class Meaning(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
        pass

    class FormMeaning(Base):
        id = Column(String, unique=True)
        form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
        meaning_pk = Column(Integer, ForeignKey("meaning.pk"), nullable=False)
        form = relationship(Wordform, innerjoin=True, backref="meanings")
        meaning = relationship(Meaning, innerjoin=True, backref="forms")


class TextSentence(Base, PolymorphicBaseMixin):
    __table_args__ = (UniqueConstraint("text_pk", "sentence_pk"),)

    text_pk = Column(Integer, ForeignKey("text.pk"), nullable=False)
    sentence_pk = Column(Integer, ForeignKey("sentence.pk"), nullable=False)
    record_number = Column(Integer, nullable=False)
    phrase_number = Column(Integer, nullable=True)

    text = relationship(
        Text,
        innerjoin=True,
        backref="sentences",
        order_by="desc(TextSentence.record_number)",
    )
    sentence = relationship(Record, innerjoin=True, backref="text_assocs")


class SentencePart(Base):
    form_pk = Column(Integer, ForeignKey("wordform.pk"))
    sentence_pk = Column(Integer, ForeignKey("sentence.pk"))
    form = relationship(Wordform, backref="sentence_assocs")
    sentence = relationship(Record, backref="forms")
    index = Column(Integer)
