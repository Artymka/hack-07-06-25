import styles from "./chatMessage.module.scss"
interface ChatMessage {
    content: string;
}
const ChatMessage: React.FC<ChatMessage> = ({ content }) => {
    return (
        <div
            className={styles.chatMessage}
        >
            {content}
        </div>
    )
}
export default ChatMessage