
import Cookies from 'js-cookie';
import { useEffect, useState } from 'react';
import './App.css';
import Portfolio from './components/Portfolio/Portfolio';
import { LoadingIndicator } from './components/LoadingIndicator/LoadingIndicator';
import { RedirectOnPrefix } from './components/RedirectOnPrefix';
import { RefreshButton } from './components/RefreshButton/RefreshButton';
import { Accounts, Asset, PerQuote } from './types';
import { clearCookies } from './utils/cookies';

export default function App() {
  const [questradeLoginUrl, setQuestradeLoginUrl] = useState<string | null>(null);
  const [fetchedAccountsAtLeastOnce, setFetchedAccountsAtLeastOnce] = useState(false);
  const [isFetchingAccounts, setIsFetchingAccounts] = useState(false);
  const [perQuote, setPerQuote] = useState<PerQuote | null>(null);

  useEffect(() => {
    (async () => {
      try {
        (async () => {
          const response = await fetch("http://127.0.0.1:6002/api/questrade/login");
          const data = await response?.json();
          setQuestradeLoginUrl(data?.url);
        })();
      } catch (e) {
        setQuestradeLoginUrl(null);
      }
    })();
  }, []); 

  useEffect(() => {
    const accessToken = Cookies.get("access_token")

    const fragment = window.location.hash.substring(1);
    let fragmentSplitted = fragment.split('&');
    fragmentSplitted.map(function(f) {
        let pair = f.split("=");
        if (pair.length === 2) {
            Cookies.set(pair[0], pair[1]);
        }
    })
  
    if (accessToken != Cookies.get("access_token")) {
        const expiresIn = Cookies.get("expires_in") || "1800";
        Cookies.set("expires_at", Math.floor(parseInt(expiresIn) + new Date().getTime() / 1000 - 300).toString());
    }
  }, []);

  const fetchAccounts = async () => {
    try {
      setIsFetchingAccounts(true);
      const response = await fetch("http://127.0.0.1:6002/api/accounts", {
        credentials: 'include'
      });
      const data = await response?.json();
      const accounts = new Map(Object.entries(data.accounts)) as Accounts;

      let perQuote: PerQuote = new PerQuote()
      for (const accountId of accounts.keys()) {
        let assets = accounts.get(accountId);
        assets?.forEach(asset => {
          let current = perQuote.get(asset.symbol) ?? new Array<Asset>();
          current.push(asset);
          perQuote.set(asset.symbol, current)
        })
      }
      setPerQuote(perQuote);
    } catch (e) {
      console.error(`Unexpected error ${e}`)
    } finally {
      setFetchedAccountsAtLeastOnce(true);
      setIsFetchingAccounts(false);
    }
  }


  useEffect(() => {
   fetchAccounts();
  }, [])

  function renderLoginLogout() {
    if (fetchedAccountsAtLeastOnce && perQuote === null && questradeLoginUrl) {
      return <button onClick={() => {
        window.location.href = questradeLoginUrl;
      }}>Login</button>;
    }

    if (fetchedAccountsAtLeastOnce && perQuote) {
      return <button onClick={() => {
        clearCookies();
      }}>Logout</button>;
    }
  }

  function renderRefreshButton() {
    if (fetchedAccountsAtLeastOnce && perQuote) {
      return <RefreshButton onRefresh={fetchAccounts} />
    }
  }

  function renderPortfolio() {
    if (fetchedAccountsAtLeastOnce && perQuote) {
      return <Portfolio perQuote={perQuote} />;
    }
  }
  
  return (
    <div className="App">
      <RedirectOnPrefix to="http://127.0.0.1:6001" />
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '2rem'
      }}>
        {renderLoginLogout()}
        {renderRefreshButton()}
      </div>
      <LoadingIndicator loading={isFetchingAccounts}>
        {renderPortfolio()}
      </LoadingIndicator>
    </div>
  )
}
