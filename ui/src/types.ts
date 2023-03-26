export class PerQuote extends Map<string, Array<Asset>>{ };

export type Assets = Array<Asset>;

export type Accounts = Map<string, Assets>;

export interface Account {
    averageEntryPrice: number,
    closedPnl: number,
    closedQuantity: number,
    currentMarketValue: number,
    currentPrice: number,
    dayPnl: number,
    isRealTime: boolean,
    isUnderReorg: boolean,
    openPnl: number,
    openQuantity: number,
    symbol: string,
    symbolId: number,
    totalCost: number
}

export interface Asset {
    averageEntryPrice: number,
    closedPnl: number,
    closedQuantity: number,
    currentMarketValue: number,
    currentPrice: number,
    dayPnl: number,
    isRealTime: boolean,
    isUnderReorg: boolean,
    openPnl: number,
    openQuantity: number,
    symbol: string,
    symbolId: number,
    totalCost: number
}
