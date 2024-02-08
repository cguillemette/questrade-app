import { Account, PerQuote } from './types';

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
      <style>{`
      .stock-container {
        padding-bottom: 20px;
      }
      .price {
        font-size: 75%;
      }
      .red {
        color: #ff3939e6;
      }
      .green {
        color: #46da46e6;
      }
      .grey {
        color: #cccccc;
      }
      `}</style>
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
        <style>{`
          .stock-container {
            padding-bottom: 20px;
          }
        `}</style>
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
      <style>{`
        .container-quote {
          padding-bottom: 0px;
        }
        .quote-container {
          font-size: 1rem;
        }
        .quote-values-container {
          display: flex;
        }
        .gain-container {
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .id {
          font-size: 30%;
        }
        .quote {
          padding-right: 10px;
          font-weight: bold;
          font-size: 100%;
          line-height: initial;
        }
        .gain {
          padding-left: 10px;
          padding-right: 10px;
          font-size: 35%;
        }
        .average-entry-price {
          padding-left: 10px;
          padding-right: 10px;
          font-size: 90%;
        }
        .total-cost {
          padding-left: 20px;
          font-size: 90%;
        }
      `}</style>
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
        <style>{`
          .display-2  {
            text-shadow: 0 5px 10px rgba(0,0,0,0.3);
            color: rgba(255,255,255,0.9);
          }
          .lead {
            font-size: 3em;
            opacity: 0.7;
          }
          @media (max-width: 767px) {
            .display-2 {
              font-size: 3em;
              margin-bottom: 1em;
            }
            .lead {
              font-size: 1.5em;
            }
          }
        `}</style>
      </div>
    </div>
  )
}