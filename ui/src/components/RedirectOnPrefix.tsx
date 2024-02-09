import { useEffect } from 'react';

export const RedirectOnPrefix = (props: { to: string }) => {
  useEffect(() => {
    // We want to redirect from the ngrok to 127.0.0.1 otherwise the cookies won't passthrough to backend.
    const origin = window.origin;
    if (origin.indexOf('127.0.0.1') === -1) {
      window.location.href = `http://127.0.0.1:6001/${window.location.hash}`;
    }
  }, [props.to]);
};
