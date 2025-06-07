import { useCallback, useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import styles from './sidebar.module.scss';
import type { Chat } from '../../store/chat';
import { Input } from '../../components/ui/input';
import useChatStore from '../../store/chat';
import useMediaQuery from '../../hooks/useMatchMedia';
import InfoPopup from '../../components/infoPopup';
import SettingsPopUp from '../../components/settingsPopup'
import Modal from 'react-modal'
import { createChatFetch } from '../../api/chat';
import useAuthStore from '../../store/auth';

const FirstIcon = '/sidebar_fI.svg';
const SecondIcon = '/sidebar_sI.svg';
const WarnIcon = '/sidebar_warn.svg';
const SettingsIcon = '/sidebar_settings.svg';
const DeleteIcon = 'sidebar_delete.svg'


const SideBar = ({ sideBarRefs, closeFunction }: {
    testMode?: boolean,
    sideBarRefs: React.RefObject<(HTMLDivElement | null)[]>,
    closeFunction: (e: MouseEvent) => boolean
}) => {
    const { chats, createChat, setCurrentChat, deleteChat } = useChatStore();
    const { user } = useAuthStore()
    const [isCollapsed, setIsCollapsed] = useState(false);
    const isLargeScreen = useMediaQuery('(min-width: 1024px)');
    const [infoPopUpVisible, setInfoPopUpVisible] = useState<boolean>(false);
    const [settingsPopUpVisible, setSettingsPopUpVisible] = useState<boolean>(false);
    const [value, setValue] = useState<string>('');
    const [chatDialog, setChatDialog] = useState<boolean>(false);
    const [chatDialogValue, setChatDialogValue] = useState<string>('');

    const handleChatDialog = () => {
        setChatDialog(!chatDialog)
    }
    const handleChangeChatValue = (e: React.ChangeEvent<HTMLInputElement>) => {
        setChatDialogValue(e.target.value)
    }

    const crateFullChat = async () => {
        createChat(chatDialogValue)
        setChatDialog(false)
        setChatDialogValue('')
        await createChatFetch(chatDialogValue, user?.email as string, user?.password as string)
    }


    const toggleSidebar = () => {
        setIsCollapsed(!isCollapsed);
    };

    const handleOpenInfo = useCallback(() => {
        if (!infoPopUpVisible) {
            setInfoPopUpVisible(true)
        }
    }, []);
    const handleCloseInfo = useCallback(() => setInfoPopUpVisible(false), []);

    const handleOpenSettings = useCallback(() => {
        if (!infoPopUpVisible) {
            setSettingsPopUpVisible(true)
        }
    }, []);
    const handleCloseSettings = useCallback(() => setSettingsPopUpVisible(false), []);




    const categorizedChats = useMemo(() => {
        const today = new Date();
        const startOfWeek = new Date(today);
        startOfWeek.setDate(today.getDate() - today.getDay());

        const result = {
            today: [] as Chat[],
            thisWeek: [] as Chat[],
            earlier: [] as Chat[],
        };

        for (let i = 0; i < chats.length; i++) {
            const chat = chats[i];
            const chatDate = typeof chat.createdAt === 'string'
                ? new Date(chat.createdAt)
                : chat.createdAt;

            if (chatDate.toDateString() === today.toDateString()) {
                result.today.unshift(chat);
            } else if (chatDate >= startOfWeek) {
                result.thisWeek.unshift(chat);
            } else {
                result.earlier.unshift(chat);
            }
        }

        return result;
    }, [chats]);

    const filteredChats = useMemo(() => {
        if (value.trim() === '') {
            return categorizedChats;
        }

        const filterChats = (chatArray: Chat[]) => chatArray.filter((chat: Chat) => chat.title?.toLowerCase().includes(value.toLowerCase()));
        return {
            today: filterChats(categorizedChats.today),
            thisWeek: filterChats(categorizedChats.thisWeek),
            earlier: filterChats(categorizedChats.earlier),
        };
    }, [value, categorizedChats]);

    useEffect(() => {
        const handleClick = (e: MouseEvent) => {
            if (closeFunction(e)) {
                setIsCollapsed(true);
            }
        };

        if (!isCollapsed && !isLargeScreen) {
            window.addEventListener('click', handleClick)
        } else {
            window.removeEventListener('click', handleClick);
        }

        return () => {
            window.removeEventListener('click', handleClick);
        };
    }, [!isCollapsed, closeFunction, isLargeScreen])

    useEffect(() => {
        if (!isLargeScreen) {
            setIsCollapsed(true)
        }
    }, [])

    return (
        <>
            <motion.div
                ref={el => { sideBarRefs.current[0] = el }}
                className={styles.sidebar}
                style={{
                    padding: isLargeScreen ? "0 10px" : "0",
                    position: isLargeScreen ? 'relative' : "absolute"
                }}
                animate={{
                    width: !isCollapsed
                        ? (isLargeScreen ? 'clamp(15.625rem, 12.054rem + 5.58vw, 18.75rem)' : '270px')
                        : (isLargeScreen ? '80px' : '0px')
                }}
                transition={{ duration: 0.2, ease: 'easeInOut' }}
            >
                <header className={styles.sidebar__header}>
                    {isLargeScreen &&
                        <motion.div
                            className={styles.sidebar__header__icons}
                            animate={{
                                flexDirection: isCollapsed ? 'column' : 'row',
                                alignItems: isCollapsed ? 'center' : 'flex-start'
                            }}
                            transition={{ duration: 0.2 }}
                        >
                            <motion.img
                                src={FirstIcon}
                                className={`${styles.sidebar__header__icons__i} mt-[3px]`}
                                onClick={toggleSidebar}
                                whileHover={{ scale: 1.1 }}
                                whileTap={{ scale: 0.95 }}
                            />
                            <motion.img
                                onClick={handleChatDialog}
                                src={SecondIcon}
                                className={`${styles.sidebar__header__icons__i}`}
                                whileHover={{ scale: 1.1 }}
                            />
                        </motion.div>
                    }
                    {!isCollapsed && (
                        <motion.span
                            className={styles.sidebar__header__logo}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                        >
                            SBER.AI
                        </motion.span>
                    )}
                </header>

                {
                    !isCollapsed && (
                        <>
                            <Input className={styles.sidebar__search}
                                value={value}
                                onChange={(e) => setValue(e.target.value)}
                            />

                            <motion.div
                                className={styles.sidebar__history}
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                style={{
                                    marginLeft: "30px"
                                }}
                            >
                                {(filteredChats.today.length > 0 &&
                                    <>
                                        <span className={styles.sidebar__history__date}>Сегодня</span>
                                        {filteredChats.today.map((chat, index) => (
                                            <span
                                                onClick={() => {
                                                    (setCurrentChat(chat.id))
                                                    console.log(chat.id)
                                                }}
                                                className={styles.sidebar__history__chat}
                                                key={index}>
                                                <span>{chat.title}</span>
                                                <img
                                                    onClick={(e) => {
                                                        e.preventDefault();
                                                        deleteChat(chat.id)
                                                    }}
                                                    src={DeleteIcon}
                                                    className={styles.sidebar__history__chat__delete} />

                                            </span>
                                        ))}
                                    </>
                                )}
                                {(filteredChats.thisWeek.length > 0 &&
                                    <>
                                        <span className={styles.sidebar__history__date}>На этой неделе</span>
                                        {filteredChats.thisWeek.map((chat, index) => (
                                            <span
                                                onClick={() => (setCurrentChat(chat.id))}
                                                className={styles.sidebar__history__chat}
                                                key={index}>
                                                <span>{chat.title}</span>
                                                <img
                                                    onClick={(e) => {
                                                        e.preventDefault();
                                                        deleteChat(chat.id)
                                                    }}
                                                    src={DeleteIcon}
                                                    className={styles.sidebar__history__chat__delete} />
                                            </span>
                                        ))}
                                    </>
                                )}
                                {(filteredChats.earlier.length > 0 &&
                                    <>
                                        <span className={styles.sidebar__history__date}>Ранее</span>
                                        {filteredChats.earlier.map((chat, index) => (
                                            <span
                                                onClick={() => (setCurrentChat(chat.id))}
                                                className={styles.sidebar__history__chat}
                                                key={index}>
                                                <span>{chat.title}</span>
                                                <img
                                                    onClick={(e) => {
                                                        e.preventDefault();
                                                        deleteChat(chat.id)
                                                    }}
                                                    src={DeleteIcon}
                                                    className={styles.sidebar__history__chat__delete} />
                                            </span>
                                        ))}
                                    </>
                                )}
                            </motion.div>

                        </>
                    )
                }

                <footer className={styles.sidebar__footer}>
                    <motion.div
                        animate={{
                            flexDirection: isCollapsed ? 'column' : 'row',

                        }}
                        onClick={() => createChat("New chart")}
                        transition={{ duration: 0.3 }}
                        className={styles.sidebar__footer__icons}
                    >
                        <motion.img
                            style={{
                                width: "30px",
                                height: "30px",
                                paddingRight: isCollapsed ? "5px" : ''
                            }}
                            onClick={handleOpenSettings}
                            src={SettingsIcon}
                            whileHover={{ scale: 1.1 }}
                            className={`${styles.sidebar__footer__icons__i} pb-[3px] `}
                        />
                        <motion.img
                            src={WarnIcon}
                            className={`${styles.sidebar__footer__icons__i}`}
                            onClick={handleOpenInfo}
                            whileHover={{ scale: 1.1 }}
                            style={{
                                paddingLeft: isCollapsed ? "2px" : ''
                            }}
                        />
                    </motion.div>
                </footer>

            </motion.div >
            {!isLargeScreen &&
                <div
                    className={styles.collapsed}
                    ref={el => { sideBarRefs.current[1] = el }}
                >
                    <span
                        className={styles.collapsed__logo}
                    >
                        SBER.AI
                    </span>
                    <div className={styles.collapsed__icons}>
                        <motion.img
                            src={FirstIcon}
                            className={`${styles.sidebar__header__icons__i} mt-[3px]`}
                            onClick={toggleSidebar}
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.95 }}
                        />
                        <motion.img
                            src={SecondIcon}
                            onClick={handleChatDialog}
                            className={`${styles.sidebar__header__icons__i}`}
                            whileHover={{ scale: 1.1 }}
                        />
                    </div>
                </div>
            }

            {
                infoPopUpVisible &&
                <InfoPopup isOpen={infoPopUpVisible} closeModal={handleCloseInfo} />
            }

            {
                settingsPopUpVisible &&
                <SettingsPopUp isOpen={settingsPopUpVisible} closeModal={handleCloseSettings} iniType='SETTINGS' />
            }

            <Modal
                isOpen={chatDialog}
                onRequestClose={handleChatDialog}
                className={styles.modalContent}
                overlayClassName={styles.modalOverlay}
                ariaHideApp={false}
            >
                <h5 className={styles.modalTitle}>Создать новый чат</h5>
                <input
                    onChange={handleChangeChatValue}
                    value={chatDialogValue}
                    placeholder='Название чата'
                    type="text" className={styles.input} />
                <button className={styles.closeButton} onClick={crateFullChat}>Создать</button>
            </Modal>

        </>
    );
};

export default SideBar;