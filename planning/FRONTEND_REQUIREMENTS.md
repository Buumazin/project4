# Frontend Requirements & UI Specification

## Technology Stack
- **Framework**: Next.js 14+ with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit or Zustand
- **HTTP Client**: fetch or axios
- **Real-time Data**: Server-Sent Events (native EventSource)
- **Charts**: Recharts or Chart.js for visualizations
- **Heatmap**: Treemap from Recharts or D3
- **Build**: Next.js static export (`output: 'export'`)

## Visual Design

### Color Palette
```
Primary Blue: #209dd7
Accent Yellow: #ecad0a
Submit Purple: #753991
Dark Background: #0d1117 or #1a1a2e
Text Gray: #c9d1d9
Border Gray: #30363d
Success Green: #238636
Alert Red: #da3633
```

### Theme
- Bloomberg-terminal inspired
- Dark mode (no light mode)
- Data-dense, professional
- Real-time visual feedback (price flashes)
- Minimal animations (focused on function)

## Main Pages

### Dashboard (/)
Homepage showing complete trading overview:
- Header with connection status
- Price grid (watchlist)
- Portfolio summary
- Positions table
- Chat interface (sidebar or modal)

## Key Components

### 1. Header
- Logo / App name
- Connection status indicator
  - Green: Connected (prices updating)
  - Yellow: Reconnecting
  - Red: Disconnected
- Current time
- Current portfolio value
- Cash balance

### 2. Price Grid (Watchlist)
```
Display default 10 tickers in grid:
- Ticker
- Current price
- Price change ($)
- Percent change (%)
- Small sparkline chart (progressively filled)

Visual feedback:
- Green background flash on uptick (+500ms fade)
- Red background flash on downtick (+500ms fade)
- Clickable to view detailed chart
```

Tickers:
```
Default: AAPL, GOOGL, MSFT, TSLA, AMZN, 
         NFLX, META, NVDA, JPM, XOM
```

### 3. Detailed Price Chart
When user clicks on a ticker:
- Large price chart (line or candlestick)
- Time range selector (1D, 5D, 1M, 3M, 1Y)
- Buy/Sell buttons
- Price statistics

### 4. Portfolio Visualization
- **Treemap Heatmap**:
  - Each box = one position
  - Size = position value ($)
  - Color = unrealized profit/loss
    - Dark green: +30% or better
    - Light green: +10% to +30%
    - Gray: -10% to +10%
    - Light red: -10% to -30%
    - Dark red: -30% or worse
  - Hover shows full details

- **P&L Chart**:
  - Line chart of total portfolio value over time
  - Starting at $10,000
  - Updates in real-time
  - Shows daily high/low

### 5. Positions Table
Responsive table showing:
| Column | Data |
|--------|------|
| Ticker | Symbol |
| Quantity | Current holdings |
| Avg Cost | Cost basis per share |
| Price | Current price |
| Value | Position value |
| P&L ($) | Profit/loss in dollars |
| P&L (%) | Profit/loss percentage |

Actions:
- Click to expand position details
- Sell all button
- Reduce position button

### 6. Chat Interface
- Chat panel (sidebar on desktop, modal on mobile)
- Message history (scrollable)
- Input field with send button
- Suggestions under input:
  - "Analyze portfolio"
  - "What should I trade?"
  - "Best performers"

Message format:
- User messages: blue, right-aligned
- Assistant messages: gray, left-aligned
- Trading suggestions highlighted with Execute button

### 7. Trade Execution Modal
When user buys/sells:
- Ticker, current price, quantity input
- Total cost calculation
- Confirmation button
- Success/error message

### 8. Connection Status
Small indicator showing:
- Real-time data connection status
- Last update timestamp
- Reconnect button if disconnected

## Responsive Design

### Desktop (>1024px)
- 3-column layout
- Watchlist grid (left): 5 columns × 2 rows
- Chart (center): Large detailed view
- Portfolio (right): Treemap + P&L + positions

### Tablet (768px - 1024px)
- 2-column layout, stacked views
- Watchlist: 3 columns
- Chart and Portfolio stack vertically

### Mobile (<768px)
- Single column, full-width
- Watchlist: 1-2 columns
- Tap to expand sections
- Chat in modal

## Data Flows

### Real-time Price Updates
```
1. Frontend connects to /api/stream/prices
2. Receives SSE updates every ~500ms
3. Updates in-memory price cache
4. Re-renders affected components
5. Shows price flash animation (+500ms fade)
6. Appends to sparkline data array
```

### Portfolio Updates
```
1. User executes trade (buy/sell)
2. POST to /api/trades/{buy|sell}
3. Backend fills order at current price
4. Response includes new position
5. Frontend updates cash balance
6. Updates positions table
7. Updates treemap
8. Appends to P&L chart
```

### Chat Interaction
```
1. User types message and hits send
2. POST to /api/chat with message
3. Backend queries portfolio
4. Calls Cerebras LLM
5. Returns analysis + trade suggestions
6. Frontend displays message + suggested trades
7. User can execute suggested trades
```

## Performance Considerations

- **Initial load**: Lazy load charting library
- **Real-time updates**: Use react hooks for efficient re-renders
- **Data caching**: Keep price cache in client state
- **Bundle size**: Tree-shake Recharts to include only charting components needed
- **Mobile**: Consider simpler chart (smaller bundle)

## Styling Approach

Use Tailwind CSS with custom configuration:
```
- Custom colors (blue, yellow, purple, grays)
- Dark theme as default
- No light theme variant
- Consistent spacing scale
- Smooth transitions (200ms)
- Focus states for accessibility
```

## Accessibility

- Semantic HTML
- ARIA labels for dynamic content
- Keyboard navigation
- Color contrast (WCAG AA)
- Readable font sizes
- Tab order logical

## Testing

- Jest unit tests for components
- React Testing Library for integration tests
- Playwright for E2E tests including SSE

## Build & Deployment

- Next.js static export (`output: 'export'`)
- Output directory: `out/`
- All assets: `out/` directory
- No server-side rendering needed
- Served by FastAPI as static files

## File Structure

```
frontend/
├── package.json
├── next.config.js      # Static export config
├── tsconfig.json
├── postcss.config.js   # Tailwind config
├── tailwind.config.ts
├── src/
│   ├── pages/
│   │   ├── index.tsx   # Main dashboard
│   │   ├── _app.tsx    # App wrapper
│   │   └── _document.tsx # HTML template
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── PriceGrid.tsx
│   │   ├── DetailChart.tsx
│   │   ├── Portfolio.tsx
│   │   ├── Heatmap.tsx
│   │   ├── PositionsTable.tsx
│   │   ├── Chat.tsx
│   │   ├── TradeModal.tsx
│   │   └── ConnectionStatus.tsx
│   ├── hooks/
│   │   ├── useMarketData.ts
│   │   ├── usePortfolio.ts
│   │   └── useChat.ts
│   ├── lib/
│   │   ├── api.ts
│   │   └── types.ts
│   └── styles/
│       └── globals.css
└── __tests__/
    └── [component tests]
```

## Success Criteria

- ✅ Builds without errors with Next.js static export
- ✅ All components render correctly
- ✅ Real-time data binding with SSE works
- ✅ Price flashes animate correctly
- ✅ Responsive on desktop/tablet/mobile
- ✅ Professional dark theme applied
- ✅ Chat interface fully functional
- ✅ Portfolio visualizations clear and accurate
- ✅ No console errors in browser
- ✅ Performance acceptable (< 2s load time)
