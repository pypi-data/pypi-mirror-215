import pathlib
import zipfile

from zenodoclient import Zenodo
from zenodoclient.api import ApiError


def test_ApiError():
    assert '404' in str(ApiError(404, {'message': 'm', 'errors': 'e'}))


def test_api():
    assert Zenodo.DOI_PATTERN.match('10.5281/zenodo.3552559')
    assert not Zenodo.DOI_PATTERN.match('10_5281/zenodo.3552559')
    assert not Zenodo.DOI_PATTERN.match('10.5281/zenodo.3552559x')


def test_download_record(mocker, record, tmpdir):
    def retrieve(_, p):
        with zipfile.ZipFile(str(p), 'w') as z:
            z.writestr('data.txt', 'abc')
    mocker.patch('zenodoclient.api.urllib.request.urlretrieve', retrieve)
    mocker.patch('zenodoclient.api.md5', mocker.Mock(return_value='1'))
    outdir = pathlib.Path(str(tmpdir))
    Zenodo().download_record(record, outdir)