---
name: gcp-document-ai-batch
description: Guidance and rules for generating Python code using GCP Document AI batch processing (long-running operations) with Google Cloud Storage.
---

# GCP Document AI Batch Processing Guidelines

When asked to generate or refactor Python code for batch processing files with Google Cloud Document AI:

## 1. Core SDK & Architecture Rules

- Use the official `google-cloud-documentai` SDK (v1 or v1beta3 API).
- Instantiating the client must use `DocumentProcessorServiceClient()`.
- Always set the client endpoint according to the processor location (e.g., `opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")`).
- Use `batch_process_documents` (async long-running operation), NOT `process_document` (synchronous inline processing).

## 2. Google Cloud Storage (GCS) Handling

- Input documents must be passed via `GcsBatchProcessRequest` using either `GcsDocuments` (explicit list of URIs) or `GcsPrefix` (bucket folder prefix).
- Output configurations MUST use `DocumentOutputConfig.GcsOutputConfig` specifying a target GCS output URI (`gcs_destination`).
- Set `mime_type` explicitly for input documents (e.g., `application/pdf`, `image/tiff`).

## 3. Operation & Polling Pattern

- Call `operation = client.batch_process_documents(request=request)`.
- Always wrap the operation wait call in a try/except block and explicitly set a timeout:
  ```python
  # Block until operation completes or times out
  operation.result(timeout=300)
  ```
- Print or log the operation name (`operation.operation.name`) immediately after starting so it can be tracked in GCP Logging.

## 4. Authentication & Credentials

- Do NOT hardcode API keys or service account JSON file paths inside the code.
- Use default implicit authentication via `google.auth.default()` or rely on the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

## 5. Required Code Structure

Always structure the batch function with full type hints and docstrings following this template pattern:

```python
import logging

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai

logger = logging.getLogger(__name__)

def process_batch_documents(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_uri: str,
    gcs_output_uri: str,
    input_mime_type: str = "application/pdf",
    timeout_seconds: int = 300,
) -> None:
    """Processes documents in batch using GCP Document AI and outputs results to GCS."""
    # 1. Setup client options for specific GCP region
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # 2. Formulate processor resource name
    name = client.processor_path(project_id, location, processor_id)

    # 3. Configure input & output GCS paths
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_input_uri, mime_type=input_mime_type)
    input_config = documentai.BatchDocumentsInputConfig(
        gcs_documents=documentai.GcsDocuments(documents=[gcs_document])
    )

    output_config = documentai.DocumentOutputConfig(
        gcs_output_config=documentai.DocumentOutputConfig.GcsOutputConfig(
            gcs_uri=gcs_output_uri
        )
    )

    # 4. Build request & trigger long-running operation
    request = documentai.BatchProcessRequest(
        name=name,
        input_documents=input_config,
        document_output_config=output_config,
    )

    operation = client.batch_process_documents(request=request)
    logger.info("Started Document AI batch operation: %s", operation.operation.name)

    # 5. Wait for completion
    try:
        operation.result(timeout=timeout_seconds)
    except Exception:
        logger.exception("Document AI batch operation failed: %s", operation.operation.name)
        raise
    logger.info("Document AI batch operation completed: %s", operation.operation.name)
```
