import InfiniteCarousel from "@/components/carousel";


const getTagline = () => {
  const lines = [
    'What kind of experience are you craving?',
    'Pick your vibe. We’ll handle the tickets',
    'Ready to discover something amazing?'
  ]
  let i = Math.floor(Math.random() * lines.length);
  return lines[i];
};


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
          <InfiniteCarousel/>
          <div className="section-2">
            <div className="item"></div>
            <div className="item"></div>
            <div className="item"></div>
            <div className="item"></div>
            <div className="item"></div>
            <div className="item"></div>
          </div>
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
