"use client";

import { useState, useCallback } from "react";
import { ControlPanel } from "@/components/control-panel";
import { PreviewPanel } from "@/components/preview-panel";
import { Header } from "@/components/header";

export interface RenderParameters {
  prompt: string;
  focalLength: number;
  yaw: number;
  pitch: number;
  lighting: number;
  colorPalette: string;
  controlNet: {
    type: "sketch" | "depth" | "canny" | "none";
    strength: number;
    image: string | null;
  };
  seed: number;
  resolution: { width: number; height: number };
  colorSpace: "sRGB" | "Adobe RGB" | "Display P3";
}

export interface Version {
  id: string;
  timestamp: Date;
  thumbnail: string;
  params: RenderParameters;
}

const initialParams: RenderParameters = {
  prompt:
    "A serene mountain landscape at golden hour with dramatic cloud formations, cinematic lighting, 8K resolution, photorealistic",
  focalLength: 35,
  yaw: 0,
  pitch: 0,
  lighting: 50,
  colorPalette: "warm",
  controlNet: {
    type: "none",
    strength: 0.75,
    image: null,
  },
  seed: 42857391,
  resolution: { width: 1920, height: 1080 },
  colorSpace: "sRGB",
};

const mockVersions: Version[] = [
  {
    id: "v1",
    timestamp: new Date(Date.now() - 3600000),
    thumbnail: "/mountain-landscape-golden-hour.jpg",
    params: { ...initialParams, focalLength: 24 },
  },
  {
    id: "v2",
    timestamp: new Date(Date.now() - 1800000),
    thumbnail: "/mountain-landscape-blue-hour.jpg",
    params: { ...initialParams, lighting: 30, colorPalette: "cool" },
  },
  {
    id: "v3",
    timestamp: new Date(Date.now() - 900000),
    thumbnail: "/mountain-landscape-dramatic.jpg",
    params: { ...initialParams, yaw: 15 },
  },
];

export default function StudioFlow() {
  const [params, setParams] = useState<RenderParameters>(initialParams);
  const [versions, setVersions] = useState<Version[]>(mockVersions);
  const [isRendering, setIsRendering] = useState(false);
  const [isValidated, setIsValidated] = useState(false);

  const handleParamChange = useCallback(
    (key: keyof RenderParameters, value: unknown) => {
      setParams((prev) => ({ ...prev, [key]: value }));
      setIsValidated(false);
    },
    []
  );

  const handleJsonChange = useCallback((newParams: RenderParameters) => {
    setParams(newParams);
    setIsValidated(false);
  }, []);

  const handleTranslate = useCallback(() => {
    // Simulate prompt translation/enhancement
    setParams((prev) => ({
      ...prev,
      prompt:
        prev.prompt + " — enhanced with professional cinematography techniques",
    }));
  }, []);

  const handleValidate = useCallback(() => {
    setIsValidated(true);
  }, []);

  const handleRender = useCallback(() => {
    setIsRendering(true);
    // Simulate render
    setTimeout(() => {
      const newVersion: Version = {
        id: `v${versions.length + 1}`,
        timestamp: new Date(),
        thumbnail: `/placeholder.svg?height=80&width=120&query=rendered scene ${params.seed}`,
        params: { ...params },
      };
      setVersions((prev) => [newVersion, ...prev]);
      setIsRendering(false);
    }, 2000);
  }, [params, versions.length]);

  const handleVersionSelect = useCallback((version: Version) => {
    setParams(version.params);
  }, []);

  return (
    <div className="min-h-screen bg-background flex flex-col antialiased">
      <Header />
      <main className="flex-1 flex overflow-hidden">
        <ControlPanel
          params={params}
          onParamChange={handleParamChange}
          onJsonChange={handleJsonChange}
          onTranslate={handleTranslate}
          onValidate={handleValidate}
          onRender={handleRender}
          isRendering={isRendering}
          isValidated={isValidated}
        />
        <PreviewPanel
          params={params}
          isRendering={isRendering}
          versions={versions}
          onVersionSelect={handleVersionSelect}
        />
      </main>
    </div>
  );
}
