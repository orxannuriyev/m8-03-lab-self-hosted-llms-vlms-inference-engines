# Self-Hosting Report

## Task 1: Performance Benchmarking Report

### Hardware & System Configuration
* **Device:** MacBook Pro 15-inch (2017)
* **Processor:** 2.8 GHz Quad-Core Intel Core i7
* **Memory:** 16 GB 2133 MHz LPDDR3
* **Graphics:** Intel HD Graphics 630 (1536 MB)
* **OS:** macOS Ventura 13.7.8
* **Inference Engine:** Ollama v0.1.48 (Legacy manual binary fallback used for Intel/Ventura environment compatibility)

### Performance Metrics Table

| Model | Model Size (Disk) | Load Time (s) | Tokens/sec | Active RAM (`ollama_llama_server`) | Peak System Memory State |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **qwen2.5:0.5b** | **397 MB** | 2.30s | 40.28 t/s | **84.8 MB** | Low memory pressure; smooth execution with zero swap overhead. |
| **phi3** | **2.0 GB** | 6.57s | 8.06 t/s | **783.7 MB** | High memory pressure; system pushed total memory usage to 12.51 GB and engaged 2.71 GB of Disk Swap. |

---

### Key Observations & Engineering Trade-Offs

1. **The 5x Generation Speed Penalty (Parameters vs. Compute):**
   Moving from the 0.5B parameters of Qwen to the ~3.8B parameters of Phi3 introduces an 8-fold increase in structural weight. On an older Intel Core i7 architecture, this math heavily strains the CPU, dropping token generation speed from an instantaneous 40.28 tokens/sec down to a chugging 8.06 tokens/sec.

2. **Memory Constrained Scaling (Active RAM vs. mmap Optmization):**
   Activity Monitor telemetry reveals that `ollama_llama_server` utilizes memory mapping (`mmap`). Instead of loading the entire 2.0 GB Phi3 model into RAM simultaneously, it only holds **783.7 MB** of active weights in resident memory during generation. However, because the system overall hit a peak usage of 12.51 GB, macOS was forced to offload 2.71 GB into virtual memory (Swap Used), indicating that 3B is the maximum practical threshold for local hosting on this hardware generation.

3. **Inference Engine Compatibility Obstacles:**
   The initial failure with `llama3.2:3b` throwing a tensor validation error (`expected 255, got 254`) highlights a major trade-off in self-hosting: modern model architectures frequently break compatibility with legacy software runners. Swapping to `phi3` on Ollama v0.1.48 successfully isolated the hardware limits from software dependency bugs.
> TODO

## Task 3: VLM Performance Evaluation (Local Single-Model Analysis)

*Note: Due to operating system constraints (macOS Ventura requiring legacy Ollama v0.1.48) and lack of a hosted Gemini API key, modern heavyweight VLMs like PaliGemma or Gemma3 could not be deployed. Therefore, this evaluation is strictly based on the lightweight, legacy-compatible Moondream (1.8B) model.*

### Model Performance Metrics

| Metric | Local VLM: `moondream` (~1.8B) |
| :--- | :--- |
| **Response Quality** | **Passable.** Successfully extracted general concepts like "tokens per second" and correctly identified the bar chart structure. However, it suffered from minor hallucinations regarding the precision of specific numerical metrics. |
| **Inference Speed** | **Stable.** Generated text at approximately 6-8 tokens/second on the local Intel mobile CPU without locking up the operating system. |
| **Financial Cost** | **$0.00** (100% free, runs entirely offline on local consumer hardware). |
| **Hardware Strain** | **Low.** Maintained a minimal memory and compute footprint, making it highly safe for legacy laptop architectures. |

### Summary Reflection
Testing multimodal capabilities on legacy environments reveals a strict baseline for self-hosting. While larger, modern visual models fail to initialize due to software version mismatches on older Ollama engines, `moondream` stands out as an incredibly resilient architecture. It allows a 2017 Intel MacBook Pro to process complex data visual assets like `sample_chart.png` completely offline. Although its analytical depth falls short of cloud-hosted giants, it achieves the primary goal of zero-cost, localized data privacy.
