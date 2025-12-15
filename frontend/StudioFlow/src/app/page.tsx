"use client";

import { useState, useCallback, useEffect } from "react";
import { ControlPanel } from "@/components/control-panel";
import { PreviewPanel } from "@/components/preview-panel";
import { Header } from "@/components/header";
import {
  translatePrompt,
  validateParams,
  renderImage,
  getVersions,
  API_BASE_URL,
} from "@/lib/api";

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

  // Load versions from backend on mount
  useEffect(() => {
    const loadVersions = async () => {
      try {
        const data = await getVersions();
        if (data && data.length > 0) {
          const mappedVersions: Version[] = data.map((v: any) => ({
            id: v.id,
            timestamp: new Date(v.timestamp),
            thumbnail: `${API_BASE_URL}${v.image_url}`,
            params: initialParams, // Use initial params as we don't store full params in DB
          }));
          setVersions(mappedVersions);
          console.log("Loaded versions from backend:", mappedVersions.length);
        }
      } catch (error) {
        console.error("Failed to load versions:", error);
      }
    };
    loadVersions();
  }, []);

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

  const handleTranslate = useCallback(async () => {
    try {
      const result = await translatePrompt(params.prompt);
      setParams((prev) => ({
        ...prev,
        prompt: result.translated_prompt || result.prompt || prev.prompt,
      }));
    } catch (error) {
      console.error("Translation failed:", error);
      alert("Failed to translate prompt. Please try again.");
    }
  }, [params.prompt]);

  const handleValidate = useCallback(async () => {
    // Validate parameters and get enhanced prompt
    try {
      const result = await validateParams(params);
      if (result.valid) {
        setIsValidated(true);

        // Show enhanced prompt to user
        const message = result.enhancedPrompt
          ? `✓ Parameters are valid!\n\nEnhanced Prompt for Image Generation:\n${result.enhancedPrompt}`
          : "✓ Parameters are valid!";

        alert(message);
        console.log("Enhanced prompt:", result.enhancedPrompt);
      } else {
        setIsValidated(false);
        alert("Validation failed: " + (result.error || "Unknown error"));
      }
    } catch (error) {
      console.error("Validation failed:", error);
      alert("Failed to validate parameters. Please try again.");
    }
  }, [params]);

  const handleRender = useCallback(async () => {
    console.log("Starting render process...");
    console.log("Prompt:", params.prompt);
    setIsRendering(true);

    try {
      // First translate prompt to FIBO JSON
      console.log("Step 1: Translating prompt...");
      const translatedJson = await translatePrompt(params.prompt);
      console.log("Translation result:", translatedJson);

      // Then render with the translated JSON
      console.log("Step 2: Rendering image...");
      const result = await renderImage(translatedJson);
      console.log("Render result:", result);

      const imageUrl = `${API_BASE_URL}${result.image_url}`;
      console.log("Full image URL:", imageUrl);

      const newVersion: Version = {
        id: `v${versions.length + 1}`,
        timestamp: new Date(),
        thumbnail: imageUrl,
        params: { ...params },
      };

      console.log("New version:", newVersion);
      setVersions((prev) => [newVersion, ...prev]);
      console.log("✓ Render complete! Image should appear in preview.");
    } catch (error) {
      console.error("Rendering failed:", error);
      alert(
        `Failed to render image: ${
          error instanceof Error ? error.message : "Unknown error"
        }`
      );
    } finally {
      setIsRendering(false);
    }
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
