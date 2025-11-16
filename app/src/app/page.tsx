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
  return (
    <div>
      <div className="header"></div>
      <main>
        <div className="search-wrapper">
          <div className="tagline">
            {getTagline()}
          </div>
          <div className="search-box">
            <input type="text" placeholder="Share your vibe..." autoCapitalize="none" autoCorrect="false" autoComplete="off" spellCheck="false" />
            <svg className="icon" width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M15.7955 15.8111L21 21M18 10.5C18 14.6421 14.6421 18 10.5 18C6.35786 18 3 14.6421 3 10.5C3 6.35786 6.35786 3 10.5 3C14.6421 3 18 6.35786 18 10.5Z" stroke="#000000" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
        </div>
        <div className="section-wrapper">
          <EmblaCarouselAutoplay slides={AUTOPLAY_SLIDES} options={AUTOPLAY_OPTIONS} />
          <EmblaCarouselAutoScroll slides={AUTOSCROLL_SLIDES} options={AUTOSCROLL_OPTIONS} speed={0.3} />
          <EmblaCarouselAutoScroll slides={AUTOSCROLL_SLIDES_2} options={AUTOSCROLL_OPTIONS_2} speed={0.6} />
          <div className="section-3">
            <div className="item"></div>
            <div className="item"></div>
            <div className="item"></div>
            <div className="item"></div>
            <div className="item"></div>
            <div className="item"></div>
          </div>
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
