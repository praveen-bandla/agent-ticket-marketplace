'use client';

import { useRef, useEffect, useState } from 'react';
import EmblaCarouselAutoplay from '@/components/EmblaCarouselAutoplay';
import EmblaCarouselAutoScroll from '@/components/EmblaCarouselAutoscroll';
import { EmblaOptionsType } from 'embla-carousel';
import { marked } from 'marked';


const getTagline = () => {
  const lines = [
    'What kind of experience are you craving?',
    'Pick your vibe. We’ll handle the tickets',
    'Ready to discover something amazing?'
  ]
  let i = Math.floor(Math.random() * lines.length);
  return lines[i];
};

const AUTOPLAY_OPTIONS: EmblaOptionsType = { loop: true }
const AUTOPLAY_SLIDE_COUNT = 4
const AUTOPLAY_SLIDES = Array.from(Array(AUTOPLAY_SLIDE_COUNT).keys())
const AUTOPLAY_TITLES = ['Jonas Brothers', 'Ed Sheeran Tickets', 'Lady Gaga Concert', 'Twice: K-Pop']

const AUTOSCROLL_OPTIONS: EmblaOptionsType = { loop: true }
const AUTOSCROLL_SLIDE_COUNT = 5
const AUTOSCROLL_SLIDES = Array.from(Array(AUTOSCROLL_SLIDE_COUNT).keys())
const AUTOSCROLL_TITLES = ['MJ - Michael Jackson', 'Harry Potter and the Cursed Child', 'Stranger Things: The First Shadow', 'Maybe Happy Ending', 'Wicked']

const AUTOSCROLL_OPTIONS_2: EmblaOptionsType = { loop: true }
const AUTOSCROLL_SLIDE_COUNT_2 = 5
const AUTOSCROLL_SLIDES_2 = Array.from(Array(AUTOSCROLL_SLIDE_COUNT_2).keys())
const AUTOSCROLL_TITLES_2 = ['MJ - Michael Jackson', 'Harry Potter and the Cursed Child', 'Stranger Things: The First Shadow', 'Maybe Happy Ending', 'Wicked']


