'use client';

import { useRef, useEffect, useState } from 'react';
import EmblaCarouselAutoplay from '@/components/EmblaCarouselAutoplay';
import EmblaCarouselAutoScroll from '@/components/EmblaCarouselAutoscroll';
import { EmblaOptionsType } from 'embla-carousel';


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
const AUTOPLAY_SLIDE_COUNT = 5
const AUTOPLAY_SLIDES = Array.from(Array(AUTOPLAY_SLIDE_COUNT).keys())

const AUTOSCROLL_OPTIONS: EmblaOptionsType = { loop: true }
const AUTOSCROLL_SLIDE_COUNT = 5
const AUTOSCROLL_SLIDES = Array.from(Array(AUTOSCROLL_SLIDE_COUNT).keys())

const AUTOSCROLL_OPTIONS_2: EmblaOptionsType = { loop: true }
const AUTOSCROLL_SLIDE_COUNT_2 = 5
const AUTOSCROLL_SLIDES_2 = Array.from(Array(AUTOSCROLL_SLIDE_COUNT_2).keys())


export default function Home() {
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const wrapperRef = useRef<HTMLDivElement | null>(null);
  const initialHeight = useRef<number>(0);

  type Message = {
    role: string;
    content: string;
  };

  const [search_data, setSearchData] = useState<Message[]>([]);

  useEffect(() => {
    if (inputRef.current) {
      initialHeight.current = inputRef.current.scrollHeight;
    }
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

  const search = async () => {
    const value = inputRef.current?.value;
    if (!value || value.length < 5 && value.length > 1024) { return; }

    let input: string | Message[] = search_data;
    if (search_data.length > 0) {
      input.push({ role: "user", content: value });
    }

    // Send search query
    let data = await fetch('http://127.0.0.1:8000/buyer/intent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'true'
      },
      body: JSON.stringify({query: input}),
    });
    let res = await data.json();
    let question = JSON.parse(res.at(-1)['content'].replace('```json', '').replace('```', ''))['question'];
    console.log(question);
    console.log('----------')
    setSearchData(res);
  };
  
  return (
    <div>
      <div className="header"></div>
      <main>
        <div className="search-wrapper">
          <div className="tagline">
            {getTagline()}
          </div>
          <div className="search-box" id="input-wrapper" ref={wrapperRef}>
            <textarea name="prompt-textarea" id="search-input" placeholder="Share your vibe..." ref={inputRef} onInput={autosize} rows={1} autoCapitalize="none" autoCorrect="false" autoComplete="one-time-code" spellCheck="false" maxLength={1024} />
            <div className="icon" onClick={() => search()}>
              <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15.7955 15.8111L21 21M18 10.5C18 14.6421 14.6421 18 10.5 18C6.35786 18 3 14.6421 3 10.5C3 6.35786 6.35786 3 10.5 3C14.6421 3 18 6.35786 18 10.5Z" stroke="#000000" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
          </div>
        </div>
        <div className="section-wrapper">
          <EmblaCarouselAutoplay slides={AUTOPLAY_SLIDES} options={AUTOPLAY_OPTIONS} />
          <EmblaCarouselAutoScroll slides={AUTOSCROLL_SLIDES} options={AUTOSCROLL_OPTIONS} speed={0.35} />
          <EmblaCarouselAutoScroll slides={AUTOSCROLL_SLIDES_2} options={AUTOSCROLL_OPTIONS_2} speed={0.5} />
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
      
    </div>
  );
}
