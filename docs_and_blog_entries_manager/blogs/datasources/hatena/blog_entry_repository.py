from typing import Optional
from urllib.parse import urlparse, parse_qsl

from blogs.datasources.hatena.api.blog_response_parser import BlogEntryResponseBody, BlogEntriesResponseBody
from blogs.datasources.hatena.templates import request_formats
from docs_and_blog_entries_manager.api.api_client import ApiClient
from docs_and_blog_entries_manager.blogs.entity.blog_entries import BlogEntries
from docs_and_blog_entries_manager.blogs.entity.blog_entry import BlogEntry
from logs.logger import Logger


class BlogEntryRepository:
    def __init__(self, blog_api_client: ApiClient, hatena_id: str, summary_entry_id: str):
        self.__api_client = blog_api_client
        self.__hatena_id = hatena_id
        self.__summary_entry_id = summary_entry_id

    # Blog
    # GET Blog
    def find_id(self, entry_id: str) -> Optional[BlogEntry]:
        xml_string_opt = self.__api_client.get(path=entry_id)
        return BlogEntryResponseBody(xml_string_opt).parse()

    def all(self) -> BlogEntries:
        next_query_params: Optional[list[tuple]] = None
        blog_entries = []
        while True:
            xml_string_opt = self.__api_client.get(query_params=next_query_params)
            if xml_string_opt is None:
                break
            blog_entries_xml = BlogEntriesResponseBody(xml_string_opt, self.__summary_entry_id)
            blog_entries.extend(blog_entries_xml.parse())
            next_url = blog_entries_xml.next_page_url()
            next_query_params = parse_qsl(urlparse(next_url).query)
            if next_query_params is None:
                break
        return BlogEntries(blog_entries)

    # POST blog
    def post_entry(self, title: str, category: str, content: str, is_draft: bool,
                   is_title_escape: bool) -> Optional[BlogEntry]:
        body = request_formats.build_blog_entry_xml_body(self.__hatena_id, title, category, content, is_draft,
                                                         is_title_escape)
        print('[Info] API execute: POST Blog')
        blog_entry_xml = self.__api_client.post(body)
        return BlogEntryResponseBody(blog_entry_xml).parse()

    def post_summary_page(self, blog_summary_entry: BlogEntry) -> bool:
        # Todo: argument is blog entry object
        # category = 'Summary'
        # title = request_formats.summary_page_title()
        # content = request_formats.build_blog_summary_entry_content(content)
        entry_xml = self.__put_entry(blog_summary_entry, False, False)
        if entry_xml is None:
            return False
        return True

    # PUT blog
    def put_entry(self, entry: BlogEntry, is_draft: bool,
                  is_title_escape: bool) -> Optional[BlogEntry]:
        blog_entry_xml = self.__put_entry(entry, is_draft, is_title_escape)
        return BlogEntryResponseBody(blog_entry_xml).parse()

    def __put_entry(self, entry: BlogEntry, is_draft: bool, is_title_escape: bool) -> \
            Optional[str]:
        body = request_formats.build_blog_entry_xml_body(self.__hatena_id, entry.title, entry.top_category,
                                                         entry.content, is_draft, is_title_escape)
        Logger.info(f'PUT Blog: {entry.title}')
        return self.__api_client.put(body, entry.id)
