import React, { useState } from "react";
import { Link } from "react-router-dom";
import styles from "../../../styles/styles";
import { AiFillStar, AiOutlineStar } from "react-icons/ai";


const ProductCard = ({ data }) => {

  const [click, setClick] = useState(false);
  const [open, setOpen] = useState(false);
  const d = data.name;
  const product_name = d.replace(/\s+/g, "-");

  return (
    <>
      <div className="w-full h-[370px] bg-white rounded-lg shadow-sm p-3 relative cursor-pointer">
        <div className="flex justify-end"></div>
        <Link to={`/product/${product_name}`}>
          <img
            src={data.image_Url[0].url}
            alt=""
            className="w-full h-[170px] object-contain"
          />
        </Link>
        <Link to="/">
          <h4 className={`${styles.shop_name}`}>
            {data.shop.name}
          </h4>
          </Link>
          <Link>
          <h4 className="pb-3 font-[500]">
            {data.name.length > 40 ? data.name.slice(0, 50) + "..." : data.name}
          </h4>

          <div className="flex">
            <AiFillStar className="mr-2 cursor-pointer" 
            color="#F6BA00"
            size={20}/>
            <AiFillStar className="mr-2 cursor-pointer"
            color="#F6BA00"
            size={20} />
            <AiFillStar className="mr-2 cursor-pointer" 
            color="#F6BA00"
            size={20}/>
            <AiFillStar className="mr-2 cursor-pointer"
            color="#F6BA00"
            size={20} />
            <AiOutlineStar className="mr-2 cursor-pointer"
            color="#F6BA00" 
            size={20}/>

          </div>
          </Link>
        </div>
    </>
  );
};

export default ProductCard;