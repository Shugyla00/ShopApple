import React from 'react';

const CategoryItems = ({items, cat}) => {
    let sorted_items = items?.filter(item => item.category === cat)
    return (
         <div className="cards">
            {sorted_items?.map(item => <div key={item.id} className="card">
                    <a style={{"textDecoration": "none"}} href="#">
                        <img src={item.photo} alt="Avatar" width="200"/>
                        <div className="container">
                            <h4><b>{item.name} {item.model}</b></h4>
                            <p>Architect & Engineer</p>
                        </div>
                    </a>
                </div>
            )}
        </div>
    );
};

export default CategoryItems;