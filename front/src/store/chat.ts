// store/chat.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

export const generateId = (): string => {
  return Math.random().toString(36).slice(2, 11);
};

export type ChatMessage = {
  id?: string;
  content: string;
  createdAt: Date;
  sender: "user" | "bot";
  isFirstRender?: boolean;
};

export type Chat = {
  id: string;
  messages: ChatMessage[];
  createdAt: Date;
  title?: string;
};

export type ChatState = {
  chats: Chat[];
  currentChatId?: string;
};

type ChatActions = {
  createChat: (title: string) => void;
  createMessage: (
    chatIndex: string,
    message: string,
    sender: "user" | "bot"
  ) => void;
  deleteChat: (id: string) => void;
  setCurrentChat: (id: string) => void;
};

type ChatStore = ChatState & ChatActions;

const initialChats: Chat[] = [
  {
    id: "baslrqjiy", // Генерация ID
    title: "Сегодняшний чат 1",
    createdAt: new Date(),
    messages: [{ content: "Привет", createdAt: new Date(), sender: "user" }],
  },
  {
    id: "3ydslmlje", // Генерация ID
    title: "Сегодняшний чат 2",
    createdAt: new Date(),
    messages: [{ content: "Как дела?", createdAt: new Date(), sender: "user" }],
  },
  {
    id: "ut7ia2quu", // Генерация ID
    title: "Вчерашний чат",
    createdAt: new Date(new Date().setDate(new Date().getDate() - 1)),
    messages: [
      {
        content: "Вчерашнее сообщение",
        createdAt: new Date(new Date().setDate(new Date().getDate() - 1)),
        sender: "user",
      },
    ],
  },
  {
    id: "73uvzizc4",
    title: "На прошлой неделе",
    createdAt: new Date(new Date().setDate(new Date().getDate() - 5)),
    messages: [
      {
        content: "Сообщение с прошлой недели",
        createdAt: new Date(new Date().setDate(new Date().getDate() - 5)),
        sender: "user",
      },
      {
        content: "Сообщение с прошлой недели от бота",
        createdAt: new Date(new Date().setDate(new Date().getDate() - 5)),
        sender: "bot",
      },
    ],
  },
  {
    id: generateId(), // Генерация ID
    title: "Старый чат",
    createdAt: new Date(new Date().setMonth(new Date().getMonth() - 1)),
    messages: [
      {
        content: "Очень старое сообщение",
        createdAt: new Date(new Date().setMonth(new Date().getMonth() - 1)),
        sender: "bot",
      },
    ],
  },
];

const useChatStore = create<ChatStore>()(
  persist(
    (set) => ({
      chats: initialChats,
      createChat: (title: string) =>
        set((state) => {
          const newChat: Chat = {
            id: generateId(),
            title: title,
            messages: [],
            createdAt: new Date(),
          };
          const chats = [...state.chats, newChat];
          return { chats };
        }),
      createMessage: (chatId, message, sender) =>
        set((state) => {
          const chats = [...state.chats];
          const chat = chats.find((chat) => chat.id === chatId);
          if (chat) {
            chat.messages.push({
              content: message,
              createdAt: new Date(),
              sender: sender,
              isFirstRender: sender === "bot",
            });
          }
          return { chats };
        }),
      deleteChat: (id: string) =>
        set((state) => {
          const chats = state.chats.filter((chat) => chat.id !== id);
          return { chats };
        }),
      setCurrentChat: (chatId: string) => {
        set((state) => {
          state.currentChatId = chatId;
          return { currentChatId: state.currentChatId };
        });
      },
    }),
    { name: "chat-storage" }
  )
);

export default useChatStore;
