import authentrics_client as authrx

client = authrx.AuthentricsClient("https://api.authentrics.ai")

client.auth.login(
    username="your_username",
    password="your_password",
)

project = client.project.create_project(
    name="My Project",
    description="This is my project",
    model_format="onnx",
)

checkpoints = [
    "path/to/checkpoint1.onnx",
    "path/to/checkpoint2.onnx",
    "path/to/checkpoint3.onnx",
    "path/to/checkpoint4.onnx",
]
for checkpoint in checkpoints:
    client.checkpoint.upload_checkpoint(
        project["id"],
        checkpoint,
        "onnx",
    )

project = client.project.get_project_by_id(project["id"])

checkpoint_ids = [checkpoint["id"] for checkpoint in project["fileList"]]

results = []
for checkpoint_id in checkpoint_ids[1:]:
    results.append(
        client.static.static_analysis(
            project_id=project["id"],
            checkpoint_id=checkpoint_id,
        )
    )

print(results)
