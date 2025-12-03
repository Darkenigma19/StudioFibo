"use client";

import type { RenderParameters } from "@/page";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Camera, RotateCcw, Sun, Palette } from "lucide-react";

interface ParameterSlidersProps {
  params: RenderParameters;
  onParamChange: (key: keyof RenderParameters, value: unknown) => void;
}

const palettes = [
  { value: "warm", label: "Warm" },
  { value: "cool", label: "Cool" },
  { value: "neutral", label: "Neutral" },
  { value: "cinematic", label: "Cinematic" },
  { value: "vibrant", label: "Vibrant" },
];

export function ParameterSliders({
  params,
  onParamChange,
}: ParameterSlidersProps) {
  return (
    <section className="space-y-4">
      <Label className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
        Render Parameters
      </Label>

      <div className="space-y-5 bg-secondary/30 rounded-lg p-4 border border-border">
        {/* Focal Length */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Camera className="w-3.5 h-3.5 text-muted-foreground" />
              <span className="text-sm font-medium">Focal Length</span>
            </div>
            <span className="text-xs font-mono bg-muted px-2 py-0.5 rounded">
              {params.focalLength}mm
            </span>
          </div>
          <Slider
            value={[params.focalLength]}
            onValueChange={([value]) => onParamChange("focalLength", value)}
            min={12}
            max={200}
            step={1}
            className="transition-smooth"
          />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>Wide</span>
            <span>Telephoto</span>
          </div>
        </div>

        {/* Yaw */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <RotateCcw className="w-3.5 h-3.5 text-muted-foreground" />
              <span className="text-sm font-medium">Yaw</span>
            </div>
            <span className="text-xs font-mono bg-muted px-2 py-0.5 rounded">
              {params.yaw}°
            </span>
          </div>
          <Slider
            value={[params.yaw]}
            onValueChange={([value]) => onParamChange("yaw", value)}
            min={-180}
            max={180}
            step={1}
            className="transition-smooth"
          />
        </div>

        {/* Pitch */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <RotateCcw className="w-3.5 h-3.5 text-muted-foreground rotate-90" />
              <span className="text-sm font-medium">Pitch</span>
            </div>
            <span className="text-xs font-mono bg-muted px-2 py-0.5 rounded">
              {params.pitch}°
            </span>
          </div>
          <Slider
            value={[params.pitch]}
            onValueChange={([value]) => onParamChange("pitch", value)}
            min={-90}
            max={90}
            step={1}
            className="transition-smooth"
          />
        </div>

        {/* Lighting */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sun className="w-3.5 h-3.5 text-muted-foreground" />
              <span className="text-sm font-medium">Lighting</span>
            </div>
            <span className="text-xs font-mono bg-muted px-2 py-0.5 rounded">
              {params.lighting}%
            </span>
          </div>
          <Slider
            value={[params.lighting]}
            onValueChange={([value]) => onParamChange("lighting", value)}
            min={0}
            max={100}
            step={1}
            className="transition-smooth"
          />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>Low Key</span>
            <span>High Key</span>
          </div>
        </div>

        {/* Color Palette */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Palette className="w-3.5 h-3.5 text-muted-foreground" />
            <span className="text-sm font-medium">Color Palette</span>
          </div>
          <Select
            value={params.colorPalette}
            onValueChange={(value) => onParamChange("colorPalette", value)}
          >
            <SelectTrigger className="bg-card border-border h-9 text-sm">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {palettes.map((palette) => (
                <SelectItem key={palette.value} value={palette.value}>
                  {palette.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
    </section>
  );
}
