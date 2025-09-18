.. Authentrics Client documentation master file, created by
   sphinx-quickstart on Mon Sep 15 18:38:37 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Authentrics Client documentation
================================

A Python client for `Authentrics.ai <https://authentrics.ai>`_ backend libraries that provides tools for checkpoint
management, model analysis, and parameter editing.

Typically, Authentrics.ai software is deployed to each user's infrastructure as a service, and the client is used to
interact with the service.

Under the hood, this client uses the `requests <https://requests.readthedocs.io/en/latest/>`_ library to make requests to the
Authentrics API. For methods that return data, the response is parsed into a Python object, usually a dictionary.

Installation
============

You can install the client using pip:

.. code-block:: bash

    pip install 'authentrics-client@git+https://github.com/Authentrics-ai/authentrics-client.git'
    

Quick Start
===========

.. code-block:: python

    import authentrics_client as authrx

    client = authrx.AuthentricsClient(
        base_url="https://<your-authentrics-api-url>",
    )

    # Login to the Authentrics API
    client.auth.login(
        username="<your-username>",
        password="<your-password>",
    )

    # Create a project
    project = client.project.create_project(
        name="<your-project-name>",
        description="<your-project-description>",
        model_format=authrx.FileType.HF_TEXT,
    )

    # Upload at least two checkpoints
    client.checkpoint.upload_checkpoint(
        project_id=project["id"],
        file_path="<your-first-checkpoint-path>",
        model_format=authrx.FileType.HF_TEXT,
    )
    project = client.checkpoint.upload_checkpoint(
        project_id=project["id"],
        file_path="<your-second-checkpoint-path>",
        model_format=authrx.FileType.HF_TEXT,
    )

    # These will take some time to validate
    import time
    
    while project["file_list"][-1]["validation_state"] == "unchecked":
        time.sleep(1)
        project = client.project.get_project_by_id(project["id"])
    
    if project["file_list"][-1]["validation_state"] == "invalid":
        raise ValueError("Checkpoint is invalid")

    # Run static analysis
    result = client.static.static_analysis(
        project_id=project["id"],
        checkpoint_id=project["file_list"][-1]["id"], # Not the first checkpoint
    )
    print(result)

.. toctree::
   :maxdepth: 3
   :hidden:

   /api
