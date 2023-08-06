"""Top-level package for clld-corpus-plugin."""
import logging
from pyramid.response import FileResponse
from pyramid.response import Response
from clld_corpus_plugin import datatables
from clld_corpus_plugin import interfaces
from clld_corpus_plugin import models


log = logging.getLogger(__name__)

__author__ = "Florian Matter"
__email__ = "florianmatter@gmail.com"
__version__ = "0.0.8"

audio_suffixes = [".mp3", ".wav"]


def audio_view(request):
    audio_id = request.matchdict["audio_id"]
    log.debug(f"Audio {audio_id} requested")
    audio_path = f"audio/{audio_id}.wav"
    if audio_path:
        response = FileResponse(audio_path, request=request, cache_max_age=86400)
        return response
    error = f"Audio [{audio_id}] requested but not found"
    log.error(error)
    return Response(f"<body>{error}</body>")


def includeme(config):
    config.registry.settings["mako.directories"].insert(
        1, "clld_corpus_plugin:templates"
    )
    config.add_static_view("clld-corpus-plugin-static", "clld_corpus_plugin:static")
    config.register_resource("text", models.Text, interfaces.IText, with_index=True)
    config.register_resource(
        "speaker", models.Speaker, interfaces.ISpeaker, with_index=True
    )
    config.register_resource("tag", models.Tag, interfaces.ITag, with_index=True)
    config.add_route("audio_route", "/audio/{audio_id}")
    config.add_view(audio_view, route_name="audio_route")

    config.register_datatable("sentences", datatables.SentencesWithAudio)
    config.register_datatable("texts", datatables.Texts)
