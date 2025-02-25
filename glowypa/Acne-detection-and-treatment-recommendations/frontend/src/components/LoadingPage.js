import LoadingGif from '../assets/loading/lowypa_loading.gif';
import './css/LoadingPage.css';
const LoadingPage = () => {
    return (
        <div className='loading__background'>
            <img className='loading__backgound--img' src={LoadingGif} alt="hih" />
        </div>
    );
};

export default LoadingPage;