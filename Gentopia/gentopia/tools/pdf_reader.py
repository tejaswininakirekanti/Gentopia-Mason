from pathlib import Path
from typing import AnyStr
from gentopia.tools.basetool import *
import requests
import io
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import urllib.parse

class PdfReaderFromPathArgs(BaseModel):
    file_path: str = Field(..., description="the path to read the file")


class PdfReaderFromPath(BaseTool):
    """read file from path"""

    name = "PdfReaderFromPath"
    description = (
        "Read a pdf file from the given path"
    )
    args_schema: Optional[Type[BaseModel]] = PdfReaderFromPathArgs

    def _run(self, file_path) -> AnyStr:
        read_path = (
            Path(file_path)
        )
        try:
            reader = PdfReader(read_path)
            content=""
            for page in range(len(reader.pages)):
                pageObj = reader.pages[page]
                content+=pageObj.extract_text()
            # slicing the content to meet limitations of gpt token count
            content = content[:4096] + '...'
            return content
        except Exception as e:
            return "Error: " + str(e)
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

class PdfReaderFromUrlArgs(BaseModel):
    url: str = Field(..., description="the path to read the file")

class PdfReaderFromUrl(BaseTool):
    """read file from url"""
    name = "PdfReaderFromUrl"
    description = (
        "Read a pdf from url"
    )
    args_schema: Optional[Type[BaseModel]] = PdfReaderFromUrlArgs

    def _run(self, url) -> AnyStr:
        
        try:
            # print(url)
            response = requests.get(url)
            if response.status_code == 200 and not url.endswith(".pdf"):
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a', href=True)
                pdf_urls=[ link for link in links if ('pdf' in link.get('href'))]            
                pdf_link = pdf_urls[0]
                # print(pdf_link)
                parsed_link = urllib.parse.urlparse(pdf_link['href'])
                if not parsed_link.scheme:
                    parsed_url = urllib.parse.urlparse(url)
                    pdf_link['href'] = parsed_url[0]+'://'+parsed_url[1]+pdf_link['href']
                    url = pdf_link['href']
                    response = requests.get(url)
            with open("temp.pdf", "wb") as pdf_file:
                pdf_file.write(response.content)
            # print('file saved')
            with open("temp.pdf", 'rb') as pdf_file:
                reader = PdfReader(pdf_file)
                content=""
                for page in range(len(reader.pages)):
                    pageObj = reader.pages[page]
                    content+=pageObj.extract_text()
            # slicing the content to meet limitations of gpt token count
            content = content[:4096] + '...'
            return content
        except Exception as e:
            return "Error: " + str(e)
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError