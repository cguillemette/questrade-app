import { Asset, Assets, PerQuote } from "../../types";

// Mock data
const asset1: Asset = {
  averageEntryPrice: 100.5,
  closedPnl: 0,
  closedQuantity: 0,
  currentMarketValue: 2200,
  currentPrice: 110,
  dayPnl: 0,
  isRealTime: true,
  isUnderReorg: false,
  openPnl: 0,
  openQuantity: 20,
  symbol: "AAPL",
  symbolId: 1,
  totalCost: 2010
};

const asset2: Asset = {
  averageEntryPrice: 75,
  closedPnl: 0,
  closedQuantity: 0,
  currentMarketValue: 600,
  currentPrice: 60,
  dayPnl: 0,
  isRealTime: true,
  isUnderReorg: false,
  openPnl: 0,
  openQuantity: 10,
  symbol: "GOOG",
  symbolId: 2,
  totalCost: 750
};

const asset3: Asset = {
  averageEntryPrice: 213,
  closedPnl: 0,
  closedQuantity: 0,
  currentMarketValue: 2050,
  currentPrice: 205,
  dayPnl: 0,
  isRealTime: true,
  isUnderReorg: false,
  openPnl: 0,
  openQuantity: 10,
  symbol: "MSFT",
  symbolId: 3,
  totalCost: 2130
};

const asset4: Asset = {
  averageEntryPrice: 105,
  closedPnl: 0,
  closedQuantity: 0,
  currentMarketValue: 3614.1,
  currentPrice: 120.47,
  dayPnl: 0,
  isRealTime: true,
  isUnderReorg: false,
  openPnl: 0,
  openQuantity: 30,
  symbol: "SHOP.TO",
  symbolId: 4,
  totalCost: 3150
};

const assets1: Assets = [asset1];
const assets2: Assets = [asset2];
const assets3: Assets = [asset3];
const assets4: Assets = [asset4];

export const perQuoteMock: PerQuote = new Map();

perQuoteMock.set("AAPL", assets1);
perQuoteMock.set("GOOG", assets2);
perQuoteMock.set("MSFT", assets3);
perQuoteMock.set("SHOP.TO", assets4);
