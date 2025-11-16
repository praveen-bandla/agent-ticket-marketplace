# Agent-Based Ticket Marketplace

An event ticket marketplace featuring autonomous AI negotiators that conduct real-time price negotiations between buyers and sellers. Built with FastAPI backend, Next.js frontend, and LLM-powered intelligent agents.

## 🏗️ Architecture Overview

### System Architecture
```
Frontend (Next.js)     →  Backend API (FastAPI)     →  AI Negotiation Engine
    ↓                      ↓                          ↓
User Interface         RESTful Endpoints          Buyer/Seller Agents
Search & Chat          Data Management           LLM-Powered Negotiations
Carousel Display       Transaction Processing     Parallel Processing
```

### Core Components

**Backend API (`/api/`)**
- **FastAPI Framework**: High-performance async web framework
- **Pydantic Models**: Type-safe data validation and serialization
- **OpenRouter/GPT Integration**: LLM service abstraction for AI negotiations
- **JSON-Based Storage**: File-based data persistence for events, tickets, bids, transactions

**AI Negotiation System (`/api/core/`)**
- **Autonomous Agents**: Buyer and seller negotiators with distinct strategies
- **Parallel Processing**: AsyncIO-based concurrent negotiation execution
- **Market Intelligence**: Reference pricing and historical data analysis
- **Conflict Resolution**: Transaction resolver with priority-based allocation

**Frontend Application (`/app/`)**
- **Next.js 16**: React-based SSR framework with TypeScript
- **Embla Carousel**: Interactive event and venue showcases
- **Real-time Chat**: LLM-powered buyer intent extraction
- **Responsive Design**: Mobile-first UI with Tailwind CSS

## 🔧 Technical Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js 16 + TypeScript | Server-side rendering, type safety |
| **Backend** | FastAPI + Python 3.12 | High-performance async API |
| **AI/ML** | OpenRouter API + GPT-5-nano | LLM-powered negotiations |
| **Data** | JSON Files + Pydantic | Structured data with validation |
| **Async** | AsyncIO + ThreadPoolExecutor | Parallel negotiation processing |
| **Styling** | Tailwind CSS + CSS Modules | Component-based styling |

## 📁 Project Structure

```
agent-ticket-marketplace/
├── api/                          # Backend FastAPI application
│   ├── core/                     # Negotiation engine
│   │   ├── agents/               # AI negotiator implementations
│   │   │   ├── buyer_negotiator.py    # Buyer agent logic
│   │   │   └── seller_negotiator.py   # Seller agent logic
│   │   ├── market_negotiate.py   # Parallel negotiation coordinator
│   │   ├── negotiation.py        # Single negotiation orchestrator
│   │   ├── sub_market.py         # Market segmentation logic
│   │   └── transaction_resolver.py    # Conflict resolution & finalization
│   ├── data/                     # JSON data storage
│   │   ├── events.json           # Event catalog
│   │   ├── venues.json           # Venue information
│   │   ├── tickets.json          # Available ticket listings
│   │   ├── bids.json             # Buyer bids and preferences
│   │   ├── search_results.json   # Bid-ticket matching results
│   │   ├── transactions.json     # Completed negotiations with history
│   │   ├── buyer_id.json         # Buyer profiles
│   │   └── seller_id.json        # Seller profiles
│   ├── models/                   # Pydantic data models
│   │   ├── bid.py                # Bid data structure
│   │   ├── buyer.py              # Buyer profile model
│   │   ├── event.py              # Event details model
│   │   ├── seller.py             # Seller profile model
│   │   ├── ticket.py             # Ticket listing model
│   │   └── venue.py              # Venue specifications
│   ├── prompts/                  # LLM prompt templates
│   │   ├── buyer_negotiation.txt # Buyer agent instructions
│   │   └── seller_negotiation.txt # Seller agent instructions
│   ├── routers/                  # API route handlers
│   │   ├── buyer.py              # Buyer intent & search endpoints
│   │   └── ticket.py             # Ticket management endpoints
│   ├── services/                 # Business logic layer
│   │   ├── buyer_service.py      # Buyer operations
│   │   ├── event_service.py      # Event data management
│   │   ├── gpt_service.py        # OpenAI/GPT integration
│   │   ├── openrouter_client.py  # OpenRouter API wrapper
│   │   └── ticket_service.py     # Ticket CRUD operations
│   └── main.py                   # FastAPI app initialization
├── app/                          # Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx        # App shell and global styles
│   │   │   ├── page.tsx          # Main marketplace interface
│   │   │   ├── globals.css       # Global styling
│   │   │   └── css/              # Component-specific styles
│   │   │       ├── styles.css    # Main UI components
│   │   │       ├── embla_autoplay.module.css    # Event carousel
│   │   │       └── embla_autoscroll.module.css  # Venue carousel
│   │   └── components/
│   │       ├── EmblaCarouselAutoplay.tsx    # Event showcase carousel
│   │       └── EmblaCarouselAutoscroll.tsx  # Venue showcase carousel
│   ├── package.json              # Dependencies and scripts
│   ├── tsconfig.json             # TypeScript configuration
│   └── next.config.ts            # Next.js configuration
├── configs.py                    # Global configuration constants
└── configs.yaml                  # Environment configuration (empty)
```

