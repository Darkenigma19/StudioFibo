"use client";

import { useState } from "react";
import type { RenderParameters } from "@/app/page";
import { Button } from "@/components/ui/button";
import { Copy, Check, ChevronRight, ChevronDown, Code2 } from "lucide-react";

interface JsonEditorProps {
  params: RenderParameters;
  onJsonChange: (params: RenderParameters) => void;
}

interface JsonNodeProps {
  keyName: string;
  value: unknown;
  depth: number;
  isLast: boolean;
  onValueChange?: (newValue: unknown) => void;
}

function JsonNode({
  keyName,
  value,
  depth,
  isLast,
  onValueChange,
}: JsonNodeProps) {
  const [isExpanded, setIsExpanded] = useState(depth < 2);
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState("");

  const indent = depth * 12;
  const isObject =
    typeof value === "object" && value !== null && !Array.isArray(value);
  const isArray = Array.isArray(value);
  const isExpandable = isObject || isArray;

  const getValueColor = () => {
    if (typeof value === "string") return "text-json-string";
    if (typeof value === "number") return "text-json-number";
    if (typeof value === "boolean") return "text-json-boolean";
    if (value === null) return "text-muted-foreground";
    return "text-foreground";
  };

  const formatValue = () => {
    if (typeof value === "string") {
      const str = String(value);
      return `"${str.length > 30 ? str.slice(0, 30) + "..." : str}"`;
    }
    if (value === null) return "null";
    return String(value);
  };

  const handleDoubleClick = () => {
    if (!isExpandable && onValueChange) {
      setIsEditing(true);
      setEditValue(typeof value === "string" ? value : JSON.stringify(value));
    }
  };

  const handleBlur = () => {
    setIsEditing(false);
    if (onValueChange) {
      try {
        const parsed =
          typeof value === "string" ? editValue : JSON.parse(editValue);
        onValueChange(parsed);
      } catch {
        // Invalid JSON, revert
      }
    }
  };

  return (
    <div className="font-mono text-[11px] leading-5">
      <div
        className="flex items-start group hover:bg-muted/30 rounded px-1 -mx-1 transition-smooth"
        style={{ paddingLeft: indent }}
      >
        {isExpandable && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="w-4 h-5 flex items-center justify-center text-muted-foreground hover:text-foreground mr-0.5 flex-shrink-0"
          >
            {isExpanded ? (
              <ChevronDown className="w-2.5 h-2.5" />
            ) : (
              <ChevronRight className="w-2.5 h-2.5" />
            )}
          </button>
        )}
        {!isExpandable && <span className="w-4 flex-shrink-0" />}

        <span className="text-json-key">{`"${keyName}"`}</span>
        <span className="text-muted-foreground mx-0.5">:</span>

        {isExpandable ? (
          <span className="text-muted-foreground">
            {isArray ? "[" : "{"}
            {!isExpanded && (
              <>
                <span className="text-muted-foreground mx-0.5">...</span>
                {isArray ? "]" : "}"}
              </>
            )}
          </span>
        ) : isEditing ? (
          <input
            type="text"
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            onBlur={handleBlur}
            onKeyDown={(e) => e.key === "Enter" && handleBlur()}
            className="bg-muted border border-accent rounded px-1 outline-none text-foreground min-w-[80px] text-[11px]"
            autoFocus
          />
        ) : (
          <span
            className={`${getValueColor()} cursor-text truncate`}
            onDoubleClick={handleDoubleClick}
          >
            {formatValue()}
            {!isLast && <span className="text-muted-foreground">,</span>}
          </span>
        )}
      </div>

      {isExpandable && isExpanded && (
        <>
          {Object.entries(value as Record<string, unknown>).map(
            ([k, v], i, arr) => (
              <JsonNode
                key={k}
                keyName={k}
                value={v}
                depth={depth + 1}
                isLast={i === arr.length - 1}
              />
            )
          )}
          <div
            style={{ paddingLeft: indent }}
            className="text-muted-foreground px-1"
          >
            <span className="w-4 inline-block" />
            {isArray ? "]" : "}"}
            {!isLast && ","}
          </div>
        </>
      )}
    </div>
  );
}

export function JsonEditor({ params }: JsonEditorProps) {
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(JSON.stringify(params, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="space-y-2">
      <div className="flex items-center justify-between">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-2 text-xs font-medium uppercase tracking-wider text-muted-foreground hover:text-foreground transition-smooth"
        >
          {isExpanded ? (
            <ChevronDown className="w-3.5 h-3.5" />
          ) : (
            <ChevronRight className="w-3.5 h-3.5" />
          )}
          <Code2 className="w-3.5 h-3.5" />
          <span>JSON Parameters</span>
        </button>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleCopy}
          className="h-6 px-2 text-xs text-muted-foreground hover:text-foreground"
        >
          {copied ? (
            <Check className="w-3 h-3 mr-1 text-success" />
          ) : (
            <Copy className="w-3 h-3 mr-1" />
          )}
          {copied ? "Copied" : "Copy"}
        </Button>
      </div>

      {isExpanded && (
        <div className="rounded-lg border border-border bg-panel overflow-hidden">
          <div className="max-h-[200px] overflow-auto custom-scrollbar p-3">
            <div className="text-muted-foreground font-mono text-[11px]">
              {"{"}
            </div>
            {Object.entries(params).map(([key, value], i, arr) => (
              <JsonNode
                key={key}
                keyName={key}
                value={value}
                depth={1}
                isLast={i === arr.length - 1}
              />
            ))}
            <div className="text-muted-foreground font-mono text-[11px]">
              {"}"}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
