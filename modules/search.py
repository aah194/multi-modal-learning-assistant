import numpy as np

def search_chunks(
    query_embedding,
    index,
    chunks,
    top_k=3
):

    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append(chunks[idx])

    return results