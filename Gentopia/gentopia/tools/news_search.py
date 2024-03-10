from typing import AnyStr
# from googlesearch import search
from gentopia.tools.basetool import *
from gnews import GNews
from itertools import islice



class GoogleNewsArgs(BaseModel):
    query: str = Field(..., description="a search query")


class GoogleNewsSearch(BaseTool):
    """Tool that adds the capability to query the Google News search API."""

    name = "google_news_search"
    description = ("A news search engine retrieving top search results from Google News api."
                   "Input should be a query.")

    args_schema: Optional[Type[BaseModel]] = GoogleNewsArgs

    def _run(self, query: AnyStr, top_k: int = 5) -> str:
        googlenews = GNews(language='english', max_results=5)
        res = googlenews.get_news(query)
        assert res is not None
        ans = []
        for it in islice(res, top_k):
            ans.append(str({
                'title': it["title"],
                'description': it["description"],
                'published date': it["published date"],
                'url': it['url'],
                'publisher': it['publisher']['title'],
                }))
        if not ans:
            return "no further information available"
        return '\n\n'.join(ans)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = GoogleNewsSearch()._run("Get top news in USA")
    print(ans)
