import { useRef, useState } from 'react';
import styles from './mainInput.module.scss'
import { sendMessage } from '../../api/chat';
import useChatStore from '../../store/chat';
import useAuthStore from '../../store/auth';

const FilesIcon = '/input_files.svg'
const ThinkIcon = '/input_think.svg'
const AudioIcon = '/input_audio.svg'
const SendIcon = '/input_send.svg'

const MainInput = ({ className, onSend }: { className: string; onSend: (isLoading: boolean) => void }) => {
    const [value, setValue] = useState<string>('')
    const [isLoading, setIsLoading] = useState(false)
    const inputRef = useRef<HTMLInputElement | null>(null)
    const { createMessage, currentChatId } = useChatStore()
    const { user } = useAuthStore()

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setValue(e.target.value)
    }

    const onPickFile = () => {
        inputRef.current?.click()
    }

    const handleSend = async () => {
        if (currentChatId && value.trim()) {
            setIsLoading(true)
            onSend(true)

            try {
                createMessage(currentChatId, value, "user")
                setValue('')
                const response = await sendMessage(value, user?.email as string, user?.password as string)
                createMessage(currentChatId, response, 'bot')
            } finally {
                setIsLoading(false)
                onSend(false)
            }
        }
    }

    return (
        <div className={`${styles.frame} ${className}`}>
            <textarea
                value={value}
                onChange={handleChange}
                placeholder='Напишите ваш запрос'
                className={styles.frame__input}
                disabled={isLoading}
            />
            <span className={styles.frame__tools}>
                <div className={styles.frame__tools__icons}>
                    <input
                        className={styles.hidden}
                        ref={inputRef}
                        type="file"
                        accept="image/*,.png,.jpg,.webp"
                        disabled={isLoading}
                    />
                    <img
                        src={FilesIcon}
                        onClick={onPickFile}
                        alt='прикрепить файл'
                        className={`${styles.frame__tools__icons__i} pt-[2px]`}
                    />
                    <img src={ThinkIcon} alt='режим думания' className={styles.frame__tools__icons__i} />
                </div>
                <div className={styles.frame__tools__icons}>
                    <img src={AudioIcon} alt='записать аудио запрос' className={styles.frame__tools__icons__i} />
                    <img
                        src={SendIcon}
                        alt='отправить запрос'
                        onClick={handleSend}
                        className={styles.frame__tools__icons__i}
                        style={isLoading ? { opacity: 0.5 } : {}}
                    />
                </div>
            </span>
        </div>
    )
}
export default MainInput