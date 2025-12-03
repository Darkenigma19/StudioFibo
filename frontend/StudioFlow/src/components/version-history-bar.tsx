"use client";

import { useRef } from "react";
import type { Version } from "@/page";
import { Clock, ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";

interface VersionHistoryBarProps {
  versions: Version[];
  onVersionSelect: (version: Version) => void;
}

function formatTimeAgo(date: Date): string {
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  if (seconds < 60) return "Just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  return `${hours}h ago`;
}

export function VersionHistoryBar({
  versions,
  onVersionSelect,
}: VersionHistoryBarProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  const scroll = (direction: "left" | "right") => {
    if (scrollRef.current) {
      const scrollAmount = 200;
      scrollRef.current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  return (
    <div className="border-b border-border bg-muted/30 px-3 py-2">
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-2 text-xs text-muted-foreground shrink-0">
          <Clock className="w-3.5 h-3.5" />
          <span className="font-medium uppercase tracking-wider">Versions</span>
          <span className="text-muted-foreground/70">({versions.length})</span>
        </div>

        <Button
          variant="ghost"
          size="icon"
          className="h-7 w-7 shrink-0"
          onClick={() => scroll("left")}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>

        <div
          ref={scrollRef}
          className="flex-1 flex items-center gap-2 overflow-x-auto scrollbar-none scroll-smooth"
        >
          {versions.map((version, index) => (
            <button
              key={version.id}
              onClick={() => onVersionSelect(version)}
              className={`
                shrink-0 flex items-center gap-2.5 px-2.5 py-1.5 rounded-lg border transition-smooth
                ${
                  index === 0
                    ? "border-accent/40 bg-accent/5 ring-1 ring-accent/20"
                    : "border-border hover:border-muted-foreground/40 hover:bg-muted/50"
                }
              `}
            >
              <img
                src={version.thumbnail || "/placeholder.svg"}
                alt={`Version ${version.id}`}
                className="w-14 h-9 object-cover rounded border border-border/50"
              />
              <div className="text-left">
                <div className="flex items-center gap-1.5">
                  <span className="text-xs font-medium">
                    v{version.id.replace("v", "")}
                  </span>
                  {index === 0 && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-accent/15 text-accent font-medium">
                      Latest
                    </span>
                  )}
                </div>
                <span className="text-[10px] text-muted-foreground">
                  {formatTimeAgo(version.timestamp)}
                </span>
              </div>
            </button>
          ))}
        </div>

        <Button
          variant="ghost"
          size="icon"
          className="h-7 w-7 shrink-0"
          onClick={() => scroll("right")}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
