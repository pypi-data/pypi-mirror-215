import pathlib

from zenodoclient.oai import Records


def test_Records(mocker):
    class Requests:
        def get(self, url, *args, **kw):
            if '/record/' in url:
                text = """\
<h4>Cite as</h4>
  <div id='invenio-csl'>
    
    <invenio-csl
        ng-init="vm.citationResult = 'the &amp; citation'"
    >
                """
            else:
                text = pathlib.Path(__file__).parent.joinpath('oaipmh.xml').read_text(
                    encoding='utf8')
            return mocker.Mock(text=text)
    mocker.patch('zenodoclient.oai.requests', Requests())
    recs = Records('tular')
    assert len(recs) == 2
    recs = sorted(recs, key=lambda r: (r.repos.repos, r.version))
    assert recs[-1].tag == 'v0.11'
    assert recs[0].citation == 'the & citation'
    assert recs[0].doi
    assert 'cldf:Wordlist' in recs[-1].keywords
