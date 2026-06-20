import asyncio
from app.services.hybrid_search import hybrid_search

qs = ['how do convolutional neural networks classify images','what is the best optimizer for reinforcement learning in robotics','how does CRISPR gene editing work','what are the rules of cricket']

async def go():
    for i, q in enumerate(qs, 1):
        r = await hybrid_search(q, top_k=3)
        print(f"\nQ{i}: {q}")
        for h in r:
            print(f'   [{h["score"]:.2f}] {h["title"][:70]}')

asyncio.run(go())