export default function Home() {
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const initialHeight = useRef<number>(0);
  const chatRef = useRef<HTMLDivElement>(null);

  type Message = {
    role: string;
    content: string;
  };

  const [tagline, setTagline] = useState('');
  const [search_data, setSearchData] = useState<Message[]>([]);
  const [isChatting, setChatting] = useState(false);

  useEffect(() => {
    if (inputRef.current) {
      initialHeight.current = inputRef.current.scrollHeight;
    }
    setTagline(getTagline());

    inputRef.current!.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        search2();
      }
    });
  }, []);

  const autosize = () => {
    const el = inputRef.current;
    if (!el) return;

    setTimeout(() => {
      el.style.height = "";
      const newHeight = el.scrollHeight;

      if (newHeight > initialHeight.current) {
        el.style.height = newHeight + "px";
        wrapperRef.current?.classList.add("expand");
      } else {
        wrapperRef.current?.classList.remove("expand");
      }
    }, 0);
  };

  function sanitizeInput(input: string) {
    if (!input) return '';
    // Remove invisible control characters
    input = input.replace(/[\x00-\x1F\x7F]/g, '');
    // Escape HTML special chars
    input = input
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/'/g, '&quot;')
      .replace(/'/g, '&#x27;');
    // Trim and truncate if too long
    return input.trim().slice(0, 1024);
  }

  const search = async () => {
    let value = inputRef.current!.value;
    value = sanitizeInput(value);
    if (!value || value.length < 5 && value.length > 1024) { return; }

    setChatting(true);
    inputRef.current!.value = '';
    autosize();
    inputRef.current!.disabled = true;
    appendMessage('user', value);
    const agent_msg = await appendMessage('agent', 'Thinking...');

    let input: string | Message[] = search_data;
    input.push({ role: "user", content: value });
    
    // Send search query
    let data = await fetch('http://127.0.0.1:8000/buyer/intent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'true'
      },
      body: JSON.stringify({query: JSON.stringify(input)}),
    });
    let res = await data.json();
    let response = JSON.parse(res.at(-1)['content'].replace('```json', '').replace('```', ''));
    if ('question' in response) {
      let question = response['question'];
      agent_msg.innerHTML = question;
    } else {
      let tickets = response;
    }
    
    setSearchData(res);
    
    const container = chatRef.current!;
    container.scrollTop = container.scrollHeight;

    inputRef.current!.disabled = false;
  };

  const search2 = async () => {
    let value = sanitizeInput(inputRef.current!.value);
    if (!value) return;

    setChatting(true);
    appendMessage("user", value);

    let socket = new WebSocket("ws://127.0.0.1:8000/buyer/intent/ws");

    socket.onopen = () => {
      let payload = {
        query: [...search_data, { role: "user", content: value }]
      };
      socket.send(JSON.stringify(payload));
    };

    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data);

      if (msg.status === "parsing") {
        appendMessage("agent", "Analyzing your request...");
      }

      if (msg.phase === "extraction") {
        let response = JSON.parse(msg.data);
        if ("question" in response) {
          appendMessage("agent", response.question);
        }
      }

      if (msg.status === "filtering") {
        appendMessage("agent", "Filtering tickets...");
      }

      if (msg.phase === "final_tickets") {
        appendMessage("agent", "Here are the best matches:");
        console.log(msg.tickets);
      }
    };

    socket.onclose = () => {
      console.log("WebSocket closed");
    };
  };


  async function appendMessage(role='user', msg: string) {
    const container = chatRef.current!;
    const item = document.createElement('div');
    if (role === 'user') {
        item.classList.add('user-msg');
    }
    else {
        item.classList.add('agent-msg');
    }
    item.innerHTML = await marked.parse(msg);
    container.appendChild(item);
    container.scrollTop = container.scrollHeight;
    return item;
  }

  const clearChat = () => {
    setChatting(false); 
    setSearchData([]);
    inputRef.current!.value = '';
    inputRef.current!.disabled = false;
    chatRef.current!.innerHTML = "";
  }
  
  return (
    <div>
      <div className="header"></div>
      <main>
        <div className="search-wrapper">
          <div className="tagline">
            {tagline}
          </div>
          <div className={`chat-wrapper ${(isChatting) ? 'chat-expand': ''}`}>
            <div className="chat-log" ref={chatRef}></div>
            {(isChatting) 
              ? <svg className="icon close-icon" width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" onClick={() => clearChat()}>
                  <path id="Vector" d="M18 18L12 12M12 12L6 6M12 12L18 6M12 12L6 18" stroke="#000000" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              : null
            }
            <div className="search-box" id="input-wrapper" ref={wrapperRef}>
              <textarea name="prompt-textarea" id="search-input" placeholder="Share your vibe..." ref={inputRef} onInput={autosize} rows={1} autoCapitalize="none" autoCorrect="false" autoComplete="one-time-code" spellCheck="false" maxLength={1024} />
              <div className="icon" onClick={() => search2()}>
                <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M15.7955 15.8111L21 21M18 10.5C18 14.6421 14.6421 18 10.5 18C6.35786 18 3 14.6421 3 10.5C3 6.35786 6.35786 3 10.5 3C14.6421 3 18 6.35786 18 10.5Z" stroke="#000000" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            </div>
          </div>
        </div>
        <div className="section-wrapper">
          <EmblaCarouselAutoplay slides={AUTOPLAY_SLIDES} options={AUTOPLAY_OPTIONS} titles={AUTOPLAY_TITLES} />
          <EmblaCarouselAutoScroll slides={AUTOSCROLL_SLIDES} options={AUTOSCROLL_OPTIONS} speed={0.35} titles={AUTOSCROLL_TITLES} />
          <EmblaCarouselAutoScroll slides={AUTOSCROLL_SLIDES_2} options={AUTOSCROLL_OPTIONS_2} speed={0.5} titles={AUTOSCROLL_TITLES_2} />
        </div>
        <div className="cta-wrapper">
          <a href="">
            <span> See full lineup</span>
            <svg className="icon" width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M10 7L15 12L10 17" stroke="#000000" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </a>
        </div>
      </main>
      <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    </div>
  );
}
