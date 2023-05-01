import './Dashboard.css';
import { useNavigate } from 'react-router-dom';

function Dashboard({pages, pkey}) {

    const navigate = useNavigate();

    function handleClick(event) {
        const path = event.target.closest('div').getAttribute('pkey');
        navigate(path);
    };

    return (
        <div className="dashboard-body">
            <div className="dashboard-header">Dashboard</div>
            <div className="dashboard-items">
                {pages.map(item => (
                    <>
                        <div className={pkey === item.key ? "dashboard-item opened" : "dashboard-item"} style = {{textOverflow: 'ellipsis', whiteSpace: 'nowrap'}} pkey={item.key} onClick={handleClick}>
                            <p>{item.name}</p>
                        </div>
                        {item.subpages.map(subitem => (
                            <div className={pkey === subitem.key ? "dashboard-subitem opened" : "dashboard-subitem"} pkey={subitem.key} onClick={handleClick}>
                                <p>{'- ' + subitem.name}</p>
                            </div>
                        ))}
                    </>
                ))}
            </div>
        </div>
    )
}

export default Dashboard;