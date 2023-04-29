import React, {useEffect, useState} from 'react';
import {API_all_items, APICategories} from "../api";

const Items = () => {
    const [currentPage, setCurrentPage] = useState(1)
    const [items, setItems] = useState(null)
    // const [totalItemsCount, setTotalItemsCount] = useState(null)
    useEffect(() => {
        API_all_items(currentPage).then(r => {
            setItems(r.results)
            // setTotalItemsCount(r.count)
        })
    }, [currentPage])
    let pages = [1,2,3,4,5,6];
    return (
        <div className="cards">
            {items?.map(item => <div key={item.id} className="card">
                    <a style={{"textDecoration": "none"}} href="#">
                        <img src={item.photo} alt="Avatar" width="200"/>
                        <div className="container">
                            <h4><b>{item.name} {item.model}</b></h4>
                            <p>Architect & Engineer</p>
                        </div>
                    </a>
                </div>
            )}
            <div>
              {pages?.map(page => <div key={page} className="pagination">
                    <button onClick={()=>setCurrentPage(page)} className={page === currentPage?"active": ""}>{page}</button>
                </div>
            )}
            </div>


        </div>
    );
};

export default Items;