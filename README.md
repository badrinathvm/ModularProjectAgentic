### Description

This project generates the scaffolding necessary for executing LangGraph applications.

## Graph Overview

The diagram below illustrates the structure and flow of the LangGraph application:

<img src="https://github.com/user-attachments/assets/a8ef398b-f2d1-4d7d-8a40-275638ed3b57" width="400"/>

## Endpoints

### Start the Graph Execution

To initiate the graph execution, provide the following parameters:

- `usecase_name`: The name of the use case you're executing.
- `action`: Set to `start` to begin the process.
- `thread_id`: A unique identifier for the thread.

Here’s the JSON payload to start the execution:

<img src="https://github.com/user-attachments/assets/e59c7394-9113-4dc3-bc82-6c9db97bc96c" width="900"/>

### Resume the Graph Execution After Providing User Input

After receiving input from the user during the "Start Graph" phase, you can resume the execution by providing the following parameters:

- `project_path`: The path where the project is located.
- `action`: Set to `resume` to continue from where the graph left off.
- `thread_id`: The same thread ID used previously to ensure the graph resumes correctly.

Here’s the JSON payload for resuming the execution:

<img src="https://github.com/user-attachments/assets/cda50697-441d-424d-abc2-fd4253f1c1db" width="900"/>

### Output

Once the graph execution is completed, the folder structure will be generated as shown below:

![Generated Folder Structure](https://github.com/user-attachments/assets/cc85cd2e-17c7-4e22-8853-1729395b74a5)
