#!/usr/bin/env python3
import json
import sys
from client import ConstructorPredictiveClickstreamSearchOptimizer

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        optimizer = ConstructorPredictiveClickstreamSearchOptimizer()
        items = [
            {"id": "c1", "title": "Wireless Noise Cancelling Headphones", "category": "Electronics", "brand": "Sony", "price": 349.0, "historical_cvr": 0.05},
            {"id": "c2", "title": "Over-Ear Studio Headphones", "category": "Audio", "brand": "AudioTechnica", "price": 149.0, "historical_cvr": 0.08},
            {"id": "c3", "title": "Budget Bluetooth Earbuds", "category": "Electronics", "brand": "Generic", "price": 29.0, "historical_cvr": 0.12}
        ]
        clickstream = {"viewed_categories": ["Electronics"], "viewed_brands": ["Sony"], "preferred_price_range": [200, 500]}
        res = optimizer.optimize_search_results("headphones", items, clickstream)
        assert len(res["ranked_results"]) == 3
        assert res["ranked_results"][0]["id"] == "c1"
        print(f"[TEST PASS] Constructor.io Optimizer Passed! Top: {res['top_rpv_product']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-constructor-optimizer", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "optimize_search_results", "description": "Constructor clickstream and RPV search optimizer"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                optimizer = ConstructorPredictiveClickstreamSearchOptimizer()
                out = optimizer.optimize_search_results(args.get("query", ""), args.get("candidates", []), args.get("user_clickstream", {}))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
