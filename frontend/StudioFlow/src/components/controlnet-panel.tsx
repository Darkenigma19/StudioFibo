"use client";

import type React from "react";

import { useState } from "react";
import { Upload, X, ImageIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { uploadControlNet } from "@/lib/api";

interface ControlNetConfig {
  type: "sketch" | "depth" | "canny" | "none";
  strength: number;
  image: string | null;
}

interface ControlNetPanelProps {
  controlNet: ControlNetConfig;
  onControlNetChange: (value: ControlNetConfig) => void;
}

const controlNetTypes = [
  { value: "none", label: "None" },
  { value: "sketch", label: "Sketch" },
  { value: "depth", label: "Depth Map" },
  { value: "canny", label: "Canny Edge" },
];

export function ControlNetPanel({
  controlNet,
  onControlNetChange,
}: ControlNetPanelProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const result = await uploadControlNet(file, controlNet.type);

      onControlNetChange({
        ...controlNet,
        image: result.path || result.filename,
      });

      // Show preview
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewUrl(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Failed to upload image. Make sure backend is running");
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    // Simulate file upload
    onControlNetChange({
      ...controlNet,
      image: "/uploaded-sketch-reference.jpg",
    });
  };

  const handleRemoveImage = () => {
    onControlNetChange({ ...controlNet, image: null });
  };

  return (
    <section className="space-y-4">
      <Label className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
        ControlNet
      </Label>

      <div className="space-y-4 bg-secondary/30 rounded-lg p-4 border border-border">
        {/* Type Selector */}
        <div className="space-y-2">
          <span className="text-sm font-medium">Control Type</span>
          <Select
            value={controlNet.type}
            onValueChange={(value: "sketch" | "depth" | "canny" | "none") =>
              onControlNetChange({ ...controlNet, type: value })
            }
          >
            <SelectTrigger className="bg-card border-border h-9 text-sm">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {controlNetTypes.map((type) => (
                <SelectItem key={type.value} value={type.value}>
                  {type.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Upload Area */}
        {controlNet.type !== "none" && (
          <>
            <div className="space-y-2">
              <span className="text-sm font-medium">Reference Image</span>
              {controlNet.image ? (
                <div className="relative group">
                  <img
                    src={controlNet.image || "/placeholder.svg"}
                    alt="ControlNet reference"
                    className="w-full h-24 object-cover rounded-md border border-border"
                  />
                  <Button
                    variant="destructive"
                    size="icon"
                    className="absolute top-2 right-2 h-6 w-6 opacity-0 group-hover:opacity-100 transition-smooth"
                    onClick={handleRemoveImage}
                  >
                    <X className="w-3 h-3" />
                  </Button>
                </div>
              ) : (
                <div
                  onDragOver={(e) => {
                    e.preventDefault();
                    setIsDragging(true);
                  }}
                  onDragLeave={() => setIsDragging(false)}
                  onDrop={handleDrop}
                  onClick={() =>
                    onControlNetChange({
                      ...controlNet,
                      image: "/sketch-reference-image.jpg",
                    })
                  }
                  className={`
                    border-2 border-dashed rounded-lg p-6 text-center cursor-pointer
                    transition-smooth
                    ${
                      isDragging
                        ? "border-accent bg-accent/5"
                        : "border-border hover:border-muted-foreground/50 hover:bg-muted/50"
                    }
                  `}
                >
                  <div className="flex flex-col items-center gap-2">
                    <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center">
                      {isDragging ? (
                        <ImageIcon className="w-5 h-5 text-accent" />
                      ) : (
                        <Upload className="w-5 h-5 text-muted-foreground" />
                      )}
                    </div>
                    <div>
                      <p className="text-sm font-medium">Drop image or click</p>
                      <p className="text-xs text-muted-foreground">
                        PNG, JPG up to 10MB
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Strength Slider */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Strength</span>
                <span className="text-xs font-mono bg-muted px-2 py-0.5 rounded">
                  {(controlNet.strength * 100).toFixed(0)}%
                </span>
              </div>
              <Slider
                value={[controlNet.strength * 100]}
                onValueChange={([value]) =>
                  onControlNetChange({ ...controlNet, strength: value / 100 })
                }
                min={0}
                max={100}
                step={1}
                className="transition-smooth"
              />
            </div>
          </>
        )}
      </div>
    </section>
  );
}
