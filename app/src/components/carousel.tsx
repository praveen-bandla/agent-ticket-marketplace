"use client";

import { useEffect, useRef, useState } from "react";

export default function InfiniteCarousel() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [index, setIndex] = useState(0);

  const items = [1, 2, 3, 4]; // replace with images or components

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % items.length);
    }, 5000); // 5 seconds
    return () => clearInterval(interval);
  }, [items.length]);

  useEffect(() => {
    if (containerRef.current) {
      const firstChild = containerRef.current.children[0] as HTMLElement;
      const itemWidth = firstChild.offsetWidth + 20; // width + margins
      containerRef.current.style.transform = `translateX(-${index * itemWidth}px)`;
    }
  }, [index]);

  return (
    <div className="section-1 overflow-hidden w-full flex justify-center">
      <div
        ref={containerRef}
        className="flex transition-transform duration-700 ease-in-out"
      >
        {items.map((item, i) => (
          <div
            key={i}
            className="item bg-gray-300 shrink-0 rounded-2xl"
            style={{ width: "900px", height: "506px", margin: "0 10px" }}
          >
            <div className="w-full h-full flex items-center justify-center text-4xl font-bold">
              {item}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
