import styles from './popup.module.scss';
import Modal from 'react-modal';
import { memo, useState, type FC } from 'react';
import { LayoutGroup, motion } from "framer-motion";
import useMediaQuery from '../../hooks/useMatchMedia';
import { Switch } from '../ui/switch';

type ModalType = 'SETTINGS' | 'PROFILE' | 'ABOUT';

interface ModalProps {
    isOpen: boolean;
    closeModal: () => void;
    iniType: ModalType;
}

const SettingsPopup: FC<ModalProps> = memo(({ isOpen, closeModal, iniType }) => {
    const isLargeScreen = useMediaQuery('(min-width: 1024px)');
    const [type, setType] = useState<ModalType>(iniType)
    const renderContent = () => {
        switch (type) {
            case 'SETTINGS':
                return (
                    <div className={styles.settings}>
                        <span className={styles.settings__line}>
                            <span>Язык</span>
                            <span>Русский</span>
                        </span>
                        <span className={styles.settings__line}>
                            <span>Тема</span>
                            <span>Тёмная</span>
                        </span>
                    </div>
                );
            case 'PROFILE':
                return (
                    <div className={styles.settings}>
                        <span className={styles.settings__line}>
                            <span>Почта</span>
                            <input className={styles.settings__line__input} placeholder='Ваша почта' />
                        </span>
                        <span className={styles.settings__line}>
                            <span>Телефон</span>
                            <input
                                type='tel'
                                className={styles.settings__line__input} placeholder='Ваш номер телефона' />
                        </span>
                        <span className={styles.settings__line}>
                            <div>
                                <span >Помогать улучшать продукт</span>
                                <p>Разрешить использовать ваш контент для обучения нашего продукта и улучшения наших услуг. Мы защищем конфиденциальность наших данных.</p>
                            </div>
                            <Switch />
                        </span>
                        <span className={styles.settings__line}>
                            <div>
                                <span >Экспортировать данные</span>
                                <p>Эти данные включают информацию о вашей учетной записи и истории ваших чатов. Экспорт может занять некоторые время. Ссылка на скачивание действительна в течении 7 дней</p>
                            </div>
                            <button
                                className={styles.settings__line__button_active}
                            >Экспортировать</button>
                        </span>
                        <span className={styles.settings__line}>
                            <span>Выйти из аккаунта</span>
                            <button
                                className={styles.settings__line__button_active}
                            >Выйти</button>
                        </span>
                        <span className={styles.settings__line}>
                            <span>Удалить все чаты</span>
                            <button
                                className={styles.settings__line__button_dizactive}
                            >Удалить</button>
                        </span>
                        <span className={styles.settings__line}>
                            <span>Удалить аккаунт</span>
                            <button
                                className={styles.settings__line__button_dizactive}
                            >Удалить</button>
                        </span>

                    </div>
                );
            case 'ABOUT':
                return (
                    <div className={styles.settings}>
                        <span className={styles.settings__line}>
                            <span>Условия пользования</span>
                            <button
                                className={styles.settings__line__button_active}
                            >Посмотреть</button>
                        </span>
                        <span className={styles.settings__line}>
                            <span>Политика конфиденциальности</span>
                            <button
                                className={styles.settings__line__button_active}
                            >Посмотреть</button>
                        </span>
                    </div>
                );
            default:
                return null;
        }
    };

    const handleType = (newType: ModalType) => {
        setType(newType)
    }


    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={closeModal}
            style={{
                overlay: {
                    backgroundColor: "rgba(0,0,0,0.4)",
                    zIndex: "9",
                    width: "100vw",
                    height: "100vh"
                },
                content: {
                    width: isLargeScreen ? "60%" : "90%",
                    height: isLargeScreen ? "80%" : "70%",
                    position: "fixed",
                    top: "50%",
                    left: "50%",
                    transform: "translate(-50%, -50%)",
                    backgroundColor: "var(--bgItem)",
                    borderRadius: "20px",
                    border: "1px solid var(--borderItem)",
                    color: "#ffffff",
                    overflow: "auto",
                    zIndex: "10"
                }
            }}
        >
            <motion.div
                className={`${styles.accordion} w-full`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
            >
                <h2 className={styles.content__h}>
                    {type === "SETTINGS" && "Настройки"}
                    {type === "PROFILE" && "Профиль"}
                    {type === "ABOUT" && "О продукте"}
                </h2>
                <LayoutGroup>
                    <motion.div className={styles.content__panel}>

                        <motion.div
                            className={`${styles.content__panel__i}`}
                            animate={{
                                backgroundColor: type === "SETTINGS" ? "var(--borderItem)" : 'var(--bgItem)',
                                color: type === "SETTINGS" ? "#ffffff" : 'var(--borderItem)'
                            }}
                            onClick={() => handleType("SETTINGS")}
                        >Настройки</motion.div>
                        <motion.div
                            className={`${styles.content__panel__i}`}
                            animate={{
                                backgroundColor:
                                    type === "PROFILE" ? "var(--borderItem)" : 'var(--bgItem)',
                                color: type === "PROFILE" ? "#ffffff" : 'var(--borderItem)'
                            }}
                            onClick={() => handleType("PROFILE")}
                        >Профиль</motion.div>
                        <motion.div
                            className={`${styles.content__panel__i}`}
                            animate={{
                                backgroundColor: type === "ABOUT" ? "var(--borderItem)" : 'var(--bgItem)',
                                color: type === "ABOUT" ? "#ffffff" : 'var(--borderItem)'
                            }}
                            onClick={() => handleType("ABOUT")}
                        >О продукте</motion.div>
                    </motion.div>
                </LayoutGroup>
                <div className={styles.content__body}>
                    {renderContent()}
                </div>
            </motion.div>
        </Modal>
    );
});

export default SettingsPopup;
