"""
Memory System - Vector + Structured
Gestisce la memoria vettoriale (RAG) e strutturata
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, List, Dict

logger = logging.getLogger(__name__)

MEMORY_FILE = "agent_memory.json"
VECTOR_DB_PATH = "./vector_memory"
SIMILARITY_THRESHOLD = 0.65


class VectorMemoryRAG:
    """Memoria vettoriale semantica con Chroma."""

    def __init__(self, persist_path: str = VECTOR_DB_PATH):
        self.client = None
        self.collection = None
        self._init_rag(persist_path)

    def _init_rag(self, persist_path: str):
        try:
            import chromadb
            from chromadb.utils import embedding_functions

            Path(persist_path).mkdir(exist_ok=True)
            self.client = chromadb.PersistentClient(path=persist_path)
            self.embedding_fn = (
                embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
            self.collection = self.client.get_or_create_collection(
                name="pythonita_rag",
                embedding_function=self.embedding_fn,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info("✅ Vector Memory attivata")
        except ImportError:
            logger.warning("⚠️ Chroma non installato")
            self.client = None
        except Exception as e:
            logger.warning(f"⚠️ Vector DB non disponibile: {e}")
            self.client = None

    def add(self, text: str, metadata: Dict = None, doc_id: str = None) -> bool:
        if not self.client or not self.collection:
            return False

        if metadata is None:
            metadata = {}
        metadata["timestamp"] = datetime.now().isoformat()

        if not doc_id:
            doc_id = f"mem_{int(datetime.now().timestamp() * 1000)}"

        try:
            self.collection.add(
                documents=[text[:1000]], metadatas=[metadata], ids=[doc_id]
            )
            return True
        except Exception as e:
            logger.error(f"Errore add: {e}")
            return False

    def search(
        self,
        query: str,
        k: int = 5,
        similarity_threshold: float = SIMILARITY_THRESHOLD,
        tipo_filter: List[str] = None,
    ) -> List[Dict]:
        if not self.client or not self.collection:
            return []

        try:
            where = None
            if tipo_filter:
                where = {"tipo": {"$in": tipo_filter}}

            params = {
                "query_texts": [query],
                "n_results": k,
                "include": ["documents", "metadatas", "distances"],
            }
            if where:
                params["where"] = where

            results = self.collection.query(**params)

            if not results["documents"] or not results["documents"][0]:
                return []

            formatted = []
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                similarity = 1 - dist
                if similarity < similarity_threshold:
                    continue
                formatted.append(
                    {"text": doc, "metadata": meta, "similarity": round(similarity, 3)}
                )
            return formatted
        except Exception as e:
            logger.error(f"Errore search: {e}")
            return []

    def get_context(self, query: str, max_results: int = 3) -> str:
        results = self.search(query, k=max_results, similarity_threshold=0.6)
        if not results:
            return ""
        return "\n".join([r["text"][:150] for r in results])


class StructuredMemory:
    """Memoria strutturata chiave-valore."""

    def __init__(self, memory_file: str = MEMORY_FILE):
        self.file = memory_file
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.file):
            try:
                with open(self.file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"history": [], "conoscenze": {}, "version": "1.0"}

    def save(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def add_entry(self, ruolo: str, contenuto: str, tipo: str = "conversazione"):
        entry = {
            "ruolo": ruolo,
            "contenuto": contenuto[:500],
            "timestamp": datetime.now().isoformat(),
            "tipo": tipo,
        }
        self.data["history"].append(entry)
        if len(self.data["history"]) > 100:
            self.data["history"] = self.data["history"][-50:]
        self.save()

    def memorize(self, chiave: str, valore: Any):
        self.data["conoscenze"][chiave] = {
            "valore": str(valore)[:500],
            "timestamp": datetime.now().isoformat(),
        }
        self.save()

    def recall(self, chiave: str) -> Optional[Any]:
        if chiave in self.data["conoscenze"]:
            return self.data["conoscenze"][chiave]["valore"]
        return None

    def get_history(self, limit: int = 10) -> List[Dict]:
        return self.data["history"][-limit:]

    def get_conoscenze(self) -> Dict:
        return self.data["conoscenze"]

    def clear(self):
        self.data = {"history": [], "conoscenze": {}, "version": "1.0"}
        self.save()

    def status(self) -> str:
        return f"History: {len(self.data['history'])}, Conoscenze: {len(self.data['conoscenze'])}"


class MemoryManager:
    """Gestore unificato di entrambi i tipi di memoria."""

    def __init__(self):
        self.vector = VectorMemoryRAG()
        self.structured = StructuredMemory()
        logger.info("✅ Memory Manager attivato")

    def store(self, text: str, tipo: str = "conversazione", chiave: str = None):
        self.vector.add(text, {"tipo": tipo})
        self.structured.add_entry(
            "utente" if tipo == "conversazione" else "system", text, tipo
        )
        if chiave:
            self.structured.memorize(chiave, text)

    def retrieve(self, query: str) -> str:
        vector_results = self.vector.search(query, k=3)
        if vector_results:
            return "\n".join([r["text"][:100] for r in vector_results])

        conoscenze = self.structured.get_conoscenze()
        for chiave, val in conoscenze.items():
            if query.lower() in chiave.lower():
                return f"{chiave}: {val['valore']}"

        return ""

    def status(self) -> str:
        return self.structured.status()
