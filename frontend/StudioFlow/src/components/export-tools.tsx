"use client";

import { useState } from "react";
import type { RenderParameters } from "@/page";
import { Button } from "@/components/ui/button";
import { Download, Settings2, Check } from "lucide-react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

interface ExportToolsProps {
  params: RenderParameters;
}

type ToneMapping = "aces" | "reinhard" | "filmic" | "none";

interface ExportFormat {
  id: string;
  label: string;
  extension: string;
  description: string;
  supportsToneMapping: boolean;
}

const exportFormats: ExportFormat[] = [
  {
    id: "exr",
    label: "OpenEXR",
    extension: ".exr",
    description: "32-bit HDR",
    supportsToneMapping: false,
  },
  {
    id: "tiff16",
    label: "TIFF 16-bit",
    extension: ".tiff",
    description: "16-bit color",
    supportsToneMapping: true,
  },
  {
    id: "jpg",
    label: "JPEG",
    extension: ".jpg",
    description: "8-bit compressed",
    supportsToneMapping: true,
  },
];

const toneMappingOptions = [
  {
    value: "aces",
    label: "ACES Filmic",
    description: "Industry standard cinematic",
  },
  {
    value: "reinhard",
    label: "Reinhard",
    description: "Natural highlight rolloff",
  },
  { value: "filmic", label: "Filmic", description: "High contrast cinematic" },
  { value: "none", label: "None", description: "Linear output" },
];

export function ExportTools({ params }: ExportToolsProps) {
  const [selectedFormat, setSelectedFormat] = useState("jpg");
  const [toneMapping, setToneMapping] = useState<ToneMapping>("aces");
  const [isExporting, setIsExporting] = useState(false);
  const [exportSuccess, setExportSuccess] = useState(false);

  const currentFormat = exportFormats.find((f) => f.id === selectedFormat);

  const handleExport = () => {
    setIsExporting(true);
    setTimeout(() => {
      setIsExporting(false);
      setExportSuccess(true);
      setTimeout(() => setExportSuccess(false), 2000);
    }, 1500);
  };

  return (
    <div className="border-t border-border bg-card px-5 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
            Export
          </span>

          <div className="flex items-center gap-2">
            {exportFormats.map((format) => (
              <button
                key={format.id}
                onClick={() => setSelectedFormat(format.id)}
                className={`
                  px-3 py-1.5 rounded-md text-xs font-medium transition-smooth
                  ${
                    selectedFormat === format.id
                      ? "bg-primary text-primary-foreground"
                      : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
                  }
                `}
              >
                {format.label}
              </button>
            ))}
          </div>

          {currentFormat?.supportsToneMapping && (
            <>
              <div className="w-px h-5 bg-border" />

              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="outline"
                    size="sm"
                    className="h-8 text-xs gap-1.5 bg-transparent"
                  >
                    <Settings2 className="w-3.5 h-3.5" />
                    Tone Mapping:{" "}
                    {
                      toneMappingOptions.find((t) => t.value === toneMapping)
                        ?.label
                    }
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-64" align="start">
                  <div className="space-y-3">
                    <Label className="text-xs font-medium">
                      Tone Mapping Curve
                    </Label>
                    <RadioGroup
                      value={toneMapping}
                      onValueChange={(v) => setToneMapping(v as ToneMapping)}
                    >
                      {toneMappingOptions.map((option) => (
                        <div
                          key={option.value}
                          className="flex items-start gap-2"
                        >
                          <RadioGroupItem
                            value={option.value}
                            id={option.value}
                            className="mt-0.5"
                          />
                          <label
                            htmlFor={option.value}
                            className="cursor-pointer"
                          >
                            <div className="text-sm font-medium">
                              {option.label}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              {option.description}
                            </div>
                          </label>
                        </div>
                      ))}
                    </RadioGroup>
                  </div>
                </PopoverContent>
              </Popover>
            </>
          )}
        </div>

        <div className="flex items-center gap-3">
          <div className="text-xs text-muted-foreground">
            <span className="font-mono">
              {params.resolution.width}×{params.resolution.height}
            </span>
            <span className="mx-1.5">•</span>
            <span>{currentFormat?.description}</span>
          </div>

          <Button
            onClick={handleExport}
            disabled={isExporting}
            className="gap-1.5 transition-smooth"
          >
            {exportSuccess ? (
              <>
                <Check className="w-4 h-4" />
                Exported
              </>
            ) : isExporting ? (
              <>
                <div className="w-4 h-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />
                Exporting...
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                Export {currentFormat?.extension}
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
