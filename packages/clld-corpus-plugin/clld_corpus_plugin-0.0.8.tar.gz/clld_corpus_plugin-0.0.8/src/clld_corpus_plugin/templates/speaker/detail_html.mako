<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%import clld_corpus_plugin.util as cutil%>
<link rel="stylesheet" href="${req.static_url('clld_corpus_plugin:static/clld-corpus.css')}"/>
<%! active_menu_item = "speakers" %>

<h3>${_('Speaker')} ${ctx.name}</h3>

<h3>${_('Sentences')}</h3>
% for s in ctx.sentences:
    <ol class="example">
        ${cutil.rendered_sentence(request, s.sentence,     sentence_link=True)}
    </ol>
% endfor

<script>
var highlight_targets = document.getElementsByName("${ctx.id}");
for (index = 0; index < highlight_targets.length; index++) {
    highlight_targets[index].children[0].classList.add("corpus-highlight");
}
</script>