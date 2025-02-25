import LoadingGifIcon from '../assets/loading/loading_icon.gif';
import './css/LoadingTask.css';

const LoadingTask = () => {
    return (
        <div className='loading__background--task'>
            <img className='loading__backgound-task--img' src={LoadingGifIcon} alt="hih" />
        </div>
    );
};

export default LoadingTask;