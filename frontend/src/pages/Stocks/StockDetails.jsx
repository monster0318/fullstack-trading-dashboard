import HTMLReactParser from 'html-react-parser'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useGetStockDetailsQuery } from '../../services/stocksAPI'

import { StockBarChart } from '../../components'

const StockDetails = () => {
  const { stockSymbol } = useParams()

  const [stockDetails, setStockDetails] = useState()
  const [stockPrices, setStockPrices] = useState()

  const { data, isFetching } = useGetStockDetailsQuery(stockSymbol)

  const detailLabels = []
  
  useEffect(() => {
    setStockDetails(data?.details?.[0])
    setStockPrices(data?.prices)
  }, [isFetching])

  // useEffect(() => {
  //   setBars(barsData?.[`0`])
  //   console.log(barsData)
  // }, [isFetchingBars])


  return (
    <div className='mt-6'>
      <h1 className='text-2xl h-16 underline bold'>
        Stock Details: {stockDetails?.exchange} {'>>'} {stockDetails?.symbol} {'>>'} {stockDetails?.name}
      </h1>
      <div className='my-8'>
        {stockDetails && Object.keys(stockDetails).map((key, i) => (
          <div key={i}>
            <div>
              
            </div>
            <p>{key}: {stockDetails[key]}</p>
          </div>
        ))}
      </div>
        {!isFetching && stockPrices &&
          <StockBarChart prices={stockPrices} />
        }
    </div>
  )
}

export default StockDetails