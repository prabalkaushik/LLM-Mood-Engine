import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, HnswConfigDiff
from fastembed import TextEmbedding
from config.settings import settings
from typing import Dict, Any

class MemoryStore:
    def __init__(self):
        try:
            self.qdrant = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
            self.qdrant.get_collections()
        except Exception:
            self.qdrant = QdrantClient(":memory:")
            
        self.collection_name = settings.qdrant_collection
        self.embedding_model = TextEmbedding("BAAI/bge-small-en-v1.5")
        self._ensure_collection()
        
    def _ensure_collection(self):
        if not self.qdrant.collection_exists(self.collection_name):
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
                hnsw_config=HnswConfigDiff(m=16, ef_construct=100)
            )
            
    def _generate_id(self, memory_id: str) -> int:
        """Deterministic integer ID from string memory_id"""
        return int(hashlib.md5(memory_id.encode('utf-8')).hexdigest()[:15], 16)
        
    def record_memory(self, payload: Dict[str, Any]):
        memory_id = payload.get("memory_id")
        if not memory_id:
            raise ValueError("memory_id is required")
            
        point_id = self._generate_id(memory_id)
        trigger_text = payload.get("trigger_text", "")
        
        embeddings = list(self.embedding_model.embed([trigger_text]))
        vector = embeddings[0].tolist()
        
        point = PointStruct(
            id=point_id,
            vector=vector,
            payload=payload
        )
        
        self.qdrant.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        
    def compute_appraisal(self, scenario_text: str, base_severity: float, developmental_agency: float, top_k: int = 2):
        embeddings = list(self.embedding_model.embed([scenario_text]))
        vector = embeddings[0].tolist()
        
        response = self.qdrant.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=top_k
        )
        results = response.points
        
        # Edge case: no memories
        if not results:
            U = 0.95
            C = max(0.05, min(0.95, developmental_agency)) # alpha_age
            S = max(0.0, min(1.0, base_severity))
            return {"U": U, "C": C, "S": S, "priors": []}
            
        sim_1 = results[0].score
        if sim_1 <= 0:
            U = 0.95
        else:
            U = max(0.05, 1.0 - sim_1)
            
        sum_sim = sum(max(0, r.score) for r in results)
        epsilon = 1e-6
        
        H_success = 0.0
        T_trauma = 0.0
        
        for r in results:
            sim_i = max(0, r.score)
            w_i = sim_i / (sum_sim + epsilon)
            
            payload = r.payload or {}
            resolved = payload.get("resolved_successfully", False)
            delta_allo = payload.get("delta_allostasis", 0.0)
            
            if resolved:
                H_success += w_i * 1.0
            
            T_trauma += w_i * max(0.0, delta_allo)
            
        C_raw = (0.35 * developmental_agency) + (0.65 * H_success) - (0.20 * T_trauma)
        C = max(0.05, min(0.95, C_raw))
        
        S_raw = base_severity * (1.0 + T_trauma)
        S = max(0.0, min(1.0, S_raw))
        
        priors = [r.payload for r in results]
        
        return {"U": U, "C": C, "S": S, "priors": priors}
