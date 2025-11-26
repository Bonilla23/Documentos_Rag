import json
import os
from datetime import datetime

class AnalyticsTracker:
    def __init__(self, data_file="./data/analytics.json"):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return self._init_data()
        return self._init_data()
    
    def _init_data(self):
        return {
            "queries": [],
            "response_times": [],
            "sources_used": {},
            "total_queries": 0,
            "total_documents": 0
        }
    
    def save(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def log_query(self, query, response_time, sources):
        self.data["queries"].append({
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "response_time": response_time
        })
        self.data["response_times"].append(response_time)
        self.data["total_queries"] += 1
        
        for source in sources:
            self.data["sources_used"][source] = self.data["sources_used"].get(source, 0) + 1
        
        self.save()
    
    def get_stats(self):
        return {
            "total_queries": self.data["total_queries"],
            "avg_response_time": sum(self.data["response_times"]) / max(len(self.data["response_times"]), 1),
            "top_sources": sorted(self.data["sources_used"].items(), key=lambda x: x[1], reverse=True)[:5]
        }
