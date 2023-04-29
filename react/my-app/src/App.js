import {useEffect, useState} from "react";
import {API_category_items, APICategories} from "./api";
import Items from "./components/Items";
import CategoryItems from "./components/CategoryItems";



function App() {
    const [categories, setCategories] = useState(null)
    const [category, setCategory] = useState(null)
    const [catItems, setCatItems] = useState(null)
    useEffect(()=>{
        APICategories().then(r => setCategories(r.results))
        API_category_items().then(r =>setCatItems(r))
    },[])
    return (
        <table className="table-page">
            <tr>
                <td>
                    <div className="header">
                        <ul id="mainmenu" className="mainmenu">
                            <li><a href="#">Home</a></li>
                            <li><a href="#">news</a></li>
                            <li><a href="#">contact</a></li>
                        </ul>
                        <div className="clear"></div>
                    </div>


                    <table className="table-content" border={0} cellPadding="0" cellSpacing="0">
                        <tr>
                            <td valign={"top"} className="left-chapters">
                                <ul id="leftchapters">
                                    <li className="selected" onClick={()=>setCategory(null)}><a href="#">Все категории</a></li>
                                    {categories?.map(cat => <li onClick={()=>setCategory(cat.id)} key={cat.id}>{cat.name}</li>)}
                                </ul>
                            </td>

                            <td valign={"top"} className="content">
                                <div className="container">
                                    {category?<CategoryItems items={catItems} cat={category}/>:<Items/>}
                                </div>

                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td valign="top">
                    <div id="footer">
                    </div>
                </td>
            </tr>
        </table>
    );
}

export default App;
