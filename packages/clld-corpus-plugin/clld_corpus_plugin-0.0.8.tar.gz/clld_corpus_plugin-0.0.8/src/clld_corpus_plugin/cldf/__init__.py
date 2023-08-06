from clldutils import jsonlib


try:
    from importlib.resources import files  # pragma: no cover
except ImportError:  # pragma: no cover
    from importlib_resources import files  # pragma: no cover


cldf_path = files("clld_corpus_plugin") / "cldf"
TextTable = jsonlib.load(cldf_path / "TextTable-metadata.json")
SpeakerTable = jsonlib.load(cldf_path / "SpeakerTable-metadata.json")
