from datetime import datetime, date
from unittest.mock import Mock

import pytest

from zenodoclient.models import (
    check_controlled_vocabulary,
    PUBLICATION_TYPES,
    IMAGE_TYPES, ACCESS_RIGHTS, RELATION_TYPES, CONTRIBUTOR_TYPES,
    check_regex,
    check_list_of_objects, check_persons, check_access_right, check_iso639_3,
    Metadata, Entity, Deposition,
    RecordFile,
)


def test_validators():
    with pytest.raises(ValueError):
        check_regex(r'[a-z]+', None, Mock(), '')

    check_regex(r'[a-z]+', None, Mock(), 'abc')

    with pytest.raises(ValueError):
        check_controlled_vocabulary(PUBLICATION_TYPES, lambda i: i is True,
                                    True, Mock(), 'abc')

    check_controlled_vocabulary(PUBLICATION_TYPES, lambda i: i is True, True,
                                Mock(), 'book')

    check_controlled_vocabulary(IMAGE_TYPES, lambda i: i is True, True, Mock(),
                                'photo')

    check_controlled_vocabulary(ACCESS_RIGHTS, lambda i: i is True, True,
                                Mock(), 'closed')

    check_controlled_vocabulary(RELATION_TYPES, lambda i: i is True, True,
                                Mock(), 'cites')

    check_controlled_vocabulary(CONTRIBUTOR_TYPES, lambda i: i is True, True,
                                Mock(), 'Sponsor')

    with pytest.raises(ValueError):
        check_list_of_objects(None, None, Mock(), 'not a list')

    with pytest.raises(ValueError):
        check_list_of_objects({'a': 1}, None, None, [dict()])

    with pytest.raises(ValueError):
        check_list_of_objects('', None, Mock(), [''])

    check_list_of_objects('', None, Mock(), [])

    with pytest.raises(ValueError):
        check_persons(None, None, None, with_type=None)

    with pytest.raises(ValueError):
        check_persons(None, None, None, with_type=True)

    with pytest.raises(ValueError):
        check_access_right('open', Metadata(), None, '')

    with pytest.raises(ValueError):
        check_iso639_3(None, None, 'abfa')

    check_iso639_3(None, None, 'abf')


def test_metadata():
    mdd = Metadata(grants=[{'links': {'self': 'x'}}]).asdict()

    assert mdd['grants'][0]['id'] == 'x'
    assert mdd['upload_type'] == 'dataset'
    assert mdd['publication_date'] == datetime.now().strftime('%Y-%m-%d')
    assert mdd['access_right'] == 'open'
    assert mdd['license'] == 'cc-by'
    assert mdd['embargo_date'] == datetime.now().strftime('%Y-%m-%d')


def test_RecordFile():
    rf = RecordFile(
        links={'self': 'x'},
        bucket=None,
        key=None,
        type=None,
        size=None,
        checksum='md5:1234')
    assert rf.checksum_protocol == 'md5'
    assert rf.checksum_value == '1234'
    assert rf.url == 'x'


def test_entity(TestEntity):
    e = Entity()
    te = TestEntity(test='', )
    te.from_dict({'test': True})

    with pytest.raises(AttributeError):
        e.__str__()

    te = TestEntity(
        test='x', l=[1, 2], d={'a': 3}, dt=date(2020, 2, 20), nested=TestEntity(test=''))
    res = te.to_dict()
    assert res['dt'] == '2020-02-20'


def test_deposition():
    md = Metadata(creators=[{'name': 'Test Creator'}], title='Test Title',
                  description='Test Description')
    d = Deposition(metadata=md, id=0, created='', modified='', owner='',
                   state='done', submitted=True)

    d.validate_update()

    empty_creator_d = Deposition(metadata=Metadata(), id=0, created='',
                                 modified='', owner='', state='done',
                                 submitted=True)

    with pytest.raises(ValueError):
        empty_creator_d.validate_update()

    empty_title_d = Deposition(
        metadata=Metadata(creators=[{'name': 'Test Creator'}]), id=0,
        created='', modified='', owner='', state='done', submitted=True)

    with pytest.raises(ValueError):
        empty_title_d.validate_update()

    emtpy_desc_d = Deposition(
        metadata=Metadata(creators=[{'name': 'Test Creator'}],
                          title='Test Title'), id=0, created='', modified='',
        owner='', state='done', submitted=True)

    with pytest.raises(ValueError):
        emtpy_desc_d.validate_update()

    with pytest.raises(ValueError):
        d.validate_publish()
