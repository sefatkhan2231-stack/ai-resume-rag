const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

interface RequestOptions {
  method?: "GET" | "POST" | "PUT" | "DELETE";
  body?: unknown;
  headers?: Record<string, string>;
}

async function request<T>(
  path: string,
  { method = "GET", body, headers = {} }: RequestOptions = {},
): Promise<T> {
  const isFormData = body instanceof FormData;

  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers: isFormData ? headers : { "Content-Type": "application/json" },
    body: isFormData ? body : body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const errorBody = await response.json();
      detail = errorBody.detail || JSON.stringify(errorBody);
    } catch {
      // response had no JSON body
    }
    throw new Error(`${response.status}: ${detail}`);
  }

  return response.json();
}

export default request;
