# Set up
* Create a free account in [Qdrant cloud](https://qdrant.tech/documentation/cloud-intro)
* Create a free account in [Auth0](https://auth0.com/signup)
* Create a new application in Auth0 and set up Machine to Machine (M2M) Authorization (refer [this](https://auth0.com/docs/get-started/onboarding/self-service-m2m) doc from Auth0 for reference)
* Replace the ```AUTH0_DOMAIN``` and ```AUTH0_API_AUDIENCE``` in .env file with the values from your Auth0 application
* Create a new account in [nomic atlas](https://atlas.nomic.ai) and create a new API Key. Replace ```NOMIC_API_KEY``` with this value
