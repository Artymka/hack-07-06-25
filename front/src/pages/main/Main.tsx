import styles from './main.module.scss'
import Chat from "../../widgets/chat"
import SideBar from "../../widgets/sideBar"
import { useRef } from 'react'


const MainPage = () => {
    const sideBarRefs = useRef<(HTMLDivElement | null)[]>([null, null]);

    // const { chats } = useChatStore()


    const collapseFunction = (e: MouseEvent) => {
        if (sideBarRefs.current[0] && !sideBarRefs.current[0].contains(e.target as Node)) {
            if (sideBarRefs.current[1] && !sideBarRefs.current[1].contains(e.target as Node)) {
                return true;
            }
        }
        return false;
    }

    return (
        <div className={styles.page}>

            <SideBar testMode={true} sideBarRefs={sideBarRefs} closeFunction={collapseFunction} />
            <Chat />
        </div>
    )
}
export default MainPage