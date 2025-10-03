# Qdrant MCP Server for Customer Support RAG Using Nomic Embedding
* In this project, we have created a **Qdrant vectorstore** based MCP server for our Customer Support RAG application.
* We extract **nomic-text-embed-v1.5** embeddings and then perform similarity search on Qdrant vectorstore.
* To ensure relevancy, we filter for queries that were marked as solved in the past month and only the filtered queries are used for similarity search.
* We have also enabled **Machine to Machine Oauth (M2M)** using **Auth0** for secure access of our MCP server
* The MCP server is hosted at FastMCP Cloud:- https://qdrant-mcp.fastmcp.app/mcp
* To check if the server is health, go to https://qdrant-mcp.fastmcp.app/health

## Set up for running locally
* Create a free account in [Qdrant cloud](https://qdrant.tech/documentation/cloud-intro)
* Replace ```<QDRANT_URL>``` with your Qdrant Cloud URL and ```<QDRANT_API_KEY>``` with your API Key in .env file
* Create a free account in [Auth0](https://auth0.com/signup)
* Create a new application in Auth0 and set up Machine to Machine (M2M) Authorization (refer [this](https://auth0.com/docs/get-started/onboarding/self-service-m2m) doc from Auth0 for reference)
* Replace the ```<AUTH0_DOMAIN>``` and ```<AUTH0_API_AUDIENCE>``` in .env file with the values from your Auth0 application
* Create a new account in [nomic atlas](https://atlas.nomic.ai) and create a new API Key. Replace ```<NOMIC_API_KEY>``` with this value
* Create a new python virtual enviroment and install the dependencies using ```pip install -r requirements.txt```
* export all the environment in the .env file
* Run the server using
  ```
  fastmcp run qdrant_vector_mcp_server.py --transport http --host 0.0.0.0
  ```

## Citations
* nomic-text-embed-v1.5
  ```bibtex
  @misc{nussbaum2024nomicembedvisionexpanding,
      title={Nomic Embed Vision: Expanding the Latent Space}, 
      author={Zach Nussbaum and Brandon Duderstadt and Andriy Mulyar},
      year={2024},
      eprint={2406.18587},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2406.18587},
  }
  ```
