from domain.blogs.entity.blog_entry import BlogEntry
from domain.blogs.entity.factory.blog_entry_deserializer import BlogEntryDeserializer
from domain.blogs.value.blog_entry_id import BlogEntryId
from domain.docs.entity.doc_entry import DocEntry
from domain.docs.entity.factory.doc_entry_deserializer import DocEntryDeserializer
from domain.docs.value.doc_entry_id import DocEntryId
from files import file_system
from infrastructure.store.stored_entry_accessor import _StoredEntryAccessor
from tests.infrastructure.store._data.path_resolver import resolve_test_data_dir_path


def test_load_entry_when_blog_entry():
    data_path = resolve_test_data_dir_path()
    blog_data_path = file_system.join_path(data_path, 'blog')
    accessor = _StoredEntryAccessor[BlogEntry, BlogEntryId](blog_data_path, BlogEntryDeserializer())
    actual: BlogEntry = accessor.load_entry(BlogEntryId('13574176438055789968'))
    assert actual.id.value == '13574176438055789968'
    assert actual.pickup is True
    assert actual.category_path.value == 'Portfolio'
    assert len(actual.categories) == 2
    assert len(actual.images.items) == 2


def test_load_entry_when_doc_entry():
    data_path = resolve_test_data_dir_path()
    doc_data_path = file_system.join_path(data_path, 'doc')
    accessor = _StoredEntryAccessor[DocEntry, DocEntryId](doc_data_path, DocEntryDeserializer())
    actual: DocEntry = accessor.load_entry(DocEntryId('20220123190520'))
    assert actual.id.value == '20220123190520'
    assert actual.pickup is False
    assert actual.category_path.value == 'Portfolio'
    assert len(actual.categories) == 2
