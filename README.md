OneExtract: High-Level Technical Documentation

Phase: Optimization & Model Upgrade

1. What is OneExtract?

OneExtract is an intelligent, event-driven document processing platform designed to transform unstructured PDF documents (invoices, reports, forms) into structured JSON data.

Unlike traditional OCR systems that rely on rigid templates or simple text extraction, OneExtract uses state-of-the-art Vision-Language Models (VLMs). It "sees" the document layout, understands relationships (like columns in a table or checked boxes), and extracts data based on a dynamic JSON Configuration provided by the user.

Key Capabilities:

Template-Free: Extracts data from unknown layouts using semantic understanding.

Multi-Modal: Processes text and visual elements (tables, charts, checkboxes) simultaneously.

Config-Driven: Users define what to extract (e.g., "Invoice Number") via a config file, not code.

2. Table Extraction Strategy (Qwen3-VL Upgrade)

We have upgraded the core extraction engine from Qwen2.5 to Qwen3-VL-8B-Instruct. This model acts as the primary reasoning engine for complex structures like tables.

The Architecture

Model: Qwen3-VL-8B-Instruct.

Method: Visual Reasoning (End-to-End). We do not perform separate OCR and then parse the text. We send the full image of the page to Qwen3.

Input: Page Image + Prompt (e.g., "Extract the 'Charges' table as a JSON list of rows.").

Output: Structured JSON object matching a Pydantic schema.

Why Qwen3-VL?

Higher Precision: Better at distinguishing between closely packed columns and rows.

Chat Template Support: Supports complex, multi-turn instructions for finding specific headers.

Visual Awareness: Can handle "implicit" tables (grids without lines).

3. Inference Architecture (Azure Services)

This section illustrates how the OneExtract Worker communicates with the AI models hosted on Azure.

Azure Inference Flow Description

OneExtract Worker (Azure Container App): This component hosts the Python Parser logic. It acts as the orchestrator.

Azure Blob Storage: Used for storing intermediate page images to minimize latency. The worker fetches the page image from here.

Azure ML Managed Endpoint (ColPali): The worker sends the page image to this endpoint for retrieval, to find the correct page.

Azure ML Managed Endpoint (Qwen3-VL): The worker sends the specific page image and the extraction prompt to this GPU-enabled endpoint.

Result: The endpoint returns the structured JSON data, which the worker then saves back to Blob Storage.

4. Inference Code Improvements

To support Qwen3-VL and improve speed, significant changes were made to the codebase.

Files Changed & Improvements

File Path

Nature of Change

Technical Detail

models/QwenV2SInfer.py

Major Upgrade

• Updated class to use Qwen3VLForConditionalGeneration.



• Implemented AutoProcessor with apply_chat_template logic.



• Added Flash Attention 2 support for 2x faster attention.



• Added bitsandbytes quantization (4-bit) to reduce VRAM usage.

config/settings.yml

Configuration

• Updated model path to "Qwen/Qwen3-VL-8B-Instruct".



• Configured device map to "auto" for multi-GPU support.

src/visual_extract/helper/VLMProcessor.py

Logic Update

• Refactored prompt construction to match Qwen3's chat format (User/System roles).

requirements.txt

Dependencies

• Upgraded transformers to latest version.



• Added accelerate and flash-attn.

5. Accuracy Evaluation Framework

To ensure the upgrade to Qwen3-VL actually improved performance, we built a dedicated evaluation pipeline.

Evaluation Methodology

Script: evaluate.py

Process: The system compares the Predicted JSON output against a human-verified Ground Truth JSON.

Matching Logic

Exact Match: Checks if the extracted value is identical to the ground truth (case-insensitive).

Fuzzy Match: If exact match fails, we use Levenshtein Distance (via thefuzz library).

Threshold: > 90% similarity is considered a "Pass" (handles minor typos like "l" vs "1").

Normalization: Strips whitespace and special characters before comparison.

Key Metrics

Accuracy: Percentage of fields extracted correctly (Total Correct / Total Fields).

Precision: measure of "hallucinations" (Correct / Total Extracted).

Recall: Measure of "missed fields" (Correct / Total in Ground Truth).

Target: >95% Functional Accuracy on standard invoices.
