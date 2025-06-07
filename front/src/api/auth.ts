import axios from "axios";
const BACKEND_URL = import.meta.env.VITE_BASE_URL;

const createAuthHeader = (email: string, password: string) => {
  const token = btoa(`${email}:${password}`);
  return `Basic ${token}`;
};

export const loginFetch = async (email: string, password: string) => {
  try {
    const response = await axios.post(`${BACKEND_URL}/api/login`, null, {
      headers: {
        Authorization: createAuthHeader(email, password),
      },
    });
    return response.data.answer;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      // Логируем ошибку для отладки
      console.error("Axios error:", error.response?.data || error.message);
      throw new Error(
        `Error: ${error.response?.data?.message || error.message}`
      );
    } else {
      console.error("Unexpected error:", error);
      throw new Error("An unexpected error occurred");
    }
  }
};

export const registerFetch = async (email: string, password: string) => {
  try {
    const response = await axios.post(
      `${BACKEND_URL}/api/register`,
      {
        username: email,
        password: password,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.data.answer;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      console.error("Error response:", error.response?.data);
      throw new Error(error.message);
    } else {
      throw new Error("An unexpected error occurred");
    }
  }
};
