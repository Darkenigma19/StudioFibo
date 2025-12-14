"use client";

import type { RenderParameters, Version } from "@/page";
import { RenderPreview } from "@/components/render-preview";
import { ExportTools } from "@/components/export-tools";
import { VersionHistoryBar } from "@/components/version-history-bar";

interface PreviewPanelProps {
  params: RenderParameters;
  isRendering: boolean;
  versions: Version[];
  onVersionSelect: (version: Version) => void;
}

export function PreviewPanel({
  params,
  isRendering,
  versions,
  onVersionSelect,
}: PreviewPanelProps) {
  // Get the latest rendered image
  const latestImage = versions.length > 0 ? versions[0].thumbnail : null;

  // Debug logging
  console.log("PreviewPanel - versions count:", versions.length);
  console.log("PreviewPanel - latestImage:", latestImage);
  if (versions.length > 0) {
    console.log("PreviewPanel - latest version:", versions[0]);
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-background">
      <VersionHistoryBar
        versions={versions}
        onVersionSelect={onVersionSelect}
      />

      <div className="flex-1 flex flex-col overflow-hidden min-w-0">
        <RenderPreview
          params={params}
          isRendering={isRendering}
          latestImage={latestImage}
        />
      </div>

      {/* Export Tools */}
      <ExportTools params={params} />
    </div>
  );
}
