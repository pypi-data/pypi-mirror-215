from apache_beam import DoFn, PTransform, ParDo, Create
import json
from apache_beam.io.filesystems import FileSystems as beam_fs

class ReadSingleFileFromGcp(DoFn):

    def process(self, element, *args, **kwargs):
        from google.cloud import storage

        client = storage.Client()
        bucket_name, blob_name = element.path[5:].split("/", 1)
        bucket = client.get_bucket(bucket_name)
        blob = storage.Blob(blob_name, bucket)
        file_str = blob.download_as_text()
        yield file_str


class ReadFileFromGCP(PTransform):
    def __init__(self, file_pattern):
        self._file_pattern = file_pattern

    def expand(self, pcoll):
        file_paths = []
        for match_result in beam_fs.match([self._file_pattern])[0].metadata_list:
            file_paths.append(match_result)

        return (
            pcoll
            | 'Create file patterns' >> Create(file_paths)
            | 'ReadJson' >> ParDo(ReadSingleFileFromGcp())
        )
