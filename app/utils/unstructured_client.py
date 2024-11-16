import os
from unstructured_ingest.v2.pipeline.pipeline import Pipeline
from unstructured_ingest.v2.interfaces import ProcessorConfig
from unstructured_ingest.v2.processes.connectors.local import (
    LocalIndexerConfig,
    LocalDownloaderConfig,
    LocalConnectionConfig,
    LocalUploaderConfig,
)
from unstructured_ingest.v2.processes.partitioner import PartitionerConfig
from unstructured_ingest.v2.processes.chunker import ChunkerConfig
from unstructured_ingest.v2.processes.embedder import EmbedderConfig
import json 

# Environment variables
UNSTRUCTURED_API_KEY = os.getenv("UNSTRUCTURED_API_KEY")
UNSTRUCTURED_API_URL = os.getenv("UNSTRUCTURED_API_URL")
LOCAL_FILE_INPUT_DIR = os.getenv(
    "LOCAL_FILE_INPUT_DIR",
    "/app/uploads/",
)  # Default to a path if not set
LOCAL_FILE_OUTPUT_DIR = os.getenv(
    "LOCAL_FILE_OUTPUT_DIR",
    "/app/processed/",
)  # Default to a path if not set


def process_document() -> dict:
    """
    Process a document using Unstructured API and save parsed results locally.

    Returns:
        dict: Parsed content and metadata.
    """
    # Ensure the necessary directories exist
    # os.makedirs(input_file_path, exist_ok=True)
    # os.makedirs(output_dir, exist_ok=True)
    os.makedirs(LOCAL_FILE_INPUT_DIR, exist_ok=True)
    os.makedirs(LOCAL_FILE_OUTPUT_DIR, exist_ok=True)

    # Run the pipeline with required configurations
    Pipeline.from_configs(
        context=ProcessorConfig(),
        # Local indexer and downloader configurations
        indexer_config=LocalIndexerConfig(input_path=LOCAL_FILE_INPUT_DIR),
        downloader_config=LocalDownloaderConfig(),
        # Local connection configuration
        source_connection_config=LocalConnectionConfig(),
        # Partitioning configuration
        partitioner_config=PartitionerConfig(
            partition_by_api=True,
            api_key=UNSTRUCTURED_API_KEY,
            partition_endpoint=UNSTRUCTURED_API_URL,
            strategy="hi_res",  # Use strategy specified in original code
            additional_partition_args={
                "split_pdf_page": True,
                "split_pdf_allow_failed": True,
                "split_pdf_concurrency_level": 15,
            },
        ),
        # Optional chunking and embedding configurations
        chunker_config=ChunkerConfig(chunking_strategy="by_title"),
        embedder_config=EmbedderConfig(embedding_provider="huggingface"),
        # Local uploader to save the output
        uploader_config=LocalUploaderConfig(output_dir=LOCAL_FILE_OUTPUT_DIR),
    ).run()

    # Read processed data from the output directory
    processed_content = []
    for file in os.listdir(LOCAL_FILE_OUTPUT_DIR):
        file_path = os.path.join(LOCAL_FILE_OUTPUT_DIR, file)
        if file.endswith(".json"):  # Assumes output files are in JSON format
            with open(file_path, "r") as f:
                data = json.load(f)
                processed_content.append(data)
            # os.remove(file_path)  # Delete the file after reading

    return {
        "content": processed_content,
        "metadata": {"output_dir": LOCAL_FILE_OUTPUT_DIR},
    }