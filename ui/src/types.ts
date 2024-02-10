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

export type Assets = Array<Asset>;

export type Accounts = Map<string, Assets>;

export class PerQuote extends Map<string, Array<Asset>>{ };
