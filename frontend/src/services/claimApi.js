import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "";

export async function uploadClaim(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axios.post(`${API_BASE}/upload-claim`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
}

export async function checkHealth() {
  const response = await axios.get(`${API_BASE}/health`);
  return response.data;
}
