# ML_Workflow
Repo overview for solving Kaggle's Tweet Sentiment Extraction [Kaggle's Tweet Sentiment Extraction Competition](https://www.kaggle.com/c/tweet-sentiment-extraction).

- Trained TensorFlow roBERTa model (from Huggingface)
- Deployed via a Flask webservice in a Docker container
- Unittests

## Installation
To start the project, follow these steps:

1. **Clone Repo:**
    ```bash
    git clone https://github.com/erlbacsi/ML_Workflow.git
    ```

2. **Install dependencies:**

    Dependencies are all in the __‘requirements.txt’__ file. This is used to build the Docker image
    ```bash
    docker build -t webservice_image .
    ```
    After that, the Docker container can be built to start the web service in the container. To do this, the script __‘webservice.py’__ is executed
    ```bash
    docker run -d -p 5000:5000 --name webservice_image webservice
    ```
    After the container has been started, the web service is active and can now respond to corresponding requests.

## Usage
This is how the web service can be used:

1. **Prepare sentiment input**

    The input is expected in JSON format. The PowerShell script __‘shell_request.ps1’__ is already available for this purpose.
    This script contains a dictionary into which any text can be inserted after the key __‘text’__. 
    In addition, the model requires input for the key __‘sentiment’__. A distinction is made between three types of text.
    The key terms for this are __‘positive’__, __‘neutral’__ and __‘negative’__.

2. **Sende den Request**

    The script can then simply be started in a PowerShell.
    ```bash
    .\shell_request.ps1
    ```
    The script sends the text to the model and receives a corresponding response, which is then displayed in the PowerShell. In addition, the response time in seconds is displayed.

## Unittests
The script __‘test_webservice.py’__ is located within the Docker container and checks the web service for some test cases.
To test the web service, a command line is opened on the Docker container.
```bash
 docker exec -it webservice
```
The script is located in the __‘usr/src/app’__ folder and can simply be started via the CMD.
```bash
python test-webservice.py -v
```
The unit tests check the web service once for correct input and once for incorrect input. The different cases can be seen in the Python script.

## Latency time improvements
- Using GPU (CUDA) for model prediction and computation
- Caching from frequent requests
- Quantisation of the ML model parameters (lower computation time and memory usage)
