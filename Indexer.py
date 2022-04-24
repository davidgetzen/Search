import xml.etree.ElementTree as et
import file_io
class Indexer:
    def __init__(self, data_path, title_path):
        self.file_path = data_path
        self.title_path = title_path

    def parse_xml(self):
        root = et.parse(self.file_path).getroot()
        all_pages = root.findall("page")
        ids_to_titles = {}
        for page in all_pages:
            page_id = int(page.find("id").text) # int(page.find("id"))
            page_title = page.find("title").text.strip()
            ids_to_titles[page_id] = page_title
        file_io.write_title_file(self.title_path, ids_to_titles)
        