## 🤖 AI Negotiation System

### Agent Architecture

**BuyerNegotiator (`/api/core/agents/buyer_negotiator.py`)**
- Represents buyer interests in ticket negotiations
- Maintains bid constraints (max price, quantity, seat preferences)
- Uses LLM-driven decision making for counter-offers
- Tracks negotiation history and price sensitivity

**SellerNegotiator (`/api/core/agents/seller_negotiator.py`)**
- Represents seller interests for ticket sales
- Enforces minimum price floors and sensitivity thresholds
- Leverages market reference values for strategic pricing
- Maintains seller reputation and transaction history

### Negotiation Flow

1. **Market Segmentation**: SubMarket organizes bids/tickets by event and seating group
2. **Parallel Processing**: MarketNegotiator runs concurrent negotiations using AsyncIO
3. **LLM Negotiations**: Agents exchange offers through structured prompt templates
4. **Agreement Tracking**: Full conversation histories preserved in transaction records
5. **Conflict Resolution**: TransactionResolver handles overlapping claims and priorities

### Key Features

- **Asynchronous Processing**: All negotiations run in parallel for optimal performance
- **Market Intelligence**: Reference pricing guides agent decision-making
- **Conversation Persistence**: Complete negotiation transcripts stored with transactions
- **Price Sensitivity**: Agents adjust strategies based on configured sensitivity levels
- **Round Limits**: Configurable maximum negotiation rounds (default: 5)

## 📊 Data Models

### Core Entities

**Event**
```python
event_id: str
name: str                    # "The Weeknd - Live at MSG"
venue: Venue                 # Associated venue object
date: str                    # ISO datetime string
reference_values: dict       # Market pricing by seat group
```

**Ticket**
```python
ticket_id: str
seller_id: str
event_id: str
group_id: str               # Seating section (FLOOR_PREMIUM, LOWER_BOWL, etc.)
quantity: int
price: float                # Listed price per ticket
min_price: float           # Seller's minimum acceptable price
sensitivity: str           # Price negotiation flexibility
immediate_sale: bool       # Skip negotiation if true
```

**Bid**
```python
bid_id: str
buyer_id: str
event_id: str
num_tickets: int
max_price: float           # Buyer's maximum acceptable price
price: float               # Initial bid price
allowed_groups: list[str]  # Acceptable seating sections
sensitivity_to_price: str  # Negotiation aggressiveness
```

**Transaction**
```python
bid_id: str
ticket_id: str
price: float               # Final negotiated price
quantity: int
buyer_id: str
seller_id: str
conversation_history: list # Complete negotiation transcript
```

### Market Structure

**Venue Seating Groups**
- **FLOOR_PREMIUM**: Front-row and VIP sections
- **LOWER_BOWL**: Mid-tier seating with good views  
- **UPPER_BOWL**: Budget-friendly upper-level seats
- **SIDE_GALLERY**: Side-view premium sections

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.12+ for backend
python --version

# Node.js 18+ for frontend  
node --version

# Environment variables
cp .env.example .env
```

### Backend Setup

```bash
# Navigate to project root
cd agent-ticket-marketplace

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install fastapi uvicorn python-dotenv pydantic openai requests

# Configure API keys in .env
OPENROUTER_API_KEY=your_openrouter_key_here

# Run development server
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd app

# Install dependencies
npm install

# Run development server
npm run dev

