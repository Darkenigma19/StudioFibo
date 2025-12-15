"use client";

import type { Version } from "@/app/page";
import { Label } from "@/components/ui/label";
import { Clock, ChevronRight } from "lucide-react";

interface VersionHistoryProps {
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

export function VersionHistory({
  versions,
  onVersionSelect,
}: VersionHistoryProps) {
  return (
    <section className="space-y-3">
      <div className="flex items-center justify-between">
        <Label className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
          Version History
        </Label>
        <span className="text-xs text-muted-foreground">
          {versions.length} versions
        </span>
      </div>

      <div className="space-y-2 max-h-[240px] overflow-y-auto custom-scrollbar pr-1">
        {versions.map((version, index) => (
          <button
            key={version.id}
            onClick={() => onVersionSelect(version)}
            className={`
              w-full flex items-center gap-3 p-2 rounded-lg border transition-smooth text-left
              ${
                index === 0
                  ? "border-accent/30 bg-accent/5"
                  : "border-border hover:border-muted-foreground/30 hover:bg-muted/50"
              }
            `}
          >
            <img
              src={version.thumbnail || "/placeholder.svg"}
              alt={`Version ${version.id}`}
              className="w-16 h-10 object-cover rounded border border-border"
            />
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium">
                  Version {version.id.replace("v", "")}
                </span>
                {index === 0 && (
                  <span className="text-xs px-1.5 py-0.5 rounded bg-accent/10 text-accent font-medium">
                    Latest
                  </span>
                )}
              </div>
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                <Clock className="w-3 h-3" />
                <span>{formatTimeAgo(version.timestamp)}</span>
              </div>
            </div>
            <ChevronRight className="w-4 h-4 text-muted-foreground" />
          </button>
        ))}
      </div>
    </section>
  );
}
