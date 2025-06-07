import styles from './iiMessage.module.scss'
import { ReactTyped } from "react-typed";
import { useEffect, useState } from 'react';

const CopyIcon = '/message_copy.svg';
const LikeIcon = '/message_like.svg';
const DislikeIcon = '/message_dislike.svg';
const ResetIcon = '/message_reset.svg';

type IIMessageProps = {
    content: string;
    messageId?: string;
};

const IIMessage = ({ content, messageId = content.slice(0, 50) }: IIMessageProps) => {
    const [hasBeenAnimated, setHasBeenAnimated] = useState(false);

    useEffect(() => {
        const animatedMessages = JSON.parse(
            sessionStorage.getItem('animatedMessages') || '{}'
        );

        if (animatedMessages[messageId]) {
            setHasBeenAnimated(true);
        } else {
            const newAnimatedMessages = { ...animatedMessages, [messageId]: true };
            sessionStorage.setItem('animatedMessages', JSON.stringify(newAnimatedMessages));
        }
    }, [messageId]);

    return (
        <div className={styles.message}>
            {!hasBeenAnimated ? (
                <ReactTyped
                    className={styles.message__content}
                    strings={[content]}
                    typeSpeed={20}
                />
            ) : (
                <div className={styles.message__content}>{content}</div>
            )}
            <span className={styles.message__icons}>
                <img src={CopyIcon} alt="копировать" className={styles.message__icons__i} />
                <img className={styles.message__icons__i} alt="лайк" src={LikeIcon} />
                <img className={styles.message__icons__i} alt="дизлайк" src={DislikeIcon} />
                <img className={styles.message__icons__i} alt="повторить запрос" src={ResetIcon} />
            </span>
        </div>
    );
};

export default IIMessage;
