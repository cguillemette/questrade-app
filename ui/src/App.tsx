
import Cookies from 'js-cookie';
import { useEffect, useState } from 'react';
import './App.css';
import Portfolio from './components/Portfolio/Portfolio';
import { LoadingIndicator } from './components/LoadingIndicator/LoadingIndicator';
import { RedirectOnPrefix } from './components/RedirectOnPrefix';
import { RefreshButton } from './components/RefreshButton/RefreshButton';
import { Accounts, Asset, PerQuote } from './types';
import { clearCookies } from './utils/cookies';
// import { perQuoteMock } from './mock/perQuote/demo';

export default function App() {
  const [questradeLoginUrl, setQuestradeLoginUrl] = useState<string | null>(null);
  const [fetchedAccountsAtLeastOnce, setFetchedAccountsAtLeastOnce] = useState(false);
  const [isFetchingAccounts, setIsFetchingAccounts] = useState(false);
  const [perQuote, setPerQuote] = useState<PerQuote | null>(null);
  const [payload, setPayload] = useState<({ [x: string]: string; } | undefined)>({});

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    (async () => {
      try {
        const response = await fetch(`${API_URL}/api/questrade/login`);
        const data = await response?.json();
        setQuestradeLoginUrl(data?.url);
      } catch (e) {
        setQuestradeLoginUrl(null);
      }
    })();
  }, []);

  useEffect(() => {
    const accessToken = Cookies.get("access_token")

    let parsedHash = false;
    const fragment = window.location.hash.substring(1);
    let fragmentSplitted = fragment.split('&');
    let _payload = fragmentSplitted.map(function (f) {
      let pair = f.split("=");
      if (pair.length === 2) {
        parsedHash = true;
        return { [pair[0]]: pair[1] }
      }
    })
    if (!_payload) {
      return;
    }
    const filtered = _payload.filter(p => p !== undefined)
    const payload = filtered?.reduce((acc, curr) => Object.assign(acc, curr), {});
    if (payload && payload["expires_in"]) {
      payload['expires_at'] = Math.floor(parseInt(payload["expires_in"]) + new Date().getTime() / 1000 - 300).toString();
    }
    setPayload(payload);

    if (parsedHash) {
      window.location.hash = "";
    }
  }, []);

  const fetchAccounts = async () => {
    try {
      setIsFetchingAccounts(true);
      const response = await fetch(`${API_URL}/api/accounts`, {
        headers: {
          'Content-Type': 'application/json',
        },
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(payload),
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
  }, [payload])

  function renderAuthAction() {
    if (fetchedAccountsAtLeastOnce && !perQuote && questradeLoginUrl) {
      return <button style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 10,
      }} onClick={() => {
        window.location.href = questradeLoginUrl;
      }}><img width="75px" src="https://upload.wikimedia.org/wikipedia/en/thumb/d/d9/Questrade_logo.svg/1024px-Questrade_logo.svg.png" /><span>Login</span>
      </button>;
    }

    if (fetchedAccountsAtLeastOnce && perQuote) {
      return <button onClick={() => {
        clearCookies();
        window.location.reload();
      }}>Logout</button>;
    }
  }

  function renderRefresh() {
    if (fetchedAccountsAtLeastOnce && perQuote) {
      return <RefreshButton onRefresh={fetchAccounts} />
    }
  }

  function renderPortfolio() {
    if (fetchedAccountsAtLeastOnce && perQuote) {
      // Mock data to generate the demo screenshot in readme
      // return <Portfolio perQuote={perQuoteMock} />;
      return <Portfolio perQuote={perQuote} />;
    }
  }

  return (
    <div className="app">
      <RedirectOnPrefix to="http://127.0.0.1:6001" />
      <div style={{
        display: 'flex',
        gap: 10,
        marginBottom: '1rem'
      }}>
        {renderAuthAction()}
        {renderRefresh()}
      </div>
      <LoadingIndicator loading={isFetchingAccounts}>
        {renderPortfolio()}
      </LoadingIndicator>
    </div>
  )
}
