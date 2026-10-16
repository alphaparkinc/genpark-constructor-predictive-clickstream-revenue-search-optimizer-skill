from client import ConstructorPredictiveClickstreamSearchOptimizer

def main():
    optimizer = ConstructorPredictiveClickstreamSearchOptimizer()
    candidates = [
        {"id": "c1", "title": "Wireless Noise Cancelling Headphones", "category": "Electronics", "brand": "Sony", "price": 349.0, "historical_cvr": 0.05},
        {"id": "c2", "title": "Over-Ear Studio Headphones", "category": "Audio", "brand": "AudioTechnica", "price": 149.0, "historical_cvr": 0.08},
        {"id": "c3", "title": "Budget Bluetooth Earbuds", "category": "Electronics", "brand": "Generic", "price": 29.0, "historical_cvr": 0.12}
    ]
    user_context = {
        "viewed_categories": ["Electronics"],
        "viewed_brands": ["Sony"],
        "preferred_price_range": [200, 500]
    }
    result = optimizer.optimize_search_results("headphones", candidates, user_context)
    print("--- Constructor.io Search Optimization Results ---")
    print(f"Query: {result['query']} | Zero Result: {result['zero_result_detected']}")
    for rank, p in enumerate(result['ranked_results'], 1):
        print(f"Rank {rank}: {p['title']} - Constructor Score: {p['constructor_rank_score']} (RPV: ${p['rpv_estimate']}, Affinity: {p['clickstream_affinity']}x)")

if __name__ == "__main__":
    main()
