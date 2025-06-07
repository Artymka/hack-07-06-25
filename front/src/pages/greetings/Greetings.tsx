import { useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import styles from './greetings.module.scss';
import useMediaQuery from '../../hooks/useMatchMedia';
import { registerFetch } from '../../api/auth';
import useAuthStore from '../../store/auth';

interface FormData {
    email: string;
    password: string;
    confirmPassword: string;
}


const Greeting: React.FC = () => {
    const isLargeScreen = useMediaQuery('(min-width: 1024px)');
    const navigate = useNavigate();
    const { login } = useAuthStore();
    const { register, handleSubmit, formState: { errors }, watch } = useForm<FormData>();

    const handleNoAuth = () => navigate('/');
    const handleToAuth = () => navigate('/auth');

    const onSubmit = async (data: FormData) => {
        const username = data.email;
        const password = data.password
        const response = await registerFetch(username, password);
        if (response) login(username, password)
        navigate('/auth')
    };

    return (
        <div className={styles.page}>
            <div className={styles.page__block_1}>
                <div className={styles.page__block_1__content}>
                    <h2>Зарегистрируйтесь в SBER.AI</h2>
                    <p>Вы можете зарегистрироваться для синхронизации рабочих чатов</p>
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

                        <input
                            className={styles.page__block_1__content__input}
                            type='password'
                            placeholder='Подтвердите пароль'
                            {...register('confirmPassword', {
                                required: 'Это поле обязательно',
                                validate: (value) => value === watch('password') || 'Пароли не совпадают'
                            })}
                        />
                        {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}

                        <button
                            className={styles.page__block_1__content__form__button}
                            type='submit'
                        >
                            Зарегистрироваться
                        </button>
                    </form>
                    <span
                        onClick={handleToAuth}
                        className={styles.page__block_1__content__link}
                    >
                        Уже есть аккаунт? Войти
                    </span>
                    <button
                        onClick={handleNoAuth}
                        className={styles.page__block_1__content__button_dis}
                    >
                        Продолжить без авторизации
                    </button>
                </div>
            </div>
            {isLargeScreen &&
                <div className={styles.page__block_2}>
                    <h2>Универсальный помощник для анализа муниципальных данных</h2>
                    <h1>SBER.AI</h1>
                </div>
            }
        </div>
    );
};

export default Greeting;
