import axios from "axios";

const BACKEND_URL = import.meta.env.VITE_BASE_URL;

// eslint-disable-next-line react-hooks/rules-of-hooks
const createAuthHeader = (email: string, password: string) => {
  const token = btoa(`${email}:${password}`);
  return `Basic ${token}`;
};

export const sendMessage = async (
  content: string,
  email: string,
  password: string
) => {
  console.log(content);
  try {
    console.log(BACKEND_URL);
    const response = await axios.post(
      `${BACKEND_URL}/api/quest`,
      {
        text: content,
      },
      {
        headers: {
          "Content-type": "application/json",
          Authorization: createAuthHeader(email, password),
        },
      }
    );
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.message);
    } else {
      throw new Error("An unexpected error occurred");
    }
  }
};

export const getChats = async (email: string, password: string) => {
  try {
    const response = await axios.post(
      `${BACKEND_URL}/api/hist`,
      {},
      {
        headers: {
          Authorization: createAuthHeader(email, password),
        },
      }
    );
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.message);
    } else {
      throw new Error("An unexpected error occurred");
    }
  }
};

export const createChatFetch = async (
  title: string,
  email: string,
  password: string
) => {
  try {
    console.log("Creating chat with title:", title);
    console.log("Using email for authentication:", email, password); // Логируем email

    const response = await axios.post(
      `${BACKEND_URL}/api/hist-create`,
      {
        title: title,
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: createAuthHeader(email, password),
        },
      }
    );

    console.log("Chat created successfully:", response.data); // Логируем успешный ответ
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      console.error("Axios error response:", error.response?.data); // Логируем данные ответа об ошибке
      console.error("Axios error message:", error.message); // Логируем сообщение об ошибке
      throw new Error(
        `Request failed: ${error.response?.status} - ${error.message}`
      );
    } else {
      console.error("Unexpected error:", error); // Логируем неожиданные ошибки
      throw new Error("An unexpected error occurred");
    }
  }
};
