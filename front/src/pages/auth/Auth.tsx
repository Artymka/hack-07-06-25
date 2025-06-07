import { useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import type { SubmitHandler } from 'react-hook-form';
import styles from './auth.module.scss';
import useMediaQuery from '../../hooks/useMatchMedia';
import { loginFetch } from '../../api/auth';
import useAuthStore from '../../store/auth';

interface FormData {
    email: string;
    password: string;
}

const Greeting: React.FC = () => {
    const isLargeScreen = useMediaQuery('(min-width: 1024px)');
    const navigate = useNavigate();
    const { login } = useAuthStore();
    const { register, handleSubmit, formState: { errors } } = useForm<FormData>();
    const handleNoAuth = () => navigate('/');
    const handleToReg = () => navigate('/register');

    const onSubmit: SubmitHandler<FormData> = async (data) => {
        const username = data.email;
        const password = data.password
        await loginFetch(username, password);
        login(username, password)
        navigate('/')
    };

    return (
        <div className={styles.page}>
            <div className={styles.page__block_1}>
                <div className={styles.page__block_1__content}>
                    <h2>Войдите в SBER.AI</h2>
                    <p>Вы можете зайти для синхронизации рабочих чатов</p>
                    <form className={styles.page__block_1__content__form} onSubmit={handleSubmit(onSubmit)}>
                        <input
                            className={styles.page__block_1__content__input}
                            placeholder='Почта'
                            {...register('email', { required: 'Это поле обязательно' })}
                        />
                        {errors.email && <span>{errors.email.message}</span>}

                        <input
                            className={styles.page__block_1__content__input}
                            type='password'
                            placeholder='Введите пароль'
                            {...register('password', { required: 'Это поле обязательно' })}
                        />
                        {errors.password && <span>{errors.password.message}</span>}
                        <button
                            className={styles.page__block_1__content__form__button}
                            type='submit'
                        >
                            Войти
                        </button>
                    </form>
                    <span
                        onClick={handleToReg}
                        className={styles.page__block_1__content__link}
                    >
                        Нет аккаунта? Зарегистрироваться
                    </span>
                    <button
                        onClick={handleNoAuth}
                        className={styles.page__block_1__content__button_dis}
                    >
                        Продолжить без авторизации
                    </button>
                </div>
            </div>
            {isLargeScreen && (
                <div className={styles.page__block_2}>
                    <h2>Универсальный помощник для анализа муниципальных данных</h2>
                    <h1>SBER.AI</h1>
                </div>
            )}
        </div>
    );
};

export default Greeting;
