from src.llm_class import LLMClient  
import os

def run_async_task(file_path: str, prompt: str) -> dict:
    """
    Handles the full async LLM workflow:
    1. Get token
    2. Upload document
    3. Create task
    4. Poll status
    5. Return result

    :param file_path: Path to the PDF file
    :param prompt: Prompt string for the task
    :return: Result dictionary or None on failure
    """
    client = LLMClient()
    file_name = os.path.basename(file_path)

    print(f"\n[Step 1] Requesting upload slot for: {file_name}")
    upload_url, doc_id = client.add_document(file_name)
    if not upload_url or not doc_id:
        return None

    print(f"[Step 2] Uploading file...")
    client.upload_document(upload_url, file_path)

    print(f"[Step 3] Creating task with prompt...")
    task_id = client.add_task(doc_id, prompt)
    if not task_id:
        return None

    print(f"[Step 4] Checking task status...")
    if client.check_task_status(task_id, file_name):
        print(f"[Step 5] Task complete. Retrieving results...\n")
        return client.get_results(task_id)

    print("Task failed or did not complete.")
    return None