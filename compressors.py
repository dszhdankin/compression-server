import zipfile
from io import BytesIO
from typing import Dict, Optional
from zipfile import ZipFile


class AbstractCompressor:

    def create_archive(self):
        pass

    def put(self, file_name: str, file_content: bytes):
        pass

    def get_archive_bytes(self) -> bytes:
        pass

    def add_extension(self, prefix: str) -> str:
        pass


class ZipCompressor(AbstractCompressor):

    def __init__(self, compression_type: int):
        self.compression_type = compression_type
        self._in_memory_file: Optional[BytesIO] = None
        self._zip_file_adapter: Optional[ZipFile] = None

    def create_archive(self):
        self._in_memory_file = BytesIO()
        self._zip_file_adapter = ZipFile(self._in_memory_file, mode="w", compression=self.compression_type)

    def put(self, file_name: str, file_content: bytes):
        self._zip_file_adapter.writestr(file_name, file_content)

    def get_archive_bytes(self) -> bytes:
        self._zip_file_adapter.close()
        self._in_memory_file.seek(0)
        archive_bytes = self._in_memory_file.read()

        self._in_memory_file = None
        self._zip_file_adapter = None

        return archive_bytes

    def add_extension(self, prefix: str) -> str:
        return prefix + ".zip"


class ZipCompressorFactory:

    def __init__(self, compression_type: int):
        self.compression_type = compression_type

    def create(self) -> ZipCompressor:
        return ZipCompressor(self.compression_type)


ZIP_COMPRESSOR_TYPES: Dict[str, int] = {
    "zipStored": zipfile.ZIP_STORED,
    "zipDeflate": zipfile.ZIP_DEFLATED,
    "zipBzip2": zipfile.ZIP_BZIP2,
    "zipLzma": zipfile.ZIP_LZMA,
}
