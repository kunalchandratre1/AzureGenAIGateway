# AzureGenAIGateway
Gen AI Gateway Custom implementations. Below is the information about all files - 
1. Rate Limit Gemini
  **Two Modes – **
  a. Common limit per client, example 200 TPM per client.
      Refer file - apim-rate-limit-gemini-default.xml
      Testing code - TestGeminiRateLimitDefault.py
  b. Separate limit per client, Client1 – 200TPM, Client2- 500TPM etc.
      Refer file - rate-limit-gemini-persub.xml
      Testing code - TestGeminiRateLimitPerSubC1.py
                     TestGeminiRateLimitPerSubC2.py


IF you want to integare Gemini AI in Azure API Management then refer to step by step video here - 

[![Integrate Gemini AI with API Management](https://img.youtube.com/vi/HNuOF09vq_I/maxresdefault.jpg)](https://youtu.be/HNuOF09vq_I)


