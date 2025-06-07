
import styles from './popup.module.scss'
import ReactModal from 'react-modal';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../ui/accordion';
import { memo, type FC } from 'react';
import useMediaQuery from '../../hooks/useMatchMedia';
interface Modal {
    isOpen: boolean
    closeModal: () => void
}
const Popup: FC<Modal> = memo(({ isOpen, closeModal }) => {
    const isLargeScreen = useMediaQuery('(min-width: 1024px)');

    return (
        <ReactModal
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
                    height: isLargeScreen ? "60%" : "70%",
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
            <Accordion
                type="single"
                collapsible
                className={`${styles.accordion} w-full`}
                defaultValue="item-1"
            >
                <AccordionItem value="item-1" className={styles.value}>
                    <h1 className={styles.logo}>QA</h1>
                    <AccordionTrigger className={styles.trigger}>Что умеет помощник?</AccordionTrigger>
                    <AccordionContent className="flex flex-col gap-[10px] text-balance">
                        <p>
                            Прорабатывать ваши идеи и предлагать свои, брать на себя рутинные задачи, помогать с учёбой, объяснять всё на свете простым языком, работать с файлами, переводить тексты на разные языки, творить, поддерживать советом и давать мнение со стороны, общаться на любые темы, развлекать взрослых и детей.
                        </p>
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem className={styles.value} value="item-2">
                    <AccordionTrigger className={styles.trigger}>Зачем нужна авторизация?</AccordionTrigger>
                    <AccordionContent className={styles.content}>
                        <p>
                            We offer worldwide shipping through trusted courier partners.
                            Standard delivery takes 3-5 business days, while express shipping
                            ensures delivery within 1-2 business days.
                        </p>
                        <p>
                            All orders are carefully packaged and fully insured. Track your
                            shipment in real-time through our dedicated tracking portal.
                        </p>
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem className={styles.value} value="item-3">
                    <AccordionTrigger className={styles.trigger}>Политика конфиденциальности</AccordionTrigger>
                    <AccordionContent className="flex flex-col gap-4 text-balance">
                        <p className='pt-4'>
                            We stand behind our products with a comprehensive 30-day return
                            policy. If you&apos;re not completely satisfied, simply return the
                            item in its original condition.
                        </p>
                        <p>
                            Our hassle-free return process includes free return shipping and
                            full refunds processed within 48 hours of receiving the returned
                            item.
                        </p>
                    </AccordionContent>
                </AccordionItem>
            </Accordion>
        </ReactModal>
    )
})

export default Popup;