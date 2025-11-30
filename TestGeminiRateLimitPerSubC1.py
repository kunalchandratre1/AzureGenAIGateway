import json
import time
import requests

# Config
apim_gateway = "https://kunalgenaigw.azure-api.net"
model = "gemini-2.0-flash"
operation = "generateContent"
subscription_key = "***Client 1 Subscription goes here***"  # Client1

runs = 50
sleep_secs = 0.5
timeout_secs = 25

url = f"{apim_gateway}/v1beta/models/{model}:{operation}"

headers = {"Content-Type": "application/json", "Accept": "application/json"}
if subscription_key:
    headers["Ocp-Apim-Subscription-Key"] = subscription_key

# Define the request payload
payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": "How does AI work? Answer in max 2 statements."
                }
            ]
        }
    ]
}


api_runs = []

def dump_response(resp):
    """Print a concise, robust view of an HTTP response (matching CallGeminiViaAPIM.py)."""
    try:
        print("Status:", resp.status_code)
        print("Headers:")
        for k, v in resp.headers.items():
            print(f"{k}: {v}")

        try:
            body = resp.json()
            print("JSON Body:")
            print(json.dumps(body, ensure_ascii=False)[:1000])
        except ValueError:
            print("Text Body:")
            print(resp.text if resp.text is not None else "<empty body>")

    except Exception as e:
        print(f"dump_response error: {e}")

        

def is_json_response(resp):
    # Treat HTTP 200 as success; Gemini via APIM may omit Content-Type
    return resp.status_code == 200

for i in range(runs):
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout_secs)
        #dump_response(resp)
        status = resp.status_code
        print("Content-Type:", resp.headers.get("Content-Type"))

        if is_json_response(resp):
            # Parse JSON defensively: try resp.json(), then fallback to manual loads
            data = None
            try:
                data = resp.json()
            except ValueError:
                try:
                    body_bytes = resp.content or b""
                    body_text = body_bytes.decode(resp.encoding or "utf-8", errors="replace")
                    data = json.loads(body_text)
                except Exception:
                    # Still not parsable as JSON
                    print(f"▶️ Run {i+1}: {status} ⛔ JSON parse error")
                    print(body_text[:400] if body_text else (resp.text[:400] if resp.text else "<empty body>"))
                    api_runs.append({"run": i+1, "status": status, "len": len(body_text or resp.text or "")})
                    time.sleep(sleep_secs)
                    continue

            # Extract candidate text if present
            text = None
            try:
                candidates = data.get("candidates") or []
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts") or []
                    for p in parts:
                        if isinstance(p, dict) and "text" in p:
                            text = p["text"]
                            break
            except Exception:
                text = None

            print(f"▶️ Run {i+1}: {status} ✅")
            print("x-request-token-count:", resp.headers.get("x-request-token-count"))
            # Optional: minute/hour totals if policy sets them
            mt = resp.headers.get("x-minute-total")
            ht = resp.headers.get("x-hour-total")
            if mt or ht:
                print(f"x-minute-total: {mt} | x-hour-total: {ht}")
            if text:
                print(f"💬 {text[:200]}")


        else:
            # Non-JSON or non-200 response; log safely
            body_snippet = resp.text[:400] if resp.text else "<empty body>"
            #body_snippet = resp.text[:400] 
            print(f"▶️ Run {i+1}: {status} ⛔")
            print("x-request-token-count:", resp.headers.get("x-request-token-count"))
            print(f"Content-Type: {resp.headers.get('Content-Type','<unknown>')}")
            print(body_snippet)

            # If 429, optional backoff to avoid hammering
            if status == 429:
                # Sleep a bit longer to respect rate limit window
                time.sleep(1.5)

        api_runs.append({"run": i+1, "status": status, "len": len(resp.text or "")})

    except requests.RequestException as e:
        print(f"▶️ Run {i+1}: request error ⛔ {e}")
        api_runs.append({"run": i+1, "status": -1, "len": 0})

    time.sleep(sleep_secs)

# Summary
total_ok = sum(1 for r in api_runs if r["status"] == 200)
total_429 = sum(1 for r in api_runs if r["status"] == 429)
total_err = sum(1 for r in api_runs if r["status"] not in (200, 429) and r["status"] != -1)
print(f"\nSummary: OK={total_ok}, 429={total_429}, OtherErrors={total_err}, Total={len(api_runs)}")
