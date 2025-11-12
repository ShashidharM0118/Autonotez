"use client";
import * as React from "react";

export function useIntersectionObserver<T extends Element = Element>(
  options: IntersectionObserverInit = { rootMargin: "0px", threshold: 0.2 }
) {
  const ref = React.useRef<T | null>(null);
  const [isIntersecting, setIsIntersecting] = React.useState(false);

  React.useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(([entry]) => {
      setIsIntersecting(entry.isIntersecting);
    }, options);
    observer.observe(el);
    return () => observer.disconnect();
  }, [options]);

  return { ref, isIntersecting } as const;
}
