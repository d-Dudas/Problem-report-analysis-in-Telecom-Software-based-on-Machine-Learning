// CSS files
import './Dashboard.css';

// Images, logos
import searchIcon from './images/search.png';

// React related
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

function Dashboard({pages, pkey, prontoList}) {

    const navigate = useNavigate();
    const [filter, setFilter] = useState("");

    function handleClick(event) {
        const path = event.target.closest('div').getAttribute('pkey');
        navigate(path);
    };

    function handleFilterChange(event) {
        const {value} = event.target;
        setFilter(value);
    }

    const checkFilterInObject = (obj, filter) => {
        const dashboard_item_name = obj.name;
        const pronto = prontoList.filter(p => p.problemReportId === dashboard_item_name);
        console.log(pronto[0]);
        const values = Object.values(pronto[0]);
        console.log(values);
      
        for (let i = 0; i < values.length; i++) {
            console.log(values[i]);
          if (('' + values[i]).toLowerCase().includes(filter.toLowerCase())) {
            return true;
          }
        }
      
        return false;
    };

    return (
        <div className="dashboard-body">
            <div className="dashboard-header">Dashboard</div>
            {pages.filter(item => item.subpages.length > 1).length <= 0 ? <></> :
                <div className="dashboard-search">
                    <div className="dashboard-search-input-div">
                        <img className="dashboard-search-icon" src={searchIcon} alt=''></img>
                        <input className='dashboard-search-input' placeholder='Search...' type = "text" name = "filter" value={filter} onChange={handleFilterChange} ></input>
                    </div>
                </div>
            }
            <div className="dashboard-items" style={pages.filter(item => item.subpages.length > 1).length <= 0 ? {translate: "1s", top: "12%"} : {top: "18%"}}>
                {pages
                    .map(item => (
                    <>
                        <div className={pkey === item.key ? "dashboard-item opened" : "dashboard-item"} style = {{textOverflow: 'ellipsis', whiteSpace: 'nowrap'}} pkey={item.key} onClick={handleClick}>
                            <p>{item.name}</p>
                        </div>
                        {item.subpages
                            .filter(subitem => checkFilterInObject(subitem, filter))
                            .map(subitem => (
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