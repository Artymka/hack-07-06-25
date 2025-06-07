import styles from './fastFunction.module.scss';

interface FastFunctionProps {
    className?: string;
    imageUrl: string;
    text: string;
}

const FastFunction = ({ className, imageUrl, text }: FastFunctionProps) => {
    return (
        <div className={`${styles.frame} ${className}`}>
            <img
                className={styles.frame__image}
                src={imageUrl}
                alt={text}
            />
            <p className={styles.frame__text}>{text}</p>
        </div>
    )
}

export default FastFunction;