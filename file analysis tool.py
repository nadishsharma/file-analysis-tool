# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nTApjpqvcFNdiKtV2xH-AMDHvuNO8u6Z
"""

pip install gradio

import gradio as gr
import os
import hashlib
from datetime import datetime

def get_file_metadata(file):
    if file is None:
        return "No file selected."

    file_path = file.name
    file_stats = os.stat(file_path)

    metadata = f"Filename: {os.path.basename(file_path)}\n"
    metadata += f"File size: {file_stats.st_size} bytes\n"
    metadata += f"Created: {datetime.fromtimestamp(file_stats.st_ctime)}\n"
    metadata += f"Last modified: {datetime.fromtimestamp(file_stats.st_mtime)}\n"
    metadata += f"Last accessed: {datetime.fromtimestamp(file_stats.st_atime)}\n"

    return metadata

def hash_file(file, hash_type):
    if file is None:
        return "No file selected."

    file_path = file.name
    hash_func = getattr(hashlib, hash_type)()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return f"{hash_type.upper()} Hash: {hash_func.hexdigest()}"

def analyze_file(file, hash_type):
    metadata = get_file_metadata(file)

    if hash_type != "None":
        hash_value = hash_file(file, hash_type)
        return f"{metadata}\n\n{hash_value}"

    return metadata

iface = gr.Interface(
    fn=analyze_file,
    inputs=[
        gr.File(label="Select a file"),
        gr.Dropdown(["None", "md5", "sha1", "sha256"], label="Select hash type (optional)")
    ],
    outputs=gr.Textbox(label="File Analysis Results"),
    title="File Analysis Tool",
    description="Upload a file to view its metadata and optionally generate a hash value."
)

iface.launch()

