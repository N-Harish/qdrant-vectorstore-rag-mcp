# from mcp.server.fastmcp import FastMCP
from qdrant_client import QdrantClient
from qdrant_client.http.models.models import QueryResponse
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, Range
import os
# from dotenv import load_dotenv, find_dotenv
from typing import List
from fastmcp import FastMCP, Context
from fastmcp.server.auth import BearerAuthProvider
from utils import get_embedding, ensure_nomic_logged_in, current_millis, one_month_before
from starlette.requests import Request
from starlette.responses import PlainTextResponse

# print(f"jwks_uri:- https://{os.getenv('AUTH0_DOMAIN')}/.well-known/jwks.json")
# print(f"issuer:- https://{os.getenv('AUTH0_DOMAIN')}/")
# print("algorithm:- RS256")
# print(f"audience:- {os.getenv('AUTH0_API_AUDIENCE')}")

auth = BearerAuthProvider(
    jwks_uri=f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/jwks.json",
    issuer=f"https://{os.getenv('AUTH0_DOMAIN')}/",
    algorithm="RS256",
    audience=os.getenv('AUTH0_API_AUDIENCE')
)

mcp = FastMCP("qdrant store retriever", auth=auth)

# mcp = FastMCP("qdrant store retriever")

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"), 
    api_key=os.getenv("QDRANT_API_KEY"), 
    # prefer_grpc=True
    )


ensure_nomic_logged_in()


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    return PlainTextResponse("OK", status_code=200)

@mcp.tool(name="/tool/qdrant_similar_vectors")
async def similar_vector(collection_name: str, query: str, limit: int, score_threshold: float, ctx: Context) -> QueryResponse:
    # Calculate timestamp for one month ago (in ms)
    # now_ms = int(datetime.datetime.now(datetime.UTC).timestamp() * 1000)
    # one_month_ago_ms = now_ms - int(30 * 24 * 60 * 60 * 1000)
    await ctx.info(f"Getting Embedding for {query}...")
    embedding = get_embedding(query)
    # print(f"shape of embedding:- {embedding.shape}")

    now_ms = current_millis()
    one_month_ago_ms = one_month_before(now_ms)
    
    # query_filter = Filter(
    #     must=[
    #         # FieldCondition(
    #         #     key="status",
    #         #     match=MatchValue(value="solved")
    #         # ),
    #         FieldCondition(
    #             key="solved_at",
    #             range=Range(gte=one_month_ago_ms, lte=now_ms)
    #         )
    #     ]
    # )
    query_filter=None
    ret = qdrant.query_points(
        collection_name=collection_name,
        query=embedding,
        with_payload=True,
        limit=limit,
        score_threshold=score_threshold,
        query_filter=query_filter
    )
    await ctx.info(f"Got these results by similarity matching:- {ret}")
    return ret

# Create ASGI application
app = mcp.http_app()


# if __name__ == "__main__":
#     mcp.run(transport='http')