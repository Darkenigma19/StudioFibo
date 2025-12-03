"use client"

import { Wand2, CheckCircle, Play, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"

interface PromptSectionProps {
  prompt: string
  onPromptChange: (value: string) => void
  onTranslate: () => void
  onValidate: () => void
  onRender: () => void
  isRendering: boolean
  isValidated: boolean
}

export function PromptSection({
  prompt,
  onPromptChange,
  onTranslate,
  onValidate,
  onRender,
  isRendering,
  isValidated,
}: PromptSectionProps) {
  return (
    <section className="space-y-3">
      <div className="flex items-center justify-between">
        <Label className="text-xs font-medium uppercase tracking-wider text-muted-foreground">Creative Prompt</Label>
        <span className="text-xs text-muted-foreground">{prompt.length} chars</span>
      </div>

      <Textarea
        value={prompt}
        onChange={(e) => onPromptChange(e.target.value)}
        placeholder="Describe your creative vision..."
        className="min-h-[140px] resize-none bg-secondary/50 border-border focus:border-accent focus:ring-accent/20 text-sm leading-relaxed transition-smooth"
      />

      <div className="flex gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={onTranslate}
          className="flex-1 text-xs font-medium transition-smooth bg-transparent"
        >
          <Wand2 className="w-3.5 h-3.5 mr-1.5" />
          Translate
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={onValidate}
          className={`flex-1 text-xs font-medium transition-smooth ${
            isValidated ? "border-success text-success bg-success/5" : ""
          }`}
        >
          <CheckCircle className="w-3.5 h-3.5 mr-1.5" />
          Validate
        </Button>
        <Button
          size="sm"
          onClick={onRender}
          disabled={isRendering}
          className="flex-1 text-xs font-medium bg-primary hover:bg-primary/90 transition-smooth"
        >
          {isRendering ? (
            <Loader2 className="w-3.5 h-3.5 mr-1.5 animate-spin" />
          ) : (
            <Play className="w-3.5 h-3.5 mr-1.5" />
          )}
          Render
        </Button>
      </div>
    </section>
  )
}
