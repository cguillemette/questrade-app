import { Account, PerQuote } from '../../types';

import './Portfolio.css';

export default function Portfolio(props: {
  perQuote: PerQuote
}) {
  return renderNew(props.perQuote);
}

function renderQuotePrice(account: Account) {
  let fontColor = "grey"
  if (account.currentPrice < account.averageEntryPrice) fontColor = "red"
  if (account.currentPrice > account.averageEntryPrice) fontColor = "green"
  let price = account.currentPrice.toFixed(2)
  return (
    <span className={`price ${fontColor}`}>
      {price}$
    </span>
  )
}

function renderBalance(perQuote: PerQuote) {
  return Array.from(perQuote.keys()).map((key) => {
    let values = perQuote.get(key);
    if (!values) {
      return null;
    }
    return (
      <div key={key} className="stock-container">
        <div className="quote">{key}&nbsp;{renderQuotePrice(values[0])}</div>
        <div key={key}>{values.map(value => renderAccount(value))}</div>
      </div>
    )
  })
}

function renderAccount(account: Account) {
  let averageEntryPrice = account.averageEntryPrice.toFixed(2)
  let gainPercentage = (((account.currentPrice / account.averageEntryPrice) - 1) * 100).toFixed(2)
  let gainAmount = (((account.currentPrice / account.averageEntryPrice) - 1) * account.totalCost).toFixed(2) 
  let totalCost = account.totalCost.toFixed(2)
  return (
    <div key={`${account.symbolId}`} className="container-quote">
      <div className="quote-values-container">
        <div className="average-entry-price">{averageEntryPrice}$</div>
        <div className="gain-container">
          <div className="gain">{gainPercentage}%</div>
          <div className="gain">{gainAmount}$</div>
        </div>
        <div className="total-cost">{totalCost}$</div>
      </div>
    </div>
  )
}

function renderNew(perQuote: PerQuote) {
  return (
    <div className="text-light rounded-0">
      <div className="mt-2 mb-2">
        <h1 className="display-2 mb-3" style={{fontWeight: 300}}>
          <span style={{fontWeight: 600}}>
            <br className="v-block d-sm-none"/>
          </span>
          {renderBalance(perQuote)}
        </h1>
      </div>
    </div>
  )
}
