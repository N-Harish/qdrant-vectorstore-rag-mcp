
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from nomic import embed
import nomic
import os
from sentence_transformers import SentenceTransformer
import torch.nn.functional as F
from typing import List


def get_embedding_hf(text: str) -> List[float]:
    model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
    sentences = [f'search_document: {text}']
    embeddings = model.encode(sentences, convert_to_tensor=True,)
    embeddings = F.layer_norm(embeddings, normalized_shape=(embeddings.shape[1],))
    embeddings = F.normalize(embeddings, p=2, dim=1)
    return embeddings[0].tolist()


def current_millis() -> int:
    """
    Return the current time in milliseconds since the UNIX epoch.
    """
    return int(time.time() * 1000)


def one_month_before(ts_ms: int):
    """
    Given a timestamp in milliseconds since the UNIX epoch,
    return a tuple of:
      - original UTC datetime
      - UTC datetime one calendar month before
      - the threshold timestamp in milliseconds
    
    Example:
        dt, before_dt, before_ts = one_month_before(1749067652348)
    """
    # 1. Convert ms → seconds → datetime
    dt = datetime.utcfromtimestamp(ts_ms / 1000.0)
    
    # 2. Subtract one calendar month
    before_dt = dt - relativedelta(months=1)
    
    # 3. Convert back to ms
    before_ts = int(before_dt.timestamp() * 1000)
    
    return before_ts


def get_embedding(text):
    output = embed.text(
        texts=[text],
        model='nomic-embed-text-v1.5',
        task_type='search_document', 
    )
    
    return output["embeddings"][0]


def ensure_nomic_logged_in():
    key = os.getenv("NOMIC_API_KEY")
    nomic.cli.login(key)



