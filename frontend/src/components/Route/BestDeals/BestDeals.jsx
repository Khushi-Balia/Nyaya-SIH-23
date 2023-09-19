import React, { useEffect, useState } from "react";
import styles from "../../../styles/styles";
import { productData } from "../../../static/data"
import ProductCard from "../ProductCard/ProductCard";

const BestDeals = () => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    const d =productData && productData?.sort((a,b) => b.total_sell - a.total_sell); 
    const firstFive = d.slice(0, 5);
    setData(firstFive);
  }, []);
  

  return (
    <div>
      <div className={`${styles.section}`}>
        <div className={`${styles.heading}`}>
          <h1>Popular Providers</h1>
        </div>
        <div className="grid grid-cols-1 gap-[20px] md:grid-cols-2 md:gap-[25px] lg:grid-cols-4 lg:gap-[25px] xl:grid-cols-5 xl:gap-[30px] mb-12 border-0">
          {
           
              data && data.map((i) => <ProductCard data={i} />)
          }
        </div>
      </div>
    </div>
  );
};

export default BestDeals;