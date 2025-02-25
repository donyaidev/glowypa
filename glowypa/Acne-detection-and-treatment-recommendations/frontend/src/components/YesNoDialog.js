import './css/YesNoDialog.css';

const YesNoDialog = ({notification, handleAccept}) => {
    return (
        <div className='yesNo__background'>
            <div className='yesNo__dialog--frame box--shadow-btn  ban--select'>
                <div className='yesNo__dialog'>
                    <div className='yesNo__dialog--title'>
                        <h1>Are you sure?</h1>
                    </div>
                    <div className='yesNo__dialog--content'>
                        <p>{notification}</p>
                    </div>
                    <div className='yesNo__dialog--button'>
                        <button className='yesNo__button--no box--shadow-btn' onClick={() => handleAccept(false)}>No</button>
                        <button className='yesNo__button--yes box--shadow-btn' onClick={() => handleAccept(true)}>Yes</button>
                    </div>
                </div>
            </div>
            
        </div>
    )
}    

export default YesNoDialog;