import { Account, PerQuote } from '../../types';
import './Portfolio.css';

export default function Portfolio(props: {
  perQuote: PerQuote
}) {
  return renderNew(props.perQuote);
}

function renderQuantity(account: Account) {
  return (
    <div className={`quantity`}>
      x {account.openQuantity}
    </div>
  )
}

function resolveColor(account: Account) {
  let fontColor = "grey"
  if (account.currentPrice < account.averageEntryPrice) {
    fontColor = "red";
  }
  if (account.currentPrice > account.averageEntryPrice) {
    fontColor = "green";
  }
  return fontColor;
}

function renderStatus(account: Account) {
  return (
    <div className={`stock-price-status ${resolveColor(account)}`}>
      ·
    </div>
  )
}

function renderQuotePrice(account: Account) {
  let price = account.currentPrice.toFixed(2)
  return (
    <div className={`stock-price top`}>
      {price}$
    </div>
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
        <div className="quote-container">
          <div className="quote">
            {key}
          </div>
          <div className="status-container">
            {renderQuantity(values[0])}
            {renderStatus(values[0])}
          </div>
        </div>
        <div key={key}>
          {values.map(value => renderAccount(value))}
        </div>
      </div>
    )
  })
}

function renderAccount(account: Account) {
  let averageEntryPrice = account.averageEntryPrice.toFixed(2)
  let gainPercentage = (((account.currentPrice / account.averageEntryPrice) - 1) * 100).toFixed(2)
  let gainAmount = (((account.currentPrice / account.averageEntryPrice) - 1) * account.totalCost).toFixed(2) 
  let currentMarketValue = account.currentMarketValue.toFixed(2)
  let totalCost = account.totalCost.toFixed(2)
  return (
    <div key={`${account.symbolId}`} className="container-quote">
      <div className="quote-values-container">
        <div className="gain-container">
          {renderQuotePrice(account)}
          <div className="average-entry-price bottom">{averageEntryPrice}$</div>
        </div>
        <div className="gain-container">
          <div className="gain top">{gainPercentage}%</div>
          <div className="gain bottom">{gainAmount}$</div>
        </div>
        <div className="gain-container">
          <div className="total-cost top">{currentMarketValue}$</div>
          <div className="total-cost bottom">{totalCost}$</div>
        </div>
      </div>
    </div>
  )
}

function renderNew(perQuote: PerQuote) {
  return (
    <div className="balance-container">
      {renderBalance(perQuote)}
    </div>
  )
}
