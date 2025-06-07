import MainInput from "../../components/mainInput";
import { ColorRing } from 'react-loader-spinner'
import styles from './chat.module.scss';
import useChatStore from "../../store/chat";
import ChatMessage from "../../components/chatMessage";
import IIMessage from "../../components/iiMessage";
import { useState } from "react";

// const demoFunctions = [
//     {
//         imageUrl: "/public/input_audio.svg",
//         text: "Заказать еду"
//     },
//     {
//         imageUrl: "/public/sidebar_user.svg",
//         text: "Отследить посылку"
//     },
//     {
//         imageUrl: "/public/sidebar_user.svg",
//         text: "Помощь с приложением"
//     }
// ];

const Chat = () => {
    const { chats, currentChatId } = useChatStore();
    const [isLoadingResponse, setIsLoadingResponse] = useState(false);

    const chat = chats.find((chat) => chat.id === currentChatId);

    return (
        <div className={styles.chat}>
            <div className={styles.chat__hello}>
                {!currentChatId &&
                    <>
                        <h1>Знакомьтесь, это ИИ-помощник</h1>
                        <h5>Он может решать ваши задачи по аналитике</h5>
                    </>}
            </div>
            <div className={styles.chat__infinity}>
                {chat && chat.messages.map((message, index) => (message.sender == 'user' ?
                    <ChatMessage
                        key={index}
                        content={message.content} />
                    :
                    <IIMessage
                        key={index}
                        content={message.content}
                        messageId={message.id || message.content.slice(0, 50)} />
                ))}

                {isLoadingResponse && (
                    <div className={styles.chat__infinity__loader}>
                        <ColorRing
                            visible={true}
                            height="45"
                            width="45"
                            ariaLabel="color-ring-loading"
                            wrapperStyle={{}}
                            wrapperClass="color-ring-wrapper"
                            colors={['#366d84', '#54C90F', '#366d84', '#54C90F', '#366d84']}
                        />
                        <p>Генерирую ответ</p>
                    </div>
                )}

            </div>
            <div className={styles.chat__bottom}>
                {/* <div className={styles.chat__functionsGrid}>
                    {demoFunctions.map((func, index) => (
                        <FastFunction
                            key={index}
                            className={styles.chatfunctionsGridi}
                            imageUrl={func.imageUrl}
                            text={func.text}
                        />
                    ))}
                </div> */}
                <MainInput
                    className={styles.chat__input}
                    onSend={(loading) => setIsLoadingResponse(loading)}
                />
            </div>
        </div>
    )
}

export default Chat;