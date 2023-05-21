// CSS files
import './Dashboard.css';

// Images, logos
import searchIcon from './images/search.png';
import loadFromDBIcon from './images/searchInDB.png';

// React related
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

function Dashboard({pages, setPages, pkey, prontoList, setProntoList}) {

    const navigate = useNavigate();
    const [filter, setFilter] = useState("");
    const [dbSearch, setDBSearch] = useState("");
    
    function handleClick(event) {
        const path = event.target.closest('div').getAttribute('pkey');
        if(path !== '/database'){
            navigate(path);
        }
    };

    function handleFilterChange(event) {
        const {value} = event.target;
        setFilter(value);
    }

    function handleDBSearch(event) {
        const {value} = event.target;
        setDBSearch(value);
    }

    const checkFilterInObject = (obj, filter) => {
        const dashboard_item_name = obj.name;
        const pronto = prontoList.filter(p => p.problemReportId === dashboard_item_name);
        const values = Object.values(pronto[0]);
      
        for (let i = 0; i < values.length; i++) {
          if (('' + values[i]).toLowerCase().includes(filter.toLowerCase())) {
            return true;
          }
        }
      
        return false;
    };

    const loadFromDB = () => {
        if(dbSearch !== '') {
            fetch('/search-in-db', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify(dbSearch)
              })
              .then(response => response.json())
              .then(data => {
                let auxProntoList = prontoList.slice();
                for(let i = 0; i < data.length; i++){
                    if(auxProntoList.filter(item => (item['problemReportId'] == data[i]['problemReportId'])) == 0) {
                        auxProntoList.push(data[i]);
                        let key = "/" + data[i].problemReportId;
                        let name = data[i].problemReportId;
                        pages[2].subpages.push({key: key, name: name});
                    }
                }
                setProntoList(auxProntoList);
                setPages(pages);
              })
              .catch(error => console.error(error));
        }
    }

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
            <div className="dashboard-items" style={pages.filter(item => item.subpages.length > 1).length <= 0 ? {translate: "1s", height: "82%"} : {height: "76%"}}>
                {pages
                    .filter(item => (item.name !== "From database" || item.subpages.length >= 1))
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
            <div className='dashboard-read-from-db-div'>
                <div className='dashboard-read-from-db-input-div'>
                    <input className='dashboard-read-from-db-input' placeholder='Search in database...' type = "text" name = "dbsearch" value={dbSearch} onChange={handleDBSearch} ></input>
                    <img className='dashboard-read-from-db-icon' src={loadFromDBIcon} alt='' onClick={loadFromDB}></img>
                </div>
            </div>
        </div>
    )
}

export default Dashboard;