# Access at http://localhost:3000
```

### Configuration

**Environment Variables**
```bash
OPENROUTER_API_KEY=your_api_key    # Required for LLM negotiations
```

**Core Settings (`configs.py`)**
```python
MAX_ROUNDS = 5                      # Maximum negotiation rounds
BIDS_JSON = "api/data/bids.json"   # Bid storage location
TICKETS_JSON = "api/data/tickets.json"  # Ticket storage location
# ... additional file paths and settings
```

## 🔌 API Endpoints

### Buyer Endpoints

**POST `/buyer/intent`**
- Processes natural language buyer requests
- Extracts structured intent (event, quantity, price range, preferences)
- Returns clarifying questions for missing information
- Filters and ranks matching tickets

### Ticket Endpoints

**GET `/ticket/`**
- Lists all available ticket inventories
- Supports filtering by event, venue, price range

**POST `/ticket/create`**
- Creates new ticket listings
- Validates seller permissions and pricing

**DELETE `/ticket/{ticket_id}`**
- Removes tickets from marketplace
- Updates transaction records

## 🧪 Usage Examples

### Running Negotiations

```python
# Initialize market negotiator
from api.core.market_negotiate import MarketNegotiator
from api.models.event import Event
from api.core.sub_market import SubMarket

# Set up submarket for specific event/seating group
market_negotiator = MarketNegotiator()
event = Event.get_event_by_id("event_001")
submarket = SubMarket(event=event, group_id="FLOOR_PREMIUM")

# Run parallel negotiations
results = await market_negotiator.negotiate_pairs_submarket(submarket)

# Process successful agreements
from api.core.transaction_resolver import TransactionResolver
resolver = TransactionResolver(results)
resolver.process_transactions()
```

### Frontend Integration

```typescript
// Send buyer search request
const response = await fetch('http://127.0.0.1:8000/buyer/intent', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "Looking for 2 Weeknd tickets, prefer floor seats, budget up to $400"
  })
});

const negotiationResults = await response.json();
```

## 📈 Performance & Scalability

### Async Architecture Benefits

- **Parallel Negotiations**: All bid-ticket pairs negotiate simultaneously
- **Non-blocking I/O**: LLM API calls don't block other operations
- **Thread Pool Execution**: CPU-intensive tasks run in background threads
- **Memory Efficiency**: Lightweight coroutine-based concurrency

### Performance Metrics

- **Negotiation Throughput**: 10-50 concurrent negotiations (depends on LLM API limits)
- **Response Times**: 2-5 seconds for intent extraction, 5-30 seconds for negotiations
- **Data Storage**: JSON-based for development, easily scalable to databases
- **Logging**: Comprehensive request/response tracking for debugging

### Production Considerations

- **Database Migration**: Replace JSON files with PostgreSQL/MongoDB
- **Caching**: Redis for session management and frequent queries  
- **Rate Limiting**: API throttling for LLM service protection
- **Load Balancing**: Horizontal scaling with container orchestration
- **Monitoring**: Observability with metrics, logging, and tracing

## 🔒 Security & Privacy

- **Input Validation**: Pydantic models enforce data integrity
- **CORS Configuration**: Controlled cross-origin access
- **API Key Management**: Environment-based secret handling
- **Price Bounds**: Negotiation constraints prevent invalid transactions
- **Data Sanitization**: Input cleaning for XSS prevention

## 🚧 Development Roadmap

### Phase 1: Core Platform (Current)
- ✅ AI negotiation engine
- ✅ Parallel processing infrastructure  
- ✅ Frontend marketplace interface
- ✅ LLM-powered buyer intent extraction

### Phase 2: Enhanced Features
- [ ] Real-time WebSocket negotiations
- [ ] Advanced market analytics dashboard
- [ ] Multi-event bundle negotiations
- [ ] Machine learning price optimization

### Phase 3: Enterprise Features
- [ ] Multi-tenant marketplace support
- [ ] Advanced fraud detection
- [ ] Payment processing integration
- [ ] Mobile application development

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines

- **Type Safety**: Use TypeScript for frontend, Python type hints for backend
- **Testing**: Add unit tests for negotiation logic and API endpoints
- **Documentation**: Update README and inline docs for new features
- **Code Style**: Follow PEP 8 (Python) and Prettier (TypeScript)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built for HackNYU 26 - Showcasing the future of AI-powered marketplaces*

