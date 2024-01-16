
import { useEffect, useState } from 'react'
import Cookies from 'js-cookie';

import './App.css'
import Accounts from './Accounts';
import { RedirectOnPrefix } from './components/RedirectOnPrefix';

export default function App() {
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
  
  return (
    <div className="App">
      <RedirectOnPrefix to="http://127.0.0.1:6001" />
      <Accounts />
    </div>
  )
}
