"use client";

import { useState } from "react";
import type { RenderParameters } from "@/app/page";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Eye, Loader2, ZoomIn, ZoomOut, Maximize2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { API_BASE_URL } from "@/lib/api";

interface RenderPreviewProps {
  params: RenderParameters;
  isRendering: boolean;
  latestImage: string | null;
}

export function RenderPreview({
  params,
  isRendering,
  latestImage,
}: RenderPreviewProps) {
  const [comparePosition, setComparePosition] = useState(50);
  const [zoom, setZoom] = useState(100);

  // Use placeholder images if no renders yet
  const beforeImage = "/mountain-landscape-original-unprocessed.jpg";
  const afterImage =
    latestImage || "/mountain-landscape-golden-hour-cinematic-rendered.jpg";

  // Debug logging
  console.log("RenderPreview - latestImage:", latestImage);
  console.log("RenderPreview - afterImage will use:", afterImage);

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-card">
        <div className="flex items-center gap-2">
          <Eye className="w-4 h-4 text-muted-foreground" />
          <span className="text-sm font-medium">Preview</span>
          {isRendering && (
            <span className="flex items-center gap-1.5 text-xs text-accent">
              <Loader2 className="w-3 h-3 animate-spin" />
              Rendering...
            </span>
          )}
        </div>
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="icon"
            className="h-7 w-7"
            onClick={() => setZoom(Math.max(50, zoom - 25))}
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </Button>
          <span className="text-xs text-muted-foreground w-10 text-center">
            {zoom}%
          </span>
          <Button
            variant="ghost"
            size="icon"
            className="h-7 w-7"
            onClick={() => setZoom(Math.min(200, zoom + 25))}
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </Button>
          <div className="w-px h-4 bg-border mx-1" />
          <Button variant="ghost" size="icon" className="h-7 w-7">
            <Maximize2 className="w-3.5 h-3.5" />
          </Button>
        </div>
      </div>

      {/* Preview Area */}
      <div className="flex-1 bg-muted/30 flex items-center justify-center p-6 overflow-hidden">
        <div
          className="relative bg-card rounded-lg shadow-lg overflow-hidden border border-border"
          style={{
            width: `${Math.min(800, (800 * zoom) / 100)}px`,
            aspectRatio: `${params.resolution.width} / ${params.resolution.height}`,
          }}
        >
          {/* Before/After Comparison */}
          <div className="absolute inset-0">
            {/* Before Image */}
            <img
              src={beforeImage}
              alt="Before"
              className="absolute inset-0 w-full h-full object-cover"
            />

            {/* After Image with Clip */}
            <div
              className="absolute inset-0 overflow-hidden"
              style={{ clipPath: `inset(0 ${100 - comparePosition}% 0 0)` }}
            >
              <img
                src={afterImage}
                alt="After"
                className="absolute inset-0 w-full h-full object-cover"
                onError={(e) => {
                  console.error("Failed to load image:", afterImage);
                  e.currentTarget.src =
                    "/mountain-landscape-golden-hour-cinematic-rendered.jpg";
                }}
              />
            </div>

            {/* Comparison Slider Line */}
            <div
              className="absolute top-0 bottom-0 w-0.5 bg-white shadow-lg z-10 cursor-ew-resize"
              style={{ left: `${comparePosition}%` }}
            >
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-white rounded-full shadow-lg flex items-center justify-center">
                <div className="flex gap-0.5">
                  <div className="w-0.5 h-3 bg-muted-foreground/60 rounded-full" />
                  <div className="w-0.5 h-3 bg-muted-foreground/60 rounded-full" />
                </div>
              </div>
            </div>

            {/* Labels */}
            <div className="absolute top-3 left-3 px-2 py-1 bg-black/60 text-white text-xs rounded font-medium backdrop-blur-sm">
              Before
            </div>
            <div className="absolute top-3 right-3 px-2 py-1 bg-black/60 text-white text-xs rounded font-medium backdrop-blur-sm">
              After
            </div>
          </div>

          {/* Rendering Overlay */}
          {isRendering && (
            <div className="absolute inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-20">
              <div className="flex flex-col items-center gap-3">
                <Loader2 className="w-8 h-8 animate-spin text-accent" />
                <span className="text-sm font-medium">
                  Rendering in progress...
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Comparison Slider Control */}
      <div className="px-4 py-3 border-t border-border bg-card">
        <div className="flex items-center gap-4">
          <Label className="text-xs font-medium text-muted-foreground whitespace-nowrap">
            Compare
          </Label>
          <Slider
            value={[comparePosition]}
            onValueChange={([value]) => setComparePosition(value)}
            min={0}
            max={100}
            step={1}
            className="flex-1"
          />
          <span className="text-xs font-mono text-muted-foreground w-10 text-right">
            {comparePosition}%
          </span>
        </div>
      </div>

      {/* Metadata Bar */}
      <div className="px-4 py-2.5 border-t border-border bg-secondary/30 flex items-center gap-6 text-xs">
        <div className="flex items-center gap-1.5">
          <span className="text-muted-foreground">Seed:</span>
          <span className="font-mono font-medium">{params.seed}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-muted-foreground">Resolution:</span>
          <span className="font-mono font-medium">
            {params.resolution.width}×{params.resolution.height}
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-muted-foreground">Color Space:</span>
          <span className="font-medium">{params.colorSpace}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-muted-foreground">Focal:</span>
          <span className="font-mono font-medium">{params.focalLength}mm</span>
        </div>
      </div>
    </div>
  );
}
