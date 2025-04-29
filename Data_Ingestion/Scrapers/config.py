import json
from pathlib import Path
from typing import Dict, Any
import os


data = {
    "faras": {
        "google_maps": {
            "query": "Faras Kenya",
            "last_total_reviews": 0  # Initialize to 0 or fetch current count
        },
        "app_store": {
            "country": "ke",
            "app_name": "faras",
            "app_id": "1616854301", 
            "last_total_reviews": 0
        },
        "play_store": {
            "app_id": "com.faras.rider",
            "last_total_reviews": 0
        }
    },
    "uber": {
        "google_maps": {
            "query": "Uber office",
            "last_total_reviews": 0
        },
        "app_store": {
            "country": "ke",
            "app_name": "uber-request-a-ride",
            "app_id": "368677368",
            "last_total_reviews": 0
        },
        "play_store": {
            "app_id": "com.ubercab",
            "last_total_reviews": 0
        }
    },
    "little": {
        "google_maps": {
            "query": "Little Kenya",
            "last_total_reviews": 0
        },
        "app_store": {
            "country": "ke",
            "app_name": "little-ride",
            "app_id": "1130691846",
            "last_total_reviews": 0
        },
        "play_store": {
            "app_id": "com.craftsilicon.littlecabrider",
            "last_total_reviews": 0
        }
    },
    "bolt": {
        "google_maps": {
            "query": "Bolt Interactive",
            "last_total_reviews": 0
        },
        "app_store": {
            "country": "ke",
            "app_name": "bolt-request-a-ride",
            "app_id": "675033630",
            "last_total_reviews": 0  
        },
        "play_store": {
            "app_id": "ee.mtakso.client",
            "last_total_reviews": 0
        }
    }
    
}




class JSONManager:
    def __init__(self, file_path: str = 'data.json'):
        self.file_path = Path(file_path)
        self._create_if_not_exists()
    
    def _create_if_not_exists(self):
        if not self.file_path.exists():
            self.file_path.write_text('{}')
    
    def read(self) -> Dict[str, Any]:
        return json.loads(self.file_path.read_text())
    
    def write(self, data: Dict[str, Any]):
        self.file_path.write_text(json.dumps(data, indent=4))
    
    def update_review_count(
        self, 
        company: str, 
        source: str, 
        new_count: int
    ) -> None:
        data = self.read()
        try:
            data[company][source]['last_total_reviews'] = new_count
            self.write(data)
        except KeyError:
            raise ValueError(f"Invalid company/source: {company}/{source}")

if __name__ == "__main__":
    config = JSONManager()
    c = config.read()
    for company, sources in c.items():
        print(sources['google_maps']['last_total_reviews'])
