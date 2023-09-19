import React, { useContext } from 'react'
import { DataContext } from '../../App';
import ProductCard from '../Route/ProductCard/ProductCard';

function Personal_Family({filter}) {
    const {data}=useContext(DataContext);

    const filterData=  data && data.filter((i)=>i.casespec && i.casespec.toLowerCase() === filter.toLowerCase())

    console.log("filter",filterData);

  return (
    <div className='flex justify-center items-center my-[2rem] w-full'>
      {
        filterData.length === 0 ? <div className='text-[36px]'>
          No Data Found
        </div> :
        <div className='flex flex-col items-center'>
          <div className='mb-4'>
            <h2>{filter.toUpperCase()}</h2>
          </div>
          <div className='flex gap-[4rem] flex-wrap w-[80%] justify-center'>
        {
          filterData.map((i)=>{
            return <ProductCard val={i} key={i._id} />
          })
        }
        </div>
        {/* <ProductCard val={filterData[0]} key={filterData[0]._id} /> */}
        </div>
      }
    </div>
  )
}

export default Personal_Family