## 🔧 Gen AI Gateway – Custom Implementations

### 1. **Rate Limit for Gemini**

Implements rate-limiting logic with **two modes**:

---

### **🅐 Common Limit Per Client**

All clients share the same rate limit (e.g., **200 TPM per client**).

- **Policy File:**  
  `apim-rate-limit-gemini-default.xml`

- **Testing Code:**  
  `TestGeminiRateLimitDefault.py`

---

### **🅑 Separate Limit Per Client**

Each client has its own customized limit (e.g., Client1 → 200 TPM, Client2 → 500 TPM, etc.)

- **Policy File:**  
  `rate-limit-gemini-persub.xml`

- **Testing Code:**  
  - `TestGeminiRateLimitPerSubC1.py`  
  - `TestGeminiRateLimitPerSubC2.py`

---


IF you want to integare Gemini AI in Azure API Management then refer to step by step video here - 

[![Integrate Gemini AI with API Management](https://img.youtube.com/vi/HNuOF09vq_I/maxresdefault.jpg)](https://youtu.be/HNuOF09vq_I)



<a href="https://youtu.be/HNuOF09vq_I" target="_blank">
  <img src="https://img.youtube.com/vi/HNuOF09vq_I/maxresdefault.jpg" alt="YouTube Video" />
</a>

