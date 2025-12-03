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
  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-background">
      <VersionHistoryBar
        versions={versions}
        onVersionSelect={onVersionSelect}
      />

      <div className="flex-1 flex flex-col overflow-hidden min-w-0">
        <RenderPreview params={params} isRendering={isRendering} />
      </div>

      {/* Export Tools */}
      <ExportTools params={params} />
    </div>
  );
}
