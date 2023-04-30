import './Dashboard.css';

function Dashboard({pages, pkey}) {

    function handleClick(event) {
        const xkey = event.target.closest('.dashboard-item').getAttribute('pkey');
        console.log(xkey);
    };

    const dashboardItems = pages.map(item => (
        <>
            <div className={pkey === item.key ? "dashboard-item opened" : "dashboard-item"} style = {{textOverflow: 'ellipsis', whiteSpace: 'nowrap'}} pkey={item.key} onClick={handleClick}>
                <p>{item.name}</p>
            </div>
            {item.subpages.map(subitem => (
                <div className={pkey === subitem.key ? "dashboard-subitem opened" : "dashboard-subitem"} pkey={subitem.key}>
                    <p>{'- ' + subitem.name}</p>
                </div>
            ))}
        </>
    ))

    return (
        <div className="dashboard-body">
            <div className="dashboard-header">Dashboard</div>
            <div className="dashboard-items">
                {dashboardItems}
            </div>
        </div>
    )
}

export default Dashboard;