
# Modular Real-Time Crypto Trading Framework

## System Overview

This document outlines the architecture and component flow for a single-user, modular crypto trading system using Coinbase. The system supports live strategy configuration, real-time OHLCV streaming, modular strategy execution, and automated trade placement.

## System Goals

- Monitor selected crypto markets in near real-time.
- Support dynamic user-defined strategies with real-time config updates.
- Process signals via a multi-step strategy engine.
- Execute limit/sell orders on Coinbase.
- Avoid duplicate trades using a central trade manager.
- Stream data via Kafka and store history in TimescaleDB.
- Allow backtesting on up to 5 years of data.

## Mermaid Architecture Diagram


```mermaid
flowchart TD
    subgraph UI["Frontend (User Config)"]
        A1["Strategy + Params 
        (Symbols, Intervals)"]
    end

    subgraph Redis["Redis (Config Cache)"]
        A2["Store: strategy_config:user_123"]
    end

    subgraph Scheduler["Scheduler Service"]
        B1["Pull Config"]
        B2["Select Top-N Symbols"]
        B3["Publish to Candidates Queue"]
    end

    subgraph DataFetcher["Data Fetcher Service"]
        C1["Subscribe to Candidates"]
        C2["Fetch OHLCV from Coinbase"]
        C3["Stream to Kafka/Store in Timescale"]
    end

    subgraph SignalEngine["Signal Engine Service"]
        D1["Subscribe to OHLCV Stream"]
        D2["Check Trade Manager"]
        D3["Run Strategy Steps (1–4)"]
        D4["Emit Signal to Redis"]
    end

    subgraph TradeManager["Trade Manager"]
        E1["Track open trades"]
        E2["Enforce single-trade rule"]
    end

    subgraph TradingExecutor["Trading Executor"]
        F1["Subscribe to Signals"]
        F2["Send Order to Coinbase"]
        F3["Update Trade State"]
    end

    A1 --> A2
    A2 --> B1
    B1 --> B2 --> B3
    B3 --> C1 --> C2 --> C3
    C3 --> D1
    D1 --> D2 --> D3 --> D4
    D2 --> E1
    D3 --> E2
    D4 --> F1 --> F2 --> F3 --> E1

```


## Component Responsibilities

### Frontend UI
- Updates strategy config (intervals, fast/slow periods, assets).
- Publishes config to Redis for live sync.

### Redis
- Stores latest user strategy configuration (`strategy_config:user_123`).
- Used as central state for caching & config sharing.

### Scheduler
- Pulls config from Redis on interval.
- Selects top-N crypto symbols (e.g., by volume).
- Publishes candidate symbol list to Kafka or Redis Stream.

### Data Fetcher
- Subscribes to updated candidate symbols.
- Adjusts fetch targets dynamically.
- Pulls OHLCV from Coinbase.
- Streams candles to Kafka or TimescaleDB.

### Signal Engine
- Listens to OHLCV streams.
- Checks active trades via Trade Manager.
- Runs 4-step signal strategy.
- Emits signals to Redis.

### Trade Manager
- Tracks all open trades.
- Prevents strategy from re-running on held positions.
- Maintains open trade registry (symbol, entry price, direction).

### Trading Executor
- Listens for signals from Redis/Kafka.
- Places real orders through Coinbase API.
- Updates Trade Manager upon fill/close.

### TimescaleDB
- Stores all raw OHLCV data for future backtesting.
