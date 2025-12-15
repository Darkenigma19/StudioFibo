"use client";

import type { RenderParameters } from "@/app/page";
import { PromptSection } from "@/components/prompt-section";
import { ParameterSliders } from "@/components/parameter-sliders";
import { ControlNetPanel } from "@/components/controlnet-panel";
import { JsonEditor } from "@/components/json-editor";

interface ControlPanelProps {
  params: RenderParameters;
  onParamChange: (key: keyof RenderParameters, value: unknown) => void;
  onJsonChange: (params: RenderParameters) => void;
  onTranslate: () => void;
  onValidate: () => void;
  onRender: () => void;
  isRendering: boolean;
  isValidated: boolean;
}

export function ControlPanel({
  params,
  onParamChange,
  onJsonChange,
  onTranslate,
  onValidate,
  onRender,
  isRendering,
  isValidated,
}: ControlPanelProps) {
  return (
    <aside className="w-[420px] min-w-[420px] border-r border-border bg-panel flex flex-col overflow-hidden">
      <div className="flex-1 overflow-y-auto custom-scrollbar p-5 space-y-6">
        <PromptSection
          prompt={params.prompt}
          onPromptChange={(value) => onParamChange("prompt", value)}
          onTranslate={onTranslate}
          onValidate={onValidate}
          onRender={onRender}
          isRendering={isRendering}
          isValidated={isValidated}
        />

        <JsonEditor params={params} onJsonChange={onJsonChange} />

        <ParameterSliders params={params} onParamChange={onParamChange} />

        <ControlNetPanel
          controlNet={params.controlNet}
          onControlNetChange={(value) => onParamChange("controlNet", value)}
        />
      </div>
    </aside>
  );
}
