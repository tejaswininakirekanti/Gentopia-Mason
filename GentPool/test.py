from pathlib import Path
from typing import AnyStr
# from gentopia.tools.basetool import *
# # from pypdf import PdfReader
import requests
# from io import BytesIO
import PyPDF2 
import io
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

# # import urllib
# class PdfReaderFromPathArgs(BaseModel):
#     file_path: str = Field(..., description="the path to read the file")


# class PdfReaderFromPath(BaseTool):
#     """read file from disk"""

#     name = "PdfReaderFromPath"
#     description = (
#         "Read a pdf file from hardisk with given path"
#     )
#     args_schema: Optional[Type[BaseModel]] = PdfReaderFromPathArgs

#     def _run(self, file_path) -> AnyStr:
#         read_path = (
#             Path(file_path)
#         )
#         try:
            
#             reader = PyPDF2.PdfReader(read_path)
#             content=""
#             for page in range(len(reader.pages)):
#                 pageObj = reader.pages[page]
#                 content+=pageObj.extract_text()
#             return content
#         except Exception as e:
#             return "Error: " + str(e)
#     async def _arun(self, *args: Any, **kwargs: Any) -> Any:
#         raise NotImplementedError

# class PdfReaderFromUrlArgs(BaseModel):
#     url: str = Field(..., description="the path to read the file")


# class PdfReaderFromUrl(BaseTool):
#     """read file from url"""

#     name = "PdfReaderFromUrl"
#     description = (
#         "Read a pdf file from url"
#     )
#     args_schema: Optional[Type[BaseModel]] = PdfReaderFromUrlArgs

def download_and_read_pdf(url):
    
    try:
        print(url)
        # url+=".pdf"
        # if not url.endswith(".pdf"):
        #     url += ".pdf"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            pdf_urls = [link['href'] for link in links if link['href'].endswith('.pdf')]
            print(pdf_urls)
        # pdf_bytes = io.BytesIO(response.content)
        # print(type(pdf_bytes))
        # reader = PyPDF2.PdfReader(pdf_bytes)
        with open("downloaded_pdf.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)
        print('file saved')
        # Now read the downloaded PDF
        with open("downloaded_pdf.pdf", 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            content=""
            for page in range(len(reader.pages)):
                # creating rotated page object
                pageObj = reader.pages[page]
                content+=pageObj.extract_text()
        content = content[:4096] + '...'
        
        return content
    except Exception as e:
        return "Error: " + str(e)
# async def _arun(self, *args: Any, **kwargs: Any) -> Any:
#     raise NotImplementedError
url = "https://arxiv.org/pdf/2308.04030"
r=download_and_read_pdf(url)
print(r)