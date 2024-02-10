import { Asset, PerQuote } from '../../types';
import './Portfolio.css';

export default function Portfolio(props: {
  perQuote: PerQuote
}) {
  return renderNew(props.perQuote);
}

function renderQuantity(asset: Asset) {
  return (
    <div className={`quantity`}>
      x {asset.openQuantity}
    </div>
  )
}

function resolveColor(asset: Asset) {
  let fontColor = "grey"
  if (asset.currentPrice < asset.averageEntryPrice) {
    fontColor = "red";
  }
  if (asset.currentPrice > asset.averageEntryPrice) {
    fontColor = "green";
  }
  return fontColor;
}

function renderStatus(asset: Asset) {
  return (
    <div className={`stock-price-status ${resolveColor(asset)}`}>
      ·
    </div>
  )
}

function renderQuotePrice(asset: Asset) {
  let price = asset.currentPrice.toFixed(2)
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

function renderAccount(asset: Asset) {
  let averageEntryPrice = asset.averageEntryPrice.toFixed(2)
  let gainPercentage = (((asset.currentPrice / asset.averageEntryPrice) - 1) * 100).toFixed(2)
  let gainAmount = (((asset.currentPrice / asset.averageEntryPrice) - 1) * asset.totalCost).toFixed(2) 
  let currentMarketValue = asset.currentMarketValue.toFixed(2)
  let totalCost = asset.totalCost.toFixed(2)
  return (
    <div key={`${asset.symbolId}`} className="container-quote">
      <div className="quote-values-container">
        <div className="gain-container">
          {renderQuotePrice(asset)}
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
