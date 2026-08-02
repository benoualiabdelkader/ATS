# Expected Interview Questions & STAR Answers

### Q1 (Technical): How do you address context window limits and retrieval latency in large-scale RAG systems?
**STAR Answer**:
- **Situation**: At Apex Intelligence Labs, enterprise search required querying 500k+ documents with latency under 50ms.
- **Task**: Architect a hybrid dense + sparse vector retrieval pipeline.
- **Action**: Implemented BM25 keyword filtering combined with ChromaDB dense embeddings, optimized with dynamic batching.
- **Result**: Reduced response latency by 68% while handling 5,000 req/sec.

### Q2 (Behavioral): Describe a situation where you had to trade off model accuracy for inference speed.
**STAR Answer**:
- **Situation**: EdgeQuant library development.
- **Task**: Compress 13B parameter LLMs for edge device deployment.
- **Action**: Applied INT8/4-bit quantization via TensorRT and ONNX.
- **Result**: Retained 98.4% FP16 accuracy while reducing memory footprint by 62%.
