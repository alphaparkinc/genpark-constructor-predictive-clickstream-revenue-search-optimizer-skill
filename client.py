"""
Constructor.io-inspired Clickstream & Revenue-per-Visit (RPV) Search Optimizer (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import re
import math
from typing import Dict, Any, List, Optional

class ConstructorPredictiveClickstreamSearchOptimizer:
    def __init__(self, optimizer_name: str = "GenPark-Constructor-Discovery-Engine"):
        self.optimizer_name = optimizer_name

    def calculate_rpv_score(self, price: float, conversion_rate: float) -> float:
        # Expected Revenue Per Visit = Price * Conversion Rate
        return round(price * max(0.001, conversion_rate), 3)

    def calculate_clickstream_affinity(self, item: Dict[str, Any], user_clickstream: Dict[str, Any]) -> float:
        clicked_categories = set(user_clickstream.get("viewed_categories", []))
        clicked_brands = set(user_clickstream.get("viewed_brands", []))
        preferred_price_range = user_clickstream.get("preferred_price_range", [0, 10000])
        
        affinity = 1.0
        if item.get("category") in clicked_categories:
            affinity += 0.4
        if item.get("brand") in clicked_brands:
            affinity += 0.3
            
        p = float(item.get("price", 50.0))
        if preferred_price_range[0] <= p <= preferred_price_range[1]:
            affinity += 0.2
        return affinity

    def optimize_search_results(self, query: str, candidates: List[Dict[str, Any]], user_clickstream: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        clickstream = user_clickstream or {}
        q_tokens = set(re.findall(r"\w+", query.lower()))
        
        scored_items = []
        for item in candidates:
            title_tokens = set(re.findall(r"\w+", item.get("title", "").lower()))
            matches = len(q_tokens & title_tokens)
            base_relevance = matches / max(1, len(q_tokens))
            
            # Constructor.io core formula: Relevance * Affinity * log(RPV + 1)
            price = float(item.get("price", 50.0))
            cvr = float(item.get("historical_cvr", 0.03))
            rpv = self.calculate_rpv_score(price, cvr)
            affinity = self.calculate_clickstream_affinity(item, clickstream)
            
            final_score = round(base_relevance * affinity * (1.0 + math.log1p(rpv)), 4)
            scored_items.append({
                **item,
                "rpv_estimate": rpv,
                "clickstream_affinity": affinity,
                "constructor_rank_score": final_score
            })
            
        scored_items.sort(key=lambda x: x["constructor_rank_score"], reverse=True)
        
        # Zero-result fallback mechanism
        is_zero_result = not any(x["constructor_rank_score"] > 0 for x in scored_items)
        fallback_recommendations = []
        if is_zero_result:
            fallback_recommendations = sorted(candidates, key=lambda x: float(x.get("historical_cvr", 0.0)), reverse=True)[:3]
            
        return {
            "optimizer": self.optimizer_name,
            "query": query,
            "zero_result_detected": is_zero_result,
            "ranked_results": scored_items if not is_zero_result else fallback_recommendations,
            "top_rpv_product": scored_items[0]["title"] if scored_items else None,
            "optimization_verdict": "DYNAMIC_CLICKSTREAM_RPV_MAXIMIZED"
        }
